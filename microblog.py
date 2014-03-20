from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
# from flaskext.seasurf import SeaSurf
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flaskext.bcrypt import Bcrypt
from flask import render_template
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskblog'

db = SQLAlchemy(app)
# csrf = SeaSurf(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    auth_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = []
    email = []
    posts = []
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<User %r>' % self.name

@app.route('/')
def index():
    return render_template('layout.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
    # if request.method == 'POST':
    #     login()
    # else:
    #     show_login_form()


# @app.route('/post', methods=['GET', 'POST'])
# @app.route('/logout')
# def log_out():
#     if request.method == 'POST':
#         log_out()
#     else:
#         show_login_form()

@app.route('/new')
def write_post(title, text):
    new_post = Post(title, text)
    db.session.add(new_post)
    db.session.commit()
    return render_template('post.html')


def read_all_posts():
    """Display posts in reverse order."""
    all_posts = Post.query().order_by(Post.id.desc()).all()
    # the above was taken from our in-class code review
    return all_posts


def read_a_post(id):
    the_post = Post.query.filter_by(id=id).first()
    if not Post:
        raise IndexError('That post doesn\'t exist!')
    else:
        return the_post


@app.route('/login')
def login(id, password):
    pass






if __name__ == '__main__':
    manager.run()
