import logging
import os
import re
import urllib.request as r
from base64 import b64encode
from io import BytesIO
from os import getenv, remove
from os.path import exists, isfile, join, dirname, realpath

import httpx
from PIL import Image
from flask import flash, session
from flask_wtf import FlaskForm
from sqlalchemy.exc import IntegrityError
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError

from app import db, models, dictionaries, settings


def create_db():
    if not exists(getenv('DATABASE_URI')):
        db.create_all()


def init_session_vars(admin=False):
    session["current_page"] = 1
    session["current_sort"] = "newest_added"
    session["access"] = True
    if admin:
        session["admin"] = True


def clear_session_vars():
    session.pop("access", None)
    session.pop("current_page", None)
    session.pop("current_sort", None)
    if "admin" in session:
        session.pop("admin", None)


def remove_temp_files():
    valid_formats = ('mp4', 'part', 'mkv', 'ytdl', 'm4a', 'jpg', 'png')
    for file in os.listdir(os.getcwd()):
        if file in os.listdir('static'):
            continue
        if isfile(file) and file.endswith(valid_formats):
            remove(file)


def register_data(**kwargs):
    try:
        data = models.Video(
            video_id=kwargs.get('video_id', None),
            url=kwargs.get('url', None),
            title=kwargs.get('title', 'Untitled'),
            author=kwargs.get('author', 'N/A'),
            author_url=kwargs.get('author_url', ''),
            description=kwargs.get('description', ''),
            views=kwargs.get('views', 'N/A'),
            date=kwargs.get('date', 'N/A'),
            likes=kwargs.get('likes', 'N/A'),
            dislikes=kwargs.get('dislikes', 'N/A'),
            subscribers=kwargs.get('subscribers', 'N/A'),
            stream=kwargs['stream'],
            thumbnail_url=kwargs.get('thumbnail_url', ''),
            thumbnail=kwargs.get('thumbnail', b''),
            profile_picture=kwargs.get('profile_picture', b'')
        )
        db.session.add(data)
        db.session.commit()
        remove_temp_files()
        return True
    except (IntegrityError, Exception) as e:
        if type(e) == IntegrityError:
            e.hide_parameters = True
            e.code = None
            s = str(e).split(":")[0]
            flash(f'{s}', 'danger')
            logging.error(e)
        else:
            flash(f'{e}', 'danger')
            logging.error(e)
        remove_temp_files()
        return False


def f_digits(st: str): return f'{int(st):,}'
def isfloat(s: str): return bool(re.match(r'^-?\d+(\.\d+)?$', s))


def clean_filename(title):
    new_title = str(title)
    for key, value in dictionaries.filename_maps.items():
        new_title = new_title.replace(key, value)
    return new_title


def format_subscribers(subs):
    for word in subs.split():
        if word.isnumeric():
            subs = word
            break
        elif isfloat(word):
            subs = f'{word}M'
            break

        if not word.isalnum():
            raw_word = re.sub(r'(\d),(\d)', r'\1\2', word)
            if raw_word.isnumeric():
                subs = word
                break
    return subs


def additional_info(*args):
    # dirty trick, reminder to open an issue in the httpx repo
    html = httpx.get(args[0].replace('http://', 'https://')).text

    dislikes_api = httpx.get(f"https://returnyoutubedislikeapi.com/votes?videoId={args[1]}")
    dislikes = dislikes_api.json()['dislikes']
    logging.debug(dislikes)

    pfp_regex = r'((avatar":{"thumbnails":\[{"url":")(https(.+?))(s48))'
    pfp = next(re.finditer(pfp_regex, html)).group(3) + "s800-c-k-c0x00ffffff-no-rj"
    logging.debug(f"PROFILE_PIC: {pfp}")

    subscribers_regex = r'}}},"trackingParams":"(.+?)(="}},"subscriberCountText":{"accessibility":{"accessibilityData":{"label":"(.+?)"}},(.+?)"})'
    subs = next(re.finditer(subscribers_regex, html)).group(3).split()[0]
    logging.debug(f"SUBSCRIBERS: {subs}")

    if not subs:
        subs = 'N/A'
    
    return pfp, subs, dislikes


def save_blobs(**kwargs):
    blobs = []

    thumb_path = f'{kwargs["vid_id"]}.{kwargs["thumb_ext"]}'
    pfp_path = f'{kwargs["vid_id"]}.{kwargs["pfp_ext"]}'
    video_path = f'{clean_filename(kwargs["vid_title"])} [{kwargs["vid_id"]}].{kwargs["vid_ext"]}'

    thumb_file = r.urlretrieve(kwargs['thumb_url'], thumb_path)[0]
    pfp_file = r.urlretrieve(kwargs['pfp_url'], pfp_path)[0]

    for file in [thumb_file, video_path, pfp_file]:
        with open(file, 'rb') as f:
            blobs.append(f.read())
        if settings.keep_original_files:
            output_path = f'./output/{kwargs["vid_id"]}'
            os.makedirs(output_path)
            os.replace(file, f'{os.path.join(os.getcwd(), output_path)}/{file}')

    return blobs


def static_files(key):
    with BytesIO() as byteStream:
        with Image.open(join(dirname(realpath(__file__)), f'static{os.sep}{key}.jpg')) as img:
            img.save(byteStream, format='PNG')
        return b64encode(byteStream.getvalue())


def quick_add(url: str):
    with YoutubeDL(dictionaries.ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url)
        except DownloadError as e:
            ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            error = ansi.sub('', str(e)).replace('\n', '. ').replace('ERROR:', '')
            remove_temp_files()
            flash(f'{error}', 'danger')
            return False

        video_id = info.get('id', None)
        video_url = info.get('webpage_url', None)
        title = info.get('title', None)
        author = info.get('uploader', None)
        author_url = info.get('uploader_url', None)
        description = info.get('description', None)
        views = info.get('view_count', 'N/A')
        date = info.get('upload_date', None)
        likes = info.get('like_count', 'N/A')
        thumbnail_url = str(info.get('thumbnails', None)[0]['url']).split("?")[0]

        views = f_digits(views)
        likes = f_digits(likes)

        profile_picture, subscribers, dislikes = additional_info(author_url, video_id)
        dislikes = f_digits(dislikes) if dislikes is not None else 'N/A'

        try:
            blobs = save_blobs(
                thumb_url=thumbnail_url,
                thumb_ext=(str(thumbnail_url).split(".")[-1]).split('?')[0],
                vid_id=video_id,
                vid_title=title,
                vid_ext=info["ext"],
                pfp_url=profile_picture,
                pfp_ext="png"
            )
            thumbnail = b64encode(blobs[0])
            stream = b64encode(blobs[1])
            profile_picture = b64encode(blobs[2])
        except Exception as e:
            logging.error(e)
            thumbnail = static_files('thumbnail')
            stream = b''
            profile_picture = static_files('profile_picture')

        data_dict = {
            'video_id': video_id,
            'url': video_url,
            'title': title,
            'author': author,
            'author_url': author_url,
            'description': description,
            'views': views,
            'date': date,
            'likes': likes,
            'dislikes': dislikes,
            'subscribers': subscribers,
            'stream': stream,
            'thumbnail_url': thumbnail_url,
            'thumbnail': thumbnail,
            'profile_picture': profile_picture
        }

        return register_data(**data_dict)


def manual_add(form: FlaskForm):
    data_dict = {f'{k}': v for k, v in form.data.items() if k != 'csrf_token' or k != 'submit'}
    data_dict['video_id'] = str(data_dict['url']).split("=")[-1] if data_dict['url'] else None
    storage_keys = ['stream', 'thumbnail', 'profile_picture']
    for key in storage_keys:
        if data_dict[key]:
            data_dict[key] = b64encode(data_dict[key].read())
        else:
            data_dict[key] = static_files(key)
    return register_data(**data_dict)
