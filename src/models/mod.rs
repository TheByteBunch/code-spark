use super::schema::users;
use diesel::{prelude::*};
use serde::{Serialize, Deserialize};

#[derive(Queryable, Insertable, Serialize, Deserialize)]
#[diesel(table_name = users)]
pub struct User {
    pub id: i32,
    pub user_email: String,
    pub user_full_name: String,
    pub user_github_profile_name: String,
}
