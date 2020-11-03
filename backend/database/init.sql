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

CREATE TABLE IF NOT EXISTS history (
    id integer PRIMARY KEY,
    title text NOT NULL,
    user_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS analysis (
    id integer PRIMARY KEY,
    created_at datetime NOT NULL,
    user_id integer NOT NULL,
    entity_id integer NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (entity_id) REFERENCES entity(id)
);

CREATE TABLE IF NOT EXISTS tweet (
    id integer PRIMARY KEY,
    text text NOT NULL,
    sentiment integer,
    created_at datetime NOT NULL,
    latitude real,
    longitude real,
    author_name text NOT NULL,
    author_address text NOT NULL,
    author_id integer NOT NULL,
    twitter_id integer NOT NULL,
    analysis_id integer NOT NULL,
    FOREIGN KEY (analysis_id) REFERENCES analysis(id)
);