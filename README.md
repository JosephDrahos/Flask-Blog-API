# RESTful API for a simple blogging platform


<p align="center"><img src="https://avatars3.githubusercontent.com/u/59034516"></p>

An API designed in flask. Uses CircleCI as the CI/CD tool and pyjwt handles the authentication. The API allows users to add and manage posts on a blog. Users get auth token after login which can then be used to access othr routes and perform other actions.

## Setup

1. Create directory and `cd` into the directory
2. clone the repo `git clone https://github.com/CIRCLECI-GWP/authentication-decorators-in-flask.git`
3. setup a virtualenv `python -m venv venv`
4. source environment `source /venv/bin/activate`
4. install dependencies `pip install -r requirements`

## Running the application

> type: `python run.py`
> serving on: `https://127.0.0.1:5000/`

## Running the tests

> type: `python -m unittest`

## Containerization
docker build --tag python-docker .

## Endpoints

- Use postman or curl to test the endpoints
- Parse auth token in `x-access-token` header.

1. User register: POST `/signup`
2. User login: POST `/login`
3. Create a post: POST `/blog/create-post`
4. Pull all available posts: GET `/blog/posts`
5. Pull specific post: GET `/blog/post/<post_id>`
6. Edit specific post: POST `/blog/edit-post`
7. Remove post: DELETE `/blog/delete-post/<post_id>`

## Details

This repo is built using the git repo: https://github.com/CIRCLECI-GWP/authentication-decorators-in-flask. I chose this repo as it was the closest to how I envisioned creating this project compared to other flask boilerplates out there. It utilizes SQLite for a database as a larger database wasn't necessary to show proof of concept for this API. 