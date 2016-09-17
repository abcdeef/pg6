import psycopg2
import sqlite3
import time, sys, math
from os.path import expanduser

home = expanduser("~")

sq = sqlite3.connect(home + '/sit2d_2.db')
sqc = sq.cursor()
conn = psycopg2.connect("dbname=gis user=florian")
cur = conn.cursor()

sqc.execute("delete from vertex")
sqc.execute("delete from polygon")
sqc.execute("delete from eigenschaften")

sqc.execute("vacuum")
sq.commit()

def toDB(data, p_id, p_lvl):
	points = data.split(",")
	seq = 0
	ll = [sys.float_info.max,0,sys.float_info.max,0]

	for point in points:	
		try:
			t = point.split(" ")
			g_x = (float(t[0]) + 180.0) / 360.0 * pow2Z;
			g_y = (1.0 - math.log(math.tan(float(t[1]) * rad2deg) + 1.0 / math.cos(float(t[1]) * rad2deg)) / math.pi) / 2.0 * pow2Z;
			sqc.execute("insert into polygon(V_L_ID,V_SEQ,V_LON,V_LAT,V_LVL) values (?,?,?,?,?)", (p_id,seq,g_x,g_y,p_lvl))
			if g_x < ll[0]:
				ll[0] = g_x
			if g_x > ll[1]:
				ll[1] = g_x
			if g_y < ll[2]:
				ll[2] = g_y
			if g_y > ll[3]:
				ll[3] = g_y
			
			seq = seq + 1
		except:
			print "Unexpected error:", sys.exc_info()[0]
			#print row			
			raise
	return ll

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

vert = [[4, 3]]
vert.pop()

lat = 52.0611
lon = 11.7229
lld =  0.1

sql = "select ST_AsText(way),osm_id,typ from v_line"
sql = sql + " where way && ST_MakeEnvelope(" + str(lon-lld) + ", " + str(lat-lld) + ", " + str(lon+lld) + ", " + str(lat+lld) + ", 4326)"
#sql = "select ST_AsText(ST_Transform(way,4326)),osm_id from planet_osm_line where 1=1"
cur.execute(sql)

x = cur.fetchall()
verts=float(cur.rowcount)

for row in x:
	if row[2] in ('service','residential'):
		r = 1.0
		g = 1.0
		b = 1.0
	elif row[2] == 'secondary':
		r = 0.965
		g = 0.976
		b = 0.745
	elif row[2] == 'primary':
		r = 0.984
		g = 0.835
		b = 0.643
	elif row[2] == 'trunk':
		r = 0.972
		g = 0.698
		b = 0.612
	elif row[2] == 'track':
		r = 0.337
		g = 0.274
		b = 0.254
	elif row[2] in ('motorway','motorway_link'):
		r = 1.0
		g = 0.1
		b = 0.1
	else:
		r = 1.0
		g = 0.0
		b = 0.0

	points = row[0].replace(")","").replace("LINESTRING(","").split(",")

	sqc.execute("insert into eigenschaften(L_ID,L_F_R,L_F_G,L_F_B,OSM_ID) values (?,?,?,?,?)", (linie,r,g,b,row[1]))

	n2 = 0
	for point in points:
		t = point.split(" ")
		g_x = (float(t[0]) + 180.0) / 360.0 * pow2Z;
		g_y = (1.0 - math.log(math.tan(float(t[1]) * rad2deg) + 1.0 / math.cos(float(t[1]) * rad2deg)) / math.pi) / 2.0 * pow2Z;

		sqc.execute("insert into vertex(V_L_ID,V_SEQ,V_LON,V_LAT) values (?,?,?,?)", (linie,n2,g_x,g_y))
		n2 = n2 + 1
	
	linie = linie + 1
	progressbar("linien",linie/verts)
	
sql = "select ST_AsText(way),osm_id,typ from v_polygon t"
sql = sql + " where way && ST_MakeEnvelope(" + str(lon-lld) + ", " + str(lat-lld) + ", " + str(lon+lld) + ", " + str(lat+lld) + ", 4326)"
#sql = sql + " where osm_id=134149361"
cur.execute(sql)

x = cur.fetchall()
poly=float(cur.rowcount)

leer = []

for row in x:
	if row[2] in ('water','riverbank'):
		r = 0.0
		g = 0.0
		b = 1.0
	elif row[2] in ('forest','wood'):
		r = 0.13
		g = 0.54
		b = 0.13
	elif row[2] == 'farmyard':
		r = 0.91
		g = 0.85
		b = 0.76
	elif row[2] == 'farmland':
		r = 0.95
		g = 0.92
		b = 0.86
	elif row[2] == 'residential':
		r = 0.878
		g = 0.87
		b = 0.87
	elif row[2] == 'building':
		r = 0.847
		g = 0.82
		b = 0.79
	elif row[2] == 'scree':
		r = 0.80
		g = 0.78
		b = 0.45
	elif row[2] == 'meadow':
		r = 0.80
		g = 0.92
		b = 0.69
	elif row[2] == 'public transport':
		r = 1.0
		g = 0.0
		b = 0.0
	elif row[2] == 'scrub':
		r = 0.72
		g = 0.89
		b = 0.72
	elif row[2] == 'park':
		r = 0.72
		g = 0.89
		b = 0.72
	elif row[2] == 'allotments':
		r = 0.90
		g = 0.78
		b = 0.67
	elif row[2] == 'landfill':
		r = 0.71	
		g = 0.71
		b = 0.57
	elif row[2] == 'wetland':
		r = 0.80
		g = 0.92
		b = 0.698
	elif row[2] == 'playground':
		r = 0.80
		g = 1.0
		b = 0.94
	elif row[2] == 'parking':
		r = 0.965
		g = 0.933
		b = 0.714
	elif row[2] == 'dog_park':
		r = 0.784
		g = 0.976
		b = 0.8
	elif row[2] == 'track':
		r = 0.455
		g = 0.863
		b = 0.729
	elif row[2] == 'pitch':
		r = 0.537
		g = 0.824
		b = 0.682
	else:
		try:
			leer.index(row[2])
		except:
			leer.append(row[2])
		r = 1.0
		g = 0.0
		b = 0.0
	#asd(row[0].replace("))",")").replace("POLYGON((","("), linie,0)
	#tmp="11 22,(33 44)"
	tmp=row[0][:-2].replace("POLYGON((","")
	try:
		if tmp.find("(") == -1:
			ll=toDB(tmp,linie, 1)
			sqc.execute("insert into eigenschaften(L_ID,L_F_R,L_F_G,L_F_B,OSM_ID,L_LON1,L_LON2,L_LAT1,L_LAT2) values (?,?,?,?,?,?,?,?,?)", (linie,r,g,b,row[1],ll[0],ll[1],ll[2],ll[3]))
		
	except:
		print "asd"
		continue
		

	linie = linie + 1
	progressbar("polygon",(linie-verts)/poly)
	
#print leer

cur.close()
conn.close()

sq.commit()
sqc.close()
