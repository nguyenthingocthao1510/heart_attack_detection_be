CREATE TABLE device (
	id VARCHAR(50),
	patient_id INT,
	FOREIGN KEY (patient_id) REFERENCES patient(id)
)