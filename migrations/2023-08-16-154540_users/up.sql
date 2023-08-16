CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    user_full_name VARCHAR(255) NOT NULL,
    user_github_profile_name VARCHAR(255) NOT NULL
);
