from app import app
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy(app)




from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'Admin', 'Sponsor', 'Influencer'
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    sponsor_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(100))
    budget = db.Column(db.Float)

class Influencer(db.Model):
    __tablename__ = 'influencers'
    influencer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    category = db.Column(db.String(100))
    niche = db.Column(db.String(100))
    reach = db.Column(db.Integer)

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    campaign_id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.sponsor_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(20), nullable=False)  # 'Public', 'Private'
    goals = db.Column(db.Text)

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    ad_request_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.campaign_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.influencer_id'), nullable=False)
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'Pending', 'Accepted', 'Rejected'

class FlaggedUser(db.Model):
    __tablename__ = 'flagged_users'
    flagged_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    flagged_by_admin_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

with app.app_context():
    db.create_all()