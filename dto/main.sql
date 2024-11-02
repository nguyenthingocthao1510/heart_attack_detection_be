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

-- INSERT VALUES SECTION --
INSERT INTO `patient` (`id`, `name`) VALUES (6, 'Patient E');
INSERT INTO `patient` (`id`, `name`) VALUES (5, 'Patient D');
INSERT INTO `patient` (`id`, `name`) VALUES (4, 'Patient C');
INSERT INTO `patient` (`id`, `name`) VALUES (3, 'Patient B');

INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (1, 'admin', NULL, 'd47d48ac2cfccaa7a22aae815a1c9895', 'e51d5aa438bf904531da4fc76a858a4d9bae725df37e013dd9d742f93c34f2a7', 1);
INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (2, 'doctor', NULL, 'd29c50090e127dfcb4135bb15bed0e08', '6cf8b0ea96ad8dea37513d927a36292b8bb814fbd6796c9c40527dacf63303d0', 2);
INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (4, 'patient', NULL, '675dc25280bf8e0327491dce963b9fb1', '88be2873a3abfef369ffa404f864c2eee0caa5c097f132cd6a023d4dd612003d', 3);
INSERT INTO `account` (`id`, `username`, `password`, `password_salt`, `password_hash`, `role_id`) VALUES (5, 'patient A', NULL, '66e1fde5d5f1fd72b7d6c6a709368ab5', 'b302f68c07a6496e7eb747f1c301d90693321b04532f9bbe119f262bae83f3a8', 3);
