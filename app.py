######################################
# author ben lawson <balawson@bu.edu>
# Edited by: Craig Einstein <einstein@bu.edu>
######################################
# Some code adapted from
# CodeHandBook at http://codehandbook.org/python-web-application-development-using-flask-and-mysql/
# and MaxCountryMan at https://github.com/maxcountryman/flask-login/
# and Flask Offical Tutorial at  http://flask.pocoo.org/docs/0.10/patterns/fileuploads/
# see links for further understanding
###################################################

import flask
from flask import Flask, Response, request, render_template, redirect, url_for
from flaskext.mysql import MySQL
import flask.ext.login as flask_login

#for image uploading
from werkzeug import secure_filename
import os, base64

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'MaulikShah'  # Change this!

#These will need to be changed according to your creditionals
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'RUchi4546@'
app.config['MYSQL_DATABASE_DB'] = 'photosharemaulik'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#begin code used for login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()
cursor.execute("SELECT email from Users")
users = cursor.fetchall()

def getUserList():
	cursor = conn.cursor()
	cursor.execute("SELECT email from Users")
	return cursor.fetchall()

class User(flask_login.UserMixin):
	pass

@login_manager.user_loader
def user_loader(email):
	users = getUserList()
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	return user

@login_manager.request_loader
def request_loader(request):
	users = getUserList()
	email = request.form.get('email')
	if not(email) or email not in str(users):
		return
	user = User()
	user.id = email
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email))
	data = cursor.fetchall()
	pwd = str(data[0][0] )
	user.is_authenticated = request.form['password'] == pwd
	return user

'''
A new page looks like this:
@app.route('new_page_name')
def new_page_function():
	return new_page_html
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
	if flask.request.method == 'GET':
		return '''
			   <form action='login' method='POST'>
				<input type='text' name='email' id='email' placeholder='email'></input>
				<input type='password' name='password' id='password' placeholder='password'></input>
				<input type='submit' name='submit'></input>
			   </form></br>
		   <a href='/'>Home</a>
			   '''
	#The request method is POST (page is recieving data)
	email = flask.request.form['email']
	cursor = conn.cursor()
	#check if email is registered
	if cursor.execute("SELECT password FROM Users WHERE email = '{0}'".format(email)):
		data = cursor.fetchall()
		pwd = str(data[0][0] )
		if flask.request.form['password'] == pwd:
			user = User()
			user.id = email
			flask_login.login_user(user) #okay login in user
			return flask.redirect(flask.url_for('protected')) #protected is a function defined in this file

	#information did not match
	return "<a href='/login'>Try again</a>\
			</br><a href='/register'>or make an account</a>"

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return render_template('hello.html', message='Logged out')

@login_manager.unauthorized_handler
def unauthorized_handler():
	return render_template('unauth.html')

#you can specify specific methods (GET/POST) in function header instead of inside the functions as seen earlier
@app.route("/register", methods=['GET'])
def register():
	return render_template('register.html', supress='True')

@app.route("/register", methods=['POST'])
def register_user():
	try:
        	F_ame=request.form.get('F_ame')
        	L_ame=request.form.get('L_ame')
		email=request.form.get('email')
		password=request.form.get('password')
		DOB=request.form.get('DOB')
		Home_town=request.form.get('Home_town')
		Gender=request.form.get('Gender')
	except:
		print "couldn't find all tokens" #this prints to shell, end users will not see this (all print statements go to shell)
		return flask.redirect(flask.url_for('register'))
	cursor = conn.cursor()
	test =  isEmailUnique(email)
	if test:
		print cursor.execute("INSERT INTO Users (First_Name, Last_Name, email, Password, DOB, Hometown, Gender) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(F_ame, L_ame, email, password, DOB, Home_town, Gender))
		conn.commit()
		#log user in
		user = User()
		user.id = email
		flask_login.login_user(user)
		return render_template('hello.html', name=email, message='Account Created!')
	else:
		print "couldn't find all tokens"
		return flask.redirect(flask.url_for('register'))

def getUsersPhotosFinal(album_id):
	print(album_id)
	cursor = conn.cursor()
	cursor.execute("SELECT data, photos.PhotoID, caption FROM Photos,stores where stores.albumID='{0}' AND Photos.PhotoID=stores.photoID".format(album_id))
	return cursor.fetchall() #NOTE list of tuples, [(imgdata, pid), ...]

def getUserIdFromEmail(email):
	cursor = conn.cursor()
	cursor.execute("SELECT UserID  FROM Users WHERE email = '{0}'".format(email))
	return cursor.fetchone()[0]

def getPhotoCaptionFromPhotos(pid):
	cursor = conn.cursor()
	cursor.execute("SELECT caption  FROM Photos WHERE PhotoID = '{0}'".format(pid))
	return cursor.fetchone()[0]

def isEmailUnique(email):
	#use this to check if a email has already been registered
	cursor = conn.cursor()
	if cursor.execute("SELECT email  FROM Users WHERE email = '{0}'".format(email)):
		#this means there are greater than zero entries with that email
		return False
	else:
		return True

def getAlbumIdFromUserId(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT AlbumID  FROM albums WHERE OwnerID = '{0}'".format(uid))
	return cursor.fetchone()[0]

def getUsersAlbums(uid):
        cursor = conn.cursor()
        cursor.execute("Select AlbumID, album_name From albums WHERE OwnerID = '{0}'".format(uid))
        return cursor.fetchall()

#end login code

@app.route('/profile')
@flask_login.login_required
def protected():
	return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile")

#begin photo uploading code
# photos uploaded using base64 encoding so they can be directly embeded in HTML
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
@flask_login.login_required
def upload_file():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		imgfile = request.files['photo']
		caption = request.form.get('caption')
		tags = request.form.get('tags')
		tag = [x.strip('#') for x in tags.split(' ')]
		print caption
		album_id= request.args.get('values')

		data = base64.standard_b64encode(imgfile.read())
		cursor = conn.cursor()
		cursor.execute("INSERT INTO Photos (caption, data) VALUES ('{0}', '{1}')".format(caption, data))

		conn.commit()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO  Stores (AlbumID) VALUES ('{0}')".format(album_id))
		conn.commit()
		cursor=conn.cursor()
		print "____________________"
		print(uid)

		print(caption)
		cursor.execute("SELECT photos.photoID from photos,albums,creates,stores where albums.OwnerID='{0}' AND stores.AlbumID=albums.albumID AND photos.photoId=stores.photoID AND photos.caption='{1}'".format(uid,caption))
		pid=cursor.fetchone()[0]
		for i in tag:
			cursor= conn.cursor()
			cursor.execute("INSERT into tags(title) values ('{0}') ".format(i))
			conn.commit()
			cursor= conn.cursor()
			cursor.execute("INSERT into associatedwith(photoID) values ('{0}')".format(pid))
			conn.commit()

		return render_template('albums.html', name=flask_login.current_user.id, message='Photo uploaded!', photos=getUsersPhotosFinal(album_id), album_id=album_id )
		#return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!', photos=getUsersPhotos(uid) )
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		album_id= request.args.get('values')
		return render_template('upload.html', album_id=album_id)
#end photo uploading code

#display album's photos
@app.route('/albums')
@flask_login.login_required
def showPhotos():
	album_id=request.args.get('values')
	print(album_id)
	return render_template('albums.html', photos=getUsersPhotosFinal(album_id), album_id= album_id)

@app.route('/delete', methods=['POST'])
@flask_login.login_required
def delete_photos():
	album_id =request.args.get('values')
	photo_id = request.args.get('values2')
	cursor = conn.cursor()
	cursor.execute("DELETE FROM photos USING photos,stores WHERE stores.albumid = '{0}' AND stores.photoid = '{1}' and photos.photoID=stores.photoid".format(album_id,photo_id))
	conn.commit()
	return render_template('albums.html', photos=getUsersPhotosFinal(album_id), album_id= album_id)

@app.route('/add_albums', methods=['POST','GET'])
@flask_login.login_required
def add_album():
	if request.method == 'POST':
		uid = getUserIdFromEmail(flask_login.current_user.id)
		name = request.form.get('album_name')
		cursor = conn.cursor()
		cursor.execute("INSERT INTO albums (album_name, ownerid) VALUES ('{0}','{1}')".format(name,uid))
		conn.commit()
		cursor = conn.cursor()
		cursor.execute("INSERT INTO creates(userID) values ('{0}')".format(uid))
		conn.commit()
		return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile",albums= getUsersAlbums(uid))
	else:
		return render_template('add_albums.html', name=flask_login.current_user.id, message="Please type the album to add!")

@app.route("/Addfriends", methods=['GET'])
def addFriends():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('friends.html', friendlist=getalist(uid), flag=True)

def getalist(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT email,First_Name,Last_Name,UserID from Users where UserID != '{0}'".format(uid))
	return cursor.fetchall()

@app.route("/friends.html", methods=['GET'])
def addFriendship():
	uid2=request.args.get('values')
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO FriendsWith(UID1,UID2) Values ('{0}','{1}')".format(uid,uid2))
	conn.commit()
	return render_template('friends.html', flag =False)

@app.route("/Viewfriends", methods=['GET'])
def viewFriends():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('viewfriends.html', friendlist=getfriendlist(uid))

def getfriendlist(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT Users.email,Users.First_Name,Users.Last_Name from Users,friendswith where Users.UserID != '{0}' AND Users.UserID=friendswith.UID2 AND friendswith.UID1='{0}' ".format(uid))
	return cursor.fetchall()

#default page
@app.route("/", methods=['GET'])
def hello():
	return render_template('hello.html', message='Welecome to Photoshare')



if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=5000, debug=True)
