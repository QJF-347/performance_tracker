import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np


MODEL_PATH = 'src/geese/goose-Per-pre/goose-per-pre/student_performance_model.pth'

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
    
model = StudentPerformanceModel()
model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
model.eval()

def predict_final_exam(attendance, participation, assignment_score, year_of_study,
                        num_subjects, class_size, peer_performance, cats, rats):
    input_data = torch.tensor([[attendance, participation, assignment_score, year_of_study,
                                num_subjects, class_size, peer_performance, cats, rats]],
                              dtype=torch.float32)
    with torch.no_grad():
        prediction = model(input_data).item()
    return max(0, min(100, prediction))