import csv
import random

def generate_student_data(num_students):
 
  data = []
  for _ in range(num_students):
    attendance = random.randint(1, 20)
    participation = random.randint(1, 20)
    assignment_score = random.randint(1, 10)
    year_of_study = random.randint(1, 6)  
    num_subjects = random.randint(3, 7) 
    class_size = random.randint(40, 200)
    peer_performance = random.randint(1, 100)
    cats = random.randint(1, 40)
    rats = random.randint(1, 10)

    
    final_exam = (
        0.45 * attendance + 
        0.30 * participation + 
        0.45 * assignment_score + 
        0.60 * (cats / 4) +  
        0.30 * rats +
        0.10 * (peer_performance / 3)  
        - 0.15 * year_of_study -  
        0.10 * num_subjects -    
        0.05 * (class_size / 20)  
    ) * 4  
    final_exam = int(final_exam) 

    student = {
        "attendance": attendance,
        "participation": participation,
        "assignment score": assignment_score,
        "year_of study": year_of_study,
        "number of subjects taken": num_subjects,
        "class size": class_size,
        "peer performance": peer_performance,
        "cats": cats,
        "rats": rats,
        "Final exam": final_exam
    }
    data.append(student)
  return data

def write_to_csv(data, filename):
  
  with open(filename, "w", newline="") as csvfile:
    fieldnames = data[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

if __name__ == "__main__":
  num_students = 10250
  student_data = generate_student_data(num_students)
  write_to_csv(student_data, "src/geese/goose-Per-pre/dataset.csv") 
  print(f"Generated data for {num_students} students and saved to student_performance_data.csv")