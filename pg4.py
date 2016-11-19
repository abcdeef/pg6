import psycopg2
import sqlite3
import sys, math
import triangulate

# -*- coding: utf-8 -*-

sq = sqlite3.connect('sit2d_4.db')
sqc = sq.cursor()
#conn = psycopg2.connect("host=dell dbname=gis user=florian")
conn = psycopg2.connect("dbname=gis user=florian")
cur = conn.cursor()

sqc.execute("delete from vertex")
sqc.execute("delete from polygon")
sqc.execute("delete from eigenschaften")
sqc.execute("delete from residential")

sq.commit()


def toDB(data, p_id, p_lvl, p_table):
	points = data.split(",")
	seq = 0
	old_point = []
	for point in points:	
		try:
			t = point.split(" ")
			g_x = (float(t[0]) + 180.0) / 360.0 * pow2Z;
			g_y = (1.0 - math.log(math.tan(float(t[1]) * rad2deg) + 1.0 / math.cos(float(t[1]) * rad2deg)) / math.pi) / 2.0 * pow2Z;

			if (seq % 2) == 0 and seq > 0:
				#print "-> " + str(old_point[0]) + " " + str(old_point[1])
				sqc.execute("insert into " + p_table + "(V_L_ID,V_SEQ,V_LON,V_LAT) values (?,?,?,?)", (p_id,seq,old_point[0],old_point[1]))
				seq = seq + 1
			#else:
				#print "erster"

			#print "   " + str(g_x) + " " + str(g_y)
			sqc.execute("insert into " + p_table + "(V_L_ID,V_SEQ,V_LON,V_LAT) values (?,?,?,?)", (p_id,seq,g_x,g_y))
			
			old_point = [g_x,g_y]
			seq = seq + 1
		except:
			print "Unexpected error:", sys.exc_info()[0]
			#print row			
			raise
	return seq

def toDB2(data, p_id, p_lvl, p_table):
	points = data.split(",")

	vert = [[4, 3]]
	vert.pop()

	for point in points:
		#print point	
		try:
			t = point.split(" ")
			g_x = (float(t[0]) + 180.0) / 360.0 * pow2Z;
			g_y = (1.0 - math.log(math.tan(float(t[1]) * rad2deg) + 1.0 / math.cos(float(t[1]) * rad2deg)) / math.pi) / 2.0 * pow2Z;

			vert.append([g_x,g_y])
		except:
			print "Unexpected error:", sys.exc_info()[0]
			#print row			
			raise

	seq = 0	
	tri = []
	plist = vert[::-1] if triangulate.IsClockwise(vert) else vert[:]
	plist.pop()
	
	while len(plist) >= 3:
		a = triangulate.GetEar(plist)
		if a == []:
			break	
		sqc.execute("insert into " + p_table + "(V_L_ID,V_SEQ,V_LON,V_LAT) values (?,?,?,?)", (p_id,seq,a[0][0],a[0][1]))
		sqc.execute("insert into " + p_table + "(V_L_ID,V_SEQ,V_LON,V_LAT) values (?,?,?,?)", (p_id,seq+1,a[1][0],a[1][1]))
		sqc.execute("insert into " + p_table + "(V_L_ID,V_SEQ,V_LON,V_LAT) values (?,?,?,?)", (p_id,seq+2,a[2][0],a[2][1]))
		seq = seq + 3	
		tri.append(a)
	#print ''
	#for point in tri:
	#	print point
	#	print str(point[0][0]) + ", " + str(point[0][1])
	#	print str(point[1][0]) + ", " + str(point[1][1])
	#	print str(point[2][0]) + ", " + str(point[2][1])
		#print 

	return seq


def asd(ert, p_id, lvl):
	if len(ert) == 0:
		return	
	if ert[0] == "(":
		level = 0
		for i, c in enumerate(ert):
			if c == "(":
				level = level + 1
			elif c == ")":
				level = level -1

			if c == ")" and level == 0:
				asd(ert[1:i],p_id,lvl+1)
				asd(ert[i+2:],p_id,lvl+1) # <-
				break

	elif ert[0] <> "(":
		n = ert.find("(")
		if n == -1:
			toDB(ert,p_id,lvl) 
		else:
			toDB(ert[0:n-1],p_id,lvl)
			asd(ert[n:],pid,lvl+1) # <-

def progressbar(header,progress):
	barLength = 20
	status = ""
	if isinstance(progress, int):
		progress = float(progress)

	block = int(round(barLength*progress))
	text = "\r{0}: [{1}] {2}% {3}".format( header,"#"*block + "-"*(barLength-block), round(progress*100,2), status)
	sys.stdout.write(text)
	if progress >= 1:
		print ""
	sys.stdout.flush()

linie = 0
pow2Z = pow(2.0, 18);
rad2deg = math.pi / 180.0;



#lat = 52.0611
#lon = 11.7229
#lld =  0.1

sql = "select ST_AsText(way),osm_id,typ from v_line"
#sql = sql + " where way && ST_MakeEnvelope(" + str(lon-lld) + ", " + str(lat-lld) + ", " + str(lon+lld) + ", " + str(lat+lld) + ", 4326)"
#sql = sql + " where osm_id in (92116198, 33955912)"
cur.execute(sql)

x = cur.fetchall()
verts=float(cur.rowcount)

for row in x:
	tmp=row[0][:-2].replace("LINESTRING(","")

	if tmp.find("(") == -1:
		line_len = toDB(tmp,linie, 1, "vertex")
		sql = "insert into eigenschaften(L_ID,OSM_ID,L_COUNT,L_TYP) values (?,?,?,?)"
		try:
			typ = unicode(row[2])
		except:
			typ = unicode()	
		sqc.execute(sql, (linie,row[1],line_len,typ ))
#hashlib.md5(str(row[2])).digest().encode('base64')[:4]  ))	

	linie = linie + 1
	progressbar("linien ",linie/verts)

sql = "select ST_AsText(way),osm_id,typ from v_building t"
#sql = sql + " where way && ST_MakeEnvelope(" + str(lon-lld) + ", " + str(lat-lld) + ", " + str(lon+lld) + ", " + str(lat+lld) + ", 4326)"
#sql = sql + " where osm_id = 26879098"
cur.execute(sql)

x = cur.fetchall()
poly=float(cur.rowcount)

leer = []

for row in x:
	tmp=row[0][:-2].replace("POLYGON((","")
	if tmp.find("(") == -1 and row[0] <> 'POLYGON EMPTY':
		tris = toDB2(tmp,linie, 1, "polygon")	
		#len(tmp.split(","))

		sql = "insert into eigenschaften(L_ID,OSM_ID,L_COUNT,L_TYP) values (?,?,?,?)"
		try:
			typ = unicode(row[2])
		except:
			typ = unicode()	
		sqc.execute(sql, (linie,row[1],tris,typ ))
		
	
	linie = linie + 1
	progressbar("polygon",(linie-verts)/poly)
	
sql = "select ST_AsText(way),osm_id,typ from v_residential t"
#sql = sql + " where osm_id=26879098"
cur.execute(sql)

x = cur.fetchall()
resi=float(cur.rowcount)

leer = []

for row in x:
	tmp=row[0][:-2].replace("POLYGON((","")
	if tmp.find("(") == -1 and row[0] <> 'POLYGON EMPTY':
		tris = toDB2(tmp,linie, 1, "residential")	
		#len(tmp.split(","))

		sql = "insert into eigenschaften(L_ID,OSM_ID,L_COUNT,L_TYP) values (?,?,?,?)"
		try:
			typ = unicode(row[2])
		except:
			typ = unicode()	
		sqc.execute(sql, (linie,row[1],tris,typ ))

	linie = linie + 1
	progressbar("residential",(linie-verts-poly)/resi)

#sql = "select distinct typ from v_polygon union all select distinct typ from v_line union all select distinct typ from v_residential"
#cur.execute(sql)
#x = cur.fetchall()
#for row in x:
	#sql = "update config_farbe set bezeichnung = ? where cf_id=?"
	#sqc.execute(sql, (row[0],hashlib.md5(str(row[0])).digest().encode('base64')[:4]  ))

cur.close()
conn.close()
sq.commit()

sqc.execute("insert into config_farbe (CF_ID,R,G,B) select distinct L_TYP,1,0,0 from eigenschaften where not exists (select * from config_farbe where CF_ID=L_TYP) and L_TYP is not null");
#sqc.execute("delete FROM polygon WHERE EXISTS (SELECT * FROM eigenschaften WHERE V_L_ID=L_ID AND L_COUNT-1=V_SEQ)");
#sqc.execute("delete FROM residential WHERE EXISTS (SELECT * FROM eigenschaften WHERE V_L_ID=L_ID AND L_COUNT-1=V_SEQ)");
#sqc.execute("UPDATE eigenschaften SET L_COUNT=L_COUNT-1 WHERE EXISTS (SELECT * FROM polygon WHERE V_L_ID = L_ID)");

sqc.execute("vacuum")
sqc.close()
