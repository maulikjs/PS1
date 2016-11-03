def userwillike(uid):
	cursor=conn.cursor()
	cursor.execute("SELECT t.tagid from tags t , associatedwith aw, photos p, stores s, albums a where a.ownerid = '{0}' and a.albumid=s.albumid and s.photoid=p.photoid and p.photoid=aw.photoid and aw.tagid=t.tagid group by t.tagid order by count(t.tagid) desc limit 5".format(uid))
	got=cursor.fetchall()
	print got
	ctr=len(got)
	print ctr


	if ctr==5:
		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3,associatedwith aw4,associatedwith aw5 where aw1.tagid= '{0}' AND aw2.tagid= '{1}' AND aw3.tagid= '{2}'AND aw4.tagid= '{3}' AND aw5.tagid= '{4}' AND aw1.photoid= p.photoid".format(got[0][0],got[1][0],got[2][0],got[3][0],got[4][0]))
		got1 = cursor.fetchall()

	if ctr>=4:
		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3,associatedwith aw4 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}' AND aw4.tagid= '{3}' AND aw1.photoid= p.photoid".format(got[0][0],got[1][0],got[2][0],got[3][0]))
		got2 = cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3,associatedwith aw4 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}' AND aw4.tagid= '{3}' AND aw1.photoid= p.photoid".format(got[4][0],got[1][0],got[2][0],got[3][0]))
		got2 = got2+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3,associatedwith aw4 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}' AND aw4.tagid= '{3}' AND aw1.photoid= p.photoid".format(got[4][0],got[2][0],got[3][0],got[0][0]))
		got2 = got2+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3,associatedwith aw4 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}' AND aw4.tagid= '{3}' AND aw1.photoid= p.photoid".format(got[4][0],got[1][0],got[3][0],got[0][0]))
		got2 = got2+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3,associatedwith aw4 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}' AND aw4.tagid= '{3}' AND aw1.photoid= p.photoid".format(got[4][0],got[2][0],got[1][0],got[0][0]))
		got2 = got2+ cursor.fetchall()

	if ctr>=3:
		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[0][0],got[1][0],got[2][0]))
		got3 = cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[0][0],got[1][0],got[3][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[0][0],got[1][0],got[4][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[1][0],got[2][0],got[0][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[1][0],got[2][0],got[3][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[1][0],got[2][0],got[4][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[2][0],got[3][0],got[4][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[2][0],got[3][0],got[0][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[3][0],got[4][0],got[0][0]))
		got3 = got3+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2,associatedwith aw3 where aw1.tagid= '{0}'AND aw2.tagid= '{1}'AND aw3.tagid= '{2}'  AND aw1.photoid= p.photoid".format(got[3][0],got[4][0],got[1][0]))
		got3 = got3+ cursor.fetchall()

	if ctr>=2:
		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[0][0],got[1][0]))
		got4 =cursor.fetchall()

		cursor=conn.cursor()
		print("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[0][0],got[2][0]))
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[0][0],got[2][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[0][0],got[3][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[0][0],got[4][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[1][0],got[2][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[1][0],got[3][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[1][0],got[4][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[2][0],got[3][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[2][0],got[4][0]))
		got4 = got4+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1, associatedwith aw2 where aw1.tagid= '{0}'AND aw2.tagid= '{1}' AND aw1.photoid= p.photoid".format(got[3][0],got[4][0]))
		got4 = got4+ cursor.fetchall()

	if ctr>=1:
		print got[1][0]
		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1 where aw1.tagid= '{0}' AND aw1.photoid= p.photoid".format(got[1][0]))
		got5=cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1 where aw1.tagid= '{0}' AND aw1.photoid= p.photoid".format(got[1][0]))
		got5 = got5+ cursor.fetchall()

		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1 where aw1.tagid= '{0}' AND aw1.photoid= p.photoid".format(got[1][0]))
		got5 = got5+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1 where aw1.tagid= '{0}' AND aw1.photoid= p.photoid".format(got[1][0]))
		got5 = got5+ cursor.fetchall()


		cursor=conn.cursor()
		cursor.execute("SELECT p.caption, p.data from photos p, associatedwith aw1 where aw1.tagid= '{0}' AND aw1.photoid= p.photoid".format(got[1][0]))
		got5 = got5+ cursor.fetchall()

	gotfinal=got1+got2+got3+got4+got5;

	return gotfinal
