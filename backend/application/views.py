from flask import current_app as app, request, jsonify, render_template
from application.security_framework import datastore
from werkzeug.security import check_password_hash, generate_password_hash
from application.models import *
from flask_security import auth_required, roles_required
from flask_security import current_user, login_user,logout_user
from sqlalchemy import func,text
from datetime import datetime, timedelta
from .instances import cache
import os


@app.get('/')
def home():
    return render_template('index.html')

@app.post('/user-login')
def user_login():
    data=request.get_json()
    email=data.get('email')
    if not email:
        return jsonify({'message':'Email Not provided'}),400
    user=datastore.find_user(email=email)
    if not user:
        return jsonify({'message':'User not found'}), 404   
    if check_password_hash(user.password , data.get('password')):
        login_user(user)
        user.current_login_at=datetime.now()
        db.session.commit()
        if user.active==False:
            return {'message':'User is blacklisted due to violation of company policies'},400
        user_roles=[]
        for role in user.roles:
            user_roles.append(role.name)
        print(user_roles)    
        return jsonify({"token":user.get_auth_token(), "email":user.email, "role":user_roles, "id":user.id}),200
    else:
        return jsonify({'message':'Wrong password'}), 400
    
@app.post('/user-register')
def user_register():
    data=request.get_json()
    email=data.get('email')
    if not email:
        return jsonify({'message':'Email Not provided'}),400
    email_exists=datastore.find_user(email=email)
    if email_exists:
         return jsonify({'message':'Email already registered'}), 400
    datastore.create_user(email=email, user_name=data.get('user_name'), password=generate_password_hash(data.get('password')), roles=["user"])  
    db.session.commit()
    user=datastore.find_user(email=email)
    return jsonify({"email":user.email, "roles":user.roles[0].name, "id":user.id}),200 

@app.get('/logout')
@auth_required()
def logout():
    current_user.last_login_at=current_user.current_login_at
    db.session.commit()
    cache.clear()
    logout_user()
    return {'message':'User is Logged Out'},200

@app.route('/song/<int:id>', methods=['GET','POST'])
@auth_required()
@cache.cached(timeout=60)
def get_song(id):
    song=Songs.query.get(id)
    db.session.commit()
    if not song:
        return jsonify({'message':'Song not Found'}),404
    rating=Rating.query.filter_by(r_song_id=id,r_user_id=current_user.id).first()
    like_exists=Likes.query.filter_by(l_user_id=current_user.id,l_song_id=id).first()
    flag_exists=Flags.query.filter_by(f_user_id=current_user.id,f_song_id=id).first()
    if rating is None:
        rating_value=0
    else:
        rating_value=rating.rating
    if like_exists:
        like=True
    else:
        like=False 
    if flag_exists:
        flag=True
    else:
        flag=False            
    if current_user.id==song.singer:
        user_is_artist=True
    else:
        user_is_artist=False 
        song.plays=song.plays+1
        db.session.commit()    
    print(song.plays)  
    print(song.singer) 
    return jsonify({'song_id':song.song_id,'song_name':song.song_name, 'path':song.song_path, 'poster':song.poster, 'lyrics':song.lyrics,'album_id':song.album,'genre':song.genre, 'creator_id':song.singer, 'creator_name':song.song_by.user_name,'plays':song.plays, 'current_user_rating':rating_value, 'total_rating':song.total_rating, 'user_is_artist':user_is_artist,'like':like, 'flag':flag, 'admin_flag':song.flag}),200
    

@app.route('/rate_song/<int:id>', methods=['POST'])
@auth_required()
def rate_song(id):
    song=Songs.query.get(id)
    data=request.json
    rating_exists=Rating.query.filter_by(r_song_id=id,r_user_id=current_user.id).first()
    if rating_exists:
        if rating_exists.rating!=data.get('value'):
            rating_exists.rating=data.get('value')
        else:
            return jsonify({'total_rating':song.total_rating}),200 
    else:
        new_rating=Rating(r_song_id=id,r_user_id=current_user.id,rating=data.get('value')) 
        db.session.add(new_rating)     
    db.session.commit()
    song_rating=Rating.query.filter_by(r_song_id=id).all()
    raters=len(song_rating)
    amt_rating=0
    for rating in song_rating:
        amt_rating=amt_rating+rating.rating
    total_rating=amt_rating/raters 
    song.total_rating=int(total_rating) 
    db.session.commit()  
    return jsonify({'total_rating':song.total_rating}),200

@app.route('/like_song/<int:id>', methods=['GET'])
@auth_required()
def like_song(id):
    song=Songs.query.get(id)
    if current_user.id==song.singer:
        return jsonify({'message':'User is Artist'}),200
    like_exists=Likes.query.filter_by(l_user_id=current_user.id,l_song_id=id).first()
    if like_exists:
        db.session.delete(like_exists)
        db.session.commit() 
        return jsonify({'like':False}),200
    else:
        like=Likes(l_user_id=current_user.id,l_song_id=id)   
        db.session.add(like)
        db.session.commit() 
        return jsonify({'like':True}),200

@app.route('/flag_song/<int:id>', methods=['GET'])
@auth_required()
def flag_song(id):
    song=Songs.query.get(id)
    if current_user.id==song.singer:
        return jsonify({'message':'User is Artist'}),200
    flag_exists=Flags.query.filter_by(f_user_id=current_user.id,f_song_id=id).first()
    if flag_exists:
        db.session.delete(flag_exists)
        db.session.commit() 
        return jsonify({'flag':False}),200
    else:
        flag=Flags(f_user_id=current_user.id,f_song_id=id)   
        db.session.add(flag)
        db.session.commit() 
        return jsonify({'flag':True}),200        


@app.route('/all_albums', methods=['GET'])
@auth_required()
def creator_albums():
    albums=Album.query.all()
    all_albums=[]
    for album in albums:
        current_album={}
        current_album['album_id']=album.album_id
        current_album['album_name']=album.album_name
        current_album['artist']=album.owner.user_name
        current_album['flag']=album.flag
        current_album['songs']=[]
        for song in album.songs:
            current_song={}
            current_song={}
            current_song['song_id']=song.song_id
            current_song['song_name']=song.song_name
            current_song['song_singer']=song.song_by.user_name
            current_song['song_audio']=song.song_path
            current_song['song_poster']=song.poster
            current_song['rating']=song.total_rating
            current_song['flag']=song.flag
            current_song['genre']=song.genre
            current_album['songs'].append(current_song)
        all_albums.append(current_album) 
    return jsonify(all_albums),200

@app.route('/artist_songs', methods=['GET']) #for getting creator songs
@auth_required()
def artist_songs():
        user=User.query.get(current_user.id)
        artist_songs=[]
        i=1
        for song in user.songs:
            song_data={}
            song_data['song_id']=song.song_id
            song_data['song_name']=song.song_name
            song_data['album_id']=song.album
            song_data['streams']=song.plays
            song_data['flag']=song.flag
            artist_songs.append(song_data)
            i+=1
        return artist_songs, 200


@app.route('/top_songs', methods=['GET'])
@auth_required()
@cache.cached(timeout=60)
def top_songs():
     top_songs=Songs.query.order_by(Songs.total_rating.desc()).limit(7).all()
     top_song=[]
     i=1
     for song in top_songs:
         current_song={}
         current_song['song_id']=song.song_id
         current_song['song_name']=song.song_name
         current_song['song_singer']=song.song_by.user_name
         current_song['song_audio']=song.song_path
         current_song['song_poster']=song.poster
         current_song['rating']=song.total_rating
         current_song['genre']=song.genre
         current_song['flag']=song.flag
         if song.album is not None:
             album=Album.query.filter_by(album_id=song.album).first()
             current_song['album']=album.album_name
         else:
             current_song['album']='Single'  
         top_song.append(current_song)
         i+=1
     return top_song,200


@app.route('/recent_uploads', methods=['GET']) #caching
@auth_required()
@cache.cached(timeout=60)
def recent_uploads():
    recent_uploads=Songs.query.order_by(Songs.timestamp.desc()).limit(7).all()
    recent_songs=[]
    for song in recent_uploads:
         current_song={}
         current_song['song_id']=song.song_id
         current_song['song_name']=song.song_name
         current_song['song_singer']=song.song_by.user_name
         current_song['song_audio']=song.song_path
         current_song['song_poster']=song.poster
         current_song['rating']=song.total_rating
         current_song['genre']=song.genre
         current_song['flag']=song.flag
         if song.album is not None:
             album=Album.query.filter_by(album_id=song.album).first()
             current_song['album']=album.album_name
         else:
             current_song['album']='Single'  
         recent_songs.append(current_song)      
    return recent_songs,200


@app.route('/discover_artists',methods=['GET'])
@auth_required()
@cache.cached(timeout=60)
def discover_artists():
    artists=db.session.query(User).join(RolesUsers).join(Role).filter(Role.name=='creator').order_by(func.random()).limit(7).all()
    new_artists=[]
    for artist in artists:
        current_artist={}
        current_artist['id']=artist.id
        current_artist['name']=artist.user_name
        current_artist['active']=artist.active
        current_artist['no_songs']=len(artist.songs)
        current_artist['no_albums']=len(artist.albums)
        current_artist['profile']=artist.profile_pic
        new_artists.append(current_artist) 
    return new_artists,200    

@app.route('/album/<int:id>', methods=['GET']) #for users
@auth_required()
@cache.cached(timeout=60)
def album_page(id):
    album=Album.query.filter_by(album_id=id).first()
    current_album={}
    current_album['name']=album.album_name
    current_album['flag']=album.flag
    current_album['artist']=album.owner.user_name
    current_album['songs']=[]
    for song in album.songs:
          current_song={}
          current_song['song_id']=song.song_id
          current_song['song_name']=song.song_name
          current_song['song_singer']=song.song_by.user_name
          current_song['song_audio']=song.song_path
          current_song['song_poster']=song.poster
          current_song['rating']=song.total_rating
          current_song['genre']=song.genre
          current_song['flag']=song.flag
          current_album['songs'].append(current_song)
    return current_album,200     

@app.route('/all_artist_songs/<int:artist_id>', methods=['GET'])
@auth_required()
def all_artist_songs(artist_id):
    artist=User.query.get(artist_id) 
    artist_songs=[]
    for song in artist.songs:
        current_song={}
        current_song['song_id']=song.song_id
        current_song['song_name']=song.song_name
        current_song['song_singer']=song.song_by.user_name
        current_song['song_audio']=song.song_path
        current_song['song_poster']=song.poster
        current_song['rating']=song.total_rating
        current_song['genre']=song.genre
        if song.album is not None:
             album=Album.query.filter_by(album_id=song.album).first()
             current_song['album']=album.album_name
        else:
             current_song['album']='Single'  
        artist_songs.append(current_song)
    return artist_songs,200   

@app.route('/creator_details', methods=['GET'])
@auth_required() 
@roles_required('creator')
@cache.cached(timeout=60)
def creator_details():
    user=User.query.get(current_user.id)
    creator_det={}
    creator_det['id']=user.id
    creator_det['name']=user.user_name
    total_streams=0
    if len(user.songs)==0:
        creator_det['total_streams']=total_streams
    else:    
        for song in user.songs:
            total_streams=total_streams+song.plays
        creator_det['total_streams']=total_streams
    return creator_det,200

base_dir="/mnt/d/Mad2 Project/frontend/src"
upload_folder=os.path.join(base_dir, "assets")
profiles_folder=os.path.join(upload_folder,"profiles")

@app.route('/creator_signup', methods=['POST'])
@auth_required()
def creator_signup():
    profile_file=request.files['profile']
    profile_file.save(os.path.join(profiles_folder,profile_file.filename))
    current_user.profile_pic=profile_file.filename
    role_user=RolesUsers(user_id=current_user.id, role_id=3)
    db.session.add(role_user)
    role_user_exists=RolesUsers.query.filter_by(user_id=current_user.id, role_id=2).first()
    db.session.delete(role_user_exists)
    db.session.commit()
    return {'message':'Role Updated'},200

@app.route('/liked_songs', methods=['GET'])
@auth_required()
def liked_songs():
    user=User.query.get(current_user.id)
    liked_songs=[]
    for song in user.liked_songs:
        current_song={}
        current_song['song_id']=song.song_id
        current_song['song_name']=song.song_name
        current_song['song_singer']=song.song_by.user_name
        current_song['song_audio']=song.song_path
        current_song['song_poster']=song.poster
        current_song['rating']=song.total_rating
        current_song['genre']=song.genre
        current_song['flag']=song.flag
        if song.album is not None:
             album=Album.query.filter_by(album_id=song.album).first()
             current_song['album']=album.album_name
        else:
             current_song['album']='Single'  
        liked_songs.append(current_song)
    return liked_songs,200 

@app.route('/genre_songs', methods=['GET'])
@auth_required()
@roles_required('admin')
@cache.cached(timeout=60)
def genre_songs():
    songs=Songs.query.all()
    pop=Songs.query.filter_by(genre='Pop').all()
    jazz=Songs.query.filter_by(genre='Jazz').all()
    indie=Songs.query.filter_by(genre='Indie').all()
    dance=Songs.query.filter_by(genre='Dance/Electronic_Music').all()
    classical=Songs.query.filter_by(genre='Classical_Music').all()
    soul=Songs.query.filter_by(genre='Soul').all()
    randb=Songs.query.filter_by(genre='R&B').all()
    country=Songs.query.filter_by(genre='Country_Music').all()
    genre_songs={}
    genre_songs['pop']=len(pop)
    genre_songs['jazz']=len(jazz)
    genre_songs['indie']=len(indie)
    genre_songs['dance']=len(dance)
    genre_songs['classical']=len(classical)
    genre_songs['soul']=len(soul)
    genre_songs['randb']=len(randb)
    genre_songs['country']=len(country)
    return genre_songs,200

@app.route('/uploads', methods=['GET'])
@auth_required()
@roles_required('admin')
def uploads():
    option=request.args.get('option')
    if option=='users':
            one_week=datetime.now()-timedelta(weeks=1)
            users=User.query.filter(User.timestamp>=one_week).all()
            dates={}
            dates_changed={}
            current_date=one_week
            today=datetime.now()
            while current_date <= today:
                dates[current_date.date()]=0
                current_date += timedelta(days=1)
            for user in users:
                dates[user.timestamp.date()]+=1    
            for date in dates:
                 changed_date=date.strftime('%Y-%m-%d')
                 dates_changed[changed_date]=dates[date]   
            return dates_changed,200   
    elif option=='songs':
            one_week=datetime.now()-timedelta(weeks=1)
            songs=Songs.query.filter(Songs.timestamp>=one_week).all()
            dates={}
            dates_changed={}
            current_date=one_week
            today=datetime.now()
            while current_date <= today:
                dates[current_date.date()]=0
                current_date += timedelta(days=1)
            for song in songs:
                dates[song.timestamp.date()]+=1    
            for date in dates:
                 changed_date=date.strftime('%Y-%m-%d')
                 dates_changed[changed_date]=dates[date] 
                 print(dates_changed)  
            return dates_changed,200  
    if option=='creators':
            one_week=datetime.now()-timedelta(weeks=1)
            users=User.query.filter(User.timestamp>=one_week,User.roles.any(Role.name == 'creator')).all()
            print(users)
            dates={}
            dates_changed={}
            current_date=one_week
            today=datetime.now()
            while current_date <= today:
                dates[current_date.date()]=0
                current_date += timedelta(days=1)
            for user in users:
                dates[user.timestamp.date()]+=1    
            for date in dates:
                 changed_date=date.strftime('%Y-%m-%d')
                 dates_changed[changed_date]=dates[date]   
            return dates_changed,200 
    else:
        return {'message':'Bad Request'},400

@app.route('/admin_flag/<int:id>', methods=['GET'])
@auth_required()
@roles_required('admin')
def a_flag(id):
    option=request.args.get('option')
    if option=='song':
        song=Songs.query.get(id)
        if song.flag==True:
           song.flag=False
        else:
            song.flag=True   
        db.session.commit()    
        return {'song_flag':song.flag},200
    if option=='artist':
        user=User.query.get(id)
        if user.active==True:
           user.active=False
        else:
            user.active=True   
        db.session.commit()    
        return {'user_active':user.active},200 
    if option=='album':
        album=Album.query.get(id)
        if album.flag==True:
           album.flag=False
        else:
            album.flag=True   
        db.session.commit()    
        return {'album_flag':album.flag},200  
    
@app.route('/get_numbers', methods=['GET'])
@auth_required()
@roles_required('admin')
@cache.cached(timeout=60)
def get_number():
    users=User.query.all()    
    songs=Songs.query.all()
    albums=Album.query.all()
    artists=User.query.filter(User.roles.any(Role.name=='creator')).all()
    numbers={}
    numbers['users']=len(users)
    numbers['songs']=len(songs)
    numbers['albums']=len(albums)
    numbers['artists']=len(artists)
    return numbers,200

@app.route('/follow_artist/<int:id>', methods=['GET'])
@auth_required()
def follow_artist(id):
    artist=User.query.get(id)
    if current_user.id==artist.id:
        return jsonify({'message':'User is Artist'}),200
    follow_exists=Followers.query.filter_by(follower_id=current_user.id,followee_id=artist.id).first()
    if follow_exists:
        db.session.delete(follow_exists)
        db.session.commit() 
        return jsonify({'follow':False}),200
    else:
        follow=Followers(follower_id=current_user.id,followee_id=artist.id)   
        db.session.add(follow)
        db.session.commit() 
        return jsonify({'follow':True}),200    
    
@app.route('/followed_artists', methods=['GET'])  
@auth_required()
def followed_artists():
    followed_artists=[]
    for artist in current_user.follows:
        current_artist={}
        current_artist['name']=artist.user_name
        current_artist['id']=artist.id
        current_artist['songs']=len(artist.songs)
        current_artist['albums']=len(artist.albums)
        current_artist['active']=artist.active
        followed_artists.append(current_artist)
    return followed_artists,200  

@app.route('/songs_by_genres/<genre>', methods=['GET'])
@auth_required()
@cache.cached(timeout=60)
def songs_by_genres(genre):
    songs=Songs.query.filter_by(genre=genre).all()
    genre_songs=[]
    for song in songs:
        current_song={}
        current_song['song_id']=song.song_id
        current_song['song_name']=song.song_name
        current_song['song_singer']=song.song_by.user_name
        current_song['audio']=song.song_path
        current_song['poster']=song.poster
        current_song['rating']=song.total_rating
        current_song['genre']=song.genre
        current_song['flag']=song.flag
        if song.album is not None:
             album=Album.query.filter_by(album_id=song.album).first()
             current_song['album']=album.album_name
        else:
             current_song['album']='Single'  
        genre_songs.append(current_song)
    return genre_songs,200    
        
           
              

        
           
