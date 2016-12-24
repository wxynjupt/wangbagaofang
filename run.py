import os
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField, SubmitField, RadioField,FileField,SelectField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask.ext.moment import Moment
from datetime import date



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,static_url_path='/static')
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
moment = Moment(app)
manager = Manager(app)
bootstrap = Bootstrap(app)

class LoginForm(Form):
    login_account = StringField('account', validators=[Required()])
    login_pass = StringField('pass', validators=[Required()])
    submit = SubmitField('Submit')

class NewClientForm(Form):
    client_name = StringField('client_name',validators=[Required()])
    client_ip = StringField('client_ip',validators=[Required()])
    client_bandwidth = RadioField('client_bandwidth',validators=[Required()])
    client_aera = SelectField('client_aera',validators=[Required()])
    client_application = FileField('client_application',validators=None)
    client_port = StringField('client_port',validators=None)
    submit = SubmitField('Submit')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    email = db.Column(db.String(120), unique=True)
    def __repr__(self):
        return '<User %r>' % self.username
    def save(self):
        db.session.add(self)
        db.session.commit()

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()

class Client_Info(db.Model):
    __tablename__ = 'client_info'
    id = db.Column(db.Integer, primary_key=True,unique=True)
    clientname = db.Column(db.String(64), unique=True, index=True)
    phone = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    ip_address = db.Column(db.String(120), unique=True)
    area = db.Column(db.String(120))
    bandwidth = db.Column(db.Integer)
    port = db.Column(db.String(120))
    is_config = db.Column(db.Integer)
    attack_num = db.Column(db.Integer)
    time = db.Column(db.DateTime)

    def __repr__(self):
        return '<Client %r>' % self.clientname
    def save(self):
        db.session.add(self)
        db.session.commit()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/index')
def index():
    month_client_count = 100
    all_client_count = Client_Info.query.count()
    isnot_config_count = Client_Info.query.count()
    attack_count = Client_Info.query.count()

    return render_template('index.html',all_client_count=all_client_count,month_client_count=month_client_count,isnot_config_count=isnot_config_count,attack_count=attack_count)


@app.route('/',methods=['POST','GET'])
def login():
    login_account = None
    login_pass = None
    login_form = LoginForm()
    if login_form.validate_on_submit():
        login_account = login_form.login_account.data()
        login_pass = login_form.login_pass.data()
        login_form.login_account.data = ''
        login_form.login_pass.data = ''
    return render_template('login.html',login_form = login_form,login_account=login_account,login_pass=login_pass)

@app.route('/adduser',methods = ['GET', 'POST'])
def adduser():
    adduserform = NewClientForm()
    if adduserform.validate_on_submit():
        clientname = adduserform.client_name.data
        clientip = adduserform.client_ip.data
        clientbandwidth = adduserform.client_bandwidth.data
        clientport = adduserform.client_port.data
        clientaera = adduserform.client_aera.data
        clientapplication = adduserform.client_application.data
        adduserform.client_name.data = ''
        adduserform.client_ip.data = ''
        adduserform.client_bandwidth.data = ''
        adduserform.client_port.data = ''
        adduserform.client_aera.data = ''
        adduserform.client_application.data = ''
        print clientip
        client_info = Client_Info(clientname = clientname,ip_address = clientip,area = clientaera,bandwidth = clientbandwidth,is_config = 0,attack_num = 0,time = datetime.datetime.now())
        db.session.add(client_info)
        db.session.commit()
    return render_template('adduser.html',adduserform = adduserform)


@app.route('/editconfig')
def editconfig():
    return render_template('editconfig.html')

@app.route('/userdetail')
def userdetail():
    return render_template('userdetail.html')
    

if __name__ == '__main__':
    manager.run()
