from flask import (Flask, session, url_for, render_template, redirect, flash,
                   request)
from flask.ext.seasurf import SeaSurf
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskblog'
app.secret_key = 'thiskeyissecret'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
bootstrap = Bootstrap(app)
csrf = SeaSurf(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, author, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.author = author

    def __repr__(self):
        return '<Post %r>' % self.title


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(40))
    email = db.Column(db.String, unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


# def write_post(title=None, text=None, author):
#     new_post = Post(title, text, author)
#     db.session.add(new_post)
#     db.session.commit()


def read_posts():
    """Display posts in reverse order."""
    all_posts = Post.query().order_by(Post.id.desc()).all()
    # the above was taken from our in-class code review
    return all_posts


def read_post(id):
    the_post = Post.query.filter_by(id=id).first()
    if not Post:
        raise IndexError('Someone there is who cannot find a post.\n'
                         'Oh, it\'s you!\n'
                         'That post doesn\'t exist!')
    else:
        return the_post


def add_user(username=None, email=None, password=None):
    if username==None:
        flash('No anonymous poets allowed. Pick a name, pilgrim.')
    if email==None:
        flash('No, no, no. You have to enter a (valid) email.')
    if password==None:
        flash('No password=your shit gets jacked. Enter a password, amigo.')


@app.route('/')
def all_posts():
    # all_posts = read_posts()
    return render_template('base.html')  # , posts=all_posts


@app.route('/compose', methods=['GET', 'POST'])
def write_post():
    return render_template('compose.html')


@app.route('/usercontrol', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and request.form['password'] == user.password:
            session['logged_in'] = True
            session['current_user'] = request.form['username']
            flash('You are logged in')
            return redirect(url_for('list_view'))
        else:
            flash('Dude, you muffed it. Try logging in again.')
    return render_template('usercontrol.html')


@app.route('/categories')
def show_categories():
    return render_template('categories.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    flash('You were logged out.')
    return redirect(url_for('all_posts'))

# @app.route('/post/<id>', method='GET')
# def single_post_view():
#     return render_template('single_post.html', id=id)

if __name__ == '__main__':
    manager.run()
