CREATE TABLE patient(
    id INT NOT NULL AUTO_INCREMENT,
    account_id INT NOT NULL,
    name VARCHAR(255),
    gender varchar(10),
    dob DATE,
		need_prediction VARCHAR(5),
		phone_number VARCHAR(15),
		email VARCHAR(255),
		address VARCHAR(255),
    PRIMARY KEY (patient_id)
    FOREIGN KEY (account_id) REFERENCES account(id)
) AUTO_INCREMENT = 1;

INSERT INTO patient (id, name, account_id, gender, dob, need_prediction, phone_number, email, address)
VALUES
(7, 'Nguyễn Văn A', 33, 'Male', '1990-05-20', 'No', '0981234567', 'nguyenvana@gmail.com', '12 Lê Lợi, Hà Nội, Việt Nam'),
(8, 'Trần Thị B', 34, 'Female', '1992-08-15', 'No', '0972345678', 'tranthib@yahoo.com', '45 Nguyễn Trãi, TP Hồ Chí Minh, Việt Nam'),
(9, 'Phạm Quốc C', 35, 'Male', '1985-12-10', 'No', '0913456789', 'phamquocc@outlook.com', '78 Hoàng Hoa Thám, Đà Nẵng, Việt Nam'),
(10, 'Lê Thu D', 36, 'Female', '1998-03-25', 'No', '0904567890', 'lethud@example.com', '90 Hai Bà Trưng, Huế, Việt Nam'),
(11, 'Đặng Minh E', 37, 'Male', '1995-07-30', 'No', '0935678901', 'dangminhe@gmail.com', '123 Võ Thị Sáu, Cần Thơ, Việt Nam');

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

ALTER TABLE patient ADD COLUMN need_prediction VARCHAR(5);
UPDATE patient SET need_prediction = 'No' WHERE id = 3;
UPDATE patient SET need_prediction = 'Yes' WHERE id = 4;
UPDATE patient SET need_prediction = 'Yes' WHERE id = 5;
UPDATE patient SET need_prediction = 'No' WHERE id = 6;

SELECT id FROM patient WHERE need_prediction = 'Yes';



