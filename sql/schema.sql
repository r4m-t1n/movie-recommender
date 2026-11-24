CREATE TABLE users(
    user_id SERIAL PRIMARY KEY
);

CREATE TABLE accounts(
    user_id INTEGER,
    name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64),
    username VARCHAR(64) NOT NULL UNIQUE,
    hashed_password VARCHAR(256) NOT NULL,
    creation_date DATE NOT NULL DEFAULT CURRENT_DATE,
    last_login TIMESTAMPTZ NULL,

    PRIMARY KEY (user_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE sessions(
    session_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    token_hash VARCHAR(256) NOT NULL UNIQUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMPTZ NOT NULL,

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
);

CREATE TABLE movies(
    movie_id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER
);

CREATE TABLE genres(
    movie_id INTEGER,
    genre_type TEXT NOT NULL,

    PRIMARY KEY (movie_id, genre_type),

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE tags(
    user_id INTEGER,
    movie_id INTEGER,
    tag TEXT NOT NULL,
    tagged_at TIMESTAMPTZ NOT NULL,

    PRIMARY KEY (user_id, movie_id, tag),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE DOMAIN SCORE AS NUMERIC(2, 1)
    CHECK (VALUE BETWEEN 0.5 and 5.0);


CREATE TABLE ratings(
    user_id INTEGER,
    movie_id INTEGER,
    rating SCORE NOT NULL,
    rated_at TIMESTAMPTZ NOT NULL,

    PRIMARY KEY (user_id, movie_id),

    FOREIGN KEY (user_id)
        REFERENCES users(user_id)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);

CREATE TABLE links(
    movie_id INTEGER,
    imdb_id INTEGER NOT NULL UNIQUE,

    PRIMARY KEY (movie_id),

    FOREIGN KEY (movie_id)
        REFERENCES movies(movie_id)
            ON UPDATE CASCADE
            ON DELETE CASCADE
);
