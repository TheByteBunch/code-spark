extern crate rocket;
use rocket::{launch, routes};
use rocket_dyn_templates::{ Template };
mod services;
pub mod  models;
pub mod  schema;

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![services::create_user])
        .mount("/", routes![services::list])
        .attach(Template::fairing())
}
