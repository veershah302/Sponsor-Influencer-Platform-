from app import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
db=SQLAlchemy(app)




from datetime import datetime



from flask_sqlalchemy import SQLAlchemy


def generate_sponsor_id():
    last_sponsor = Sponsor.query.order_by(Sponsor.sponsor_id.desc()).first()
    if last_sponsor:
        last_id = int(last_sponsor.sponsor_id.replace("SP", ""))
        new_id = f"SP{last_id + 1}"
    else:
        new_id = "SP1"
    return new_id

def generate_influencer_id():
    last_influencer = Influencer.query.order_by(Influencer.influencer_id.desc()).first()
    if last_influencer:
        last_id = int(last_influencer.influencer_id.replace("INF", ""))
        new_id = f"INF{last_id + 1}"
    else:
        new_id = "INF1"
    return new_id

def generate_admin_id():
    last_admin = Admin.query.order_by(Admin.admin_id.desc()).first()
    if last_admin:
        last_id = int(last_admin.admin_id.replace("AD", ""))
        new_id = f"AD{last_id + 1}"
    else:
        new_id = "AD1"
    return new_id


class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.String(100), primary_key=True,default=generate_admin_id)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pass_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(120), unique=True)

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    sponsor_id = db.Column(db.String(100), primary_key=True, default=generate_sponsor_id)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pass_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    company_name = db.Column(db.String(100),nullable=False)
    industry = db.Column(db.String(100),nullable=False)
    budget = db.Column(db.Float)

class Influencer(db.Model):
    __tablename__ = 'influencers'
    influencer_id = db.Column(db.String(100), primary_key=True, default=generate_influencer_id)
    username = db.Column(db.String(80), unique=True, nullable=False)
    pass_hash = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(100),nullable=False)
    niche = db.Column(db.String(100),nullable=False)
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
    sponsor_id = db.Column(db.String(100), db.ForeignKey('sponsors.sponsor_id'), nullable=False)
    influencer_id = db.Column(db.String(100), db.ForeignKey('influencers.influencer_id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'Pending', 'Accepted', 'Rejected'
    acceptedamount = db.Column(db.Float, nullable=True)
    requirements=db.Column(db.Text)
    


class CampaignMessage(db.Model):
    __tablename__ = 'campaignmessages'
    cmessage_id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('ad_requests.ad_request_id'), nullable=False)
    sender_id = db.Column(db.String(100), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # 'Sponsor', 'Influencer'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Message(db.Model):
    __tablename__ = 'messages'
    message_id = db.Column(db.Integer, primary_key=True)
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_requests.ad_request_id'), nullable=False)
    sender_id = db.Column(db.String(100), nullable=False)
    sender_type = db.Column(db.String(20), nullable=False)  # 'Sponsor', 'Influencer'
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Negotiation(db.Model):
    __tablename__ = 'negotiations'
    negotiation_id = db.Column(db.Integer, primary_key=True)
    ad_request_id = db.Column(db.Integer, db.ForeignKey('ad_requests.ad_request_id'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.sponsor_id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.influencer_id'), nullable=False)
    sponsor_negotiation_amount = db.Column(db.Float, nullable=True)
    influencer_negotiation_amount = db.Column(db.Float, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)






class FlaggedUser(db.Model):
    __tablename__ = 'flagged_users'
    flagged_user_id = db.Column(db.Integer, nullable=False)
    flagged_user_type = db.Column(db.String(20), nullable=False)  # 'Sponsor', 'Influencer'
    flagged_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

# Initialize the database
with app.app_context():
    db.create_all()


    
    admin = Admin.query.first()
    if not admin:
        password_hash = generate_password_hash('1234')
        admin = Admin(username='admin', pass_hash=password_hash, name='Admin')
        db.session.add(admin)
        db.session.commit()

    


