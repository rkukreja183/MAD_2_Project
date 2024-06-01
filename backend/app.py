import os
from flask import Flask
from flask_security import Security,SQLAlchemyUserDatastore,login_required
from config import LocalDev
from application.models import *
from application.resources import api
from application.security_framework import datastore
from flask_cors import CORS
from application.instances import cache
from celery.schedules import crontab
from application.tasks import daily_reminder, creator_report
from application.worker import celery_init_app

app=None
def create_app():
    app=Flask(__name__)
    app.config.from_object(LocalDev)
    db.init_app(app)
    api.init_app(app)
    cache.init_app(app)
    with app.app_context():
        import application.views
    app.app_context().push()
    security=Security(app, datastore)
    return app

app=create_app()
CORS(app)
celery_app=celery_init_app(app)

@celery_app.on_after_configure.connect
def send_email(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/1'),
        daily_reminder.s(),
    )
    sender.add_periodic_task(
        crontab(minute='*/1'),
        creator_report.s(),
    )



if __name__=='__main__':
    app.run(debug=True)