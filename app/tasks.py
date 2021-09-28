from os import getenv
from os.path import exists

from flask import flash
from youtube_dl import YoutubeDL

from app import db, models


def create_db():
    if not exists(getenv('DATABASE_URI')):
        db.create_all()


def register_data(**kwargs):
    data = models.Video(
        url=kwargs.get('url', '#'),
        title=kwargs.get('title', '(Untitled)'),
        author=kwargs.get('author', '(Unknown)'),
        author_url=kwargs.get('author_url', ''),
        description=kwargs.get('description', ''),
        views=kwargs['views'],
        date=kwargs['date'],
        likes=kwargs.get('likes', 'N/A'),
        dislikes=kwargs.get('dislikes', 'N/A'),
        subscribers=kwargs.get('subscribers', 'N/A'),
        thumbnail=kwargs.get('thumbnail', 'thumb.jpg'),
        profile_picture=kwargs.get('profile_picture', 'profile.jpg')
    )
    db.session.add(data)
    db.session.commit()


def get_video_info(url: str):
    with YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)

        video_url = info.get('webpage_url', None)
        title = info.get('title', None)
        author = info.get('uploader', None)
        author_url = info.get('uploader_url', None)
        description = info.get('description', None)
        views = info.get('view_count', None)
        date = info.get('upload_date', None)
        likes = info.get('like_count', 'N/A')
        dislikes = info.get('dislike_count', 'N/A')
        subscribers = info.get('subscribers', 'N/A')  # Unknown location for subscribers data
        thumbnails = info.get('thumbnails', None)
        profile_picture = info.get('profile_picture', None)  # Insert profile picture scrap here

        data_dict = {
            "url": video_url,
            "title": title,
            "author": author,
            "author_url": author_url,
            "description": description,
            "views": views,
            "date": date,
            'likes': likes,
            'dislikes': dislikes,
            'subscribers': subscribers,
            'thumbnail': thumbnails[0]['url'],
            'profile_picture': profile_picture
        }

        try:
            register_data(**data_dict)
            return True
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return False
