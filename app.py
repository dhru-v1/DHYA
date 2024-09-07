from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
app.config['SESSION_TYPE'] = 'filesystem'

mongo = PyMongo(app)
Session(app)

@app.route('/')
def home():
    if 'username' in session:
        email = session['email']
        name = session['name']
        usename = session['username']
        return render_template('home.html', name=name)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        if mongo.db.users.find_one({'username': username}):
            flash('Username already exists!')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        mongo.db.users.insert_one({'email':email,'username': username,'name': name, 'password': hashed_password})
        flash('Registration successful!')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            session['email'] = user['email']
            session['name'] = user['name']
            return redirect(url_for('home'))
            return redirect(url_for('home'))
        flash('Invalid username or password!')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
