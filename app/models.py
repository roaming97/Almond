from app import db

# Database models


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=True, default='')
    views = db.Column(db.String(25), nullable=False)
    date = db.Column(db.String(8), nullable=False)
    likes = db.Column(db.String(12), nullable=True)
    dislikes = db.Column(db.String(12), nullable=True)
    subscribers = db.Column(db.String(12), nullable=True)
    stream = db.Column(db.LargeBinary, unique=True, nullable=True)  # Nullable for now
    thumbnail = db.Column(db.String(50), nullable=True, default='thumb.jpg')
    profile_picture = db.Column(db.String(50), nullable=True, default='profile.jpg')

    def __repr__(self):
        return f"Video(" \
               f"'{self.url}'" \
               f"'{self.title}', " \
               f"'{self.author}', " \
               f"'{self.description}'," \
               f"'{self.views}', " \
               f"'{self.date}', " \
               f"'{self.likes}', " \
               f"'{self.dislikes}', " \
               f"'{self.thumbnail}'," \
               f"'{self.profile_picture}')"
