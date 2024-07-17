from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from datetime import datetime, timedelta
from library.main import db, app
from library.models import PostModel, User, token_required

@app.route('/', methods=['GET'])
def home():
    return make_response(jsonify({'message':'pong'}),200)

# register route
@app.route('/signup', methods=['POST'])
def signup_user(): 
    data = request.get_json() 
    hashed_password = generate_password_hash(data['password'], method='scrypt')
    
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password, admin=False)
        db.session.add(new_user) 
        db.session.commit() 

        return jsonify({'message': 'registered successfully'}), 201
    else:
        return make_response(jsonify({"message": "User already exists!"}), 409)

# user login route
@app.route('/login', methods=['POST'])
def login():
    auth = request.get_json()
    if not auth or not auth.get('username') or not auth.get('password'):
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic-realm= "Login required!"'})

    user = User.query.filter_by(username=auth['username']).first()
    if not user:
        return make_response('Could not verify user!', 401, {'WWW-Authenticate': 'Basic-realm= "No user found!"'})

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({'public_id': user.public_id}, app.config['SECRET_KEY'], 'HS256')
        return make_response(jsonify({'token': token}), 201)

    return make_response('Could not verify password!', 403, {'WWW-Authenticate': 'Basic-realm= "Wrong Password!"'})


#  add a post
@app.route('/blog/create-post', methods=['POST'])
@token_required
def create_post(current_user):
    '''adds a new post to collection!'''
    data = request.get_json()

    if len(data['title']) > 200:
        return make_response(jsonify({"message": "post title length cannot exceed 200 character limit"}), 413)
    if len(data['title']) < 1:
        return make_response(jsonify({"message": "post title length cannot be < 1"}), 422)
    if len(data['content']) > 5000:
        return make_response(jsonify({"message": "post content length cannot exceed 5000 character limit"}), 413)
    if len(data['content']) < 1:
        return make_response(jsonify({"message": "post content length cannot be < 1"}), 422)
    
    new_post = PostModel(title=data['title'],content=data['content'], owner=current_user) 
    db.session.add(new_post)  
    db.session.commit() 
    return jsonify({'message' : 'new post created'})

# get all posts
@app.route('/blog/posts', methods=['GET'])
@token_required
def get_posts(current_user):

   posts = PostModel.query.all()
   output = []
   for post in posts:
       post_data = {}
       post_data['id'] = post.id
       post_data['title'] = post.title
       post_data['content'] = post.content
       post_data['owner'] = post.user_id
       output.append(post_data)
 
   return jsonify({'posts' : output})

# get all posts
@app.route('/blog/post/<post_id>', methods=['GET'])
@token_required
def get_post(current_user,post_id):

    post = PostModel.query.filter_by(id=post_id).first()
    if not post:  
        return make_response(jsonify({'message': 'post does not exist'}),404)

    post_data = {}
    post_data['id'] = post.id
    post_data['title'] = post.title
    post_data['content'] = post.content
    post_data['owner'] = post.user_id

    return jsonify(post_data)

# editing a post
@app.route('/blog/edit-post', methods=['POST'])
@token_required
def edit_post(current_user): 
    data = request.get_json()
    post = PostModel.query.filter_by(id=data['post_id']).first()  

    if len(data['title']) > 200:
        return make_response(jsonify({"message": "post title cannot exceed 200 character limit"}), 413)
    if len(data['title']) < 1:
        return make_response(jsonify({"message": "post title length cannot be < 1"}), 422)
    if len(data['content']) > 5000:
        return make_response(jsonify({"message": "post cannot exceed 5000 character limit"}), 413)
    if len(data['content']) < 1:
        return make_response(jsonify({"message": "post length cannot be < 1"}), 422)
    if not post:  
        return make_response(jsonify({'message': 'post does not exist'})  ,404)
    if post.user_id != current_user.id:
        return make_response(jsonify({'message': 'post does not belong to user'})  ,403)
    
    post.title = data['title']
    post.content = data['content']
    db.session.commit()  
    return jsonify({'message': 'post updated'})

# deleting a post
@app.route('/blog/delete-post/<post_id>', methods=['DELETE'])
@token_required
def delete_post(current_user,post_id): 
 
    post = PostModel.query.filter_by(id=post_id).first()  
    if not post:  
        return make_response(jsonify({'message': 'post does not exist'})  ,404)
    if post.user_id != current_user.id:
        return make_response(jsonify({'message': 'post does not belong to user'})  ,403)
    
    db.session.delete(post) 
    db.session.commit()  
    return jsonify({'message': 'post deleted'})
