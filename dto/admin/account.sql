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












