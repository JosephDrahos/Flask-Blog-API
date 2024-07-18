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
    - request json: {username: str, password: str}
    - return json: {message: str}
2. User login: POST `/login`
    - request json: {username: str, password: str}
    - return json: {token: str}
3. Create a post: POST `/blog/create-post`
    - header: {'content-type': "application/json",x-access-token: str}
    - request json: {title: str, content: str} 
    - return json: {message: str}
4. Pull all available posts: GET `/blog/posts`
    - header: {'content-type': "application/json",x-access-token: str}
    - request json: {}
    - return json: {posts: [{id: int, title: str, content: str, owner: str}]}
5. Pull single post: GET `/blog/post/<post_id>`
    - header: {'content-type': "application/json",x-access-token: str}
    - request post_id: int
    - return json: {id: int, title: str, content: str, owner: str}
6. Edit existing post: POST `/blog/edit-post`
    - header: {'content-type': "application/json",x-access-token: str}
    - request json: {post_id: int, title: str, content: str} 
    - return json: {message: str}
7. Remove post: DELETE `/blog/delete-post/<post_id>`
    - header: {'content-type': "application/json",x-access-token: str}
    - request post_id: int
    - return json: {message: str}

## Details

This repo is built using the git repo: https://github.com/CIRCLECI-GWP/authentication-decorators-in-flask. The functional code is located within the library directory where the database models are defined in models.py and the endpoints are defined in resources.py. I chose this repo as it was the closest to how I envisioned creating this project compared to other flask boilerplates out there. I wanted a simple project structure and the JWT implementation was what I had in mind to use for this projects authentication. This project utilizes SQLAlchemy interfaced with SQLite for a database as a larger database wasn't necessary to show proof of concept for this API and the Alembic migration implementation is helpful for the potential future. 

## Improvements
- Add time to blog post model as the datetime of post is also important data to tie to the post. I would store datetimetz to keep track of date, time, and timezone of the users post.
- Use a .env file for secret information such as database credentials, api tokens, secret keys, etc. 
- I would add password salting to further secure user passwords inside the database.
- I would use table joins in the get all posts and get single post endpoints to improve efficiency when getting the post and the owners username. 
- I would also use pydantic to define the request and response object structure to ensure consistency within the API.