CREATE TABLE patient(
    id INT NOT NULL AUTO_INCREMENT,
    account_id INT NOT NULL,
    name VARCHAR(255),
    gender varchar(10),
    dob DATE,
    PRIMARY KEY (patient_id)
    FOREIGN KEY (account_id) REFERENCES account(id)
) AUTO_INCREMENT = 1;

DROP TABLE patient;

INSERT INTO account (

ALTER TABLE patient ADD COLUMN account_id INT NOT NULL;
ALTER TABLE patient ADD CONSTRAINT account_ibfk_2 FOREIGN KEY (account_id) REFERENCES account(id);

UPDATE patient SET account_id = 16 WHERE id IN (6,5,4,3);

ALTER TABLE patient ADD COLUMN pt_gender VARCHAR(10);
ALTER TABLE patient ADD COLUMN pt_dob DATE;
