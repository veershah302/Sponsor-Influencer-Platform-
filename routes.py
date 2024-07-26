from app import app
from flask import render_template,request,url_for,flash,redirect,session

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import Sponsor,db,Influencer,Admin,Campaign,AdRequest,Message

import datetime
#----
#decorator for authorisation
def auth_required_sponsor(func):
    @wraps(func)
    def inner(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id and user_id.startswith('SP'):
            return func(*args, **kwargs)
        else:
            flash('Please login as an sponsor to continue')
            return redirect(url_for('sponsorlogin'))
    return inner
    
def auth_required_influencer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id and user_id.startswith('INF'):
            return func(*args, **kwargs)
        else:
            flash('Please login as an influencer to continue')
            return redirect(url_for('influencerlogin'))
    return inner

    
def auth_required_admin(func):
    @wraps(func)
    def inner(*args, **kwargs):
        user_id = session.get('user_id')
        if user_id and user_id.startswith('AD'):
            return func(*args, **kwargs)
        else:
            flash('Please login as an admin to continue')
            return redirect(url_for('adminlogin'))
    return inner

def auth_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Please login to continue')
            return redirect(url_for('login'))
    return inner




@app.route("/")
@auth_required
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("registerseparator.html")

@app.route("/login")
def login():
    return render_template("loginseparator.html")

@app.route("/sponsorregister")
def sponsorregister():
    return render_template("register_sponsor.html")

@app.route("/influencerregister")
def influencerregister():
    return render_template("register_influencer.html")

@app.route("/sponsorlogin")
def sponsorlogin():
    return render_template("login_sponsor.html")


@app.route("/influencerlogin")
def influencerlogin():
    return render_template("login_influencer.html")





@app.route("/sponsorregister", methods=["post"])

def sponsorregister_post():
    username=request.form.get("username")
    password=request.form.get("password")
    confirmpassword=request.form.get("confirmpassword")
    name=request.form.get("name")
    email=request.form.get("email")
    company_name=request.form.get("company_name")
    industry=request.form.get("industry")
    budget=request.form.get("budget")

    if not (username and password and confirmpassword and company_name and budget):
        flash("Fill out all the required details")
        return redirect(url_for("sponsorregister"))
    if password!=confirmpassword:
        flash("Password and confirm password do not match")
        return redirect(url_for("sponsorregister"))
    
    user = Sponsor.query.filter_by(username=username).first()
    user1 = Sponsor.query.filter_by(email=email).first()

    if user:
        flash('Username already exists')
        return redirect(url_for('sponsorregister'))
    
    if user1:
        flash("Email already exists")
        return redirect(url_for("sponsorregister"))
    password_hash = generate_password_hash(password)
    
    new_user = Sponsor(username=username, pass_hash=password_hash, name=name, email=email,company_name=company_name,industry=industry,budget=budget)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('sponsorlogin'))
    





@app.route("/influencerregister", methods=["post"])
def influencerregister_post():
    username=request.form.get("username")
    password=request.form.get("password")
    confirmpassword=request.form.get("confirmpassword")
    name=request.form.get("name")
    email=request.form.get("email")
    category=request.form.get("category")
    niche=request.form.get("niche")
    reach=request.form.get("reach")
    if not (username and password and confirmpassword and category and niche and reach):
        flash("Fill out all the required details")
        return redirect(url_for("influencerregister"))
    if password!=confirmpassword:
        flash("Password and confirm password do not match")
        return redirect(url_for("influencerregister"))
    user = Influencer.query.filter_by(username=username).first()
    user1 = Sponsor.query.filter_by(email=email).first()

    

    if user:
        flash('Username already exists')
        return redirect(url_for('influencerregister'))
    if user1:
        flash("Email already exists")
        return redirect(url_for("influencerregister"))
    password_hash = generate_password_hash(password)
    new_user = Influencer(username=username, pass_hash=password_hash, name=name, email=email,category=category,niche=niche,reach=reach)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('influencerlogin'))



@app.route('/sponsorlogin', methods=['POST'])
def sponsorlogin_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please fill out all fields')
        return redirect(url_for('login'))
    
    user = Sponsor.query.filter_by(username=username).first()
    
    if not user:
        flash('Username does not exist')
        return redirect(url_for('sponsorlogin'))
    
    if not check_password_hash(user.pass_hash, password):
        flash('Incorrect password')
        return redirect(url_for('sponsorlogin'))
    
    session['user_id'] = user.sponsor_id
    flash('Login successful')
    return redirect(url_for('index'))





@app.route('/influencerlogin', methods=['POST'])
def influencerlogin_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please fill out all fields')
        return redirect(url_for('login'))
    
    user = Influencer.query.filter_by(username=username).first()
    
    if not user:
        flash('Username does not exist')
        return redirect(url_for('influencerlogin'))
    
    if not check_password_hash(user.pass_hash, password):
        flash('Incorrect password')
        return redirect(url_for('influencerlogin'))
    
    session['user_id'] = user.influencer_id
    flash('Login successful')
    return redirect(url_for('index'))


@app.route("/logout")
@auth_required
def logout():
    session.pop('user_id',None)
    return redirect(url_for("login"))






@app.route("/sponsorprofile")
@auth_required_sponsor
def sponsorprofile():
    user = Sponsor.query.get(session['user_id'])
    return render_template('sponsorprofile.html', user=user)


@app.route("/influencerprofile")
@auth_required_influencer
def influencerprofile():
    user = Influencer.query.get(session['user_id'])
    return render_template('influencerprofile.html', user=user)



@app.route("/adminprofile")
@auth_required_admin
def adminprofile():
    user = Admin.query.get(session['user_id'])
    return render_template('adminprofile.html', user=user)

@app.route('/sponsorprofile', methods=['POST'])
@auth_required_sponsor
def sponsorprofile_post():
    username = request.form.get('username')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    name = request.form.get('name')
    email=request.form.get("email")
    budget=request.form.get("budget")

    if not username or not cpassword or not password:
        flash('Please fill out all the required fields')
        return redirect(url_for('profile'))
    
    user = Sponsor.query.get(session['user_id'])
    if not check_password_hash(user.pass_hash, cpassword):
        flash('Incorrect password')
        return redirect(url_for('sponsorprofile'))
    
    if username != user.username:
        new_username = Sponsor.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists')
            return redirect(url_for('sponsorprofile'))
    
    new_password_hash = generate_password_hash(password)
    user.username = username
    user.pass_hash = new_password_hash
    user.name = name
    user.email=email
    user.budget=budget
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('sponsorprofile'))




@app.route('/influencerprofile', methods=['POST'])
@auth_required_influencer
def influencerprofile_post():
    username = request.form.get('username')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    name = request.form.get('name')
    email=request.form.get("email")
    reach=request.form.get("reach")

    if not username or not cpassword or not password:
        flash('Please fill out all the required fields')
        return redirect(url_for('influencerprofile'))
    
    user = Influencer.query.get(session['user_id'])
    if not check_password_hash(user.pass_hash, cpassword):
        flash('Incorrect password')
        return redirect(url_for('influencerprofile'))
    
    if username != user.username:
        new_username = Sponsor.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists')
            return redirect(url_for('influencerprofile'))
    
    new_password_hash = generate_password_hash(password)
    user.username = username
    user.pass_hash = new_password_hash
    user.name = name
    user.email=email
    user.reach=reach
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('influencerprofile'))







@app.route('/adminlogin', methods=['POST'])
def adminlogin_post():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash('Please fill out all fields')
        return redirect(url_for('login'))
    
    user = Admin.query.filter_by(username=username).first()
    
    if not user:
        flash('Username does not exist')
        return redirect(url_for('adminlogin'))
    
    if not check_password_hash(user.pass_hash, password):
        flash('Incorrect password')
        return redirect(url_for('adminlogin'))
    
    session['user_id'] = user.admin_id
    flash('Login successful')
    return redirect(url_for('index'))





@app.route("/adminlogin")
def adminlogin():
    return render_template("login_admin.html")




@app.route('/adminprofile', methods=['POST'])
@auth_required_admin
def adminprofile_post():
    username = request.form.get('username')
    cpassword = request.form.get('cpassword')
    password = request.form.get('password')
    name = request.form.get('name')
    email=request.form.get("email")
    

    if not username or not cpassword or not password:
        flash('Please fill out all the required fields')
        return redirect(url_for('profile'))
    
    user = Admin.query.get(session['user_id'])
    if not check_password_hash(user.pass_hash, cpassword):
        flash('Incorrect password')
        return redirect(url_for('adminprofile'))
    
    if username != user.username:
        new_username = Admin.query.filter_by(username=username).first()
        if new_username:
            flash('Username already exists')
            return redirect(url_for('adminprofile'))
    
    new_password_hash = generate_password_hash(password)
    user.username = username
    user.pass_hash = new_password_hash
    user.name = name
    user.email=email
    db.session.commit()
    flash('Profile updated successfully')
    return redirect(url_for('adminprofile'))



@app.route("/campaign/add", methods=["POST"])
@auth_required_sponsor
def add_campaign_post():
    userid=session.get("user_id")
    
    
    name = request.form.get("name")
    description = request.form.get("description")
    start_date = datetime.datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
    end_date = datetime.datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
    budget = request.form.get("budget")
    visibility = request.form.get("visibility")
    goals = request.form.get("goals")

    if not ( name and description and start_date and end_date and budget and visibility and goals):
        flash("Please fill out all required fields.")
        return redirect(url_for("add_campaign"))

    new_campaign = Campaign(
        sponsor_id=userid,
        name=name,
        description=description,
        start_date=start_date,
        end_date=end_date,
        budget=budget,
        visibility=visibility,
        goals=goals
    )

    db.session.add(new_campaign)
    db.session.commit()
    flash("Campaign added successfully!")
    return redirect(url_for("add_campaign"))

    

@app.route("/campaign/add")
@auth_required_sponsor
def add_campaign():
    return render_template("addcampaign.html")

@app.route("/campaign/view")
@auth_required_sponsor
def view_campaign():
    campaigns=Campaign.query.filter_by(sponsor_id=session.get("user_id")).all()
    return render_template("viewcampaign.html",campaigns=campaigns)

@app.route("/campaign/edit/<int:id>")
@auth_required_sponsor
def edit_campaign(id):
    
    for campaign in Campaign.query.filter_by(sponsor_id=session.get("user_id")).all():
        if id == campaign.campaign_id:
            return render_template('editcampaign.html',campaign=campaign)

    else:
        flash("Unauthorised access")
        return redirect(url_for("view_campaign"))
    

@app.route("/campaign/edit/<int:id>",methods=["post"])
@auth_required_sponsor
def edit_campaign_post(id):
    for campaign in Campaign.query.filter_by(sponsor_id=session.get("user_id")).all():
        if id == campaign.campaign_id:

            
            name = request.form.get("name")
            description = request.form.get("description")
            start_date = datetime.datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
            end_date = datetime.datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
            budget = request.form.get("budget")
            visibility = request.form.get("visibility")
            goals = request.form.get("goals")
            
            campaign.name=name
            campaign.description=description
            campaign.start_date=start_date
            campaign.end_date=end_date
            campaign.budget=budget
            campaign.visibility=visibility
            campaign.goals=goals
            db.session.commit()
            flash("changes saved successfully")
            return(redirect(url_for("edit_campaign",id=id)))
    else:
        flash("Unauthorised access")
        return(redirect(url_for("view_campaign")))
        
@app.route("/campaign/delete/<int:id>", methods=["post"])
@auth_required_sponsor
def delete_campaign(id):
    for campaign in Campaign.query.filter_by(sponsor_id=session.get("user_id")).all():
        if id == campaign.campaign_id:
            db.session.delete(campaign)
            db.session.commit()
            flash("Campaign deleted successfully.")
            return redirect(url_for("view_campaign"))
    else:
        flash("Forbidden access")
        return redirect(url_for("view_campaign"))
    

@app.route('/adrequest/add/<int:id>')
@auth_required_sponsor
def add_adrequest(id):
    
    sponid=session.get("user_id")
    campaigns=Campaign.query.filter_by(sponsor_id=sponid)
    influencer=Influencer.query.all()
    if id:
        campaign=Campaign.query.get(id)
        if campaign:
            if campaign.sponsor_id == sponid:
                return render_template("addadrequest.html",default_campaign_id=campaign.campaign_id,campaigns=campaigns,influencers=influencer)
    
    
    return render_template("addadrequest.html",campaigns=campaigns,influencers=influencer)


      
@app.route("/adrequest/add/<int:id>",methods=["post"])
@auth_required_sponsor
def add_adrequest_post(id):
    sponsor_id=session.get("user_id")
    cgn=Campaign.query.get(id)
    if not cgn:
        flash("Unauthorised access")
        return(redirect(url_for("view_adrequest")))
    if cgn.sponsor_id!=sponsor_id:
        flash("Unauthorised access")
        return(redirect(url_for("view_adrequest")))


    campaign_id = request.form.get('campaign_id')
    influencer_id = request.form.get('influencer_id')
    sponsor_negotiation_amount = request.form.get('sponsor_negotiation_amount')
    messages = request.form.get('messages')
    
    adrequest=AdRequest(campaign_id=campaign_id,influencer_id=influencer_id,sponsor_negotiation_amount=sponsor_negotiation_amount
                        ,sponsor_id=sponsor_id,status="Pending")
    

    db.session.add(adrequest)

    db.session.commit()
    message=Message(sender_id=sponsor_id, sender_type="Sponsor",message=messages,ad_request_id=adrequest.ad_request_id)

    db.session.add(message)


    db.session.commit()
    return redirect(url_for("view_all_adrequests"))

    
@app.route('/adrequest/view/<int:ad_request_id>', methods=['GET'])
@auth_required_sponsor
def view_adrequest(ad_request_id):
    ad_request=AdRequest.query.get(ad_request_id)
    sponid=session.get("user_id")
    if not ad_request:
        flash("Not found")
        return redirect(url_for("view_all_adrequests"))

    if ad_request.sponsor_id!=sponid:
        flash("Unauthorised access")
        return redirect(url_for("view_all_adrequests"))
    
    message=Message.query.filter_by(ad_request_id=ad_request_id).first()
    influencer=Influencer.query.get(ad_request.influencer_id)
    campaign=Campaign.query.get(ad_request.campaign_id)
    return render_template('viewadrequest.html', ad_request=ad_request,messages=message.message,influencer=influencer.name,campaign=campaign.name)


@app.route('/adrequest/view/')
@auth_required_sponsor
def view_all_adrequests():
    sponid=session.get("user_id")
    adrequests=AdRequest.query.filter_by(sponsor_id=sponid)
    return(render_template("viewalladrequests.html",ad_requests=adrequests))

        
    
@app.route('/adrequest/delete/<int:ad_request_id>', methods=['POST'])
@auth_required_sponsor

def delete_adrequest(ad_request_id):
    sponid=session.get("user_id")
    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        flash("Ad request does not exist")
        return redirect(url_for('view_adrequests'))
    if ad_request.sponsor_id!=sponid:
        flash("Unauthorised access")
    
    db.session.delete(ad_request)
    db.session.commit()
    flash('Ad Request deleted successfully!', 'success')
    return redirect(url_for('view_all_adrequests'))



@app.route('/adrequest/edit/<int:ad_request_id>/', methods=['GET', 'POST'])
@auth_required_sponsor
def edit_adrequest(ad_request_id):
    sponid=session.get("user_id")
    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        flash("Ad request does not exist")
        return redirect(url_for('view_adrequests'))
    if ad_request.sponsor_id!=sponid:
        flash("Unauthorised access")

    if request.method == 'POST':
        ad_request.campaign_id = request.form.get('campaign_id')
        ad_request.influencer_id = request.form.get('influencer_id')
        ad_request.sponsor_negotiation_amount = request.form.get('sponsor_negotiation_amount')
        ad_request.status = request.form.get('status')
        
        db.session.commit()
        flash('Ad Request updated successfully!', 'success')
        return redirect(url_for('view_ad_request', ad_request_id=ad_request.ad_request_id))

    
    influencers = Influencer.query.all()
    cid=ad_request.campaign_id
    campaign=(Campaign.query.get(cid))
    message=Message.query.filter_by(ad_request_id=ad_request_id).first()
    
    return render_template('editadrequest.html', ad_request=ad_request, influencers=influencers,campaign_name=campaign.name,message=message.message)
    

@app.route('/messages/<int:ad_request_id>', methods=['GET', 'POST'])
@auth_required
def messages(ad_request_id):
    user_id = session.get('user_id')
    user_type = 'Sponsor' if user_id.startswith('SP') else 'Influencer'
    
    ad_request = AdRequest.query.get(ad_request_id)
    if not ad_request:
        flash('Ad request not found')
        return redirect(url_for('index'))

    # Verify that the current user is involved in the ad request
    if (user_type == 'Sponsor' and ad_request.sponsor_id != user_id) or \
       (user_type == 'Influencer' and ad_request.influencer_id != user_id):
        flash('Unauthorized access')
        return redirect(url_for('index'))
    
    # Fetch messages related to the ad request
    messages = Message.query.filter_by(ad_request_id=ad_request_id).all()

    if request.method == 'POST':
        # Handle sending new messages
        message_text = request.form.get('message')
        if not message_text:
            flash('Message cannot be empty')
            return redirect(url_for('messages', ad_request_id=ad_request_id))
        
        message = Message(
            ad_request_id=ad_request_id,
            sender_id=user_id,
            sender_type=user_type,
            message=message_text
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent')
        return redirect(url_for('messages', ad_request_id=ad_request_id))

    return render_template('messages.html', messages=messages, ad_request=ad_request, user_type=user_type)
