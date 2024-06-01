from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_security import UserMixin,RoleMixin

db=SQLAlchemy()

class User(db.Model, UserMixin):
   id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
   user_name=db.Column(db.String(),nullable=False)
   password=db.Column(db.String(),nullable=False)
   email = db.Column(db.String(255), unique=True, nullable=False)
   active=db.Column(db.Boolean())
   fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
   profile_pic=db.Column(db.String(),nullable=True)
   timestamp=timestamp=db.Column(db.DateTime, default=datetime.utcnow)
   current_login_at=db.Column(db.DateTime)
   last_login_at=db.Column(db.DateTime)
   roles=db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
   playlists=db.relationship('Playlistuser',backref="by_user")
   liked_songs=db.relationship('Songs',backref='liked_by', secondary='likes')
   rated_songs=db.relationship('Songs',backref='rated_by', secondary='rating')
   songs=db.relationship('Songs',backref="song_by")
   albums=db.relationship('Album',backref="owner")
   followers=db.relationship('User',secondary='followers',primaryjoin="followers.c.followee_id==user.c.id",
            secondaryjoin="followers.c.follower_id==user.c.id", backref='follows')
   flagged_songs=db.relationship('Songs', backref='flagged_by', secondary='flags')
   #it is a child of parent class db.model

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class Album(db.Model):
   album_id=db.Column(db.Integer(),primary_key=True)
   album_name=db.Column(db.String(),nullable=False)
   artist_id=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
   flag=db.Column(db.Boolean, default=False)
   songs=db.relationship('Songs',backref='from_album')

class Songs(db.Model):
   song_id=db.Column(db.Integer(),primary_key=True)
   song_name=db.Column(db.String(),nullable=False)  
   singer=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
   album=db.Column(db.Integer(),db.ForeignKey('album.album_id'),nullable=True)
   lyrics=db.Column(db.Text(),nullable=False)
   genre=db.Column(db.String(),nullable=False)
   total_rating=db.Column(db.Integer(),default=0)
   song_path=db.Column(db.String(),nullable=False)
   timestamp=db.Column(db.DateTime, default=datetime.utcnow)
   poster=db.Column(db.String(),nullable=False)
   flag=db.Column(db.Boolean, default=False)
   plays=db.Column(db.Integer(), default=0)

class Likes(db.Model):
   relationship_id=db.Column(db.Integer(),primary_key=True,autoincrement=True) 
   l_user_id=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
   l_song_id=db.Column(db.Integer(),db.ForeignKey('songs.song_id'),nullable=False) 

class Rating(db.Model):
   rating_id=db.Column(db.Integer(),primary_key=True,autoincrement=True) 
   r_user_id=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
   r_song_id=db.Column(db.Integer(),db.ForeignKey('songs.song_id'),nullable=False)
   rating=db.Column(db.Integer(),default=0)

class Playlist(db.Model):
   relationship_id=db.Column(db.Integer(),primary_key=True)
   playlist_id=db.Column(db.Integer(),db.ForeignKey('playlistuser.p_id'),nullable=False)
   p_song_id=db.Column(db.Integer(),db.ForeignKey('songs.song_id'),nullable=False)

class Playlistuser(db.Model):
   p_id=db.Column(db.Integer(),primary_key=True) 
   p_user_id=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False) 
   playlist_name=db.Column(db.String(),nullable=False) 
   songs=db.relationship('Songs',backref="in_playlists",secondary="playlist")

class Followers(db.Model):
   relationship_id=db.Column(db.Integer(),primary_key=True,autoincrement=True) 
   follower_id=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
   followee_id=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False) 

class Flags(db.Model):
   __table_name__='followers'
   relationship_id=db.Column(db.Integer(),primary_key=True,autoincrement=True) 
   f_user_id=db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)
   f_song_id=db.Column(db.Integer(),db.ForeignKey('songs.song_id'),nullable=False) 

