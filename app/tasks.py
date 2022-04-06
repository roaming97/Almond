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
from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError

from app import db, models, dictionaries


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
        return True
    except (IntegrityError, Exception) as e:
        if type(e) == IntegrityError:
            e.hide_parameters = True
            e.code = None
            s = str(e).split(":")[0]
            flash(f'{s}', 'danger')
        else:
            flash(f'{e}', 'danger')
        return False


def f_digits(st: str): return f'{int(st):,}'
def remove_temp_files(*args): [remove(a) for a in args if isfile(a)]
def isfloat(s: str): return bool(re.match(r'^-?\d+(\.\d+)?$', s))


def clean_filename(title):
    new_title = str(title)
    for key, value in dictionaries.filename_maps.items():
        new_title = new_title.replace(key, value)
    return new_title


def additional_info(*args):
    raw_html = httpx.get(args[0])
    a_info = []
    pfp = args[1]
    subs = args[2]

    pfp_regex = r'((avatar":{"thumbnails":\[{"url":")(https(.+?))(s48))'
    subscribers_regex = r'("},"subscriberCountText":{"accessibility":{"accessibilityData":{"label":"(.+?)"}},(.+?)"},"t)'
    subscribers_regex_2 = r'}}},"trackingParams":"(.+?)(="}},"subscriberCountText":{"accessibility":{"accessibilityData":{"label":"(.+?)"}},(.+?)"})'

    for profile_picture_search in re.finditer(pfp_regex, str(raw_html.text)):
        pfp = profile_picture_search.group(3) + "s1000-c-k-c0x00ffffff-no-rj"

    for subscribers_count_search in re.finditer(subscribers_regex, str(raw_html.text)):
        subs = subscribers_count_search.group(2)

    for subscribers_count_search in re.finditer(subscribers_regex_2, str(raw_html.text)):
        subs = subscribers_count_search.group(3)

    if not subs:
        subs = 'N/A'
    else:
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
    a_info.append(pfp)
    a_info.append(subs)
    return a_info


def save_blobs(**kwargs):
    blobs = []
    thumb_path = f'{kwargs["vid_id"]}.{kwargs["thumb_ext"]}'
    pfp_path = f'{kwargs["vid_id"]}.{kwargs["pfp_ext"]}'

    video_path = f'{clean_filename(kwargs["vid_title"])}-{kwargs["vid_id"]}.{kwargs["vid_ext"]}'

    thumb_file = r.urlretrieve(kwargs['thumb_url'], thumb_path)
    pfp_file = r.urlretrieve(kwargs['pfp_url'], pfp_path)
    with open(thumb_file[0], 'rb') as t:
        blobs.append(t.read())
    with open(video_path, 'rb') as v:
        blobs.append(v.read())
    with open(pfp_file[0], 'rb') as p:
        blobs.append(p.read())
    remove_temp_files(thumb_path, pfp_path, video_path)
    return blobs


def quick_add(url: str):
    with YoutubeDL(dictionaries.ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url)
        except DownloadError as e:
            ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            error = ansi.sub('', str(e)).replace('\n', '. ').replace('ERROR:', '')
            flash(f'{error}', 'danger')
            return False

        video_id = info.get('id', None)
        video_url = info.get('webpage_url', None)
        title = info.get('title', None)
        author = info.get('uploader', None)
        author_url = info.get('uploader_url', None)
        description = info.get('description', None)
        views = info.get('view_count', None)
        date = info.get('upload_date', None)
        likes = info.get('like_count', None)
        dislikes = info.get('dislike_count', None)
        thumbnail_url = str(info.get('thumbnails', None)[0]['url']).split("?")[0]

        views = f_digits(views)
        likes = f_digits(likes)
        # dislikes = f_digits(dislikes)
        dislikes = 'N/A'

        profile_picture = None
        subscribers = None
        [profile_picture, subscribers] = additional_info(author_url, profile_picture, subscribers)

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
        except Exception:
            thumbnail = b''
            stream = b''
            profile_picture = b''

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


def static_files(key):
    with BytesIO() as byteStream:
        with Image.open(join(dirname(realpath(__file__)), f'static/{key}.jpg')) as img:
            img.save(byteStream, format='PNG')
        return b64encode(byteStream.getvalue())


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
