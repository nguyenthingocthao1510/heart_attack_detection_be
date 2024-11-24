class DataPreprocessor:
    def __init__(self):
        self.cp_mapping = {
            'None': 0,
            'Typical angina': 1,
            'Atypical angina': 2,
            'Non-anginal pain': 3,
            'Asymptomatic': 4
        }
        self.slp_mapping = {
            'None': 0,
            'Upsloping': 1,
            'diagnosis_result': 2,
            'Downsloping': 3
        }
        self.thall_mapping = {
            'None': 0,
            'Normal': 1,
            'Fixed defect': 2,
            'Reversible defect': 3
        }
    
    def preprocess(self, data):
        data['sex'] = 1 if data['sex'] == 'Male' else 0
        data['exng'] = 1 if data['exng'] == 'Yes' else 0
        data['fbs'] = 1 if data['fbs'] > 120 else 0
        
        data['cp'] = self.cp_mapping.get(data['cp'], 0)
        data['slp'] = self.slp_mapping.get(data['slp'], 0)
        data['thall'] = self.thall_mapping.get(data['thall'], 0)
        
        return data
