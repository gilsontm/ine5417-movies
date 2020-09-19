CREATE TABLE IF NOT EXISTS user (
    id integer PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);

-- password: default
INSERT INTO user (id, name, email, username, password)
VALUES (1, "default", "default", "default", "$2b$12$NNTCAftVS7/FpwfFQTQ6fuZc0C56v1NJV0fEFWspLQAzQ6zESrZpK")
EXCEPT SELECT * FROM user;
