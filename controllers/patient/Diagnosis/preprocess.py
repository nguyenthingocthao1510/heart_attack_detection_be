def preprocess(data):
    data['sex'] = 1 if data['sex'] == 'Male' else 0

    data['exng'] = 1 if data['exng'] == 'Yes' else 0

    data['fbs'] = 1 if data['fbs'] > 120 else 0

    match data['cp']:
        case 'None':
            data['cp'] = 0
        case 'Typical angina':
            data['cp'] = 1
        case 'Atypical angina':
            data['cp'] = 2
        case 'Non-anginal pain':
            data['cp'] = 3
        case 'Asymptomatic':
            data['cp'] = 4

    match data['slp']:
        case 'None':
            data['slp'] = 0
        case 'Upsloping':
            data['slp'] = 1
        case 'diagnosis_result':
            data['slp'] = 2
        case 'Downsloping':
            data['slp'] = 3

    match data['thall']:
        case 'None':
            data['thall'] = 0
        case 'Normal':
            data['thall'] = 1
        case 'Fixed defect':
            data['thall'] = 2
        case 'Reversible defect':
            data['thall'] = 3
    
    return data