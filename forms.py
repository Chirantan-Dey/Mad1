from flask_wtf import *
from wtforms import *
from wtforms.validators import *
from datetime import *

class LoginForm(FlaskForm):
    user_type = RadioField('User Type', choices=[('admin', 'Admin'), ('sponsor', 'Sponsor'), ('influencer', 'Influencer')], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Next')

class AdminForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SponsorForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    industry = StringField('Industry', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    submit = SubmitField('Submit')

class InfluencerForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    niche = StringField('Niche', validators=[DataRequired()])
    total_followers = IntegerField('Total Followers', validators=[DataRequired()])
    active_followers = IntegerField('Active Followers', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CampaignForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%d-%m-%Y', validators=[DataRequired()])
    end_date = DateField('End Date', format='%d-%m-%Y', validators=[DataRequired()])
    budget = FloatField('Budget', validators=[DataRequired()])
    visibility = RadioField('Visibility', choices=[('public', 'Public'), ('private', 'Private')], validators=[DataRequired()])
    goals = TextAreaField('Goals', validators=[DataRequired()])
    submit = SubmitField('Create')

class AdRequestForm(FlaskForm):
    campaign_id = IntegerField('Campaign ID', validators=[DataRequired()])
    influencer_id = IntegerField('Influencer ID', validators=[DataRequired()])
    messages = TextAreaField('Messages', validators=[DataRequired()])
    requirements = TextAreaField('Requirements', validators=[DataRequired()])
    payment_amount = FloatField('Payment Amount', validators=[DataRequired()])
    status = StringField('Status', validators=[DataRequired()])
    submit = SubmitField('Create')

class PaymentForm(FlaskForm):
    card_number = StringField('Card Number', validators=[DataRequired()])
    expiration_date = StringField('Expiration Date', validators=[DataRequired()])
    cvv = StringField('CVV', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Pay')
