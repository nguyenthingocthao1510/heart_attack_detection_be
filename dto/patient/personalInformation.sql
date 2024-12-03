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

UPDATE patient SET account_id = 20 WHERE id = 4;
UPDATE patient SET account_id = 21 WHERE id = 5;
UPDATE patient SET account_id = 22 WHERE id = 6;

ALTER TABLE patient ADD COLUMN account_id INT NOT NULL;
ALTER TABLE patient ADD CONSTRAINT account_ibfk_2 FOREIGN KEY (account_id) REFERENCES account(id);
ALTER TABLE patient DROP COLUMN pt_dob;

ALTER TABLE patient ADD COLUMN gender VARCHAR(10);
UPDATE patient SET gender = 'Male' WHERE id = 3;
UPDATE patient SET gender = 'Female' WHERE id = 4;
UPDATE patient SET gender = 'Male' WHERE id = 5;
UPDATE patient SET gender = 'Female' WHERE id = 6;

ALTER TABLE patient ADD COLUMN dob DATE;
UPDATE patient SET dob = '1960-12-20' WHERE id = 3;
UPDATE patient SET dob = '2002-08-14' WHERE id = 4;
UPDATE patient SET dob = '1976-05-25' WHERE id = 5;
UPDATE patient SET dob = '1945-07-22' WHERE id = 6;

