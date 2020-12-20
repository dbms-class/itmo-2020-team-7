CREATE TABLE IF NOT EXISTS Laboratory (
  id SERIAL PRIMARY KEY, 
  name TEXT NOT NULL, 
  sndname_boss TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Active_agent (
  id SERIAL PRIMARY KEY, 
  name TEXT NOT NULL UNIQUE,
  formula TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Certificate (
  id SERIAL PRIMARY KEY, 
  number BIGINT NOT NULL UNIQUE CHECK(number > 0),
  validity DATE NOT NULL, 
  laboratory_id INT NOT NULL, 
  FOREIGN KEY (laboratory_id) REFERENCES Laboratory ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Producer (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Form (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Drug (
  id SERIAL PRIMARY KEY, 
  tradename TEXT NOT NULL, 
  intern_name TEXT NOT NULL, 
  form_id INT NOT NULL, 
  producer_id INT NOT NULL, 
  certificate_id INT NOT NULL UNIQUE, 
  active_agent_id INT NOT NULL,
  FOREIGN KEY (form_id) REFERENCES Form ON DELETE CASCADE,  
  FOREIGN KEY (producer_id) REFERENCES Producer ON DELETE CASCADE, 
  FOREIGN KEY (certificate_id) REFERENCES Certificate ON DELETE CASCADE, 
  FOREIGN KEY (active_agent_id) REFERENCES Active_agent ON DELETE CASCADE,
  UNIQUE (tradename, form_id)
);

CREATE TABLE IF NOT EXISTS Warehouse (
  id SERIAL PRIMARY KEY, 
  address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Distributor (
  id SERIAL PRIMARY KEY, 
  name TEXT NOT NULL, 
  address TEXT NOT NULL, 
  account_number BIGINT(20) NOT NULL UNIQUE CHECK(account_number > 0), 
  contact_person_name TEXT NOT NULL, 
  phone_number BIGINT(10) NOT NULL CHECK(phone_number > 0)
);

CREATE TABLE IF NOT EXISTS Package_type (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Sale_package (
  id SERIAL PRIMARY KEY,
  drug_id INT NOT NULL,
  package_type_id INT NOT NULL,
  price INT NOT NULL CHECK(price > 0),
  FOREIGN KEY (drug_id) REFERENCES Drug ON DELETE CASCADE,
  FOREIGN KEY (package_type_id) REFERENCES Package_type ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Transport_package (
  id SERIAL PRIMARY KEY,
  sale_package_id INT NOT NULL UNIQUE,
  sale_package_amount INT NOT NULL CHECK(sale_package_amount > 0),
  weight INT NOT NULL CHECK(weight > 0),
  FOREIGN KEY (sale_package_id) REFERENCES Sale_package ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Supply (
  id SERIAL PRIMARY KEY, 
  distributor_id INT NOT NULL, 
  transport_package_id INT NOT NULL,
  transport_package_amount INT NOT NULL CHECK(transport_package_amount > 0),
  FOREIGN KEY (distributor_id) REFERENCES Distributor ON DELETE CASCADE,
  FOREIGN KEY (transport_package_id) REFERENCES Transport_package ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Warehouse_supply (
  warehouse_id INT NOT NULL, 
  supply_id INT NOT NULL, 
  arrival_time DATE NOT NULL, 
  warehouse_keeper TEXT NOT NULL, 
  FOREIGN KEY (warehouse_id) REFERENCES Warehouse ON DELETE CASCADE, 
  FOREIGN KEY (supply_id) REFERENCES Supply ON DELETE CASCADE,
  PRIMARY KEY (warehouse_id, supply_id, arrival_time)
);

CREATE TABLE IF NOT EXISTS Pharmacy_shop (
  id SERIAL PRIMARY KEY, 
  address TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Car (
  id SERIAL PRIMARY KEY, 
  registration_number TEXT NOT NULL UNIQUE,
  maintanence_data DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS Pharmacy_drug (
  id SERIAL PRIMARY KEY, 
  pharmacy_shop_id INT NOT NULL,
  sale_package_id INT NOT NULL,
  price FLOAT NOT NULL CHECK(price > 0), 
  amount INT NOT NULL CHECK(amount >= 0), 
  FOREIGN KEY (pharmacy_shop_id) REFERENCES Pharmacy_shop ON DELETE CASCADE, 
  FOREIGN KEY (sale_package_id) REFERENCES Sale_package ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Car_task (
  id SERIAL PRIMARY KEY,
  car_id INT NOT NULL,
  date DATE NOT NULL,
  warehouse_id INT NOT NULL,
  transport_package_id INT NOT NULL,
  transport_package_amount INT NOT NULL CHECK(transport_package_amount > 0),
  pharmacy_shop_id INT NOT NULL,
  FOREIGN KEY (car_id) REFERENCES Car ON DELETE CASCADE,
  FOREIGN KEY (warehouse_id) REFERENCES Warehouse ON DELETE CASCADE,
  FOREIGN KEY (transport_package_id) REFERENCES Transport_package ON DELETE CASCADE,
  FOREIGN KEY (pharmacy_shop_id) REFERENCES Pharmacy_shop ON DELETE CASCADE,
  UNIQUE (car_id, date, warehouse_id, pharmacy_shop_id)
);
