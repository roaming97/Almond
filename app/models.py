from app import db, admin
from app.settings import private_app
from flask import session, abort
from flask_admin.contrib.sqla import ModelView

# Database models


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(11), unique=True, nullable=True)
    url = db.Column(db.String(50), unique=True, nullable=True)
    title = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(60), nullable=False)
    author_url = db.Column(db.String(60), nullable=True)
    description = db.Column(db.Text, nullable=True, default='')
    views = db.Column(db.String(25), nullable=True)
    date = db.Column(db.String(8), nullable=True)
    likes = db.Column(db.String(12), nullable=True)
    dislikes = db.Column(db.String(12), nullable=True)
    subscribers = db.Column(db.String(12), nullable=True)
    stream = db.Column(db.LargeBinary, unique=True, nullable=False)
    thumbnail_url = db.Column(db.String(50), nullable=True)
    thumbnail = db.Column(db.LargeBinary, nullable=True)
    profile_picture = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self):
        return f"Video(" \
               f"'{self.video_id}'" \
               f"'{self.url}'" \
               f"'{self.title}', " \
               f"'{self.author}', " \
               f"'{self.author_url}', " \
               f"'{self.description}'," \
               f"'{self.views}', " \
               f"'{self.date}', " \
               f"'{self.likes}', " \
               f"'{self.dislikes}', " \
               f"'{self.subscribers}', " \
               f"'{self.stream}', " \
               f"'{self.thumbnail_url}'," \
               f"'{self.thumbnail}'," \
               f"'{self.profile_picture}')"


# Admin

class AlmondModelView(ModelView):
    page_size = 3
    column_exclude_list = ['stream', 'thumbnail', 'profile_picture']
    def is_accessible(self): return True if "admin" in session and private_app else abort(403)


admin.add_view(AlmondModelView(Video, db.session))
