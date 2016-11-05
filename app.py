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
from flask.ext.login import current_user
from collections import Counter
import operator

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
aid=0

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
	cursor.execute("SELECT photos.data, photos.PhotoID, photos.caption FROM Photos,stores where stores.albumID='{0}' AND Photos.PhotoID=stores.photoID".format(album_id))
	Globalvariableforphotos = cursor.fetchall()
	return Globalvariableforphotos #NOTE list of tuples, [(imgdata, pid), ...]

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

@app.route('/tags', methods=['GET'])
@flask_login.login_required
def display_tag_photos():
	tag = request.args.get('value1')
	flag = request.args.get('value2')
	uid = getUserIdFromEmail(flask_login.current_user.id)
	print flag
	if flag == '1':
		print('Something ia hishc')

		print('Something ia hishc')
		global Globalvariableforphotos
		Globalvariableforphotos = getPhotosWithTags(uid, tag, flag)
		return render_template('albums.html', tagphotos= Globalvariableforphotos)
	elif flag == '2':
		print('Something ia hishc')

		print('Something ia hishc')
		global Globalvariableforphotos
		Globalvariableforphotos = getPhotosWithTags(uid, tag, '1')
		return render_template('albums.html', notusertagphotos= Globalvariableforphotos)
	elif flag == '0':
		print('not not not')
		global Globalvariableforphotos
		Globalvariableforphotos = getPhotosWithTags(uid, tag, flag)
		global Globalvariableforphotos1
		Globalvariableforphotos1 = getPhotosWithTags(uid, tag, 2)
		return render_template('albums.html', tag1photos= Globalvariableforphotos, notusertagphotos = Globalvariableforphotos1)

@app.route('/profile')
@flask_login.login_required
def protected():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('hello.html', name=flask_login.current_user.id, message="Here's your profile", albums=getUsersAlbums(uid), tags=getUserTags(uid), othertags=getOtherTags(uid), top10tags=getTop10Tags())

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
		tag = [x.strip(' ') for x in tags.split(' ')]
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

			tagid = getTagIDFromTagName(i)
			if tagid == None:
				cursor = conn.cursor()
				cursor.execute("INSERT INTO tags(Title) VALUES ('{0}')".format(i))
				conn.commit()
				tagid1 = getTagIDFromTagName(i)
				pid = getPidFromData(data, caption)
				print tagid1
				associated_with(tagid1, pid)
			else:
				pid = getPidFromData(data, caption)
				associated_with(tagid, pid)

		return render_template('albums.html', name=flask_login.current_user.id, message='Photo uploaded!', photos=getUsersPhotosFinal(album_id), album_id=album_id )
		#return render_template('hello.html', name=flask_login.current_user.id, message='Photo uploaded!', photos=getUsersPhotos(uid) )
	#The method is GET so we return a  HTML form to upload the a photo.
	else:
		album_id= request.args.get('values')
		return render_template('upload.html', album_id=album_id)
#end photo uploading code

def associated_with(tagid, pid):
	cursor = conn.cursor()
	cursor.execute("INSERT INTO associatedwith (Tagid, Photoid) values ('{0}', '{1}')".format(tagid[0], pid))
	conn.commit()

def getTagIDFromTagName(title):
	cursor = conn.cursor()
	cursor.execute("SELECT Tags.TagID FROM Tags Where title = '{0}'".format(title))
	flag = cursor.fetchone()
	if flag == None:
		return None
	else:
		return flag

@app.route('/allalbums', methods=['POST','GET'])
def displayallalbums():
	cursor = conn.cursor()
	cursor.execute("SELECT  a.albumid, a.album_name, u.userid, u.first_name, u.last_name From Albums a, Users u Where a.Ownerid = u.userid")
	return render_template('allalbums.html', allalbums=cursor.fetchall())


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

@app.route('/deletealbum', methods=['POST'])
@flask_login.login_required
def delete_album():
	if request.method == 'POST':
		aid=request.args.get('value')
		print(aid)
		uid=getUserIdFromEmail(flask_login.current_user.id)
		print(uid)

		cursor = conn.cursor()
		cursor.execute("DELETE FROM photos using photos, stores WHERE photos.photoid = stores.photoid and stores.albumid = '{0}'".format(aid))
		conn.commit()

		cursor = conn.cursor()
		cursor.execute("DELETE FROM Albums WHERE Albumid = '{0}'".format(aid))
		conn.commit()

		return render_template('hello.html', name=flask_login.current_user.id, message="Album DELETED!", albums=getUsersAlbums(uid))

@app.route("/Addfriends", methods=['GET'])
def addFriends():
	uid = getUserIdFromEmail(flask_login.current_user.id)
	return render_template('friends.html', friendlist=getalist(uid),albums=getUsersAlbums(uid), flag=True)

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


@app.route('/youmaylike', methods=['POST','GET'])
@flask_login.login_required
def youMayAlsoLike():
	uid= getUserIdFromEmail(flask_login.current_user.id)
	return render_template('hello.html', youmaylike= userwillike(uid))


def userwillike(uid):
	cursor=conn.cursor()
	cursor.execute("SELECT t.tagid from tags t , associatedwith aw, photos p, stores s, albums a where a.ownerid = '{0}' and a.albumid=s.albumid and s.photoid=p.photoid and p.photoid=aw.photoid and aw.tagid=t.tagid group by t.tagid order by count(t.tagid) desc limit 5".format(uid))
	got=cursor.fetchall()


	cursor=conn.cursor()
	cursor.execute("SELECT photoid from photos")
	photoidlist=cursor.fetchall()

	rank = {}
	for i in photoidlist:
		for j in got:
			cursor=conn.cursor()
			cursor.execute("SELECT p.photoid from photos p, associatedwith aw where aw.tagid= '{0}' AND aw.photoid= '{1}' AND aw.photoid=p.photoid".format(j[0],i[0]))
			got1=cursor.fetchall()
			if got1:
				if i[0] not in rank:
					rank[i[0]] = 1
				else:
					rank[i[0]]+=1


	sorted_rank = sorted(rank.items(), key=operator.itemgetter(1), reverse=True)
	print sorted_rank


#	concise_rank={}
#	for key,value in sorted_rank:
#		k = key
#		concise_rank.setdefault(k,[])
#		concise_rank[k].append(value)
#		cursor=conn.cursor()
#		cursor.execute("SELECT count(aw.tagid) from photos p, associatedwith aw where p.photoid = '{0}' AND aw.photoid=p.photoid".format(key))
#		gotconcise=cursor.fetchall()
#		concise_rank[k].append(gotconcise[0][0])

#	print concise_rank

	gotnew=()
	for key,value in sorted_rank:
		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p where p.photoid='{0}'".format(key))
		gotnew += cursor.fetchall()
	Globalvariableforphotos = gotnew
	return gotnew



@app.route('/search', methods=['POST'])
@flask_login.login_required
def display_tag_search_photos():
	tags = request.form.get('tags')
	tags = tags.split(" ")
	return render_template('albums.html', tagsearchphotos= getTagSearchPhotos(tags))

	tags = request.form.get('tags')
	tags = tags.split(" ")
	if current_user.is_authenticated:
		uid=getUserIdFromEmail(flask_login.current_user.id)
	else:
		uid=4
	global Globalvariableforphotos
	Globalvariableforphotos = getTagSearchPhotos(tags)
	return render_template('album.html', tagsearchphotos= Globalvariableforphotos, uid=uid)

def getTagIDFromTagName(title):
	cursor = conn.cursor()
	cursor.execute("SELECT TagID FROM Tags Where title = '{0}'".format(title))
	flag = cursor.fetchone()
	if flag == None:
		return None
	else:
		return flag

def getPidFromData(data, caption):
	cursor = conn.cursor()
	cursor.execute("SELECT Photoid FROM Photos Where data = '{0}' and caption = '{1}'".format(data, caption))
	return cursor.fetchone()[0]

def getPhotosWithTags(uid, tag, flag):
	if flag == '1':
		cursor = conn.cursor()
		cursor.execute("SELECT DISTINCT p.caption, p.data FROM Photos p, Albums a, Tags t, Associatedwith tp WHERE tp.tagid = '{0}' and p.Photoid = tp.photoid".format(tag))
		Globalvariableforphotos = cursor.fetchall()
		return Globalvariableforphotos
	elif flag == 2:
		cursor = conn.cursor()
		cursor.execute("SELECT DISTINCT p1.caption, p1.data FROM Photos p1, Associatedwith tp1 WHERE tp1.tagid = '{1}' and p1.Photoid = tp1.photoid and p1.caption NOT IN (SELECT DISTINCT p.caption FROM Photos p, Users u, Albums a, Tags t,stores s, Associatedwith tp WHERE a.OwnerID='{0}' and p.photoid=s.photoid and s.albumid=a.albumid and tp.tagid ='{1}' AND p.Photoid=tp.photoid)".format(uid, tag))
		Globalvariableforphotos = cursor.fetchall()
		return Globalvariableforphotos
	else:
		cursor = conn.cursor()
		cursor.execute("SELECT DISTINCT p.caption, p.data FROM Photos p, Users u, Albums a, Tags t, Associatedwith tp,stores s WHERE a.OwnerID = '{0}' and p.photoid = s.photoid and s.albumid = a.albumid  and tp.tagid = '{1}' and p.Photoid = tp.photoid".format(uid, tag))
		Globalvariableforphotos = cursor.fetchall()
		return Globalvariableforphotos

@app.route('/top10')
def showtop10users():
	cursor = conn.cursor()
	cursor.execute("SELECT userid, first_name, last_name, email from users")
	top10users = cursor.fetchall()
	print(top10users)
	user_activity = {}
	for i in top10users:
		cursor = conn.cursor()
		cursor.execute("SELECT count(*) from photos,albums where albums.ownerid = {0} and stores.albumid = albums.albumid and photos.photoid=stores.p".format(i[0]))
		photo_count = cursor.fetchall()[0]
		cursor = conn.cursor()
		cursor.execute("SELECT count(*) from comments,writes where writes.userID= '{0}' and commennts.cid=writes.cid".format(i[0]))
		comment_count = cursor.fetchall()[0]
		#print(comment_count[0],photo_count[0])
		rank_count = int(comment_count[0]) + int(photo_count[0])
		user_activity[str(i[1]+" "+i[2]+" "+i[3])] =rank_count
	user_activity = sorted(user_activity.items(), key=operator.itemgetter(1) ,reverse=True)
	return render_template('top10users.html', user_activity=user_activity)

def getTagSearchPhotos(tags):

	tagids = ()
	for i in tags:
		tagids = tagids +  getTagidsFromTags(i)
		print tagids
		#tagsids = cursor.fetchone()[0] + " "

	for i in tagids:
		print i

	s = ""
	for i in tagids:
		s = s + ", associatedwith t" + str(i[0])
	print s

	q = ""
	for i in tagids:
		q = q + "p.photoid = t" + str(i[0]) + ".photoid and "
	print q

	w = ""
	ctr=len(tagids)
	c=0
	for i in tagids:
		if(c<ctr-1):
			w = w + "t" + str(i[0]) + ".tagid = " + str(i[0]) + " and "
		else:
			w = w + "t" + str(i[0]) + ".tagid = " + str(i[0])
		c = c + 1
	print w

	st = s + " Where " + q + " " + w
	print st
	print ("SELECT p.caption, p.data FROM Photos p" + st)
	cursor = conn.cursor()
	cursor.execute("SELECT p.caption, p.data FROM Photos p" + st)
	Globalvariableforphotos = cursor.fetchall()
	return Globalvariableforphotos

	# cursor.execute("SELECT DISTINCT p.caption, p.data FROM Photos p, Tags t, Associate_with tp WHERE p.album_id and tp.tag_id = t.tagID and p.Photo_id = tp.photo_id and t.title = tags".format(uid, tag))
	# return cursor.fetchall()
def getTagidsFromTags(tag):
	cursor = conn.cursor()
	cursor.execute("SELECT t.tagID FROM Tags t Where t.title = '{0}'".format(tag))
	return cursor.fetchall()
def getUserTags(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT DISTINCT t.tagID, t.title FROM Photos p, Albums a, Tags t, Associatedwith tp,stores s WHERE a.OwnerID = '{0}' and p.photoid = s.photoid and s.albumid=a.albumid  and t.tagid = tp.tagid and p.Photoid = tp.photoid".format(uid))
	return cursor.fetchall()

def getOtherTags(uid):
	cursor = conn.cursor()
	cursor.execute("SELECT DISTINCT t1.tagID, t1.title FROM Tags t1 WHERE t1.tagID NOT IN (SELECT DISTINCT t.tagID FROM Photos p, Albums a, Tags t, Associatedwith tp,stores s WHERE a.OwnerID = '{0}' and p.photoid = s.photoid and s.albumid=a.albumid   and t.tagid = tp.tagid and p.Photoid = tp.photoid)".format(uid))
	return cursor.fetchall()

def getTop10Tags():
	cursor = conn.cursor()
	cursor.execute("SELECT  t.tagid, t.title From Associatedwith tp, Tags t Where tp.tagid = t.tagID group by tp.tagid order by count(tp.tagid) desc limit 10")
	return cursor.fetchall()

@app.route('/commentsdisplay', methods=['POST'])
def display_comments():

        pid=request.args.get('value')
        print(pid)
        cursor = conn.cursor()
        cursor.execute("SELECT u.userid, u.First_Name, u.Last_Name, c.Commenttext FROM Comments c, User u,photos p Where c.photoid = p.photoid and c.Commenterid = u.user_id".format(pid))
        userss = cursor.fetchall()
        return render_template('displaycomments.html', usercomments = userss)

@app.route('/ccc', methods=['POST'])
def add_comment():

        pid=request.args.get('value')
        flag=request.args.get('value1')
        print(pid)
        text = request.form.get('text')
        if current_user.is_authenticated:
        	uid=getUserIdFromEmail(flask_login.current_user.id)
        else:
        	uid = 99

		cursor = conn.cursor()
		cursor.execute("INSERT INTO Comments (Commenttext) VALUES ('{0}') ".format(text))
		conn.commit()

		cursor=conn.cursor()
		cursor.execute("INSERT INTO Writes(userid) VALUES ('{0}') ".format(uid))
		con.commit()

		cursor = conn.cursor()
        cursor.execute("INSERT INTO has(photoid) VALUES ('{0}') ".format(pid))
        conn.commit()

        if flag == '1':
        	return render_template('albums.html', notusertagphotos= Globalvariableforphotos)
        elif flag == '2':
        	return render_template('albums.html', tagsearchphotos= Globalvariableforphotos, uid=uid)
        elif flag == '3':
        	return render_template('albums.html', photos=Globalvariableforphotos, albumid=aid, flag=flag)

@app.route('/xyz')
def displayPhotos():
    if current_user.is_authenticated:
       	uid=getUserIdFromEmail(flask_login.current_user.id)
    else:
        uid = 4
    flag=request.args.get('value1')
    print flag
    global aid
    aid=request.args.get('values')
    print(aid)
    global Globalvariableforphotos
    Globalvariableforphotos = getUsersPhotosFinal(aid)
    uploadflag=request.args.get('value1')
    return render_template('albums.html', photos=Globalvariableforphotos, albumid=aid, flag=flag, uploadflag=uploadflag, uid=uid)


@app.route('/likes', methods=['POST'])
@flask_login.login_required
def like_photo():
	pid = request.args.get('value')
	flag = request.args.get('value1')
	uid = getUserIdFromEmail(flask_login.current_user.id)
	cursor = conn.cursor()
	cursor.execute("INSERT INTO Likes (userid, photoid) values ('{0}', '{1}')".format(uid, pid))
	conn.commit()
	if flag == '1':
		return render_template('albums.html', message='Like Added', photos=Globalvariableforphotos, albumid=aid)
	elif flag == '2':
		return render_template('albums.html', message='Like Added', tagphotos= Globalvariableforphotos)
	elif flag == '3':
		return render_template('albums.html', message='Like Added', tag1photos= Globalvariableforphotos, notusertagphotos = Globalvariableforphotos1)
	elif flag == '4':
		return render_template('albums.html', message='Like Added', tagsearchphotos= Globalvariableforphotos)
		#render_template('album.html', photos=getUsersPhotos(aid), albumid=aid)


@app.route('/likeusers', methods=['POST'])
@flask_login.login_required

def display_like_users():

        pid=request.args.get('value')
        print(pid)
        cursor = conn.cursor()
        cursor.execute("SELECT u.userid, u.First_Name, u.last_name FROM User u, Likes l Where l.photoid = '{0}' and l.userid = u.userid".format(pid))
        userss = cursor.fetchall()
        print userss
        return render_template('userliked.html', likeusers = userss)

#GIve tag reccomendations
@app.route('/ppp', methods=['POST'])
@flask_login.login_required
def recommendations2():
	tags = request.form.get('tags')
	tags1 = []
	tags = tags.split(" ")
	for i in tags:
		print i
		tags1.append(i)
	print tags1
	cursor = conn.cursor()
	cursor.execute("SELECT aw.photoid FROM Associatedwith aw, Tags t Where t.title = '{0}' and t.tagid = aw.tagid or t.title = '{1}' and t.tagid = aw.tagid".format(tags1[0], tags1[1]))
	photo_ids = cursor.fetchall()
	recommendation=[]
	for photo_id in photo_ids:
		cursor = conn.cursor()
		cursor.execute("SELECT t.title FROM Associatedwith aw, Tags t Where t.tagid = aw.tagid and aw.photoid = '{0}'".format(photo_id[0]))
		tagnames = cursor.fetchall()
		for tagname in tagnames:
			print tagname
			if tagname[0] in tags1:
				tagname
				continue
			else:
				recommendation.append(tagname[0])
	print recommendation
	counts = Counter(recommendation)
	recommendations = sorted(set(recommendation), key=counts.get, reverse=True)
	recommendations = recommendations[0:5]
	return render_template('upload.html', albumid=aid, tagrecommendations=recommendations)

#default page
@app.route("/", methods=['GET'])
def hello():
	return render_template('hello.html', message='Welecome to Photoshare')



if __name__ == "__main__":
	#this is invoked when in the shell  you run
	#$ python app.py
	app.run(port=5000, debug=True)
