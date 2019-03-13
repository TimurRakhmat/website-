from flask_restful import reqparse, abort, Api, Resource
import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired
from flask import Flask
from flask import redirect
from flask import render_template
from flask import jsonify
from flask import make_response
from flask import request
from requests import get, post, delete, put


class AddRevForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddGameForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    image = StringField('ссылка на фото', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class AddCommForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegistrForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    passwordcheck = PasswordField('Повторите пароль', validators=[DataRequired()])
    image = StringField('ссылка на фото', validators=[DataRequired()])
    submit = SubmitField('Войти')


class DB:
    def __init__(self):
        conn = sqlite3.connect('games.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class GamesModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS games 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             text VARCHAR(1000),
                             imgadrs VARCHAR(100)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, img):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO games 
                          (title, text, imgadrs) 
                          VALUES (?,?,?)''', (title, content, img))
        cursor.close()
        self.connection.commit()

    def get(self, game_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM games WHERE id = ?", (str(game_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM games")
        rows = cursor.fetchall()
        return rows

    def delete(self, game_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM games WHERE id = ?''', (str(game_id),))
        cursor.close()
        self.connection.commit()


class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             imgadrs VARCHAR(100)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, user_name, password_hash, img):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, imgadrs) 
                          VALUES (?,?)''', (user_name, password_hash, img))
        cursor.close()
        self.connection.commit()

    def exists(self, user_name, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ? AND password_hash = ?",
                       (user_name, password_hash))
        row = cursor.fetchone()
        return (True, row[0]) if row else (False,)

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id),))
        cursor.close()
        self.connection.commit()


class ReviewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS rewiew
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER
                             game_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_id, game_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO rewiew
                          (title, content, user_id, geme_id) 
                          VALUES (?,?,?,?)''', (title, content, str(user_id), str(game_id)))
        cursor.close()
        self.connection.commit()

    def get(self, rew_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM rewiew WHERE id = ?", (str(rew_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute("SELECT * FROM rewiew WHERE user_id = ?",
                           (str(user_id),))
        else:
            cursor.execute("SELECT * FROM rewiew")
        rows = cursor.fetchall()
        return rows

    def delete(self, rew_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM rewiew WHERE id = ?''', (str(rew_id),))
        cursor.close()
        self.connection.commit()


class CommentsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS comment
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user_id INTEGER,
                             userimg VARCHAR(100),
                             rew_id INTEGER
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user_id, img, rev_id):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO comment 
                          (title, content, user_id, userimg, rew_id) 
                          VALUES (?,?,?,?,?)''', (title, content, str(user_id), img, str(rev_id)))
        cursor.close()
        self.connection.commit()

    def get(self, com_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM comment WHERE id = ?", (str(com_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, review_id=None):
        cursor = self.connection.cursor()
        if review_id:
            cursor.execute("SELECT * FROM comment WHERE user_id = ?",
                           (str(review_id),))
        else:
            cursor.execute("SELECT * FROM comment")
        rows = cursor.fetchall()
        return rows

    def delete(self, com_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM comment WHERE id = ?''', (str(com_id),))
        cursor.close()
        self.connection.commit()


class Game(Resource):
    def get(self, game_id):
        abort_if_game_not_found(game_id)
        game = GamesModel(db.get_connection()).get(game_id)
        return render_template('game.html', game=game, reviews=get('http://localhost:8080/review'), session=session)

    def delete(self, game_id):
        abort_if_game_not_found(game_id)
        GamesModel(db.get_connection()).delete(game_id)
        return jsonify({'success': 'OK'})


class GamePost(Resource):
    def get(self):
        if 'username' not in session:
            return redirect('/login')
        form = AddGameForm()
        if form.validate_on_submit():
            post('http://localhost:8080/game', json={'tilte': form.title.data,
                                                     'content': form.content.data,
                                                     'image': form.image.data})
            return redirect('/game')
        return render_template('add_game.html', form=form, session=session)


class GamesList(Resource):
    def get(self):
        user = GamesModel(db.get_connection()).get_all()
        return user

    def post(self):
        args = gparser.parse_args()
        game = GamesModel(db.get_connection())
        game.insert(args['title'], args['content'], args['image'])
        return jsonify({'success': 'OK'})


class User(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        user = UsersModel(db.get_connection()).get(user_id)
        return user

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        UsersModel(db.get_connection()).delete(user_id)
        return jsonify({'success': 'OK'})


class UserLogin(Resource):
    def get(self):
        form = LoginForm()
        if form.validate_on_submit():
            user_name = form.username.data
            password = form.password.data
            exists = UsersModel(db.get_connection()).exists(user_name, password)
            if (exists[0]):
                session['username'] = user_name
                session['user_id'] = exists[1]
            return redirect("/")
        return render_template('login.html', form=form, session=session)


class UserReg(Resource):
    def get(self):
        form = RegistrForm()
        if form.validate_on_submit():
            post('http://localhost:8080/user', json={'name': form.username.data,
                                                     'password': form.password.data,
                                                     'image': form.image.data})
            return True
        return render_template('reg.html', form=form, session=session)


class UsersList(Resource):
    def get(self):
        user = UsersModel(db.get_connection()).get_all()
        return jsonify({'users': user})

    def post(self):
        args = uparser.parse_args()
        user = UsersModel(db.get_connection())
        user.insert(args['name'], args['password'], args['image'])
        return jsonify({'success': 'OK'})


class Review(Resource):
    def get(self, rew_id):
        abort_if_rewiew_not_found(rew_id)
        rew = ReviewsModel(db.get_connection()).get(rew_id)
        return render_template('review.html', review=rew, coments=get('http://localhost:8080/comment'), session=session)

    def delete(self, rew_id):
        abort_if_rewiew_not_found(rew_id)
        ReviewsModel(db.get_connection()).delete(rew_id)
        return jsonify({'success': 'OK'})


class ReviewPost(Resource):
    def get(self, game_id):
        if 'username' not in session:
            return redirect('/login')
        form = AddRevForm()
        if form.validate_on_submit():
            post('http://localhost:8080/game', json={'tilte': form.title.data,
                                                     'content': form.content.data,
                                                     'id': game_id})
            return redirect('/game')
        return render_template('add_game.html', form=form, session=session)


class ReviewsList(Resource):
    def get(self):
        rews = ReviewsModel(db.get_connection()).get_all()
        return rews

    def post(self):
        args = parser.parse_args()
        rews = ReviewsModel(db.get_connection())
        rews.insert(args['title'], args['content'], session['user_id'], args['id'])
        return jsonify({'success': 'OK'})


class Comment(Resource):
    def get(self, com_id):
        abort_if_comment_not_found(com_id)
        coms = CommentsModel(db.get_connection()).get(com_id)
        return coms

    def delete(self, com_id):
        abort_if_comment_not_found(com_id)
        CommentsModel(db.get_connection()).delete(com_id)
        return jsonify({'success': 'OK'})


class CommentPost(Resource):
    def get(self, rev_id):
        if 'username' not in session:
            return redirect('/login')
        form = AddCommForm()
        if form.validate_on_submit():
            post('http://localhost:8080/game', json={'tilte': form.title.data,
                                                     'content': form.content.data,
                                                     'id': rev_id})
            return redirect('/game')
        return render_template('add_game.html', form=form, session=session)


class CommentsList(Resource):
    def get(self):
        coms = CommentsModel(db.get_connection()).get_all()
        return coms

    def post(self):
        args = parser.parse_args()
        coms = CommentsModel(db.get_connection())
        coms.insert(args['title'], args['content'], args['id'])
        return jsonify({'success': 'OK'})


class MainPage(Resource):
    def get(self):
        return render_template('index.html', games=get('http://localhost:8080/game'), session=session)


def abort_if_user_not_found(user_id):
    if not UsersModel(db.get_connection()).get(user_id):
        abort(404, message="User {} not found".format(user_id))


def abort_if_game_not_found(id):
    if not GamesModel(db.get_connection()).get(id):
        abort(404, message="User {} not found".format(id))


def abort_if_comment_not_found(id):
    if not CommentsModel(db.get_connection()).get(id):
        abort(404, message="User {} not found".format(id))


def abort_if_rewiew_not_found(id):
    if not ReviewsModel(db.get_connection()).get(id):
        abort(404, message="User {} not found".format(id))


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
session = {}
db = DB()
UsersModel(db.get_connection()).init_table()
GamesModel(db.get_connection()).init_table()
ReviewsModel(db.get_connection()).init_table()
CommentsModel(db.get_connection()).init_table()


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('id', required=True, type=int)

uparser = reqparse.RequestParser()
uparser.add_argument('name', required=True)
uparser.add_argument('password', required=True)
uparser.add_argument('image', required=True)

gparser = reqparse.RequestParser()
gparser.add_argument('title', required=True)
gparser.add_argument('content', required=True)
gparser.add_argument('image', required=True)


api.add_resource(MainPage, '/')
api.add_resource(GamesList, '/game')
api.add_resource(Game, '/game/<int:game_id>')
api.add_resource(ReviewsList, '/review')
api.add_resource(Review, '/review/<int:rev_id>')
api.add_resource(CommentsList, '/comment')
api.add_resource(Comment, '/comment/<int:com_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(UsersList, '/users')
api.add_resource(UserLogin, '/login')
api.add_resource(UserReg, '/registr')
api.add_resource(GamePost, '/add_game')
api.add_resource(ReviewPost, '/add_rew/<int:game_id>')
api.add_resource(CommentPost, '/add_com/<int:rev_id>')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

