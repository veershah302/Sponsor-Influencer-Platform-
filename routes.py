from app import app
from flask import render_template,request,url_for,flash,redirect,session

from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from models import Sponsor,db,Influencer


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

    if user:
        flash('Username already exists')
        return redirect(url_for('sponsorregister'))
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

    if user:
        flash('Username already exists')
        return redirect(url_for('influencerregister'))
    password_hash = generate_password_hash(password)
    new_user = Influencer(username=username, pass_hash=password_hash, name=name, email=email,category=category,niche=niche,reach=reach)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('influencerlogin'))



@app.route('/sponsorlogin', methods=['POST'])
def sponsor_login_post():
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
def influencer_login_post():
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




