from flask_restful import Api,Resource, reqparse, fields, marshal_with, request
from application.models import *
import os
from flask_security import auth_required,current_user, roles_required
from sqlalchemy import func
from .instances import cache

api=Api()

parser=reqparse.RequestParser()

parser.add_argument("song_name",type=str, help="Song Name is required and it should be a String", required=True)
parser.add_argument("singer_id",type=int, help="Singer_id should be a integer", required=True)
parser.add_argument("song_album",type=str)
parser.add_argument("song_lyrics",type=str, help="Song Lyrics are required", required=True)
parser.add_argument("song_genre",type=str, )
parser.add_argument("song_path",type=str)
parser.add_argument("song_poster",type=str)

base_dir="/mnt/d/Mad2 Project/frontend/src"
upload_folder=os.path.join(base_dir, "assets")
songs_folder=os.path.join(upload_folder,"songs")
poster_folder=os.path.join(upload_folder,"posters")

song_fields = {
    'song_id':   fields.String,
    'song_name': fields.String,
    'artist_name': fields.String(attribute=lambda x: x.song_by.user_name),
    'album_id': fields.Integer,
    'lyrics':fields.String,
    'genre': fields.String,
    'total_rating': fields.Integer,
    'song_path':fields.String,
    'timestamp': fields.String,
    'poster': fields.String,
    'flag':fields.Boolean,
    'plays': fields.Integer,
    'in_playlists':fields.List(fields.Integer, attribute=lambda x: [playlist.p_id for playlist in x.in_playlists]),
    'user_flags':fields.Integer(attribute=lambda x: len(x.flagged_by))
}

class SongApi(Resource):
    @auth_required()
    @marshal_with(song_fields)
    def get(self):
        all_songs=Songs.query.all()
        return all_songs,200

    @auth_required() #for creator post 
    def post(self):
        audio_file=request.files['audio_file']
        poster_file=request.files['poster_file']
        song_name=request.form.get('song_name')
        lyrics=request.form.get('lyrics')
        genre=request.form.get('genre')
        song_option=request.form.get('song_option')
        audio_file.save(os.path.join(songs_folder,audio_file.filename))
        poster_file.save(os.path.join(poster_folder,poster_file.filename))
        if song_option=="album":
            album_id=request.form.get('album_id')
            if album_id!='null':
                song=Songs(song_name=song_name,singer=current_user.id, album=album_id,lyrics=lyrics, genre=genre, song_path=audio_file.filename, poster=poster_file.filename)
                db.session.add(song)
                db.session.commit()
            else:
                   song=Songs(song_name=song_name,singer=current_user.id,lyrics=lyrics, genre=genre, song_path=audio_file.filename, poster=poster_file.filename)  
                   db.session.add(song)
        else:  
          song=Songs(song_name=song_name,singer=current_user.id,lyrics=lyrics, genre=genre, song_path=audio_file.filename, poster=poster_file.filename)
          db.session.add(song)
        db.session.commit()
        return 200
    
    def put(self, song_id):
        song=Songs.query.get(song_id)
        song_name=request.form.get('song_name')
        lyrics=request.form.get('lyrics')
        genre=request.form.get('genre')
        song_option=request.form.get('song_option')
        if 'audio_file' in request.files:
            audio_file=request.files['audio_file']
            audio_file.save(os.path.join(songs_folder,audio_file.filename))
            song.song_path=audio_file.filename
        if 'poster_file' in request.files:
            poster_file=request.files['poster_file'] 
            poster_file.save(os.path.join(poster_folder,poster_file.filename))  
            song.poster=poster_file.filename
        print(song_option)    
        song.song_name=song_name
        song.lyrics=lyrics
        song.genre=genre
        if song_option=='single':
            if song.album is not None:
                       song.album=None
        else:
            album_id=request.form.get('album_id')
            if album_id!='null':
                if song.album!=album_id:
                    song.album=album_id        
        db.session.commit()
        return 200                 

    @auth_required()
    @roles_required('creator')
    def delete(self,song_id):
        song=Songs.query.get(song_id)
        db.session.delete(song)
        db.session.commit()   
        return 200    

album_fields={
    'album_id':   fields.String,
    'album_name': fields.String,
    'artist_id': fields.Integer,
    'flag':fields.Boolean,
    'songs':fields.List(fields.Nested(song_fields))
}
class AlbumApi(Resource):
    @auth_required()
    @roles_required('creator')
    @marshal_with(album_fields)   ##used for creator to get all albums of creator
    def get(self):
        option=request.args.get('option')
        if option=='all':
            albums=Album.query.filter_by(artist_id=current_user.id).all()
            return albums,200
        else:
            id=int(option)
            album=Album.query.get(id)
            return album,200
    
    @auth_required()
    @roles_required('creator')
    def put(self,song_id,album_id):
        option=request.args.get('option')
        album=Album.query.get(album_id)
        if current_user.id!=album.artist_id:
            return {'message':"Cannot Access"},400
        if option!='change':
            current_song=Songs.query.get(song_id)
        if option=='add':
            if current_song.album is not None:
                current_song.album=None
            album.songs.append(current_song)
        elif option=='remove':
            for song in album.songs:
                if song.song_id==current_song.song_id:
                    album.songs.remove(song)
        else:
            data=request.json
            album.album_name=data.get('album_name')           
        db.session.commit()
        return 200
    
    @auth_required()
    @roles_required('creator')
    def post(self):
        data=request.json
        album_name=data.get('album_name')
        album=Album(album_name=album_name,artist_id=current_user.id)
        db.session.add(album)
        db.session.commit()
        return {'album_id':album.album_id},200
    
    @auth_required()
    @roles_required('creator')
    def delete(self,album_id):
        album=Album.query.get(album_id)
        db.session.delete(album)
        db.session.commit()
        return 200

playlist_fields={
    'p_id':fields.Integer,
    'playlist_name':fields.String,
    'songs':fields.List(fields.Nested(song_fields))
}

class PlaylistApi(Resource):
    @marshal_with(playlist_fields)
    @auth_required()
    def get(self):
        option=request.args.get('option')
        if option=="all":
            playlists=Playlistuser.query.filter_by(p_user_id=current_user.id).all()   
            return playlists,200
        else:
            id=int(option)
            playlist=Playlistuser.query.get(id)
            return playlist,200
    
    @auth_required()
    def post(self):
        data=request.json
        playlist_name=data.get('playlist_name')
        playlist=Playlistuser(playlist_name=playlist_name, p_user_id=current_user.id)
        db.session.add(playlist)
        db.session.commit()
        return {'playlist_id':playlist.p_id}, 200
    
    @auth_required()
    def put(self,song_id,playlist_id):
        playlist=Playlistuser.query.get(playlist_id)
        option=request.args.get('option')
        if option!='change':
           song=Songs.query.get(song_id)
        if option=='add':
            if song in playlist.songs:
                return 200
            else:
                playlist.songs.append(song) 
        elif(option=='remove'):
            playlist.songs.remove(song)
        else:
            data=request.json
            playlist.playlist_name=data.get('playlist_name')    
        db.session.commit()
        return 200           
    
    @auth_required()
    def delete(self,playlist_id):
        playlist=Playlistuser.query.get(playlist_id)
        db.session.delete(playlist)
        db.session.commit()
        return 200

artist_fields={
    'id':fields.Integer,
    'user_name':fields.String,
    'songs':fields.List(fields.Nested(song_fields)),
    'albums':fields.List(fields.Nested(album_fields)),
    'top_songs':fields.List(fields.Nested(song_fields)),
    'new_uploads':fields.List(fields.Nested(song_fields)),
    'active':fields.Boolean,
    'follow':fields.Boolean,
    'streams':fields.Integer,
    'follower_len':fields.Integer,
    'profile_pic':fields.String
}

class ArtistApi(Resource):
    @marshal_with(artist_fields)
    @auth_required()
    def get(self,artist_id):
        option=request.args.get('option')
        if option==None:
            artist=User.query.get(artist_id)
            artist.top_songs=Songs.query.filter(Songs.singer==artist_id).order_by(Songs.total_rating.desc()).limit(7).all()
            artist.new_uploads=Songs.query.filter(Songs.singer==artist_id).order_by(Songs.timestamp.desc()).limit(7).all()
            artist.streams=0
            artist.follower_len=len(artist.followers)
            for song in artist.songs:
                artist.streams+=song.plays
            if current_user in artist.followers:
                artist.follow=True
            else:
                artist.follow=False    
            return artist,200
        else:
            artists=User.query.filter(User.roles.any(Role.name == 'creator')).all()
            return artists,200

         
api.add_resource(SongApi, '/api/song', '/api/update_song/<int:song_id>', '/api/delete_song/<int:song_id>')        
api.add_resource(AlbumApi, '/api/add_album/<int:song_id>/<int:album_id>','/api/album', '/api/delete_album/<int:album_id>')   
api.add_resource(PlaylistApi, '/api/add_playlist/<int:song_id>/<int:playlist_id>', '/api/playlist','/api/delete_playlist/<int:playlist_id>')
api.add_resource(ArtistApi, '/api/artist/<int:artist_id>')
