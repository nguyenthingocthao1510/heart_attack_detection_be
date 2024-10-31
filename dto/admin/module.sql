CREATE TABLE module(
id INT NOT NULL AUTO_INCREMENT,
name VARCHAR(255),
route VARCHAR(255),
image VARCHAR(255),
PRIMARY KEY(id)
) AUTO_INCREMENT = 1;

CREATE TABLE module_permission (
    module_id INT,
    permission_id INT,
    FOREIGN KEY (module_id) REFERENCES module(id),
    FOREIGN KEY (permission_id) REFERENCES permission(id)
);

CREATE TABLE module_role_permission(
module_id INT,
role_id INT,
permission_id INT,
    FOREIGN KEY (module_id) REFERENCES module(id),
    FOREIGN KEY (role_id) REFERENCES role(id),
    FOREIGN KEY (permission_id) REFERENCES permission(id)
);

