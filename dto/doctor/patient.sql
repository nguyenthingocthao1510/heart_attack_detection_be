CREATE TABLE patient(
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255),
    PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

INSERT INTO `patient` (`id`, `name`) VALUES (6, 'Patient E');
INSERT INTO `patient` (`id`, `name`) VALUES (5, 'Patient D');
INSERT INTO `patient` (`id`, `name`) VALUES (4, 'Patient C');
INSERT INTO `patient` (`id`, `name`) VALUES (3, 'Patient B');
