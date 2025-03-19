# train_cnn_pytorch.py
import sqlite3
import os
import numpy as np
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from sklearn.model_selection import train_test_split
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("Script started!")

db_path = 'annotation_db.sqlite' 

image_dir = os.path.expanduser('~/Documents/AnnotationProject/images')
img_size = (64, 64)

# Custom Dataset
class CatDogDataset(Dataset):
    def __init__(self, file_paths, labels, transform=None):
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        img = Image.open(self.file_paths[idx]).convert('RGB')
        if self.transform:
            img = self.transform(img)
        label = self.labels[idx]
        return img, label

# Load data
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("SELECT i.file_path, a.label FROM images i JOIN annotations a ON i.id = a.image_id")
data = cursor.fetchall()
conn.close()

file_paths = [row[0] for row in data]
labels = [1 if row[1] == 'dog' else 0 for row in data]  # 1 = dog, 0 = cat

# Updated Data Split: Train (64), Validation (16), Test (20)
X_temp, X_test, y_temp, y_test = train_test_split(file_paths, labels, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=0.2, random_state=42)

transform = transforms.Compose([
    transforms.Resize(img_size),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
])

train_dataset = CatDogDataset(X_train, y_train, transform=transform)
val_dataset = CatDogDataset(X_val, y_val, transform=transform)
test_dataset = CatDogDataset(X_test, y_test, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

# Define CNN
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.conv3 = nn.Conv2d(64, 64, 3)
        self.fc1 = nn.Linear(64 * 6 * 6, 64)
        self.fc2 = nn.Linear(64, 1)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 64 * 6 * 6)
        x = self.relu(self.fc1(x))
        x = self.sigmoid(self.fc2(x))
        return x

# Train model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SimpleCNN().to(device)
criterion = nn.BCELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

logging.debug("Training model")
for epoch in range(10):
    # Training Loop
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device).float()
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs.squeeze(), labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        predicted = (outputs.squeeze() > 0.5).float()
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    train_accuracy = 100 * correct / total

    # Validation Loop
    model.eval()
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device).float()
            outputs = model(images)
            predicted = (outputs.squeeze() > 0.5).float()
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()
    val_accuracy = 100 * val_correct / val_total

    print(f"Epoch {epoch+1}, Loss: {running_loss/len(train_loader):.4f}, "
          f"Training Accuracy: {train_accuracy:.2f}%, Validation Accuracy: {val_accuracy:.2f}%")

# Evaluate model on test set
model.eval()
correct = 0
total = 0
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device).float()
        outputs = model(images)
        predicted = (outputs.squeeze() > 0.5).float()
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_accuracy = 100 * correct / total
print(f"Test Accuracy: {test_accuracy:.2f}%")

# Save model
torch.save(model.state_dict(), 'cat_dog_cnn_pytorch.pth')
logging.debug("Model saved as cat_dog_cnn_pytorch.pth")
