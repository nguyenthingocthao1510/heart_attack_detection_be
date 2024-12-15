CREATE TABLE temp_sensor_data(
  id INT NOT NULL AUTO_INCREMENT,
  thalachh DOUBLE,
  restecg INT,
  PRIMARY KEY (id)
) AUTO_INCREMENT = 1;

INSERT INTO temp_sensor_data
VALUES (1, 120, 510);
INSERT INTO temp_sensor_data
VALUES (2, 120, 510);
INSERT INTO temp_sensor_data
VALUES (3, 120, 510);
INSERT INTO temp_sensor_data
VALUES (4, 120, 510);

SELECT * FROM temp_sensor_data
ORDER BY id DESC
LIMIT 1;

SELECT *
FROM patient as p
LEFT JOIN patient_record as pr
ON p.id = pr.patient_id
WHERE p.account_id = 21;

