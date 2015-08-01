# -*- coding: utf-8

from flask import Flask, render_template, request, session, redirect, \
        url_for, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.htpasswd import HtPasswdAuth
import requests
import ConfigParser
from functools import wraps

# Import forms
from forms import LoginForm

# Bootstrap
from flask.ext.bootstrap import Bootstrap

config = ConfigParser.RawConfigParser()
try:
    config.readfp(open(r'settings.conf'))
except IOError as e:
    print e

try:
    ApiKeyYoutube = config.get('Main', 'api_key')
    my_username = config.get('Main', 'username')
    my_password = config.get('Main', 'password')
except (ConfigParser.NoSectionError, ConfigParser.NoOptionError) as e:
    print e

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///video.db'
app.config['FLASK_HTPASSWD_PATH'] = '/home/memtube/.htpasswd'
app.config['FLASK_SECRET'] = 'Hey Hey Kids, secure me!'
htpasswd = HtPasswdAuth(app)
db = SQLAlchemy(app)
ApiKeyYoutube = 'AIzaSyCbduO-H4OZ6_kwSgAj1QO9NDVrkCp9mXw'
>>>>>>> 226d07972e6d0ad21d255b7db3210e724d68b09b
Googleurl = 'https://www.googleapis.com/youtube/v3/'
bootstrap = Bootstrap(app)

# This is for handling sessions
app.config['SECRET_KEY'] = '\xf0\x90\x10\xe5\x01&\x95\x12\x83u\x0caI\x18\xd2\xc2\xc9\x93\xc5\x9d\xa1kpl\xf1\xe0T\x88\x97ni\xda\xc4\xfa\xfd\x969\xc7\xe6\xe2\xbb\xcexq\xe5\xb0\x8f\xf0\x7f\xa2\x8e8)\xe9m\xadT\x84\xd1\xf6\xa3\xad\xf6\xdc'


# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

class Channel(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    channelid = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(512))

    def __init__(self, channelid=None, name=None):
        self.channelid = channelid
        self.name = name

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    videoid = db.Column(db.String(250), unique=True)

    def __init__(self, videoid=None):
        self.videoid = videoid

# db.drop_all()
db.create_all()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.uname.data != my_username or form.pwd.data != my_password:
            flash('Invalid login credentials. Please try again.')
        else:
            session['logged_in'] = True
            return redirect(url_for('channels'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('channels'))


@app.route('/', methods=['GET', 'POST'])
#@login_required
@htpasswd.required
def channels(user):
    if request.method == 'POST':
        channelid = request.form['url'].split("/channel/")[-1]
        apiurl = Googleurl + 'channels?part=snippet&id=' + \
            channelid + '&key=' + ApiKeyYoutube
        j = requests.get(apiurl).json()
        name = j['items'][0]['snippet']['title']
        me = Channel(channelid, name)
        db.session.add(me)
        db.session.commit()

    return render_template("channels.html", rows=Channel.query.all())


@app.route('/channel-videos-list/<channelid>/<page>/')
# @login_required
def video_list(channelid, page):
    apiurl = Googleurl + 'search?part=snippet&channelId=' + channelid + \
        '&key=' + ApiKeyYoutube + '&maxResults=9&order=date&type=video'
    if page != 'first_page':
        apiurl = apiurl + '&pageToken=' + page
    j = requests.get(apiurl).json()
    n = 0
    for i in j['items']:
        videoid = j['items'][n]['id']['videoId']
        v = Video.query.filter(Video.videoid == videoid).first()
        if v:
            j['items'][n]['viwed'] = 1
        n += 1
    channel_name = Channel.query.filter(Channel.channelid == channelid).first()
    return render_template("video_list.html", allinfo=j, namec=channel_name)


@app.route('/view-video/<channelid>/<videoid>/')
# @login_required
def view_video(channelid, videoid):
    channel_name = Channel.query.filter(Channel.channelid == channelid).first()
    v = Video.query.filter(Video.videoid == videoid).first()
    return render_template("view_video.html", namec=channel_name, idv=videoid,
                           v=v)


@app.route('/_viwed')
# @login_required
def _viwed():
    videoid = request.args.get('videoid')
    me = Video(videoid)
    db.session.add(me)
    db.session.commit()
    return ""


if __name__ == "__main__":
        # app.run()
        # app.debug = True
        app.run(host='188.120.229.137', port=80)
        # app.run(host='0.0.0.0')