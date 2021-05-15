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
  phone_number VARCHAR(20),
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

COMMIT;
