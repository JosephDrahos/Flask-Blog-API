# RESTful API for a simple blogging platform


An API designed in flask. Uses pyjwt to handle the authentication. The API allows users to add and manage posts on a blog. Users get auth token after login which can then be used to access other routes and perform other actions.

## Setup

1. Create directory and `cd` into the directory
2. clone the repo `git clone https://github.com/JosephDrahos/Flask-Blog-API.git`
3. setup a virtualenv `python -m venv venv`
4. source environment `source /venv/bin/activate`
4. install dependencies `pip install -r requirements`

## Running the application

> type: `python run.py`
> serving on: `https://127.0.0.1:5000/`

## Running the tests

> type: `python -m unittest`

## Containerization
docker build -t blog-api .
docker run blog-api

## Endpoints

- Use postman or curl to test the endpoints
- Parse auth token in `x-access-token` header.

1. User register: POST `/signup`
2. User login: POST `/login`
3. Create a post: POST `/blog/create-post`
4. Pull all available posts: GET `/blog/posts`
5. Pull single post: GET `/blog/post/<post_id>`
6. Edit existing post: POST `/blog/edit-post`
7. Remove post: DELETE `/blog/delete-post/<post_id>`

## Details

This repo is built using the git repo: https://github.com/CIRCLECI-GWP/authentication-decorators-in-flask. I chose this repo as it was the closest to how I envisioned creating this project compared to other flask boilerplates out there. I wanted a simple project structure and the JWT implementation was what I had in mind to use for this projects authentication. This project utilizes SQLAlchemy interfaced with SQLite for a database as a larger database wasn't necessary to show proof of concept for this API and the Alembic migration implementation is helpful for the potential future. Additional improvements I would add if given more time is to use a .env file for secret information such as database credentials, api tokens, secret keys, etc. I would add password salting to further secure user passwords inside the database. I would also flesh out the blog post class to tie an image to the post. This could be done by having a separate blob database to store images and the blog post inside the SQL database would contain the path to this image.