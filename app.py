from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]

    if not file:
        return "No file uploaded"

    math_marks = []
    physics_marks = []
    python_marks = []
    students = []

    stream = file.stream.read().decode("UTF8").splitlines()
    reader = csv.DictReader(stream)

    try:
        for row in reader:
            name = row["Name"]
            math = int(row["Math"])
            physics = int(row["Physics"])
            python = int(row["Python"])

            math_marks.append(math)
            physics_marks.append(physics)
            python_marks.append(python)

            total = math + physics + python

            students.append({
                "name": name,
                "math": math,
                "physics": physics,
                "python": python,
                "total": total
            })

    except Exception as e:
        return f"Error processing file: {str(e)}"

    if not students:
        return "Uploaded file is empty or invalid format."

    avg_math = sum(math_marks) / len(math_marks)
    avg_physics = sum(physics_marks) / len(physics_marks)
    avg_python = sum(python_marks) / len(python_marks)

    averages = {
        "Math": avg_math,
        "Physics": avg_physics,
        "Python": avg_python
    }

    weak_subject = min(averages, key=averages.get)
    topper = max(students, key=lambda x: x["total"])

    class_avg_total = (avg_math + avg_physics + avg_python)

    for student in students:
        if student["total"] > class_avg_total:
            student["performance"] = "Above Average"
        elif student["total"] < class_avg_total:
            student["performance"] = "Below Average"
        else:
            student["performance"] = "Average"

    def get_grade(avg):
        if avg >= 90:
            return "Excellent"
        elif avg >= 75:
            return "Good"
        elif avg >= 50:
            return "Average"
        else:
            return "Needs Improvement"

    return render_template(
        "result.html",
        students=students,
        topper=topper,
        avg_math=avg_math,
        avg_physics=avg_physics,
        avg_python=avg_python,
        weak_subject=weak_subject,
        grade_math=get_grade(avg_math),
        grade_physics=get_grade(avg_physics),
        grade_python=get_grade(avg_python)
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)