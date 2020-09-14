CREATE TABLE IF NOT EXISTS user (
    id integer PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);

INSERT INTO user (id, name, email, username, password)
VALUES (1, "default", "default", "default", "default")
EXCEPT SELECT * FROM user;
