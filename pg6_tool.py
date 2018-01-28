import sys, math
import sqlite3
from threading import Thread

RSHIFT = 3

pow2Z = pow(2.0, 18);
rad2deg = math.pi / 180.0;
NDIGITS = 4

def list_diff(list1, list2):
    counts = {}
    for x in list1:
        try:
            counts[x] += 1
        except:
            counts[x] = 1
    for x in list2:
        try:
            counts[x] -= 1
            if counts[x] < 0:
                raise ValueError('All elements of list2 not in list2')
        except:
            raise ValueError('All elements of list2 not in list1') 
    result = []
    for k, v in counts.iteritems():
        result += v*[k] 
    return result

def aufStrecke(A,B,P):
#Punkt P auf Strecke AB
	C = [B[0] - A[0], B[1] - A[1]]
	if C[0] != 0:
		r = (P[0] - A[0]) / C[0]
	else:
		r = (P[1] - A[1]) / C[1]

	if r < 0 or r > 1:
		return False
	else:
		return True

def sp(A,B,C,D):
   try:
	#print ''
	#print A
	#print B
	#print C
	#print D
#Schnittpunkt von AB und CD
	a1 = A[1] - B[1]
	a2 = C[1] - D[1]
	b1 = B[0] - A[0]
	b2 = D[0] - C[0]

	#print "a1: " + str(a1)
	#print "a2: " + str(a2)
	#print "b1: " + str(b1)
	#print "b2: " + str(b2)

	#if (a1 == 0 and a2 == 0) or (b1 == 0 and b2 == 0):
	if A[0]-C[0]+A[1]-C[1] == 0 or A[0]-D[0]+A[1]-D[1] == 0:
		return A
	if B[0]-C[0]+B[1]-C[1] == 0 or B[0]-D[0]+B[1]-D[1] == 0:
		return B
	if (a1 == 0 and a2 == 0) or (b1 == 0 and b2 == 0):
		return None
	
	c1 = B[0] * A[1] - A[0] * B[1]
	c2 = D[0] * C[1] - C[0] * D[1]
	ds = a1 * b2 - a2 * b1
	#print "c1: " + str(c1)
	#print "c2: " + str(c2)
	#print "ds: " + str(ds)

	if ds == 0:
		return
	
	s = [round((c1 * b2 - c2 * b1) / ds, NDIGITS), round((a1 * c2 - a2 * c1) / ds, NDIGITS)]
	#print "s: " + str(s)
	if aufStrecke(A,B, s) == False:
		return None
	if aufStrecke(C,D, s) == False:
		return None

	return s

   except:	
	print "\nA: " + str(A)
	print "B: " + str(B)
	print "C: " + str(C)
	print "D: " + str(D)
	
	print "a1: " + str(a1)
	print "a2: " + str(a2)
	print "b1: " + str(b1)
	print "b2: " + str(b2)
	print "c1: " + str(c1)
	print "c2: " + str(c2)

	print ""
	raise
	    
def sp2(A,B,C,D):
   try:
	#print ''
	#print A
	#print B
	#print C
	#print D
#Schnittpunkt von AB und CD
	a1 = A[2] - B[2]
	a2 = C[2] - D[2]
	b1 = B[1] - A[1]
	b2 = D[1] - C[1]

	#print "a1: " + str(a1)
	#print "a2: " + str(a2)
	#print "b1: " + str(b1)
	#print "b2: " + str(b2)

	#if (a1 == 0 and a2 == 0) or (b1 == 0 and b2 == 0):
	if A[1]-C[1]+A[2]-C[2] == 0 or A[1]-D[1]+A[2]-D[2] == 0:
		#return A
		return None
	if B[1]-C[1]+B[2]-C[2] == 0 or B[1]-D[1]+B[2]-D[2] == 0:
		#return B
		return None
	if (a1 == 0 and a2 == 0) or (b1 == 0 and b2 == 0):
		return None
	
	c1 = B[1] * A[2] - A[1] * B[2]
	c2 = D[1] * C[2] - C[1] * D[2]
	ds = a1 * b2 - a2 * b1
	#print "c1: " + str(c1)
	#print "c2: " + str(c2)
	#print "ds: " + str(ds)

	if ds == 0:
		return
	
	s = [0,0,round((c1 * b2 - c2 * b1) / ds, NDIGITS), round((a1 * c2 - a2 * c1) / ds, NDIGITS)]
	#print "s: " + str(s)
	if aufStrecke(A[1:],B[1:],s[2:]) == False:
		return None
	if aufStrecke(C[1:],D[1:],s[2:]) == False:
		return None

	return s

   except:	
	print "\nA: " + str(A)
	print "B: " + str(B)
	print "C: " + str(C)
	print "D: " + str(D)
	
	print "a1: " + str(a1)
	print "a2: " + str(a2)
	print "b1: " + str(b1)
	print "b2: " + str(b2)
	print "c1: " + str(c1)
	print "c2: " + str(c2)

	print ""
	raise

def angleV(p1, p2):
	# Winkel zwischen 2 Vektoren
	# angle: 1 -> 180grad, 0 -> 90grad
	return (p1[0] * p2[0] + p1[1] * p1[1]) / (math.sqrt(p1[0]**2 + p1[1]**2) * math.sqrt(p2[0]**2 + p2[1]**2))

def aufLinie(B, C, A):
        # BC -> Gerade; A -> Punkt
	# 0 -> auf Linie, <0 -> unterhalb, >0 -> oberhalb
	return round((A[0] - B[0]) * (B[1] - C[1]) + (A[1] - B[1]) * (C[0] - B[0]),4)

def toSlippyMap(p_t):
    return [ (float(p_t[0]) + 180.0) / 360.0 * pow2Z, (1.0 - math.log(math.tan(float(p_t[1]) * rad2deg) + 1.0 / math.cos(float(p_t[1]) * rad2deg)) / math.pi) / 2.0 * pow2Z ]

#results = []
#def binaersuche_rekursiv3(werte, index, gesucht, start, ende):
#	global results
#	results = [-1,-1]
#	
#	mitte = (start + ende)//2
#
#	threads = []
#	process = Thread(target=binaersuche_rekursiv2, args=[0, results, werte, index, gesucht, start, ende])
#	process.start()
#	threads.append(process)
#	process = Thread(target=binaersuche_rekursiv2, args=[1, results, werte, index, gesucht, start, ende])
#	process.start()
#	threads.append(process)
#
#	for process in threads:
#		process.join()
#	if results[0] == -1:
#		return results[1]
#	else:
#		return results[0]

#def binaersuche_rekursiv2(a, result, werte, index, gesucht, start, ende):
#	result[a] = binaersuche_rekursiv(werte, index, gesucht, start, ende)
#	return True

def binaersuche_rekursiv(werte, index, gesucht, start, ende):
    if ende < start:
        return -1
    mitte = (start + ende)//2
    #print "->" + str(start) + " " + str(mitte) + " " + str(ende)
    if werte[mitte][index] == gesucht:
        return mitte
    elif werte[mitte][index] < gesucht:
        return binaersuche_rekursiv(werte, index, gesucht, mitte+1, ende)
    else:
        return binaersuche_rekursiv(werte, index, gesucht, start, mitte-1)
 
def progressbar(header,progress,footer=""):
	barLength = 20
        h_l = len(header)
        if h_l > 5:
            header = header[0:4]+"."
        header = "{}:{}".format(header," "*int(5-h_l))
	status = ""
	if isinstance(progress, int):
		progress = float(progress)

	block = int(round(barLength*progress))
	text = "\r{} [{}] {:>7.2%} {} {}".format( header,"#"*block + "-"*(barLength-block),progress, status, footer)
	sys.stdout.write(text)
	if progress >= 1:
		print ""
	sys.stdout.flush()

def createIX(array,col):
	ix = []
	#print "createIX"
	array.sort(key=lambda student: student[col])
	#s1 = timer()
	for index,em in enumerate(array):
		i = binaersuche_rekursiv(ix,0,em[col],0,len(ix)-1)
		
		if i == -1:
			ix.append([em[col],[index]])
		else:
			ix[i][1].append(index)
	#s2 = timer()
	#print str(round(s2 - s1,1))+"s"
	return ix

def fillDB(db_file,vertex,indices3,indices2,indices2n,config_farbe,lines3,lines2):
    sq = sqlite3.connect(db_file)
    sqc = sq.cursor()
    sqc.executemany("insert into vertex (V_ID,V_LON,V_LAT) values (?,?,?)", vertex)
    sqc.executemany("insert into indices (I_L_ID,I_V_ID,I_SEQ) values (?,?,?)", indices3)
    sqc.executemany("insert into indices (I_L_ID,I_V_ID,I_SEQ) values (?,?,?)", indices2)
    sqc.executemany("insert into indices2n (W_L_ID,W_V_ID,I_SEQ1,I_SEQ2,W_R_LON,W_R_LAT,W_SEQ) values (?,?,?,?,?,?,?)", indices2n)
    sqc.executemany("insert into config_farbe(CF_ID,R,G,B,CF_BEZ) values (?,?,?,?,?)", config_farbe)
    sqc.executemany("insert into eigenschaften(L_ID,L_CF_ID,L_LVL) values (?,?,?)", lines3)
    sqc.executemany("insert into eigenschaften(L_ID,L_CF_ID,L_LVL) values (?,?,?)", lines2)
    #sqc.execute("update vertex set v_lon1=cast(v_lon as int),v_lat1=cast(v_lat as int)")
    #sqc.execute("insert into config_farbe (CF_ID,R,G,B) select distinct L_CF_ID,1,0,0 from eigenschaften where not exists (select * from config_farbe where CF_ID=L_CF_ID) and L_CF_ID is not null")
    sqc.execute("INSERT INTO tiles (T_LON,T_LAT) SELECT DISTINCT CAST(V_LON AS INTEGER)>>" + str(RSHIFT) + ",CAST(V_LAT AS INTEGER)>>" + str(RSHIFT) + " FROM vertex")
    sqc.execute("INSERT INTO tiles2L (T2L_L_ID,T2L_T_ID) SELECT L_ID,T_ID FROM v_tiles2L_create t")
    sq.commit()
    sqc.execute("vacuum")
    sqc.close()
    sq.close()

def clearDB(db_file):
    sq = sqlite3.connect(db_file)
    sqc = sq.cursor()
    sqc.execute("delete from vertex")
    sqc.execute("delete from indices")
    sqc.execute("delete from indices2n")
    sqc.execute("delete from eigenschaften")
    sqc.execute("delete from tiles2L")
    sqc.execute("delete from tiles")
    sqc.execute("delete from config_farbe")
    sqc.execute("delete from V")
    sqc.execute("delete from L")
    sqc.execute("delete from R")
    sq.commit()
    sqc.execute("vacuum")
    sqc.close()
    sq.close()
    
def trDB(db_file, lvl):
    print "TR: " + db_file
    sq = sqlite3.connect(db_file)
    sqc = sq.cursor()
    sqc.execute("insert into L SELECT t.L_ID,g.r AS L_CF_R,g.g AS L_CF_G,g.b AS L_CF_B FROM eigenschaften t JOIN config_farbe g ON t.L_CF_ID = g.CF_ID where t.L_LVL=" + str(lvl))
    sqc.execute("insert into V SELECT distinct I_L_ID,I_SEQ,V_LAT,V_LON,CAST(V_LAT AS INTEGER)>>" + str(RSHIFT) + ",CAST(V_LON AS INTEGER)>>" + str(RSHIFT) + " FROM indices JOIN vertex ON I_V_ID=V_ID join eigenschaften on L_ID=I_L_ID where L_LVL=" + str(lvl))
    sqc.execute("insert into R SELECT w_l_id,w_seq,V_LAT,V_LON,CAST(V_LAT AS INTEGER)>>" + str(RSHIFT) + ",CAST(V_LON AS INTEGER)>>" + str(RSHIFT) + " FROM indices2n JOIN vertex ON w_v_id=V_ID join eigenschaften on L_ID=W_L_ID where L_LVL=" + str(lvl))
    sqc.execute("drop table config_farbe")
    sqc.execute("drop table eigenschaften")
    sqc.execute("drop table indices")
    sqc.execute("drop table indices2n")
    sqc.execute("drop table tiles")
    sqc.execute("drop table tiles2L")
    sqc.execute("drop table vertex")
    sq.commit()
    sqc.execute("vacuum")
    sqc.close()
    sq.close()
