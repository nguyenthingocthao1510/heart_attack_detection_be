CREATE TABLE module_role(
module_id INT,
role_id INT,
    FOREIGN KEY (module_id) REFERENCES module(id),
    FOREIGN KEY (role_id) REFERENCES role(id)
);
