from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, validators

class SensorInputForm(FlaskForm):
    thalachh = FloatField('Heart Rate', [validators.InputRequired(), validators.NumberRange(min=0)])
    restecg = FloatField('ECG', [validators.InputRequired(), validators.NumberRange(min=0)])

class UserInputForm(FlaskForm):
    age = IntegerField('Age', [validators.InputRequired(), validators.NumberRange(min=1)])
    trtbps = FloatField('Resting Blood Pressure', [validators.NumberRange(min=0)])
    chol = FloatField('Cholesterol', [validators.NumberRange(min=0)])
    oldpeak = FloatField('Oldpeak', [validators.NumberRange(min=0)])
    sex = IntegerField('Sex', [validators.InputRequired(), validators.AnyOf([0, 1])])
    exng = IntegerField('Exercise Induced Angina', [validators.AnyOf([0, 1])])
    caa = IntegerField('Number of Major Vessels', [validators.NumberRange(min=0, max=4)])
    cp = IntegerField('Chest Pain Type', [validators.NumberRange(min=0, max=3)])
    fbs = IntegerField('Fasting Blood Sugar', [validators.AnyOf([0, 1])])
    slp = IntegerField('Slope', [validators.NumberRange(min=0, max=2)])
    thall = IntegerField('Thalassemia', [validators.NumberRange(min=0, max=3)])
