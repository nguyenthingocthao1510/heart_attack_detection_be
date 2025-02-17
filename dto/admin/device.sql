INSERT INTO module(name, route, image) VALUES 
('Device', '/device', 'https://cdn.icon-icons.com/icons2/3803/PNG/512/defibrillator_medical_device_icon_233087.png');

INSERT INTO device(id, patient_id) VALUES
('ESP8266_10000000', 4),
('ESP8266_10000001', 3),
('ESP8266_10000002', 6);
INSERT INTO device(id) VALUES
('ESP8266_10000003'),
('ESP8266_10000004'),
('ESP8266_10000005'),
('ESP8266_10000006');

UPDATE device SET patient_id = null WHERE id IN ('ESP8266_10000001', 'ESP8266_10000002', 'ESP8266_10000003');

INSERT INTO module_role(module_id, role_id) VALUES (23, 1);
INSERT INTO module_role_permission(module_id, role_id, permission_id) VALUES
(23, 1, 1), (23, 1, 2), (23, 1, 3), (23, 1, 4), (23, 1, 5);