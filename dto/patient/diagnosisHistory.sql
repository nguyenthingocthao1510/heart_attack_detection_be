CREATE TABLE diagnosis_history (
	id INT NOT NULL AUTO_INCREMENT,
	patient_id INT,
	thalachh DOUBLE,
	restecg INT,
	diagnosis_time TIMESTAMP,
	PRIMARY KEY (id),
	FOREIGN KEY (patient_id) REFERENCES patient(id)
) AUTO_INCREMENT = 1;

DROP TABLE diagnosis_history;

ALTER TABLE diagnosis_history ADD COLUMN result INT;
UPDATE diagnosis_history SET result = 0;