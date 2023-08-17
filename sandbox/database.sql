DROP DATABASE IF EXISTS code_spark;

CREATE DATABASE code_spark;

\c code_spark;

CREATE TABLE user_account (
    id BIGSERIAL PRIMARY KEY,
    user_email VARCHAR(255) NOT NULL,
    user_full_name VARCHAR(255) NOT NULL,
    user_github_profile_name (VARCHAR(255)) NOT NULL,
);

CREATE TABLE match_request (
    id BIGSERIAL PRIMARY KEY,
    match_request_sender_id VARCHAR(255) NOT NULL,
    match_request_receiver_id VARCHAR(255) NOT NULL,
    match_request_status INT NOT NULL,
    created_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    accepted_date TIMESTAMPTZ
);

