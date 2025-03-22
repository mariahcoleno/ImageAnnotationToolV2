import sqlite3
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torchvision import models, transforms
from sklearn.model_selection import train_test_split
from PIL import Image

# Load labeled data from database
def load_labeled_data():
    conn = sqlite3.connect('annotation_db.sqlite')
    c = conn.cursor()
    c.execute("SELECT i.file_path, a.label FROM images i JOIN annotations a ON i.id = a.image_id")
    data = c.fetchall()
    conn.close()
    
    X, y = [], []
    transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    for file_path, label in data:
        img = Image.open(file_path).convert('RGB')
        img = transform(img)
        X.append(img)
        y.append(1 if label == 'dog' else 0)  # Assuming 'cat' = 0, 'dog' = 1
    return torch.stack(X), torch.tensor(y)

# Define CNN (simple ResNet18)
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.model = models.resnet18(weights="DEFAULT")  # Updated here
        self.model.fc = nn.Linear(self.model.fc.in_features, 2)  # 2 classes: cat/dog
    
    def forward(self, x):
        return self.model(x)

# Compute accuracy
def compute_accuracy(model, loader):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    model.train()
    return correct / total

# Main training
def main():
    # Load data
    X, y = load_labeled_data()
    print(f"Loaded {len(X)} labeled images")
    
    # Split: 80/10/10
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    print(f"Train size: {len(X_train)}, Val size: {len(X_val)}, Test size: {len(X_test)}")
    
    # DataLoaders
    train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=16, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=16)
    test_loader = DataLoader(TensorDataset(X_test, y_test), batch_size=16)
    
    # Model, loss, optimizer
    model = CNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # Training loop
    num_epochs = 10
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        
        # Compute accuracies
        train_acc = compute_accuracy(model, train_loader)
        val_acc = compute_accuracy(model, val_loader)
        avg_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1}, Loss: {avg_loss:.4f}, Training Accuracy: {train_acc:.2%}, "
              f"Validation Accuracy: {val_acc:.2%}")
    
    # Final test accuracy
    test_acc = compute_accuracy(model, test_loader)
    print(f"Test Accuracy: {test_acc:.2%}")
    
    # Save model
    torch.save(model.state_dict(), 'cat_dog_cnn_pytorch.pth')
    print("Model saved as cat_dog_cnn_pytorch.pth")

if __name__ == "__main__":
    main()
