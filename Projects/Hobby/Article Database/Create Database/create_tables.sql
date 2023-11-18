CREATE TABLE company (
    name varchar(200) NOT NULL,
    domain varchar(200),
    year_founded int,
    industry varchar(100),
    locality varchar(100),
    country varchar(100),
    linkedin_url varchar(500),
    current_employee_estimate bigint,
    total_employee_estimate bigint,
    PRIMARY KEY (name)
    );
    
CREATE TABLE search (
    search_id varchar(200) NOT NULL,
    search_term varchar(100) NOT NULL,
    date_from varchar(10) NOT NULL,
    date_to varchar(10) NOT NULL,
    newspaper text,
    n_results BIGINT,
    PRIMARY KEY (search_id)
    );
CREATE TABLE company_search (
  search_id varchar(200) NOT NULL,
  company_name varchar(200) NOT NULL,
  FOREIGN KEY (search_id) REFERENCES search(search_id),
  FOREIGN KEY (company_name) REFERENCES company(name)
  );

CREATE TABLE article ( 
article_id varchar(200) NOT NULL,
title varchar(300) NOT NULL,
text LONGTEXT NOT NULL,
section varchar(50),
web_url varchar(500),
date varchar(20),
PRIMARY KEY (article_id)
);

CREATE TABLE article_search (
  search_id varchar(200) NOT NULL,
  article_id varchar(200) NOT NULL,
  FOREIGN KEY (search_id) REFERENCES search(search_id),
  FOREIGN KEY (article_id) REFERENCES article(article_id)
  );

CREATE TABLE person (
person_id varchar(200) NOT NULL,
name varchar(100) NOT NULL,
bio text,
country varchar(50),
position varchar(50),
gender varchar(10),
age int,
twitter varchar(500),
PRIMARY KEY (person_id)
);

CREATE TABLE written_by (
  article_id varchar(200) NOT NULL,
  person_id varchar(200) NOT NULL,
  FOREIGN KEY (article_id) REFERENCES article(article_id),
  FOREIGN KEY (person_id) REFERENCES person(person_id)
  );
