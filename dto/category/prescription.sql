CREATE TABLE prescription(
 id INT NOT NULL AUTO_INCREMENT,
 medicine_id INT,
 patient_id INT,
 prescription_date DATE,
 medicine_amount INT,
 doctor_id int,
 note VARCHAR(255),
 description VARCHAR(255),
 PRIMARY KEY(id),
 FOREIGN KEY(medicine_id) REFERENCES medicine(id),
 FOREIGN KEY(patient_id) REFERENCES patient(id),
 FOREIGN KEY(doctor_id) REFERENCES doctor(id)
) AUTO_INCREMENT = 1;