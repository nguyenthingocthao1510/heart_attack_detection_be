CREATE TABLE device (
	id VARCHAR(50) NOT NULL,
	patient_id INT,
	PRIMARY KEY (id),
	FOREIGN KEY (patient_id) REFERENCES patient(id)
)

UPDATE device SET patient_id = 5 WHERE id = 'ESP8266_12500837';

DELETE TABLE device;
