from app import app
from application.security_framework import datastore
from application.models import db,Role
from flask_security import hash_password
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

date=datetime.now()
with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name='admin', description='This is admin')
    datastore.find_or_create_role(name='user', description='This is User')
    datastore.find_or_create_role(name='creator', description='This is Creator') 
    db.session.commit()
    if not datastore.find_user(email='admin@email.com'):
        datastore.create_user(email='admin@email.com', user_name='admin',password=generate_password_hash('admin'), roles=["admin"])
    datastore.create_user(email='taylor@email.com', user_name='Taylor Swift', password=generate_password_hash('taylor'), roles=["creator"], timestamp=date-timedelta(days=2))
    datastore.create_user(email='louis@email.com', user_name='Louis Armstrong', password=generate_password_hash('louis'), roles=["creator"], timestamp=date-timedelta(days=3))
    datastore.create_user(email='kailash@email.com', user_name='Kailash Kher', password=generate_password_hash('kailash'), roles=["creator"], timestamp=date-timedelta(days=1))
    datastore.create_user(email='harry@email.com', user_name='Harry Styles', password=generate_password_hash('harry'), roles=["creator"], timestamp=date-timedelta(days=2))
    datastore.create_user(email='rashi@email.com', user_name='Rashika Kukreja', password=generate_password_hash('rashi'), roles=["user"], timestamp=date-timedelta(days=4))
    datastore.create_user(email='darsh@email.com', user_name='Darsh Kukreja', password=generate_password_hash('darsh'), roles=["user"], timestamp=date-timedelta(days=3))     
    db.session.commit()    
    