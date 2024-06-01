from celery import shared_task
from .models import *
from .mail_service import send_message
from datetime import datetime, timedelta
from jinja2 import Template
import os

base_dir = "/mnt/d/Mad2 Project/backend/templates"
creator_report_path = os.path.join(base_dir, "creator_report.html")


@shared_task(ignore_result=True)
def daily_reminder():
    users=User.query.all()
    current_date = datetime.now().date()
    for user in users:
        if user.current_login_at is not None:
            print(user.current_login_at)
            if user.current_login_at.date()!= current_date:
                   send_message(user.email, "Reminder", 'Daily reminder to visit Meloverse')
    return "Reminder sent!"


@shared_task(ignore_result=True)
def creator_report():
    # creators = User.query.join(User.roles).filter(Role.id == 2).all()
    # thirty_days_ago = datetime.now().date() - timedelta(days=30)
    # songs_added = []
    # songs_rating = []
    # songs_played = 0
    # for creator in creators:
    #     for song in creator.songs:
    #         if song.date_added.date() >= thirty_days_ago:
    #             songs_added.append(song)
    #             songs_rating.append(song.rating)
    #             songs_played += song.played
    #     rating = round((sum(songs_rating) / len(songs_rating)), 2)
    #     with open(creator_report_path, "r") as f:
    #         template = Template(f.read())
    #         send_message(
    #             creator.email,
    #             "Monthly Report",
    #             template.render(
    #                 creator=creator,
    #                 songs=songs_added,
    #                 rating=rating,
    #                 streams=songs_played,
    #             ),
    #         )
    # return "Report Sent"
    artists=User.query.filter(User.roles.any(Role.name=='creator')).all()
    one_month=datetime.now()-timedelta(weeks=4)
    songs=[]
    rating=0
    streams=0
    total_rating=0
    flags=0
    for artist in artists:
         for song in artist.songs:
              if song.timestamp>=one_month:
                   songs.append(song)
                   rating+=song.total_rating
                   streams+=song.plays
                   if song.flag==True:
                        flags+=1
         if rating!=0 and len(songs)!=0:
                total_rating=int(rating/len(songs))        
         with open(creator_report_path, "r") as f:
            template = Template(f.read())
            send_message(
                artist.email,
                "Monthly Report",
                template.render(
                    songs=songs,
                    average_rating=total_rating,
                    streams=streams,
                    flags=flags
                ),
            )
    return "Report Sent"                        
         