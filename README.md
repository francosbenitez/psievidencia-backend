# psievidencia-backend

## Schema

**User**

* email
* password

**UserProfile**

* user_id
* first_name
* last_name
* image
* facebook_profile
* twitter_profile
* linkedin_profile
* instagram_profile

## API

**/users**

* GET
* POST

**/users/:id**

* GET
* PUT
* DELETE

## Running locally

1. Clone this repo
1. cd into this repo
1. Create a python virtual environment: `python -m venv venv`
1. Activate virtual environment: `source venv/bin/activate`
1. `pip install -r requirements.txt`
1. `python manage.py runserver`
