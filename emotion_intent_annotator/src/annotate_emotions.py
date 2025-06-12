import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from textblob import TextBlob
import logging
import traceback
import shap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import whisper
import nltk
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
nltk.download('punkt', quiet=True)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class EmotionIntentAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Emotion and Intent Annotator")
        self.sentiment_classifier = None
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
        self.model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')
        self.model.eval()
        self.annotations = []
        self.current_segment_index = 0
        self.segments = []
        self.prev_emotion = None
        self.media_id = 1
        self.filename = ""
        self.emotions = ['happy', 'sad', 'neutral', 'disappointment']
        self.intents = ['joke', 'complain', 'inform']
        self.force_plot_type = tk.StringVar(value="traditional")
        self.history = []  # Stack to store states for undo
        self.setup_gui()
        # Disable buttons that require segments initially
        self.suggest_button.config(state='disabled')
        self.save_button.config(state='disabled')
        self.edit_button.config(state='disabled')
        self.visualize_button.config(state='disabled')

    def setup_gui(self):
        self.upload_button = tk.Button(self.root, text="Upload File", command=self.upload_file)
        self.upload_button.pack(pady=10)
        self.text_display = tk.Text(self.root, height=5, width=50)
        self.text_display.pack(pady=10)
        self.edit_button = tk.Button(self.root, text="Edit Text", command=self.edit_text)
        self.edit_button.pack(pady=5)
        self.save_edit_button = tk.Button(self.root, text="Save Edit", command=self.save_edit, state='disabled')
        self.save_edit_button.pack(pady=5)
        self.suggest_button = tk.Button(self.root, text="Suggest Labels", command=self.suggest_labels)
        self.suggest_button.pack(pady=5)
        tk.Label(self.root, text="Emotion:").pack()
        self.emotion_var = tk.StringVar()
        self.emotion_dropdown = ttk.Combobox(self.root, textvariable=self.emotion_var, values=self.emotions, state='readonly')
        self.emotion_dropdown.pack()
        tk.Label(self.root, text="Intent:").pack()
        self.intent_var = tk.StringVar()
        self.intent_dropdown = ttk.Combobox(self.root, textvariable=self.intent_var, values=self.intents, state='readonly')
        self.intent_dropdown.pack()
        self.save_button = tk.Button(self.root, text="Save Annotation", command=self.save_annotation)
        self.save_button.pack(pady=5)
        self.undo_button = tk.Button(self.root, text="Undo Last Annotation", command=self.undo_annotation, state='disabled')
        self.undo_button.pack(pady=5)
        self.visualize_button = tk.Button(self.root, text="Visualize Suggestions", command=self.visualize_suggestions, state='disabled')
        self.visualize_button.pack(pady=5)
        tk.Label(self.root, text="Force Plot Type:").pack()
        self.force_plot_traditional = tk.Radiobutton(self.root, text="Traditional Force Plot", variable=self.force_plot_type, value="traditional")
        self.force_plot_traditional.pack()
        self.force_plot_text_based = tk.Radiobutton(self.root, text="Text-based Force Plot", variable=self.force_plot_type, value="text")
        self.force_plot_text_based.pack()
        self.export_button = tk.Button(self.root, text="Export CSV", command=self.export_csv)
        self.export_button.pack(pady=5)

    def edit_text(self):
        self.text_display.config(state='normal')
        self.save_edit_button.config(state='normal')
        self.edit_button.config(state='disabled')

    def save_edit(self):
        self.text_display.config(state='disabled')
        self.segments[self.current_segment_index] = self.text_display.get("1.0", tk.END).strip()
        self.save_edit_button.config(state='disabled')
        self.edit_button.config(state='normal')
        logger.debug(f"Edited segment {self.current_segment_index}: {self.segments[self.current_segment_index]}")

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Supported files", "*.mp4 *.m4a *.wav *.txt"),
            ("Video files", "*.mp4"),
            ("Audio files", "*.m4a *.wav"),
            ("Text files", "*.txt")
        ])
        if file_path:
            self.filename = os.path.basename(file_path)
            logger.debug(f"Selected file: {file_path}")
            if file_path.endswith(('.mp4', '.m4a', '.wav')):
                try:
                    model = whisper.load_model("base")
                    result = model.transcribe(file_path)
                    full_text = " ".join([seg['text'].strip() for seg in result['segments']])
                    self.segments = [sentence.strip() for sentence in nltk.sent_tokenize(full_text) if sentence.strip()]
                except Exception as e:
                    logger.error(f"Transcription failed: {str(e)}")
                    messagebox.showerror("Error", f"Failed to transcribe {file_path.split('.')[-1]} file.")
                    self.segments = []
                    return
            elif file_path.endswith('.txt'):
                try:
                    with open(file_path, 'r') as f:
                        text = f.read().strip()
                        logger.debug(f"Raw text from file: {text}")
                        if not text:
                            logger.error("Uploaded file is empty")
                            messagebox.showerror("Error", "The uploaded file is empty.")
                            self.segments = []
                            return
                        self.segments = [sentence.strip() for sentence in nltk.sent_tokenize(text) if sentence.strip()]
                        if not self.segments:
                            logger.error("No valid segments found after tokenization")
                            messagebox.showerror("Error", "No valid sentences found in the file.")
                            self.segments = []
                            return
                except Exception as e:
                    logger.error(f"Failed to read or process file: {str(e)}")
                    messagebox.showerror("Error", f"Failed to read the file: {str(e)}")
                    self.segments = []
                    return
            else:
                messagebox.showerror("Error", "Unsupported file format.")
                self.segments = []
                return
            logger.debug(f"Segments after upload: {self.segments}, length: {len(self.segments)}")
            self.current_segment_index = 0
            self.annotations = []
            self.prev_emotion = None
            self.history = []  # Reset history on new file upload
            self.undo_button.config(state='disabled')  # Disable undo button
            logger.debug(f"Current segment index set to: {self.current_segment_index}")
            self.display_segment()

    def display_segment(self):
        logger.debug(f"Displaying segment - current_index: {self.current_segment_index}, total segments: {len(self.segments)}")
        if not self.segments:
            logger.debug("No segments available, disabling buttons")
            self.text_display.config(state='normal')
            self.text_display.delete(1.0, tk.END)
            self.text_display.config(state='disabled')
            self.suggest_button.config(state='disabled')
            self.save_button.config(state='disabled')
            self.edit_button.config(state='disabled')
            self.visualize_button.config(state='disabled')
            self.root.update()
            logger.debug(f"Buttons disabled due to empty segments")
            return
        if self.current_segment_index < len(self.segments):
            logger.debug(f"Segment to display: {self.segments[self.current_segment_index]}")
            self.text_display.config(state='normal')
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, self.segments[self.current_segment_index])
            self.text_display.config(state='disabled')
            self.suggest_button.config(state='normal')
            self.save_button.config(state='normal')
            self.edit_button.config(state='normal')
            self.visualize_button.config(state='normal')
            self.emotion_var.set('')
            self.intent_var.set('')
            self.root.update()
            logger.debug(f"Buttons enabled, visualize button state: {self.visualize_button['state']}")
        else:
            logger.debug("All segments annotated, disabling buttons")
            messagebox.showinfo("Done", "All segments annotated.")
            self.text_display.config(state='normal')
            self.text_display.delete(1.0, tk.END)
            self.text_display.config(state='disabled')
            self.suggest_button.config(state='disabled')
            self.save_button.config(state='disabled')
            self.edit_button.config(state='disabled')
            self.visualize_button.config(state='disabled')
            self.root.update()
            logger.debug(f"Buttons disabled, visualize button state: {self.visualize_button['state']}")

    def suggest_labels(self):
        logger.debug(f"Attempting to suggest labels - current_index: {self.current_segment_index}, segments length: {len(self.segments)}")
        if not self.segments or self.current_segment_index >= len(self.segments):
            logger.error(f"Cannot suggest labels: segments empty or index out of range (index: {self.current_segment_index}, segments: {len(self.segments)})")
            messagebox.showwarning("Warning", "No segment available to suggest labels. Please upload a file.")
            return
        segment = self.segments[self.current_segment_index]
        logger.debug(f"Processing segment: {segment}")
        try:
            if not self.sentiment_classifier:
                logger.debug("Loading sentiment classifier: distilbert-base-uncased-finetuned-sst-2-english")
                self.sentiment_classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english', device=-1)
                logger.debug("Sentiment classifier loaded")
            try:
                with torch.no_grad():
                    sentiment_pred = self.sentiment_classifier(segment)
                sentiment = sentiment_pred[0]['label'].lower()
                sentiment_score = sentiment_pred[0]['score']
            except Exception as e:
                logger.error(f"Sentiment prediction failed: {str(e)}")
                logger.debug(traceback.format_exc())
                raise
        except Exception as e:
            logger.warning(f"Sentiment classifier failed: {str(e)}")
            logger.debug(traceback.format_exc())
            blob = TextBlob(segment)
            polarity = blob.sentiment.polarity
            sentiment = "negative" if polarity < 0 else "positive" if polarity > 0 else "neutral"
            sentiment_score = abs(polarity)
            logger.debug(f"Fallback to TextBlob: sentiment={sentiment}, score={sentiment_score}")

        contrast = any(keyword in segment.lower() for keyword in ['actually', 'but', 'however', 'just kidding'])
        top_emotion = 'happy' if sentiment == "positive" else "sad" if sentiment == "negative" else "neutral"
        intent = "joke" if sentiment == "positive" else "complain" if sentiment == "negative" else "inform"

        if sentiment == "negative" and contrast and self.prev_emotion == "happy":
            top_emotion = "disappointment"
            intent = "complain"

        logger.debug(f"Prev emotion: {self.prev_emotion}, Sentiment: {sentiment}, Score: {sentiment_score}, Contrast: {contrast}")
        logger.debug(f"Top emotion: {top_emotion}")
        self.emotion_var.set(top_emotion)
        self.intent_var.set(intent)
        logger.debug(f"After update - Suggested labels for '{segment}': {top_emotion}, {intent}")

    def save_annotation(self):
        emotion = self.emotion_var.get()
        intent = self.intent_var.get()
        if not emotion or not intent:
            messagebox.showwarning("Warning", "Please select an emotion and intent.")
            return
        if not self.segments or self.current_segment_index >= len(self.segments):
            logger.error(f"Cannot save annotation: segments empty or index out of range (index: {self.current_segment_index}, segments: {len(self.segments)})")
            messagebox.showwarning("Warning", "No segment available to annotate.")
            return
        segment = self.segments[self.current_segment_index]
        # Store the current state in history for undo
        self.history.append({
            'annotations': self.annotations.copy(),  # Copy current annotations
            'current_segment_index': self.current_segment_index,
            'prev_emotion': self.prev_emotion,
            'emotion_var': self.emotion_var.get(),
            'intent_var': self.intent_var.get()
        })
        # Proceed with saving the annotation
        self.annotations.append({
            'media_id': self.media_id,
            'filename': self.filename,
            'segment': segment,
            'emotion': emotion,
            'intent': intent
        })
        self.prev_emotion = emotion
        self.current_segment_index += 1
        # Enable the undo button since there's now an action to undo
        self.undo_button.config(state='normal')
        self.display_segment()

    def undo_annotation(self):
        if not self.history:
            messagebox.showinfo("Info", "Nothing to undo.")
            return
        # Pop the last state from history
        last_state = self.history.pop()
        # Restore the previous state
        self.annotations = last_state['annotations']
        self.current_segment_index = last_state['current_segment_index']
        self.prev_emotion = last_state['prev_emotion']
        self.emotion_var.set(last_state['emotion_var'])
        self.intent_var.set(last_state['intent_var'])
        # Redisplay the previous segment
        self.display_segment()
        # Disable the undo button if there's nothing left to undo
        if not self.history:
            self.undo_button.config(state='disabled')
        logger.debug(f"Undo performed. Current segment index: {self.current_segment_index}, Annotations: {len(self.annotations)}")

    def visualize_suggestions(self):
        if not self.segments or self.current_segment_index >= len(self.segments):
            messagebox.showwarning("Warning", "No segment available for visualization.")
            return
        
        segment = self.segments[self.current_segment_index]
        logger.debug(f"Original segment: {segment}")
        
        try:
            # Tokenize the input segment
            tokenized_data = self.tokenizer(segment, return_tensors='np', padding=True, truncation=True, max_length=32)
            input_ids = tokenized_data['input_ids']
            logger.debug(f"Tokenized input IDs: {input_ids}, shape: {input_ids.shape}")
            tokens = [self.tokenizer.convert_ids_to_tokens(ids) for ids in input_ids][0]
            logger.debug(f"Raw tokens before filtering: {tokens}, length: {len(tokens)}")

            # Prepare background data for SHAP
            background_texts = [
                "This is neutral text about nothing in particular.",
                "I'm feeling okay today.",
                "The weather is normal outside.",
                "The project is on schedule.",
                "Everything is going according to plan.",
                "This is a typical day."
            ]
            tokenized_background = self.tokenizer(background_texts, return_tensors='np', padding=True, truncation=True, max_length=32)
            background_input_ids = tokenized_background['input_ids']
            logger.debug(f"Tokenized background input IDs shape: {background_input_ids.shape}")

            # Define model prediction function for SHAP
            def model_predict(input_ids):
                with torch.no_grad():
                    attention_mask = np.ones_like(input_ids)
                    inputs = torch.tensor(input_ids).long()
                    masks = torch.tensor(attention_mask).long()
                    outputs = self.model(inputs, attention_mask=masks)
                    logits = outputs.logits.numpy()
                    probs = torch.softmax(torch.tensor(logits), dim=-1).numpy()
                logger.debug(f"Model prediction probabilities: {probs}")
                return probs[:, 1]  # Return probability of positive sentiment

            # Compute SHAP values
            explainer = shap.KernelExplainer(model_predict, background_input_ids[:3])
            shap_values = explainer.shap_values(input_ids, nsamples=500)
            logger.debug(f"Raw SHAP values: {shap_values}")

            # Process tokens and SHAP values
            shap_values_array = np.array(shap_values)
            if len(shap_values_array.shape) > 1:
                shap_values_reshaped = shap_values_array.reshape(1, -1)
            else:
                shap_values_reshaped = shap_values_array.reshape(1, -1)
            logger.debug(f"SHAP values reshaped: {shap_values_reshaped}, shape: {shap_values_reshaped.shape}")

            # Filter out special tokens
            valid_indices = []
            for i, token in enumerate(tokens):
                if token not in ['[CLS]', '[SEP]', '[PAD]']:
                    valid_indices.append(i)
            
            tokens_filtered = [tokens[i] for i in valid_indices]
            # Truncate long tokens by removing numeric suffixes (e.g., "overwhelming_282267" -> "overwhelming")
            tokens_filtered = [token.split('_')[0] if '_' in token and token.split('_')[-1].isdigit() else token for token in tokens_filtered]
            shap_values_filtered = [shap_values_reshaped[0, i] for i in valid_indices]
            
            logger.debug(f"Tokens filtered: {tokens_filtered}")
            logger.debug(f"SHAP values filtered: {shap_values_filtered}")

            # Compute model prediction for the segment
            inputs = self.tokenizer(segment, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                outputs = self.model(**inputs)
            logits = outputs.logits.detach().numpy()
            probs = torch.softmax(torch.tensor(logits), dim=-1).numpy()
            prediction_prob = probs[0, 1]  # Probability of positive sentiment
            prediction_label = "Positive" if prediction_prob > 0.5 else "Negative"

            # Plot summary plot (scatter plot)
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create horizontal bars with SHAP values
            for i, (token, value) in enumerate(zip(tokens_filtered, shap_values_filtered)):
                color = '#ff0051' if value >= 0 else '#008bfb'  # SHAP color scheme
                ax.barh(i, value, color=color, alpha=0.8, height=0.6)
                # Position the SHAP value above the bar
                x_pos = value if value >= 0 else 0  # Align with the end of the bar for positive, center for negative
                ha = 'left' if value >= 0 else 'right'  # Horizontal alignment
                x_offset = 0.005 if value >= 0 else -0.005  # Small offset to avoid overlap with bar
                ax.text(x_pos + x_offset, i + 0.5, f"{value:.4f}", 
                        va='bottom', ha=ha, fontsize=6)

            # Customize the plot
            ax.set_yticks(range(len(tokens_filtered)))
            ax.set_yticklabels(tokens_filtered, fontsize=8)
            ax.axvline(x=0, color='black', linestyle='-', alpha=0.5, linewidth=1)
            ax.set_xlabel("SHAP value (impact on model output)", fontsize=12)
            ax.set_title(f"SHAP Summary for {prediction_label} Sentiment (Prob: {prediction_prob:.6f})", fontsize=14)
            
            # Add segment information
            fig.text(0.5, 0.02, f"Segment: {segment}", ha='center', fontsize=10, wrap=True)
            
            # Adjust layout with standard margins
            plt.margins(y=0.1)
            plt.tight_layout()
            plt.subplots_adjust(left=0.2, bottom=0.15)
            
            # Save summary plot
            shap_filename = f"shap_summary_segment{self.current_segment_index + 1}.png"
            plt.savefig(shap_filename, bbox_inches='tight', dpi=150)
            plt.close()
            logger.debug(f"Summary plot saved as: {os.path.abspath(shap_filename)}")
            
            # Generate Force Plot based on selection
            plot_type = self.force_plot_type.get()
            logger.debug(f"Force plot type selected: {plot_type}")
            
            if plot_type == "traditional":
                force_plot_filename = self.generate_traditional_force_plot(tokens_filtered, shap_values_filtered, segment, prediction_prob)
            else:
                force_plot_filename = self.generate_text_based_force_plot(tokens_filtered, shap_values_filtered, segment)
            
            logger.debug("\n=== DETAILED SHAP ANALYSIS ===")
            for token, value in zip(tokens_filtered, shap_values_filtered):
                logger.debug(f"Token: '{token}' -> SHAP: {value:.6f}")
            logger.debug("==============================\n")
            
            if force_plot_filename:
                messagebox.showinfo("Visualization", f"SHAP visualizations saved:\n- Summary plot: {shap_filename}\n- Force plot: {force_plot_filename}")
            else:
                messagebox.showinfo("Visualization", f"SHAP summary plot saved as {shap_filename}")
                
        except Exception as e:
            logger.error(f"SHAP visualization failed: {str(e)}")
            logger.debug(traceback.format_exc())
            messagebox.showerror("Error", "Failed to generate SHAP visualization.")

    def generate_traditional_force_plot(self, tokens, shap_values, segment, prediction_prob):
        """Generate a custom SHAP waterfall plot with precise decimal places and standard SHAP color scheme."""
        try:
            expected_value = 0.5  # For balanced sentiment analysis
            
            # Convert to numpy array
            values_array = np.array(shap_values)
            logger.debug(f"SHAP values array: {values_array}")
            
            # Compute the sum of SHAP values
            shap_sum = np.sum(values_array)
            computed_prediction = expected_value + shap_sum
            logger.debug(f"Computed prediction from SHAP: {computed_prediction}, True prediction: {prediction_prob}")

            # If the computed prediction doesn't match the true prediction, scale the SHAP values
            if abs(computed_prediction - prediction_prob) > 1e-4:  # Allow for small numerical differences
                scaling_factor = (prediction_prob - expected_value) / shap_sum if shap_sum != 0 else 1
                values_array = values_array * scaling_factor
                logger.debug(f"Scaled SHAP values by factor {scaling_factor} to match true prediction: {values_array}")

            # Create the waterfall plot
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Sort tokens and SHAP values by absolute value (largest to smallest)
            sorted_indices = np.argsort(np.abs(values_array))[::-1]
            sorted_values = values_array[sorted_indices]
            sorted_tokens = [tokens[i] for i in sorted_indices]
            
            # Compute cumulative contributions starting from the expected value
            cumulative = expected_value
            
            # Plot each contribution
            for i, (value, token) in enumerate(zip(sorted_values, sorted_tokens)):
                # Determine color based on SHAP value (standard SHAP colors: red for positive, blue for negative)
                color = "#ff0051" if value >= 0 else "#008bfb"
                
                # Draw the bar
                ax.barh(i, value, left=cumulative, color=color, edgecolor="black", linewidth=0.5)
                
                # Add the SHAP value label with 6 decimal places
                label = f"+{value:.6f}" if value > 0 else f"{value:.6f}"
                label_pos = cumulative + value/2 if abs(value) > 0.05 else cumulative + value
                ax.text(label_pos, i, label, va='center', ha='center', fontsize=10, color='black' if abs(value) > 0.05 else 'gray')
                
                # Update cumulative value
                cumulative += value
            
            # Draw connecting lines between bars
            for i in range(len(sorted_values) - 1):
                ax.plot([cumulative - sorted_values[i], cumulative - sorted_values[i]], [i, i + 1], color='gray', linestyle='--', alpha=0.5)
            
            # Set y-axis labels (tokens)
            ax.set_yticks(range(len(sorted_tokens)))
            ax.set_yticklabels([f"{token}" for token in sorted_tokens], fontsize=10)
            
            # Set x-axis labels
            ax.set_xlabel("Model Output Value", fontsize=12)
            
            # Add base value bar
            ax.barh(len(sorted_tokens), expected_value, color='#b3b3b3', edgecolor='black', linewidth=0.5)
            ax.text(expected_value/2, len(sorted_tokens), f"Base value\n{expected_value:.3f}", ha='center', va='center', fontsize=10)
            
            # Add prediction value
            ax.axvline(cumulative, color='gray', linestyle='--', alpha=0.5)
            ax.text(cumulative, -0.5, f"f(x) = {prediction_prob:.6f}", ha='center', va='top', fontsize=10, color='red' if prediction_prob > 0.5 else 'blue')
            
            # Set title with proper spacing
            ax.set_title("SHAP Waterfall Plot", fontsize=14, pad=20)
            ax.text(0.5, -0.15, f"Segment: {segment}", ha='center', transform=ax.transAxes, fontsize=8, wrap=True)
            
            # Adjust layout and margins
            plt.margins(y=0.1)
            ax.set_xlim(min(0, min([cumulative] + [expected_value + sum(sorted_values[:i+1]) for i in range(len(sorted_values))])) - 0.1,
                        max(1, max([cumulative] + [expected_value + sum(sorted_values[:i+1]) for i in range(len(sorted_values))])) + 0.1)
            
            # Invert y-axis to match SHAP waterfall style
            ax.invert_yaxis()
            
            plt.tight_layout()
            plt.subplots_adjust(bottom=0.25)
            
            # Save the plot
            filename = f"shap_force_traditional_segment{self.current_segment_index + 1}.png"
            plt.savefig(filename, bbox_inches='tight', dpi=150)
            plt.close(fig)
            logger.debug(f"Traditional force plot saved as: {os.path.abspath(filename)}")
            return filename

        except Exception as e:
            logger.error(f"Traditional force plot generation failed: {str(e)}")
            logger.debug(traceback.format_exc())
            return None

    def generate_text_based_force_plot(self, tokens, shap_values, segment):
        """Generate text-based SHAP force plot."""
        try:
            # Calculate prediction probability
            outputs = self.model(**self.tokenizer(segment, return_tensors='pt', padding=True, truncation=True))
            logits = outputs.logits.detach().numpy()
            probs = torch.softmax(torch.tensor(logits), dim=-1).numpy()
            prediction = probs[0, 1]  # Positive sentiment probability
            
            expected_value = 0.5  # For balanced sentiment analysis
            
            # Create text-based force plot
            fig, ax = plt.subplots(figsize=(14, 10))
            
            # Main title with prediction and expected value
            ax.text(0.5, 0.95, f"Text-based Force Plot", ha='center', fontsize=16, weight='bold')
            ax.text(0.5, 0.88, f"Prediction (Positive Sentiment Probability): {prediction:.3f}", ha='center', fontsize=14)
            ax.text(0.5, 0.83, f"Expected Value: {expected_value:.3f}", ha='center', fontsize=14)
            
            # Create text with colored background
            y_pos = 0.7
            x_center = 0.5
            word_positions = []
            total_width = 0
            
            # First pass: calculate positions and widths
            current_x = 0
            for word, value in zip(tokens, shap_values):
                word_width = max(len(word) * 0.015, 0.05)  # Ensure minimum width
                word_positions.append((word, value, current_x, word_width))
                current_x += word_width + 0.01  # Add spacing between words
                total_width = current_x - 0.01  # Remove last spacing
            
            # Second pass: center and draw
            start_x = x_center - total_width/2
            for i, (word, value, x_offset, width) in enumerate(word_positions):
                centered_x = start_x + x_offset
                
                # Color based on SHAP value
                if value > 0:
                    color = '#ff0051'  # SHAP red
                    alpha = min(abs(value) * 2, 0.8)
                else:
                    color = '#008bfb'  # SHAP blue
                    alpha = min(abs(value) * 2, 0.8)
                
                # Draw background rectangle
                rect = plt.Rectangle((centered_x, y_pos - 0.02), width, 0.05, 
                                    facecolor=color, alpha=alpha)
                ax.add_patch(rect)
                
                # Add word
                ax.text(centered_x + width/2, y_pos, word, ha='center', va='center', fontsize=10)
                # Add SHAP value below the word
                ax.text(centered_x + width/2, y_pos - 0.04, f"{value:.4f}", ha='center', va='top', fontsize=8)
            
            # Add legend for SHAP values (sorted by importance)
            y_pos = 0.55
            ax.text(0.5, y_pos, "Top Word Contributions:", ha='center', fontsize=14, weight='bold')
            y_pos -= 0.03
            
            # Sort by absolute SHAP value
            word_shap_mapping = list(zip(tokens, shap_values))
            word_shap_mapping.sort(key=lambda x: abs(x[1]), reverse=True)
            
            for i, (word, value) in enumerate(word_shap_mapping):
                if i >= 5:  # Limit to top 5 words
                    break
                color = '#ff0051' if value > 0 else '#008bfb'
                ax.text(0.5, y_pos, f"{word}: {value:.4f}", ha='center', fontsize=12, color=color)
                y_pos -= 0.025
            
            # Add explanation
            ax.text(0.5, 0.1, "Color Legend:", ha='center', fontsize=14, weight='bold')
            ax.text(0.5, 0.07, "Red: Pushes prediction towards positive sentiment", ha='center', fontsize=12, color='#ff0051')
            ax.text(0.5, 0.04, "Blue: Pushes prediction towards negative sentiment", ha='center', fontsize=12, color='#008bfb')
            
            # Add segment text
            ax.text(0.5, 0.78, f"Segment: {segment}", ha='center', fontsize=10, style='italic', wrap=True)
            
            # Remove axis
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            filename = f"shap_force_text_segment{self.current_segment_index + 1}.png"
            plt.tight_layout()
            plt.savefig(filename, bbox_inches='tight', dpi=150)
            plt.close()
            logger.debug(f"Text-based force plot saved as {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"Text-based force plot generation failed: {str(e)}")
            logger.debug(traceback.format_exc())
            return None

    def export_csv(self):
        df = pd.DataFrame(self.annotations)
        df.to_csv('annotations_export.csv', index=False)
        messagebox.showinfo("Export", "Annotations exported to annotations_export.csv")

if __name__ == "__main__":
    os.environ["OMP_NUM_THREADS"] = "1"
    torch.set_num_threads(1)
    import multiprocessing
    multiprocessing.set_start_method('fork', force=True)
    root = tk.Tk()
    app = EmotionIntentAnnotator(root)
    root.mainloop()
