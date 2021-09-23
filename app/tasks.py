
from app import db
from app import models

def create_database():
    db.create_all()
    db.session.close()

def register_data(title, author, description, views, date, likes, dislikes, subscribers, url, thumbnail, profile_picture):    
    data = models.Video(title=title, author=author, description=description, views=views, date=date, likes=likes, dislikes=dislikes, subscribers=subscribers, url=url, thumbnail=thumbnail, profile_picture=profile_picture)
    db.session.add(data)
    db.session.commit()
    db.session.close()