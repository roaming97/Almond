from app.models import Video

filename_maps = {
    '"': "'",
    ':': ' -',
    '?': '',
    '*': '_',
    '/': '_',
    '\\': '_',
    '|': '_',
    '||': '_'
}

video_sorts = {
    'newest-added': Video.id.desc(),
    'oldest-added': Video.id,
    'newest': Video.date.desc(),
    'oldest': Video.date
}

ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
    'noplaylist': True
}
