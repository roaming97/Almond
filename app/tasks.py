from os import getenv
from os.path import exists
from app import db
from app import models


def create_db():
    if not exists(getenv('DATABASE_URI')):
        db.create_all()


def register_data(**kwargs):
    data = models.Video(
        title=kwargs.get('title', 'Untitled'),
        author=kwargs.get('author', 'User'),
        description=kwargs.get('description', ''),
        views=kwargs['views'],
        date=kwargs['date'],
        likes=kwargs.get('likes', '?'),
        dislikes=kwargs.get('dislikes', '?'),
        subscribers=kwargs.get('subscribers', '?'),
        url=kwargs['url'],
        thumbnail=kwargs.get('thumbnail', 'thumb.jpg'),
        profile_picture=kwargs.get('profile_picture', 'profile.jpg')
    )
    db.session.add(data)
    db.session.commit()
