from controllers.baseRepository import BaseRepository
from collections import defaultdict
from flask import request, jsonify

class DeviceRepo(BaseRepository):
    def __init__(self):
        super().__init__(
            db_table = "device",
        )
    
    def get_device(self):
        cur = self._get_cursor()
        try:
            cur.execute("SELECT * FROM device")        
            devices = cur.fetchall()
            device_dict = defaultdict(list)
            total_available = 0
            total_assigned = 0
            for device in devices:
                if not device[1]:
                    status = 'Available'
                    total_available += 1
                else:
                    status = 'Assigned'
                    total_assigned += 1

                entry = {
                    'device_id': device[0],
                    'patient_id': device[1]
                }
                device_dict[status].append(entry)
            
            device = [
                {
                    'status': status, 
                    'entries': entries, 
                    'total': total_assigned if status == 'Assigned' else total_available
                }
                for status, entries in device_dict.items()
            ]

            return jsonify(
                {
                    "device": device,
                    "total": total_available + total_assigned
                }), 200
        except Exception as e:
            return f"An error occurred: {e}", 500
        finally:
            cur.close()