-- schema.sql

DROP TABLE IF EXISTS user;

CREATE TABLE user (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS roles;

CREATE TABLE roles (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    role_name TEXT UNIQUE NOT NULL
);

DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    department_name TEXT UNIQUE NOT NULL,
    department_description TEXT UNIQUE NOT NULL
);

DROP TABLE IF EXISTS employee;

CREATE TABLE employee (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT UNIQUE NOT NULL,
    join_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    weekly_salary DECIMAL(9,2) DEFAULT 0.0,
    commission_per_sale INTEGER DEFAULT 0,
    hour_rate DECIMAL(9,2) DEFAULT 0.0,
    role_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (department_id) REFERENCES departments(id)
);


INSERT INTO departments (department_name, department_description) VALUES ('department 1', 'department 1 description'), ('department 2', 'department 2 description'),('department 3', 'department 3 description');

INSERT INTO roles (role_name) VALUES ('manager'), ('saler'), ('employee') , ('worker');

INSERT INTO employee (
    employee_name,
    weekly_salary,
    commission_per_sale,
    hour_rate,
    role_id,
    department_id
)
VALUES 
    ('Mary Poppins', 10000, 0, 0, 1, 1),
    ('John Doe', 1000, 10, 0, 2, 1),
    ('Tom Cat', 6000, 0, 0, 3, 2),
    ('Mary Ann', 5000, 0, 0, 3, 1),
    ('James Bond', 0, 0, 1000, 4, 3);



