from app import db

# Database models


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(5000), nullable=True, default='')
    views = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(25), nullable=False)
    likes = db.Column(db.Integer, nullable=True)
    dislikes = db.Column(db.Integer, nullable=True)
    subscribers = db.Column(db.String(20), nullable=True)
    # stream = db.Column(db.LargeBinary, unique=True, nullable=False)
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
