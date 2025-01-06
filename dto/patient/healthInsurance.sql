CREATE TABLE health_insurance
(
  id int PRIMARY KEY AUTO_INCREMENT,
  patient_id int,
  account_id int,
  registration_place VARCHAR(255),
  shelf_life DATE,
  five_years_insurance DATE,
  place_provide VARCHAR(255),
  create_date DATE,
  modified_by VARCHAR(255),
  FOREIGN KEY (patient_id) REFERENCES patient(id),
  FOREIGN KEY (account_id) REFERENCES account(id)
);


