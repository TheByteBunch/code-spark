extern crate diesel;
extern crate rocket;
use diesel::pg::PgConnection;
use diesel::prelude::*;
use dotenvy::dotenv;
use rocket::response::{status::Created, Debug};
use rocket::serde::{json::Json, Deserialize, Serialize};
use rocket::{get, post };
use crate::models;
use crate::schema;
use rocket_dyn_templates::{context, Template};
use std::env;

pub fn establish_connection_pg() -> PgConnection {
    dotenv().ok();
    let database_url = env::var("DATABASE_URL").expect("DATABASE_URL must be set");
    PgConnection::establish(&database_url)
        .unwrap_or_else(|_| panic!("Error connecting to {}", database_url))
}

#[derive(Serialize, Deserialize)]
pub struct NewUser {
    user_email: String,
    user_full_name: String,
    user_github_profile_name: String,
}

type Result<T, E = Debug<diesel::result::Error>> = std::result::Result<T, E>;

#[post("/users", format = "json", data = "<user>")]
pub fn create_user(user: Json<NewUser>) -> Result<Created<Json<NewUser>>> {
    use models::User;
    let connection = &mut establish_connection_pg();

    let new_user = User {
        id: 1,
        user_email: user.user_email.to_string(),
        user_full_name: user.user_full_name.to_string(),
        user_github_profile_name: user.user_github_profile_name.to_string(),
    };

    diesel::insert_into(self::schema::users::dsl::users)
        .values(&new_user)
        .execute(connection)
        .expect("Error saving new user");
    Ok(Created::new("/").body(user))
}

#[get("/users")]
pub fn list() -> Template {
    use self::models::User;
    let connection = &mut establish_connection_pg();
    let results = self::schema::users::dsl::users
        .load::<User>(connection)
        .expect("Error loading users");
    Template::render("users", context! {users: &results, count: results.len()})
}

