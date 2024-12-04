from flask import *
from models import db, Admin, Sponsor, Influencer, Ad, Campaign, Login
from forms import *
from flask_login import *
# from plotly import *
import plotly.graph_objs as go
from plotly.subplots import *

import os

def register_routes(app,db,bcrypt):
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            logout_user()
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        login_form = LoginForm()
        user_type = ''
        if request.method == 'POST':
            user_type = login_form.user_type.data
            username = login_form.username.data
            password = login_form.password.data
            if user_type == 'admin':
                return redirect(url_for('admin_register'))
            elif user_type == 'sponsor':
                return redirect(url_for('sponsor_register'))
            elif user_type == 'influencer':
                return redirect(url_for('influencer_register'))
        return render_template('register.html', login_form=login_form,user_type=user_type)

    @app.route('/register/admin', methods=['GET', 'POST'])
    def admin_register():
        username = request.args.get('username')
        password = request.args.get('password')
        
        form = AdminForm(username=username, password=password)
        login_form = LoginForm()
        if form.validate_on_submit():
            admin = Admin(name=form.name.data)
            db.session.add(admin)
            db.session.commit()
            password=login_form.password.data
            hashed_password=bcrypt.generate_password_hash(password)
            login = Login(user='admin', username=login_form.username.data.upper(), password=hashed_password, admin_id=admin.id)
            db.session.add(login)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('admin_register.html', form=form,login_form=login_form)

    @app.route('/register/sponsor', methods=['GET', 'POST'])
    def sponsor_register():
        username = request.args.get('username')
        password = request.args.get('password')
        form = SponsorForm(username=username, password=password)
        login_form = LoginForm()
        if form.validate_on_submit():
            sponsor = Sponsor(name=form.name.data, industry=form.industry.data, budget=form.budget.data)
            db.session.add(sponsor)
            db.session.commit()
            password=login_form.password.data
            hashed_password=bcrypt.generate_password_hash(password)
            login = Login(user='sponsor', username=login_form.username.data, password=hashed_password, sponsor_id=sponsor.id)
            db.session.add(login)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('sponsor_register.html', form=form,login_form=login_form)

    @app.route('/register/influencer', methods=['GET', 'POST'])
    def influencer_register():
        username = request.args.get('username')
        password = request.args.get('password')
        form = InfluencerForm(username=username, password=password)
        login_form = LoginForm()
        if form.validate_on_submit():
            influencer = Influencer(name=form.name.data, category=form.category.data, niche=form.niche.data, total_followers=form.total_followers.data, active_followers=form.active_followers.data)
            db.session.add(influencer)
            db.session.commit()
            password=login_form.password.data
            hashed_password=bcrypt.generate_password_hash(password)
            login = Login(user='influencer', username=login_form.username.data, password=hashed_password, influencer_id=influencer.id)
            db.session.add(login)
            db.session.commit()
            return redirect(url_for('index'))
        return render_template('influencer_register.html', form=form,login_form=login_form)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user_type = login_form.user_type.data
            username = login_form.username.data
            password = login_form.password.data
            
            
            user = Login.query.filter_by(username=username, user=user_type).first()
            if user and bcrypt.check_password_hash(user.password,password):
                if user_type == 'sponsor':
                    sponsor = Sponsor.query.get(user.sponsor_id)
                    if sponsor.flagged:
                        flash('Your account has been flagged. Please contact support.', 'danger')
                        return redirect(url_for('login'))
                elif user_type == 'influencer':
                    influencer = Influencer.query.get(user.influencer_id)
                    if influencer.flagged:
                        flash('Your account has been flagged. Please contact support.', 'danger')
                        return redirect(url_for('login'))
                login_user(user)
                # Successful login
                flash('Login successful!', 'success')
                if user_type == 'admin':
                    # Redirect to admin dashboard or profile
                    return redirect(url_for('admin_dashboard'))
                elif user_type == 'sponsor':
                    # Redirect to sponsor dashboard or profile
                    return redirect(url_for('sponsor_dashboard'))
                elif user_type == 'influencer':
                    # Redirect to influencer dashboard or profile
                    return redirect(url_for('influencer_dashboard'))
            else:
                # Incorrect username or password
                flash('Invalid username or password. Please try again.', 'danger')
        
        return render_template('login.html', login_form=login_form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    
    
    @app.route('/admin/dashboard')
    @login_required

    def admin_dashboard():
        # Fetch data
        total_sponsors = Sponsor.query.count()
        total_influencers = Influencer.query.count()
        total_users = {'sponsors': total_sponsors, 'influencers': total_influencers}

        
        influencer_data = []
        campaigns = Campaign.query.all()
        public_campaigns = len(Campaign.query.filter_by(visibility='public').all())
        private_campaigns = len(Campaign.query.filter_by(visibility='private').all())
        for campaign in campaigns:
            ads = Ad.query.filter_by(campaign_id=campaign.id).all()
            influencers = {}
            for ad in ads:
                influencer = Influencer.query.get(ad.influencer_id)
                if influencer.id not in influencers:
                    influencers[influencer.id] = {
                        'influencer': influencer,
                        'ads': []
                    }
                influencers[influencer.id]['ads'].append(ad)
        
            campaign_influencers = []
            for influencer_id, data in influencers.items():
                campaign_influencers.append(data)
            
            influencer_data.append({
                'campaign': campaign,
                'influencers': campaign_influencers
            })
                
        

        ad_statuses = db.session.query(Ad.status, db.func.count(Ad.id)).group_by(Ad.status).all()
        ad_labels = [status for status, count in ad_statuses]
        ad_values = [count for status, count in ad_statuses]

        
        flagged_sponsors = Sponsor.query.filter_by(flagged=True).count()
        unflagged_sponsors = total_sponsors - flagged_sponsors
        flagged_influencers = Influencer.query.filter_by(flagged=True).count()
        unflagged_influencers = total_influencers - flagged_influencers

        # Generate charts
        users_pie = go.Figure(data=[go.Pie(
            labels=['Sponsors', 'Influencers'],
            values=[total_sponsors, total_influencers],
            marker=dict(colors=['#36A2EB', '#FFCE56']),
            textinfo='label+percent+value'
        )])
        users_pie.update_layout(template="plotly_dark", title='Users')

        campaigns_pie = go.Figure(data=[go.Pie(
            labels=['Public Campaigns', 'Private Campaigns'],
            values=[public_campaigns, private_campaigns],
            marker=dict(colors=['#4BC0C0', '#F7464A']),
            textinfo='label+percent+value'
        )])
        campaigns_pie.update_layout(template="plotly_dark", title='Campaigns')

        ads_pie = go.Figure(data=[go.Pie(
            labels=ad_labels,
            values=ad_values,
            marker=dict(colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#F7464A']),
            textinfo='label+percent+value'
        )])
        ads_pie.update_layout(template="plotly_dark", title='Ads')

        flagged_users_pie = go.Figure(data=[go.Pie(
            labels=['Flagged Sponsors', 'Flagged Influencers'],
            values=[flagged_sponsors, flagged_influencers],
            marker=dict(colors=['#FF6384', '#36A2EB']),
            textinfo='label+percent+value'
        )])
        flagged_users_pie.update_layout(template="plotly_dark", title='Flagged Users')

        flagged_vs_unflagged_sponsors = go.Figure(data=[go.Pie(
            labels=['Flagged Sponsors', 'Unflagged Sponsors'],
            values=[flagged_sponsors, unflagged_sponsors],
            marker=dict(colors=['#FF6384', '#36A2EB']),
            textinfo='label+percent+value'
        )])
        flagged_vs_unflagged_sponsors.update_layout(template="plotly_dark", title='Flagged vs Unflagged Sponsors')

        flagged_vs_unflagged_influencers = go.Figure(data=[go.Pie(
            labels=['Flagged Influencers', 'Unflagged Influencers'],
            values=[flagged_influencers, unflagged_influencers],
            marker=dict(colors=['#FF6384', '#36A2EB']),            
            textinfo='label+percent+value'
        )])
        flagged_vs_unflagged_influencers.update_layout(template="plotly_dark", title='Flagged vs Unflagged Influencers')

        # Save charts as images
        if not os.path.exists(os.path.join(app.root_path, 'static', 'charts')):
            os.makedirs(os.path.join(app.root_path, 'static', 'charts'))

        users_pie.write_image(os.path.join(app.root_path, 'static', 'charts', 'users_pie.png'))
        campaigns_pie.write_image(os.path.join(app.root_path, 'static', 'charts', 'campaigns_pie.png'))
        ads_pie.write_image(os.path.join(app.root_path, 'static', 'charts', 'ads_pie.png'))
        flagged_users_pie.write_image(os.path.join(app.root_path, 'static', 'charts', 'flagged_users_pie.png'))
        flagged_vs_unflagged_sponsors.write_image(os.path.join(app.root_path, 'static', 'charts', 'flagged_vs_unflagged_sponsors.png'))
        flagged_vs_unflagged_influencers.write_image(os.path.join(app.root_path, 'static', 'charts', 'flagged_vs_unflagged_influencers.png'))


        return render_template(
            'admin_dashboard.html',
            total_users=total_users,
            admins=Admin.query.all(),
            sponsors=Sponsor.query.all(),
            influencers=Influencer.query.all(),
            campaigns=campaigns,
            influencer_data = influencer_data,
            public_campaigns=public_campaigns,
            private_campaigns=private_campaigns,
            ads=Ad.query.all(),
            ad_statuses=dict(ad_statuses),
            flagged_sponsors=flagged_sponsors,
            flagged_influencers=flagged_influencers,
            users_chart_path=url_for('static', filename='charts/users_pie.png'),
            campaigns_chart_path=url_for('static', filename='charts/campaigns_pie.png'),
            ads_chart_path=url_for('static', filename='charts/ads_pie.png'),
            flagged_users_chart_path=url_for('static', filename='charts/flagged_users_pie.png'),
            flagged_vs_unflagged_sponsors_chart_path=url_for('static', filename='charts/flagged_vs_unflagged_sponsors.png'),
            flagged_vs_unflagged_influencers_chart_path=url_for('static', filename='charts/flagged_vs_unflagged_influencers.png')    
        )

    @app.route('/flag_sponsor/<int:sponsor_id>', methods=['POST'])
    def flag_sponsor(sponsor_id):
        sponsor = Sponsor.query.get_or_404(sponsor_id)
        sponsor.flagged = not sponsor.flagged
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    @app.route('/flag_influencer/<int:influencer_id>', methods=['POST'])
    def flag_influencer(influencer_id):
        influencer = Influencer.query.get_or_404(influencer_id)
        influencer.flagged = not influencer.flagged
        db.session.commit()
        return redirect(url_for('admin_dashboard'))

    

    @app.route('/influencer/dashboard', methods=['GET', 'POST'])
    @login_required
    def influencer_dashboard():
        influencer = db.session.query(Influencer).join(Login).filter(Login.id == current_user.id).first_or_404()
        if request.method == 'POST':
            if 'update_profile' in request.form:
                influencer.name = request.form.get('name', influencer.name)
                influencer.category = request.form.get('category', influencer.category)
                influencer.total_followers = request.form.get('total_followers', influencer.total_followers)
                influencer.active_followers = request.form.get('active_followers', influencer.active_followers)
                influencer.niche = request.form.get('niche', influencer.niche)
                db.session.commit()
                flash('Profile updated successfully!')
        search_query = request.form.get('search_query')
        search_filter = request.form.get('search_filter')

        if search_query:
            
            if search_filter == 'budget':
                campaigns_search = Campaign.query.filter(Campaign.budget >= float(search_query)).all()
            elif search_filter == 'goals':
                campaigns_search = Campaign.query.filter(Campaign.goals.ilike(f"%{search_query}%")).all()
        else:
            campaigns_search = ""

        influencer_data = []
        campaigns = Campaign.query.join(Ad).filter(Ad.influencer_id == influencer.id, Campaign.visibility == 'public').all()        
        campaigns_with_ads = []
        for campaign in campaigns:
            ads = Ad.query.filter_by(campaign_id=campaign.id, influencer_id=influencer.id).all()
            for ad in ads:
                ad.sponsor = Sponsor.query.get(ad.sponsor_id)
            campaigns_with_ads.append({
                'campaign': campaign,
                'ads': ads
            })

        influencer_data.append({
            'influencer': influencer,
            'campaigns_with_ads': campaigns_with_ads
        })

        
        edit_mode = request.args.get('edit_mode', 'False') == 'True'
        ad_id = request.args.get('ad_id')

        return render_template(
            'influencer_dashboard.html',
            campaigns_search=campaigns_search,
            influencers=influencer,
            influencer_data=influencer_data,
            edit_mode=edit_mode,
            ad_id=ad_id,
            
        )
    
    @app.route('/ad_status/<int:ad_id>', methods=['POST'])
    def ad_status(ad_id):
        ad = Ad.query.get_or_404(ad_id)
        ad.status = request.form.get('ad')
        db.session.commit()
        return redirect(url_for('influencer_dashboard'))
    
    @app.route('/influencer/negotiate/<int:ad_id>', methods=['POST'])
    
    def negotiate(ad_id):
        action = request.form.get('action')
        if action == 'negotiate':
            return redirect(url_for('influencer_dashboard', edit_mode=True, ad_id=ad_id))
        elif action == 'submit':
            ad = Ad.query.get_or_404(ad_id)
            ad.payment_amount = request.form.get('amt')
            ad.status = "Negotiated"
            db.session.commit()
            return redirect(url_for('influencer_dashboard', edit_mode=False))
        return redirect(url_for('influencer_dashboard', edit_mode=False))
    
    @app.route('/sponsor_dashboard', methods=['GET', 'POST'])
    @login_required
    def sponsor_dashboard():
        sponsor = db.session.query(Sponsor).join(Login).filter(Login.id == current_user.id).first_or_404()
        if request.method == 'POST':
            if 'update_profile' in request.form:
                sponsor.name = request.form.get('name', sponsor.name)
                sponsor.industry = request.form.get('industry', sponsor.industry)
                sponsor.budget = request.form.get('budget', sponsor.budget)
                
                db.session.commit()
                flash('Profile updated successfully!')

        
        search_query = request.form.get('search_query')
        search_filter = request.form.get('search_filter')

        if search_query:
            if search_filter == 'name':
                influencers = Influencer.query.filter(Influencer.name.ilike(f"%{search_query}%")).all()
            elif search_filter == 'category':
                influencers = Influencer.query.filter(Influencer.category.ilike(f"%{search_query}%")).all()
            elif search_filter == 'total_followers':
                influencers = Influencer.query.filter(Influencer.total_followers >= int(search_query)).all()
            elif search_filter == 'active_followers':
                influencers = Influencer.query.filter(Influencer.active_followers >= int(search_query)).all()
        else:
            influencers = ""
        campaigns =Campaign.query.filter(Campaign.sponsor_id == Sponsor.id).all()
        influencer_data=Influencer.query.all()        

        return render_template('sponsor_dashboard.html', influencers=influencers, campaigns=campaigns, sponsor=sponsor, influencer_data=influencer_data)
    
    @app.route('/create_campaign', methods=['POST'])
    def create_campaign():  
            
        name = request.form.get('name')
        description = request.form.get('description')
        start_date_raw = request.form.get('start_date')
        end_date_raw = request.form.get('end_date')        
        start_date = datetime.strptime(start_date_raw, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_raw, '%Y-%m-%d').date()
        budget = request.form.get('budget')
        visibility = request.form.get('visibility')
        goals = request.form.get('goals')
        sponsor = db.session.query(Sponsor).join(Login).filter(Login.id == current_user.id).first_or_404()
        sponsor_id = sponsor.id
        new_campaign = Campaign(name=name,description=description, start_date=start_date, end_date=end_date, budget=budget, visibility=visibility, goals=goals,sponsor_id=sponsor_id)
        db.session.add(new_campaign)
        db.session.commit()
        flash('Campaign created successfully!')
        return redirect(url_for('sponsor_dashboard'))

    @app.route('/update_campaign/<int:campaign_id>', methods=['POST'])
    def update_campaign(campaign_id):
        campaign = Campaign.query.get(campaign_id)
        campaign.name = request.form['name']
        campaign.description = request.form['description']
        campaign.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        campaign.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        campaign.budget = request.form['budget']
        db.session.commit()
        flash('Campaign updated successfully!')
        return redirect(url_for('sponsor_dashboard'))

    @app.route('/delete_campaign/<int:campaign_id>', methods=['POST'])
    def delete_campaign(campaign_id):
        campaign = Campaign.query.get(campaign_id)
        db.session.delete(campaign)
        db.session.commit()
        flash('Campaign deleted successfully!')
        return redirect(url_for('sponsor_dashboard'))

    @app.route('/create_ad_request/<int:campaign_id>', methods=['POST'])
    def create_ad_request(campaign_id):
        influencer_id = int(request.form.get('influencer_id', ''))
        messages= request.form.get('messages', '')
        requirements = request.form.get('requirements', '')
        payment_amount = request.form.get('payment_amount', '0')
        status = 'Pending'
        campaign = Campaign.query.get_or_404(campaign_id)
        sponsor_id = campaign.sponsor_id
        new_ad = Ad(campaign_id=campaign_id, influencer_id=influencer_id, messages=messages, requirements=requirements, payment_amount=payment_amount, status=status,sponsor_id=sponsor_id)
        db.session.add(new_ad)
        db.session.commit()
        flash('Ad request created successfully!')
        return redirect(url_for('sponsor_dashboard'))

    @app.route('/update_ad_request/<int:ad_id>', methods=['POST'])
    def update_ad_request(ad_id):
        ad = Ad.query.get(ad_id)
        ad.influencer_id = int(request.form['influencer_id'])
        ad.requirements = request.form['requirements']
        ad.payment_amount = request.form['payment_amount']
        ad.status = 'Pending'
        db.session.commit()
        flash('Ad request updated successfully!')
        return redirect(url_for('sponsor_dashboard'))

    @app.route('/delete_ad_request/<int:ad_id>', methods=['POST'])
    def delete_ad_request(ad_id):
        ad = Ad.query.get(ad_id)
        db.session.delete(ad)
        db.session.commit()
        flash('Ad request deleted successfully!')
        return redirect(url_for('sponsor_dashboard'))
    