from datetime import datetime
from App import db

# Database models


class Video(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(5000), nullable=False, default='')
    link = db.Column(db.String(100), nullable=False, default='')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # stream = db.Column(db.LargeBinary, unique=True, nullable=False)
    thumbnail = db.Column(db.String(20), nullable=False, default='thumb.jpg')

    def __repr__(self):
        return f"Video('{self.title}', '{self.author}', '{self.description}')"
