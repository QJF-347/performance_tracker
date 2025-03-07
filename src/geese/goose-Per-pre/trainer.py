import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import r2_score

# Load dataset
data = pd.read_csv("src/geese/goose-Per-pre/dataset.csv").dropna()

# Separate features and target
X = data.drop(columns=["Final exam"]).values  # Features
y = data["Final exam"].values.reshape(-1, 1)  # Target (reshaped for scaler)

# Normalize features and target
X_scaler = MinMaxScaler()
X = X_scaler.fit_transform(X)

y_scaler = MinMaxScaler()
y = y_scaler.fit_transform(y)

# Save scalers
joblib.dump(X_scaler, "X_scaler.pkl")
joblib.dump(y_scaler, "y_scaler.pkl")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert to PyTorch tensors
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32)

# Create DataLoader
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# Define Neural Network Model
class StudentPerformanceModel(nn.Module):
    def __init__(self):
        super(StudentPerformanceModel, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(9, 32),  
            nn.LeakyReLU(0.01),  
            nn.Dropout(0.2),    
            nn.Linear(32, 16),  
            nn.LeakyReLU(0.01),  
            nn.Linear(16, 8),  
            nn.ReLU(),  
            nn.Linear(8, 1)
        )
    
    def forward(self, x):
        return self.model(x)

# Initialize Model
model = StudentPerformanceModel()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.00025)

# Training Loop
epochs = 50
for epoch in range(epochs):
    model.train()
    total_loss = 0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        predictions = model(X_batch)
        loss = criterion(predictions, y_batch)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    
    print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(train_loader):.4f}")

# Save the trained model
torch.save(model.state_dict(), "src/geese/goose-Per-pre/goose-per-pre/student_performance_model.pth")

# Evaluate Model
model.eval()
y_pred = model(X_test_tensor).cpu().detach().numpy()
y_test_actual = y_test_tensor.cpu().numpy()

# Convert back to original scale
y_pred = y_scaler.inverse_transform(y_pred)
y_test_actual = y_scaler.inverse_transform(y_test_actual)

# Calculate MSE and R² Score
mse = np.mean((y_pred - y_test_actual) ** 2)
r2 = r2_score(y_test_actual, y_pred)

print(f"Test MSE: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# ============================
#      LOAD & PREDICT
# ============================
def load_model():
    # Load model
    model = StudentPerformanceModel()
    model.load_state_dict(torch.load("src/geese/goose-Per-pre/goose-per-pre/student_performance_model.pth"))
    model.eval()
    
    # Load scalers
    X_scaler = joblib.load("X_scaler.pkl")
    y_scaler = joblib.load("y_scaler.pkl")

    return model, X_scaler, y_scaler

def predict(model, X_scaler, y_scaler, new_data):
    # Normalize input features
    new_data_scaled = X_scaler.transform(new_data)

    # Convert to tensor
    new_data_tensor = torch.tensor(new_data_scaled, dtype=torch.float32)

    # Predict
    with torch.no_grad():
        prediction = model(new_data_tensor).numpy()

    # Convert  back to original 
    final_exam_score = y_scaler.inverse_transform(prediction.reshape(-1, 1)).flatten()[0]

    return final_exam_score

# Example Prediction
model, X_scaler, y_scaler = load_model()
new_student_data = np.array([[10, 15, 8, 3, 5, 100, 45, 35, 7]])  # Sample input
predicted_score = predict(model, X_scaler, y_scaler, new_student_data)

print(f"Predicted Final Exam Score: {predicted_score:.2f}")
