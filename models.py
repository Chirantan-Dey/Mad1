from app import db
from flask_login import UserMixin

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    login_details = db.relationship('Login', backref='admin', lazy=True)
    
    def __repr__(self):
        return f"<Admin {self.name}>"

class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    login_details = db.relationship('Login', backref='sponsor', lazy=True)
    campaigns = db.relationship('Campaign', backref='sponsor', lazy=True)
    ads = db.relationship('Ad', backref='sponsor', lazy=True)
    
    def __repr__(self):
        return f"<Sponsor {self.name}>"

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    niche = db.Column(db.String(100), nullable=False)
    total_followers = db.Column(db.Integer, nullable=False)
    active_followers = db.Column(db.Integer, nullable=False)
    flagged = db.Column(db.Boolean, default=False)
    login_details = db.relationship('Login', backref='influencer', lazy=True)
    ads = db.relationship('Ad', backref='influencer', lazy=True)
    
    def __repr__(self):
        return f"<Influencer {self.name}>"

class Ad(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    messages = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    def __repr__(self):
        return f"<Ad {self.id} - Campaign {self.campaign_id}>"

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(10), nullable=False)  # 'public' or 'private'
    goals = db.Column(db.Text, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'), nullable=False)
    ads = db.relationship('Ad', backref='campaign', lazy=True)
    
    def __repr__(self):
        return f"<Campaign {self.name}>"

class Login(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'))
    
    def __repr__(self):
        return f"<Login {self.username}>"
    
    def get_id(self):
        return self.id
