import urllib.request as r
from base64 import b64encode
from os import getenv, remove
from os.path import exists, isfile

from flask import flash
from youtube_dl import YoutubeDL

from app import db, models


def create_db():
    if not exists(getenv('DATABASE_URI')):
        db.create_all()


def register_data(**kwargs):
    data = models.Video(
        video_id=kwargs["video_id"],
        url=kwargs["url"],
        title=kwargs.get('title', 'Untitled'),
        author=kwargs.get('author', 'N/A'),
        author_url=kwargs.get('author_url', ''),
        description=kwargs.get('description', ''),
        views=kwargs['views'],
        date=kwargs['date'],
        likes=kwargs.get('likes', 'N/A'),
        dislikes=kwargs.get('dislikes', 'N/A'),
        subscribers=kwargs.get('subscribers', 'N/A'),
        stream=kwargs.get('stream', None),
        thumbnail_url=kwargs.get('thumbnail_url', None),
        thumbnail=kwargs.get('thumbnail', b''),
        profile_picture=kwargs.get('profile_picture', 'profile.jpg')
    )
    db.session.add(data)
    db.session.commit()


def save_blobs(with_video=True, **kwargs):
    blobs = []
    thumb_path = f'{kwargs["vid_id"]}.{kwargs["thumb_ext"]}'
    video_path = f'{kwargs["vid_title"]}-{kwargs["vid_id"]}.{kwargs["vid_ext"]}'

    thumb_file = r.urlretrieve(kwargs['thumb_url'], thumb_path)
    with open(thumb_file[0], 'rb') as t:
        blobs.append(t.read())
    if with_video:
        with open(video_path, 'rb') as v:
            blobs.append(v.read())
    if isfile(thumb_path):
        remove(thumb_path)
    if isfile(video_path):
        remove(video_path)
    return blobs


def get_video_info(url: str, with_blobs=True):
    with YoutubeDL({'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'}) as ydl:
        info = ydl.extract_info(url)

        video_id = info.get('id', None)
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
        thumbnail_url = str(info.get('thumbnails', None)[0]['url']).split("?")[0]
        profile_picture = info.get('profile_picture', None)  # Insert profile picture scrap here

        if with_blobs:
            blobs = save_blobs(
                thumb_url=thumbnail_url,
                thumb_ext=(str(thumbnail_url).split(".")[-1]).split('?')[0],
                vid_id=video_id,
                vid_title=title,
                vid_ext=info["ext"]
            )
            thumbnail = b64encode(blobs[0])
            stream = b64encode(blobs[1])
        else:
            thumbnail = b''
            stream = b''

        data_dict = {
            "video_id": video_id,
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
            'stream': stream,
            'thumbnail_url': thumbnail_url,
            'thumbnail': thumbnail,
            'profile_picture': profile_picture
        }

        try:
            register_data(**data_dict)
            return True
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            return False
