from os import getenv
from os.path import exists

from flask import redirect, url_for, flash
from youtube_dl import YoutubeDL

from app import db
from app import models


def create_db():
    if not exists(getenv('DATABASE_URI')):
        db.create_all()


def register_data(**kwargs):
    data = models.Video(
        url=kwargs.get('url', '#'),
        title=kwargs.get('title', '(Untitled)'),
        author=kwargs.get('author', '(Unknown)'),
        description=kwargs.get('description', ''),
        views=kwargs['views'],
        date=kwargs['date'],
        likes=kwargs.get('likes', '?'),
        dislikes=kwargs.get('dislikes', '?'),
        subscribers=kwargs.get('subscribers', '?'),
        thumbnail=kwargs.get('thumbnail', 'thumb.jpg'),
        profile_picture=kwargs.get('profile_picture', 'profile.jpg')
    )
    db.session.add(data)
    db.session.commit()
    flash('Video submitted successfully', 'success')
    return redirect(url_for('index'))


def get_video(url: str):
    with YoutubeDL({}) as ydl:
        info = ydl.extract_info(url)

        url = info.get('webpage_url', None)
        title = info.get('title', None)
        author = info.get('uploader', None)
        description = info.get('description', None)
        views = info.get('view_count', None)
        date = info.get('upload_date', None)
        likes = info.get('like_count', None)
        dislikes = info.get('dislike_count', None)
        subscribers = info.get('', None)  # Unknown location for subscribers data
        thumbnail = info.get('thumbnail', None)
        profile_picture = info.get('', None)  # Insert profile picture scrap here

        data_dict = {
            "url": url,
            "title": title,
            "author": author,
            "description": description,
            "views": views,
            "date": date,
            'likes': likes,
            'dislikes': dislikes,
            'subscribers': subscribers,
            'thumbnail': thumbnail,
            'profile_picture': profile_picture
        }

        try:
            register_data(**data_dict)
        except Exception as e:
            return str(e)

