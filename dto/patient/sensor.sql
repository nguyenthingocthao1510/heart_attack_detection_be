CREATE TABLE sensor_data (
  id INT NOT NULL AUTO_INCREMENT,
  device_id VARCHAR(50),
  thalachh DOUBLE,
  restecg INT,
  PRIMARY KEY (id),
	FOREIGN KEY (device_id) REFERENCES device(id)
) AUTO_INCREMENT = 1;

ALTER TABLE sensor_data ADD avg_bpm DOUBLE;
ALTER TABLE sensor_data ADD timestamp TIMESTAMP;

DELETE FROM sensor_data;

INSERT INTO sensor_data
VALUES (1, 120, 510);
INSERT INTO sensor_data
VALUES (2, 120, 510);
INSERT INTO sensor_data
VALUES (3, 120, 510);
INSERT INTO sensor_data
VALUES (4, 120, 510);

SELECT * FROM temp_sensor_data
ORDER BY id DESC
LIMIT 1;

SELECT *
FROM patient as p
LEFT JOIN patient_record as pr
ON p.id = pr.patient_id
WHERE p.account_id = 21;

SELECT sd.thalachh, sd.restecg
FROM sensor_data sd 
JOIN device d ON sd.device_id = d.id
WHERE patient_id = 5
ORDER BY sd.id DESC 
LIMIT 1

