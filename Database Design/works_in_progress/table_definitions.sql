BEGIN;

DROP TABLE IF EXISTS sold;
DROP TABLE IF EXISTS belongs_to;
DROP TABLE IF EXISTS discounted_on;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS active_on;
DROP TABLE IF EXISTS advertising_campaign;
DROP TABLE IF EXISTS holiday;
DROP TABLE IF EXISTS date;
DROP TABLE IF EXISTS childcare_store;
DROP TABLE IF EXISTS time_limit;
DROP TABLE IF EXISTS store;
DROP TABLE IF EXISTS city;

CREATE EXTENSION IF NOT EXISTS tablefunc;

CREATE TABLE category (
  category_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (category_name)
);

CREATE TABLE product (
  pid INTEGER NOT NULL,
  retail_price NUMERIC NOT NULL,
  product_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (pid)
);

CREATE TABLE belongs_to (
  pid INTEGER NOT NULL,
  category_name VARCHAR(50) NOT NULL,
  PRIMARY KEY (pid, category_name),
  CONSTRAINT fk_belongs_to_cateogry_name_category_category_name FOREIGN KEY (category_name) REFERENCES category (category_name),
  CONSTRAINT fk_belongs_to_pid_product_pid FOREIGN KEY (pid) REFERENCES product (pid)
);

CREATE TABLE advertising_campaign (
  campaign_description VARCHAR(255) NOT NULL,
  PRIMARY KEY (campaign_description)
);

CREATE TABLE date (
  date DATE NOT NULL,
  PRIMARY KEY (date)
);

CREATE TABLE holiday (
  date DATE NOT NULL,
  holiday_names VARCHAR(255) NOT NULL,
  PRIMARY KEY (date),
  CONSTRAINT fk_holiday_date_date_date FOREIGN KEY (date) REFERENCES date (date)
);

CREATE TABLE active_on (
  campaign_description VARCHAR(255) NOT NULL,
  date DATE NOT NULL,
  PRIMARY KEY (campaign_description, date),
  CONSTRAINT fk_active_on_campaign_desc_advertising_campaign_campaign_desc FOREIGN KEY (campaign_description) REFERENCES advertising_campaign (campaign_description),
  CONSTRAINT fk_active_on_date_date_date FOREIGN KEY (date) REFERENCES date (date)
);

CREATE TABLE discounted_on (
  pid INTEGER NOT NULL,
  date DATE NOT NULL,
  discount_price NUMERIC NOT NULL,
  PRIMARY KEY (pid, date),
  CONSTRAINT fk_discounted_on_pid_product_pid FOREIGN KEY (pid) REFERENCES product (pid),
  CONSTRAINT fk_discounted_on_date_date_date FOREIGN KEY (date) REFERENCES date (date)
);

CREATE TABLE city (
  city_name VARCHAR(50) NOT NULL,
  state CHAR(2) NOT NULL,
  population INTEGER NOT NULL,
  PRIMARY KEY (city_name, state)
);

CREATE TABLE time_limit (
  minutes INTEGER UNIQUE NOT NULL,
  PRIMARY KEY (minutes)
);

CREATE TABLE store (
  store_number INTEGER NOT NULL,
  phone_number VARCHAR(20) NOT NULL,
  street_address VARCHAR(50),
  has_restaurant BOOLEAN NOT NULL,
  has_snack_bar BOOLEAN NOT NULL,
  city_name VARCHAR(50) NOT NULL,
  state CHAR(2) NOT NULL,
  PRIMARY KEY (store_number),
  CONSTRAINT fk_store_city_name_state_city_city_name_state FOREIGN KEY (city_name, state) REFERENCES city (city_name, state)
);

CREATE TABLE childcare_store (
  store_number INTEGER NOT NULL,
  minutes INTEGER NOT NULL,
  PRIMARY KEY (store_number),
  CONSTRAINT fk_childcare_store_store_number_store_store_number FOREIGN KEY (store_number) REFERENCES store (store_number),
  CONSTRAINT fk_childcare_store_minutes_time_limit_minutes FOREIGN KEY (minutes) REFERENCES time_limit (minutes)
);

CREATE TABLE sold (
  store_number INTEGER NOT NULL,
  date DATE NOT NULL,
  pid INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  PRIMARY KEY (store_number, date, pid),
  CONSTRAINT fk_sold_store_number_store_store_number FOREIGN KEY (store_number) REFERENCES store (store_number),
  CONSTRAINT fk_sold_date_date_date FOREIGN KEY (date) REFERENCES date (date),
  CONSTRAINT fk_sold_pid_product_pid FOREIGN KEY (pid) REFERENCES product (pid)
);

-- SEED VALUES

INSERT INTO city
VALUES
  ('Atlanta', 'GA', 3000000),
  ('San Francisco', 'CA', 8000000);

INSERT INTO time_limit
VALUES
  (15),
  (30),
  (45);

INSERT INTO store
VALUES
  (1, '15553472653', '123 Road St., Atlanta, Georgia', TRUE, FALSE, 'Atlanta', 'GA'),
  (2, '15557448374', '456 Way St., San Francisco, California', FALSE, TRUE, 'San Francisco', 'CA');

INSERT INTO childcare_store
VALUES
  (1, 30);

INSERT INTO date
VALUES
  ('2021-03-08'),
  ('2021-02-02'),
  ('2021-01-06'),
  ('2020-09-12'),
  ('2020-02-02');

INSERT INTO category
VALUES
  ('Movies'),
  ('Couches and Sofas'),
  ('Outdoor Furniture');

INSERT INTO product
VALUES
  (1, 5.00, 'Star Wars'),
  (2, 7.00, 'Departures'),
  (3, 3.50, 'Jaws'),
  (4, 800.00, 'Big Couch'),
  (5, 400.00, 'Small Couch'),
  (6, 350.00, 'Two-Seat Sofa');

INSERT INTO belongs_to
VALUES
  (1, 'Movies'),
  (2, 'Movies'),
  (3, 'Movies'),
  (4, 'Couches and Sofas'),
  (4, 'Outdoor Furniture'),
  (5, 'Couches and Sofas'),
  (5, 'Outdoor Furniture'),
  (6, 'Couches and Sofas');

INSERT INTO discounted_on
VALUES
  (4, '2021-03-08', 100.00),
  (5, '2021-03-08', 200.00);

INSERT INTO sold
VALUES
  (1, '2020-02-02', 4, 2),
  (1, '2020-02-02', 5, 9),
  (1, '2021-02-02', 4, 5),
  (1, '2021-02-02', 5, 3),
  (1, '2021-02-02', 6, 1),
  (1, '2021-03-08', 1, 10),
  (1, '2021-03-08', 4, 17),
  (1, '2021-03-08', 5, 7),
  (1, '2020-09-12', 5, 5),
  (2, '2020-09-12', 4, 6),
  (1, '2021-03-08', 2, 7);

INSERT INTO advertising_campaign
VALUES
  ('Campaign 1'),
  ('Campaign 2');

COMMIT;
