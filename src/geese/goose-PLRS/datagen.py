import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Subjects
subjects = ["Math", "Physics", "Chemistry", "Biology", "English", "History", "Computer Science"]

# Generate Student Performance Data
num_students = 1000
data = []

for student_id in range(1, num_students + 1):
    for subject in subjects:
        exam_score = np.random.randint(30, 100)  # Exam score out of 100
        assignment_score = np.random.randint(0, 10)  # Assignment score out of 10
        participation_score = np.random.randint(0, 20)  # Participation out of 20
        attendance_score = np.random.randint(0, 20)  # Attendance out of 20
        
        data.append([student_id, subject, exam_score, assignment_score, participation_score, attendance_score])

# Create DataFrame
performance_df = pd.DataFrame(data, columns=["Student ID", "Subject", "Exam Score", "Assignment Score", "Participation Score", "Attendance Score"])
performance_df.to_csv("src/geese/goose-PLRS/student_performance.csv", index=False)
print("Student performance dataset saved!")

# Generate Study Materials Data
study_materials = []
material_types = ["Video", "Article", "Quiz"]

topics = {
    "Math": ["Algebra", "Geometry", "Calculus", "Statistics"],
    "Physics": ["Mechanics", "Electricity", "Optics", "Thermodynamics"],
    "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry"],
    "Biology": ["Genetics", "Anatomy", "Ecology"],
    "English": ["Grammar", "Literature", "Writing Skills"],
    "History": ["Ancient History", "Modern History", "World Wars"],
    "Computer Science": ["Programming", "Data Structures", "Algorithms"]
}

for subject, topic_list in topics.items():
    for topic in topic_list:
        for _ in range(5):  # Generate 5 materials per topic
            material_type = np.random.choice(material_types)
            difficulty = np.random.choice(["Beginner", "Intermediate", "Advanced"])
            resource_link = f"https://example.com/{subject.lower()}/{topic.lower()}-{material_type.lower()}"
            
            study_materials.append([subject, topic, material_type, difficulty, resource_link])

# Create DataFrame
study_materials_df = pd.DataFrame(study_materials, columns=["Subject", "Topic", "Material Type", "Difficulty Level", "Resource Link"])
study_materials_df.to_csv("src/geese/goose-PLRS/study_materials.csv", index=False)
print("Study materials dataset saved!")
