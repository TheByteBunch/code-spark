// @generated automatically by Diesel CLI.

diesel::table! {
    users (id) {
        id -> Int4,
        #[max_length = 255]
        user_email -> Varchar,
        #[max_length = 255]
        user_full_name -> Varchar,
        #[max_length = 255]
        user_github_profile_name -> Varchar,
    }
}
