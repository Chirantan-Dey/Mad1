import os
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from models import Admin, Sponsor, Influencer, Ad, Campaign, Login

# Initialize the Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = '8f42a73054b1749f8f58848be5e6502c'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

def create_sample_data():
    # Create sample Admins
    admin1 = Admin(name='Alice')
    admin2 = Admin(name='Bob')

    # Create sample Sponsors
    sponsor1 = Sponsor(name='TechCorp', industry='Technology', budget=1000000, flagged=False)
    sponsor2 = Sponsor(name='HealthPlus', industry='Healthcare', budget=500000, flagged=True)

    # Create sample Influencers
    influencer1 = Influencer(name='John Doe', category='Fitness', niche='Bodybuilding', total_followers=500000, active_followers=450000, flagged=False)
    influencer2 = Influencer(name='Jane Smith', category='Lifestyle', niche='Minimalism', total_followers=200000, active_followers=190000, flagged=True)

    # Create sample Campaigns
    campaign1 = Campaign(name='Summer Tech Launch', description='Launch of new tech gadgets for summer', start_date=date(2024, 6, 1), end_date=date(2024, 9, 1), budget=200000, visibility='public', goals='Increase brand awareness')
    campaign2 = Campaign(name='Healthy Living Campaign', description='Promoting healthy lifestyle products', start_date=date(2024, 1, 1), end_date=date(2024, 12, 31), budget=300000, visibility='private', goals='Boost product sales')

    # Create sample Ads
    ad1 = Ad(campaign=campaign1, influencer=influencer1, messages='Promote our new fitness tracker.', requirements='Include a swipe-up link.', payment_amount=5000, status='Pending')
    ad2 = Ad(campaign=campaign2, influencer=influencer2, messages='Share your daily routine using our products.', requirements='Mention the discount code.', payment_amount=3000, status='Approved')
    ad3 = Ad(campaign=campaign1, influencer=influencer2, messages='Highlight the tech features.', requirements='Show the product in use.', payment_amount=4000, status='Completed')

    # Create sample Logins with hashed passwords
    login1 = Login(user='admin', username='alice_admin', password=bcrypt.generate_password_hash('password123').decode('utf-8'), admin=admin1)
    login2 = Login(user='sponsor', username='techcorp_sponsor', password=bcrypt.generate_password_hash('password123').decode('utf-8'), sponsor=sponsor1)
    login3 = Login(user='influencer', username='john_influencer', password=bcrypt.generate_password_hash('password123').decode('utf-8'), influencer=influencer1)
    login4 = Login(user='admin', username='bob_admin', password=bcrypt.generate_password_hash('password456').decode('utf-8'), admin=admin2)
    login5 = Login(user='sponsor', username='healthplus_sponsor', password=bcrypt.generate_password_hash('password456').decode('utf-8'), sponsor=sponsor2)
    login6 = Login(user='influencer', username='jane_influencer', password=bcrypt.generate_password_hash('password456').decode('utf-8'), influencer=influencer2)

    # Add sample data to session
    db.session.add(admin1)
    db.session.add(admin2)
    db.session.add(sponsor1)
    db.session.add(sponsor2)
    db.session.add(influencer1)
    db.session.add(influencer2)
    db.session.add(campaign1)
    db.session.add(campaign2)
    db.session.add(ad1)
    db.session.add(ad2)
    db.session.add(ad3)
    db.session.add(login1)
    db.session.add(login2)
    db.session.add(login3)
    db.session.add(login4)
    db.session.add(login5)
    db.session.add(login6)

    # Commit session to save data to the database
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_sample_data()
        print("Sample data created successfully.")
