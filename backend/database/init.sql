CREATE TABLE IF NOT EXISTS user (
    id integer PRIMARY KEY,
    email text NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);

-- password: default
INSERT INTO user (id, email, username, password)
VALUES (1, "default", "default", "$2b$12$NNTCAftVS7/FpwfFQTQ6fuZc0C56v1NJV0fEFWspLQAzQ6zESrZpK")
EXCEPT SELECT * FROM user;

CREATE TABLE IF NOT EXISTS entity (
    id integer PRIMARY KEY,
    tmdb_id integer NOT NULL,
    media_type text NOT NULL
);

CREATE TABLE IF NOT EXISTS favorite (
    id integer PRIMARY KEY,
    user_id integer NOT NULL,
    entity_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (entity_id) REFERENCES entity(id)
);