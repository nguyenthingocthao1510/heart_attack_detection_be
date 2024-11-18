CREATE TABLE patient(
    patient_id INT NOT NULL AUTO_INCREMENT,
    account_id INT NOT NULL,
    patient_name VARCHAR(255),
    patient_gender varchar(10),
    patient_dob DATE,
    PRIMARY KEY (patient_id)
    FOREIGN KEY (account_id) REFERENCES account(id)
) AUTO_INCREMENT = 1;