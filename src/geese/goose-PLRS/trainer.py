import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from torch.utils.data import Dataset, DataLoader

# Load student performance data
student_data = pd.read_csv("src/geese/goose-PLRS/student_performance.csv")
study_materials = pd.read_csv("src/geese/goose-PLRS/study_materials.csv")



# Encode subjects as numerical values
subject_encoder = LabelEncoder()
study_materials["subject_id"] = subject_encoder.fit_transform(study_materials["Subject"])
student_data["subject_id"] = subject_encoder.transform(student_data["Subject"])
student_data.rename(columns={
    "Student ID": "student_id",
    "Subject": "subject"
}, inplace=True)

study_materials.rename(columns={"Subject": "subject"}, inplace=True)
# Normalize scores
scaler = MinMaxScaler()
student_data["Exam Score"] = scaler.fit_transform(student_data[["Exam Score"]])


# Create Student-Study Material Interaction Matrix
interactions = student_data.groupby(["student_id", "subject"]).mean()["Exam Score"].unstack().fillna(0)


# Convert to PyTorch tensor
interaction_matrix = torch.tensor(interactions.values, dtype=torch.float32)
num_students, num_subjects = interaction_matrix.shape

# Define Collaborative Filtering Model
class MatrixFactorization(nn.Module):
    def __init__(self, num_students, num_subjects, embedding_dim=10):
        super(MatrixFactorization, self).__init__()
        self.student_embedding = nn.Embedding(num_students, embedding_dim)
        self.subject_embedding = nn.Embedding(num_subjects, embedding_dim)
    
    def forward(self, student_idx, subject_idx):
        student_embedded = self.student_embedding(student_idx)
        subject_embedded = self.subject_embedding(subject_idx)
        return (student_embedded * subject_embedded).sum(1)

# Initialize model
embedding_dim = 10
model = MatrixFactorization(num_students, num_subjects, embedding_dim)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

# Prepare training data
student_idx, subject_idx = np.where(interaction_matrix > 0)
labels = interaction_matrix[student_idx, subject_idx]
student_idx = torch.tensor(student_idx, dtype=torch.long)
subject_idx = torch.tensor(subject_idx, dtype=torch.long)
labels = torch.tensor(labels, dtype=torch.float32)

# Training loop
epochs = 50
for epoch in range(epochs):
    optimizer.zero_grad()
    predictions = model(student_idx, subject_idx)
    loss = criterion(predictions, labels)
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}/{epochs}, Loss: {loss.item():.4f}")

# Function to recommend study materials
def recommend_study_materials(student_id, top_n=5):
    student_idx = torch.tensor([student_id], dtype=torch.long)
    subject_scores = model(student_idx, torch.arange(num_subjects))
    recommended_subjects = torch.argsort(subject_scores, descending=True)[:top_n]
    recommended_subjects = recommended_subjects.numpy()
    recommended_subject_names = subject_encoder.inverse_transform(recommended_subjects)
    return study_materials[study_materials["subject"].isin(recommended_subject_names)]

# Example Recommendation
student_id = 0
recommended_materials = recommend_study_materials(student_id)
print(recommended_materials)
