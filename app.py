from flask import Flask, render_template, request
from model import predict_performance, accuracy
import mysql.connector
import os

# Connect to MySQL using environment variable
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("DB_PASSWORD"),
    database="student_db"
)

cursor = db.cursor()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    prob = None

    if request.method == 'POST':
        attendance = int(request.form['attendance'])
        study_hours = int(request.form['study_hours'])
        internal_marks = int(request.form['internal_marks'])

        # Backend validation
        if not (0 <= attendance <= 100 and 
                0 <= study_hours <= 24 and 
                0 <= internal_marks <= 100):

            cursor.execute("SELECT * FROM predictions")
            history = cursor.fetchall()

            return render_template(
                'index.html',
                result="Invalid Input! Please enter valid values.",
                prob=None,
                accuracy=round(accuracy * 100, 2),
                history=history
            )

        prediction, prob = predict_performance(attendance, study_hours, internal_marks)

        grades = {
            4: "Grade A",
            3: "Grade B",
            2: "Grade C",
            1: "Grade D",
            0: "Fail"
        }

        result = grades[prediction]

        # Insert into database
        cursor.execute(
            "INSERT INTO predictions (attendance, study_hours, internal_marks, grade) VALUES (%s, %s, %s, %s)",
            (attendance, study_hours, internal_marks, result)
        )
        db.commit()

    # Fetch history
    cursor.execute("SELECT * FROM predictions")
    history = cursor.fetchall()

    return render_template(
        'index.html',
        result=result,
        prob=prob,
        accuracy=round(accuracy * 100, 2),
        history=history
    )

if __name__ == '__main__':
    app.run(debug=True, port=5050)