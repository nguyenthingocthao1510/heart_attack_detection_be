-- CREATE TABLE SECTION --
CREATE TABLE patient(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

CREATE TABLE medicine (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  uses VARCHAR(255),
  description VARCHAR(255),
  PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

CREATE TABLE permission(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(255),
PRIMARY KEY(id)
) AUTO_INCREMENT = 1;

CREATE TABLE module(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(255),
PRIMARY KEY(id)
) AUTO_INCREMENT = 1;

CREATE TABLE role(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(255),
PRIMARY KEY(id)
) AUTO_INCREMENT = 1;

CREATE TABLE module_role_permission(
module_id INT,
role_id INT,
permission_id INT,
    FOREIGN KEY (module_id) REFERENCES module(id),
    FOREIGN KEY (role_id) REFERENCES role(id),
    FOREIGN KEY (permission_id) REFERENCES permission(id)
);


CREATE TABLE account (
id INT NOT NULL AUTO_INCREMENT,
username VARCHAR(255),
password VARCHAR(255),
password_salt VARCHAR(255),
password_hash VARCHAR(255),
role_id INT,
PRIMARY KEY (id),
FOREIGN KEY (role_id) REFERENCES role(id)
) AUTO_INCREMENT = 1;

CREATE TABLE module(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(255),
route VARCHAR(255),
image VARCHAR(255),
PRIMARY KEY(id)
) AUTO_INCREMENT = 1;

CREATE TABLE module_role(
module_id INT,
role_id INT,
    FOREIGN KEY (module_id) REFERENCES module(id),
    FOREIGN KEY (role_id) REFERENCES role(id)
);

CREATE TABLE role(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(255),
PRIMARY KEY(id)
) AUTO_INCREMENT = 1;

CREATE TABLE module_role_permission(
module_id INT,
role_id INT,
permission_id INT,
    FOREIGN KEY (module_id) REFERENCES module(id),
    FOREIGN KEY (role_id) REFERENCES role(id),
    FOREIGN KEY (permission_id) REFERENCES permission(id)
);

CREATE TABLE doctor
(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(255),
PRIMARY KEY(id)
) AUTO_INCREMENT = 1;

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

CREATE TABLE diagnosis (
    diagnosis_id INT NOT NULL AUTO_INCREMENT,
    patient_id INT,
    doctor_id INT,
    diagnosis_date DATETIME,
    diagnosis_result INT,
    trtbps INT,
    chol INT,
    thalachh INT,
    oldpeak DOUBLE(2,2),
    exng CHAR(3),
    caa INT,
    cp VARCHAR(20),
    fbs INT,
    restecg INT,
    slp VARCHAR(20),
    thall VARCHAR(20),
    FOREIGN KEY (id) REFERENCES patient(id)

)

CREATE TABLE patient_record
(
  id INT PRIMARY KEY AUTO_INCREMENT,
  doctor_id INT,
  patient_id INT,
  account_id INT,
  age INT, 
  trtbps INT,  
  chol INT,  
  thalachh INT,  
  oldpeak INT, 
  sex VARCHAR(255),  
  exng VARCHAR(255),  
  caa INT,  
  cp VARCHAR(255),  
  fbs INT,  
  restecg INT, 
  slp VARCHAR(255), 
  thall VARCHAR(255),
  create_date DATE,
  FOREIGN KEY (patient_id) REFERENCES patient(id),
  FOREIGN KEY (doctor_id) REFERENCES doctor(id),
  FOREIGN KEY (account_id) REFERENCES account(id)
)AUTO_INCREMENT = 1;

-- INSERT VALUES SECTION --
INSERT INTO `patient` (`id`, `name`) VALUES (6, 'Patient E');
INSERT INTO `patient` (`id`, `name`) VALUES (5, 'Patient D');
INSERT INTO `patient` (`id`, `name`) VALUES (4, 'Patient C');
INSERT INTO `patient` (`id`, `name`) VALUES (3, 'Patient B');

INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (1, 'admin', NULL, 'd47d48ac2cfccaa7a22aae815a1c9895', 'e51d5aa438bf904531da4fc76a858a4d9bae725df37e013dd9d742f93c34f2a7', 1);
INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (2, 'doctor', NULL, 'd29c50090e127dfcb4135bb15bed0e08', '6cf8b0ea96ad8dea37513d927a36292b8bb814fbd6796c9c40527dacf63303d0', 2);
INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (4, 'patient', NULL, '675dc25280bf8e0327491dce963b9fb1', '88be2873a3abfef369ffa404f864c2eee0caa5c097f132cd6a023d4dd612003d', 3);
INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (5, 'patient A', NULL, '66e1fde5d5f1fd72b7d6c6a709368ab5', 'b302f68c07a6496e7eb747f1c301d90693321b04532f9bbe119f262bae83f3a8', 3);
