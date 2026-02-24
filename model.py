import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# Updated dataset with grades
data = {
    'attendance': [95, 88, 75, 60, 50, 85, 92, 40, 70, 80],
    'study_hours': [7, 5, 3, 2, 1, 6, 7, 1, 3, 4],
    'internal_marks': [92, 85, 70, 55, 40, 88, 95, 35, 65, 78],
    'grade': [4, 3, 2, 1, 0, 3, 4, 0, 2, 3]  # 4=A, 3=B, 2=C, 1=D, 0=Fail
}

df = pd.DataFrame(data)

X = df[['attendance', 'study_hours', 'internal_marks']]
y = df['grade']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

accuracy = model.score(X_test, y_test)

def predict_performance(attendance, study_hours, internal_marks):
    prediction = model.predict([[attendance, study_hours, internal_marks]])
    probability = model.predict_proba([[attendance, study_hours, internal_marks]])
    return prediction[0], round(max(probability[0]) * 100, 2)