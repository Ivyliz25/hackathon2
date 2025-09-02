CREATE DATABASE recipe_app;
USE recipe_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL
);


CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ingredients TEXT NOT NULL,
    suggestions TEXT NOT NULL,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
