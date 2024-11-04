from dbconfig.app import db
from flask import request, jsonify
import pandas as pd
import pickle
from controllers.patient.Diagnosis.preprocess import preprocess

with open(r'controllers/patient/Diagnosis/svc.pkl', 'rb') as model:
    svc = pickle.load(model)
with open(r'controllers/patient/Diagnosis/scaler.pkl', 'rb') as scaler:
    scaler = pickle.load(scaler)

model_cols = ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak',
                    'sex_1', 'exng_1', 'caa_1', 'caa_2', 'caa_3', 'caa_4',
                    'cp_1', 'cp_2', 'cp_3', 'fbs_1', 
                    'restecg_1', 'restecg_2', 'slp_1', 'slp_2',
                    'thall_1', 'thall_2', 'thall_3']

def predict():
    if request.method == 'POST':
        data = request.get_json()

    saved_data = data

    print(saved_data)

    preprocess(data)
        
    if not data or not all(key in data for key in ['age', 'trtbps', 'chol', 'thalachh', 'oldpeak', 
                                                   'sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall']):
        return jsonify({'error': 'Missing value, please enter again.'}), 400

    df = pd.DataFrame([data])

    df = pd.get_dummies(df, columns=['sex', 'exng', 'caa', 'cp', 'fbs', 'restecg', 'slp', 'thall'])
    
    df = df.reindex(columns=model_cols, fill_value=0)

    df[['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']] = scaler.fit_transform(df[['age', 'trtbps', 'chol', 'thalachh', 'oldpeak']])

    prediction = svc.predict(df)

    cur = db.cursor()
    try:
        diagnosis_result = prediction
        cur.execute('INSERT INTO diagnosis VALUES (%s)', (saved_data))
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        cur.close()

    print(saved_data)

    return jsonify({'prediction': int(prediction[0]),
                    'diagnosis': saved_data}), 200