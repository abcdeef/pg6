#!/usr/bin/env python
import sqlite3
import sys, math
from timeit import default_timer as timer
from shutil import copyfile
import triangulate
from imposm.parser import OSMParser
import os
from pg6_tool import *
#from vbvb import *
import copy
from multiprocessing import Process, Lock

import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

# -*- coding: utf-8 -*-

PBF = "sachsen-anhalt-latest.osm.pbf"
#B = 3 / 40075017 * math.cos(g1[1] * rad2deg) / pow(2.0, 18.0 + 8.0) * 256;
B = 0.0638 / 2
NDIGITS = 5


vertex = []
vertex_ix = []
#I_L_ID,I_V_ID,I_SEQ
indices3 = []
indices2 = []
indices2n = []
indices2n_ix = []
lines3 = []
lines2 = []
tmp = []
whitelist = []
config_farbe = []

sq = sqlite3.connect("sit2d_6.db")
sqc = sq.cursor()

x = sqc.execute("select CF_ID,R,G,B,CF_BEZ from config_farbe").fetchall()
for em in x:
    config_farbe.append([em[0],em[1],em[2],em[3],em[4]])

clearDB("sit2d_6.db")

linie = 0
pow2Z = pow(2.0, 18);
rad2deg = math.pi / 180.0;
v_id = -1

def insertVIX(p_x, p_y, v_id):
    global vertex_ix
    
    ende = len(vertex_ix)
    v_ix = -1
    n2 = binaersuche_rekursiv(vertex_ix, 0, p_x, 0, ende-1)
    n = n2

    while n > -1 and vertex_ix[n][0] == p_x:
	if vertex_ix[n][0] == p_x and vertex_ix[n][1] == p_y:
		v_ix = n
		break
	n = n - 1
    while v_ix == -1 and n2 > -1 and n2 < ende and vertex_ix[n2][0] == p_x:
	if vertex_ix[n2][0] == p_x and vertex_ix[n2][1] == p_y:
		v_ix = n2
		break
	n2 = n2 + 1
    
    if v_ix == -1:
        vertex_ix.append([p_x, p_y, [v_id]])
    else:
        vertex_ix[v_ix][2].append(v_id)    
         
   
def findV(p_x, p_y, l_id = -1):
    global vertex
    global vertex_ix
    global RSHIFT
    #print "findV"
    i_x = int(p_x)>>RSHIFT
    i_y = int(p_y)>>RSHIFT
    v_ix = -1
    
    for index, number in enumerate(vertex_ix,start=0):
        if number[0] == i_x and number[1] == i_y:
            v_ix = index
            break
    
    if v_ix == -1:
        return -1

    for number in vertex_ix[v_ix][2]:
        if vertex[number][1] == p_x and vertex[number][2] == p_y:
            return vertex[number][0]
    
    return -1

def findV2(p_x, p_y):
	global vertex
	global vertex_ix
	global RSHIFT

	i_x = int(p_x)>>RSHIFT
	i_y = int(p_y)>>RSHIFT
	v_ix = -1
    
	for index, number in enumerate(vertex_ix,start=0):
		if number[0] == i_x and number[1] == i_y:
			v_ix = index
			break
    
	if v_ix == -1:
		return -1

	for number in vertex_ix[v_ix][2]:
		if vertex[number][1] == p_x and vertex[number][2] == p_y:
			return number

	return -1

#mutex = Lock()
#def vbvb4():
#	P_vbvb4()

def vbvb4():
	global indices2
	global vertex
	
	indices_tmp = copy.copy(indices2)
	indices_tmp.sort(key=lambda x: (x[0],x[2]))
	indices2 = []
		
	tmp_len = float(len(indices_tmp))
	i = 0

	old_em = indices_tmp[0]
	indices_tmp.append([-1,-1,-1])
	asd = []
	ende = len(vertex) - 1

	for em in indices_tmp:
		progressbar("vbvb4",i/tmp_len)
		if em[0] != old_em[0]:
			
			plist = asd[::-1] if triangulate.IsClockwise(asd) else asd[:]
			asd = []
			#print "########"
			seq = 0
			while len(plist) >= 3:
				a = triangulate.GetEar(plist)

				if a == []:
					break
				indices2.append([old_em[0],a[0][2],seq])
				indices2.append([old_em[0],a[1][2],seq+1])
				indices2.append([old_em[0],a[2][2],seq+2])
				seq = seq + 3
					
		a = binaersuche_rekursiv(vertex,0,em[1],0,ende)	

		asd.append([vertex[a][1],vertex[a][2],vertex[a][0]])
		old_em = copy.copy(em)
		i = i + 1
	    
def insertV(p_x, p_y):
    g_x=round(p_x,NDIGITS)
    g_y=round(p_y,NDIGITS)
    
    global v_id
    global vertex
    
    x = findV(g_x, g_y)

    if x == -1:
        v_id = v_id + 1
        vertex.append((v_id,g_x,g_y))
        insertVIX(int(g_x)>>RSHIFT, int(g_y)>>RSHIFT, len(vertex)-1)
        
        return v_id
    
    return x

def insertV2(p_x, p_y):
    global v_id
    global vertex
    
    g_x=round(p_x,NDIGITS)
    g_y=round(p_y,NDIGITS)
    
    v_id = v_id + 1    
    vertex.append((v_id,g_x,g_y))
    insertVIX(int(g_x)>>RSHIFT, int(g_y)>>RSHIFT, len(vertex)-1)
        
    return v_id

def insert_indices2n(W_L_ID, W_V_ID, I_SEQ1, I_SEQ2, W_R_LON, W_R_LAT, W_SEQ):
    global indices2n
    global indices2n_ix
    
    v_ix = -1
    for index, number in enumerate(indices2n_ix,start=0):
        if number[0] == W_V_ID:
            v_ix = index
            break
    
    if v_ix == -1:
        indices2n_ix.append([W_V_ID, [v_id]])
    else:
        indices2n_ix[v_ix][1].append(v_id)  
        
    indices2n.append([W_L_ID, W_V_ID, I_SEQ1, I_SEQ2, W_R_LON, W_R_LAT, W_SEQ])

ebene3 = ['highway','tracktype', 'foot', 'bicycle']
ebene2 = ['waterway','natural','landuse','building','barrier','construction','covered','disused','military']
whitelist = ebene2 + ebene3

def tag_filter(tags):
    for key in tags.keys():
        if key not in whitelist:
            del tags[key]
            #v = 1
           
def poly_add(osmid,refs,color,lvl):
    global poly_count
    seq = 0
    for node in refs:
        indices2.append([osmid,node,seq])
        tmp.append(node)
        seq = seq + 1
    tmp.pop()
    indices2.pop()
    lines2.append([osmid,color, lvl])
    poly_count = poly_count +1

def ways_add(osmid,refs,color):
	global poly_count
	#return
	#print "asd"
	seq = 0
	old_node = -1
	for node in refs:
		if old_node == node:
			continue
		if seq > 1:
			indices2n.append([osmid, old_node, None, None, None, None, seq])
			seq = seq + 1
		indices2n.append([osmid, node, None, None, None, None, seq])
		tmp.append(node)
		seq = seq + 1
		old_node = node
	lines3.append([osmid, color, 3])
	poly_count = poly_count +1
   
def myrel(ways):
	if len(ways) == 0:
	        return
    	#print "############################"
	#for a in ways:
		#print "---------"
		#print a

	#for osmid, tags, refs in ways:
		#if osmid  != 281352000:
		#	continue
		#print osmid
		#print refs
		#print tags

poly_count=0	
def myways(ways):
	global poly_count
	if len(ways) == 0:
		return
    	
	for osmid, tags, refs in ways:
		#if osmid  not in (395675446,27216435,27809465,27280925,366358001,394911465,26613341,27811900,8162072):
		if osmid  not in (27811900, 8162072,1):
		#if poly_count > 10000:
			continue
		
		#print 
		print osmid
		#print refs
		print tags

		if tags.get('building') != None:
			if tags.get('barrier') == None and tags.get('construction') == None and tags.get('covered') == None and tags.get('culvert') == None and tags.get('disused') == None and tags.get('military') == None:
				poly_add(osmid,refs,'building', 2)
				continue
			
		if tags.get('waterway')=='riverbank':
			poly_add(osmid,refs,'waterway_riverbank', 1)
			continue
		if tags.get('natural')=='water':
			poly_add(osmid,refs,'natural_water', 1)
			continue
		if tags.get('landuse')=='forest':
			poly_add(osmid,refs,'landuse_forest', 1)
			continue
		if tags.get('multipolygon')=='farmland':
			poly_add(osmid,refs,'landuse_farmland', 1)
			continue
			                        
		h = tags.get('highway')
		if h in ['secondary','tertiary','track','motorway','motorway_link','trunk','residential','service','primary']: 
			if h == 'track'and tags.get('tracktype') not in ['grade1','grade2']:
				continue
			if tags.get('foot') != None or tags.get('bicycle') != None:
				continue
			ways_add(osmid,refs,'highway_' + h)
					
n = 0        
def coords_callback(coords):
    global verts
    global n
    
    for osm_id, lon, lat in coords:
        if n == int(verts):
            return
        
        if vertex[n][0] == osm_id:
            t = toSlippyMap([lon,lat])
            g_x=round(t[0],NDIGITS)
            g_y=round(t[1],NDIGITS)            
            vertex[n] = [osm_id,g_x,g_y]
            n = n + 1
            progressbar("verts",n/verts)
            
   
def vbvb1():
    global B
    seq = 0
    ende = len(vertex)
    old_p = -1
    #print ende
    ind = len(indices2n)
   
    for i in xrange(0,ind,2):
      #try:
        i1 = binaersuche_rekursiv(vertex,0,indices2n[i][1],0,ende-1)
        i2 = binaersuche_rekursiv(vertex,0,indices2n[i+1][1],0,ende-1)
      

        r = [ round(vertex[i2][1] - vertex[i1][1],NDIGITS), round(vertex[i2][2] - vertex[i1][2],NDIGITS) ]
      
        n = [-r[1], r[0]]
      
        l_n = math.sqrt(n[0]**2+n[1]**2)

        nn = [ n[0] / l_n * B, n[1] / l_n * B ]
      
        p = [ round(vertex[i1][1] + nn[0],NDIGITS), round(vertex[i1][2] + nn[1],NDIGITS), round(vertex[i1][1] - nn[0],NDIGITS), round(vertex[i1][2] - nn[1],NDIGITS), round(vertex[i2][1] + nn[0],NDIGITS), round(vertex[i2][2] + nn[1],NDIGITS), round(vertex[i2][1] - nn[0],NDIGITS), round(vertex[i2][2] - nn[1],NDIGITS) ]
        #print p
        v_id = [ insertV(p[0],p[1]), insertV(p[2],p[3]), insertV(p[4],p[5]), insertV(p[6],p[7]) ]
        #print v_id
        if old_p != indices2n[i][0]:
            seq = 0
            
	# Dreieck 1
        for ii in range(0, 3):
            indices3.append([indices2n[i][0], v_id[ii], seq])
            seq = seq + 1
        # Dreieck 2
        for ii in range(1, 4):
            indices3.append([indices2n[i][0], v_id[ii], seq])
            seq = seq + 1
            
        indices2n[i][2] = seq-6
        indices2n[i][3] = seq-5
        indices2n[i+1][2] = seq-2
        indices2n[i+1][3] = seq-1
        
        indices2n[i][4] = r[0]
        indices2n[i][5] = r[1]
        indices2n[i+1][4] = -r[0]
        indices2n[i+1][5] = -r[1]
        
        old_p = indices2n[i][0]

        #print '##############'
        progressbar("vbvb1",(i+2)/float(ind))
      #except:
          #print "--"
          #for em in indices2n:
            #print em
          #print r
          #print n
          #print l_n
          #print nn
          #raise

ttt = [[0,0,0,0]]
def f_ttt(t1,t2,t3):
    p1=0
    p2=0
    p3=0
    
    if t1 > 0:
        p1 = 1
    elif t1 < 0:
        p1 = 2
        
    if t2 > 0:
        p2 = 1
    elif t2 < 0:
        p2 = 2
        
    if t3 > 0:
        p3 = 1
    elif t3 < 0:
        p3 = 2
    
    for em in ttt:
        if em[0] == p1 and em[1] == p2 and em[2] == p3:
            em[3] = em[3]+1
            return
    
    ttt.append([p1,p2,p3,1])

def vbvb3_neu(x3):
	global i_ix
        global indices2n
	global indices3

	footer = ""
	verts = float(len(x2))
	
	for em in x3:
		print em
	start = timer()
	for index,gh in enumerate(x3,start=1):
		
		i2n = []
		t1 = timer()

		i2n.append(binaersuche_rekursiv(indices2n,1,gh,0,len(indices2n)-1))
		
		if indices2n[i2n[0]+1][1] == gh:
			i2n.append(i2n[0]+1)
		if indices2n[i2n[0]+2][1] == gh:
			i2n.append(i2n[0]+2)
		if indices2n[i2n[0]-1][1] == gh:
			i2n.append(i2n[0]-1)
		if indices2n[i2n[0]-2][1] == gh:
			i2n.append(i2n[0]-2)
		
		
		p08=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[0]][0], 0, len(i_ix)-1)
		for em in i_ix[p08][1]:
			if indices3[em][2] == indices2n[i2n[0]][2]:
				p0 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]
			if indices3[em][2] == indices2n[i2n[0]][3]:
				p1 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]

		p18=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[1]][0], 0, len(i_ix)-1)
		for em in i_ix[p18][1]:
			if indices3[em][2] == indices2n[i2n[1]][2]:
				p2 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]
			if indices3[em][2] == indices2n[i2n[1]][3]:
				p3 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]

		p28=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[2]][0], 0, len(i_ix)-1)
		for em in i_ix[p28][1]:
			if indices3[em][2] == indices2n[i2n[2]][2]:
				p4 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]
			if indices3[em][2] == indices2n[i2n[2]][3]:
				p5 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]
        
		a = p0[1:]
		b = p1[1:]
		c = [a[0]+indices2n[i2n[0]][4],a[1]+indices2n[i2n[0]][5]]
		d = [b[0]+indices2n[i2n[0]][4],b[1]+indices2n[i2n[0]][5]]	

		e = p2[1:]
		f = p3[1:]
		g = [e[0]+indices2n[i2n[1]][4],e[1]+indices2n[i2n[1]][5]]
		h = [f[0]+indices2n[i2n[1]][4],f[1]+indices2n[i2n[1]][5]]

		i = p4[1:]
		j = p5[1:]
		k = [i[0]+indices2n[i2n[2]][4],i[1]+indices2n[i2n[2]][5]]
		l = [j[0]+indices2n[i2n[2]][4],j[1]+indices2n[i2n[2]][5]]

		s1 = sp(a,c,i,k)
		#if s1 == None:
		s12 = sp(a,c,j,l)
		#if s1 == None:
		s13 = sp(b,d,i,k)
		#if s1 == None:
		s14 = sp(b,d,j,l)

		s2 = sp(a,c,e,g)
		#if s2 == None:
		s22 = sp(a,c,f,h)
		#if s2 == None:
		s23 = sp(b,d,e,g)
		#if s2 == None:
		s24 = sp(b,d,f,h)
		
		s3 = sp(e,g,i,k)
		#if s3 == None:
		s32 = sp(e,g,j,l)
		#if s3 == None:
		s33 = sp(f,h,i,k)
		#if s3 == None:
		s34 = sp(f,h,j,l)

		print s1
		print s12
		print s13
		print s14
		print '---------'
		print s2
		print s22
		print s23
		print s24
		print '---------'
		print s3
		print s32
		print s33
		print s34

		draw([[a,b,d,c],[e,f,h,g],[i,j,l,k]],[s1, s2, s3])
		#draw([[a,b,d,c]],[])
		#draw([[e,f,h,g]],[])
		#draw([[i,j,l,k]],[])
		#draw([[a,b,d,c],[i,j,l,k]],[])

		if index % 10 == 0:
			tmp =  timer()
			footer = str(round(index / (tmp - start),2)) + "k/s"
		#progressbar("vbvb3",index/verts,footer)
		#return

	end = timer()
	print str(round(end - start,1))+"s"

def vbvb2_neu(x2):
	global i_ix
        global indices2n
	global indices3
	 
	sp_sta = [0,0,0,0]
	footer = ""
	verts = float(len(x2))

	start = timer()
	for index,gh in enumerate(x2,start=1):
		if index % 10 == 0:
			tmp =  timer()
			footer = str(round(index / (tmp - start),2)) + "k/s"

		progressbar("vbvb2",index/verts,footer)
		
		t1 = timer()
		i2n = []

		i2n.append(binaersuche_rekursiv(indices2n,1,gh,0,len(indices2n)-1))
		if indices2n[i2n[0]+1][1] == gh:
			i2n.append(i2n[0]+1)
		else:
			i2n.append(i2n[0]-1)                        
                	                     
		if indices2n[i2n[0]][4] == -indices2n[i2n[1]][4] and indices2n[i2n[0]][5] == -indices2n[i2n[1]][5]:
			continue

		p08=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[0]][0], 0, len(i_ix)-1)
		for em in i_ix[p08][1]:
			if indices3[em][2] == indices2n[i2n[0]][2]:
				p0 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]
			if indices3[em][2] == indices2n[i2n[0]][3]:
				p1 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]
		p18=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[1]][0], 0, len(i_ix)-1)
		for em in i_ix[p18][1]:
			if indices3[em][2] == indices2n[i2n[1]][2]:
				p2 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]
			if indices3[em][2] == indices2n[i2n[1]][3]:
				p3 = vertex[binaersuche_rekursiv(vertex, 0, indices3[em][1], 0, len(vertex)-1)]		

		a = p0[1:]
		b = p1[1:]
		c = [a[0]+indices2n[i2n[0]][4],a[1]+indices2n[i2n[0]][5]]
		d = [b[0]+indices2n[i2n[0]][4],b[1]+indices2n[i2n[0]][5]]	
		
		e = p2[1:]
		f = p3[1:]
		g = [e[0]+indices2n[i2n[1]][4],e[1]+indices2n[i2n[1]][5]]
		h = [f[0]+indices2n[i2n[1]][4],f[1]+indices2n[i2n[1]][5]]
				
		s = sp(b, d, f, h)
		#print s
		if s != None:
			i = insertV(s[0], s[1])
			[asd,seq] = update_indices2(indices3, i, p1[0], indices2n[i2n[0]][0], i, p3[0], indices2n[i2n[1]][0])
			l_indices = len(indices3)
			i_ix[asd][1].append(l_indices)
			i_ix[asd][1].append(l_indices+1)
			i_ix[asd][1].append(l_indices+2)
			indices3.append([indices2n[i2n[0]][0], i, seq+1])
			indices3.append([indices2n[i2n[0]][0], p0[0], seq+2])
			indices3.append([indices2n[i2n[0]][0], p2[0], seq+3])
			sp_sta[3] = sp_sta[3] + 1
			continue

		s = sp(a, c, e, g)
		#print s
		if s != None:
			i = insertV(s[0], s[1])
			[asd,seq] = update_indices2(indices3, i, p0[0], indices2n[i2n[0]][0], i, p2[0], indices2n[i2n[1]][0])
			l_indices = len(indices3)
			i_ix[asd][1].append(l_indices)
			i_ix[asd][1].append(l_indices+1)
			i_ix[asd][1].append(l_indices+2)
			indices3.append([indices2n[i2n[0]][0], i, seq+1])
			indices3.append([indices2n[i2n[0]][0], p1[0], seq+2])
			indices3.append([indices2n[i2n[0]][0], p3[0], seq+3])
			sp_sta[0] = sp_sta[0] + 1
			continue
		
		s = sp(a, c, f, h)
		#print s
		if s != None:
			i = insertV(s[0], s[1])
			[asd,seq] = update_indices2(indices3, i, p0[0], indices2n[i2n[0]][0], i, p3[0], indices2n[i2n[1]][0])
			l_indices = len(indices3)
			i_ix[asd][1].append(l_indices)
			i_ix[asd][1].append(l_indices+1)
			i_ix[asd][1].append(l_indices+2)
			indices3.append([indices2n[i2n[0]][0], i, seq+1])
			indices3.append([indices2n[i2n[0]][0], p1[0], seq+2])
			indices3.append([indices2n[i2n[0]][0], p2[0], seq+3])
			sp_sta[1] = sp_sta[1] + 1
			continue

		s = sp(b, d, e, g)
		#print s
		if s != None:
			i = insertV(s[0], s[1])
			[asd,seq] = update_indices2(indices3, i, p1[0], indices2n[i2n[0]][0], i, p2[0], indices2n[i2n[1]][0])
			l_indices = len(indices3)
			i_ix[asd][1].append(l_indices)
			i_ix[asd][1].append(l_indices+1)
			i_ix[asd][1].append(l_indices+2)
			indices3.append([indices2n[i2n[0]][0], i, seq+1])
			indices3.append([indices2n[i2n[0]][0], p0[0], seq+2])
			indices3.append([indices2n[i2n[0]][0], p3[0], seq+3])
			sp_sta[2] = sp_sta[2] + 1
			continue
		#return

		

	end = timer()
	print "sp_sta: " + str(sp_sta)
	print str(round(end - start,1))+"s"

def update_indices2(indices, i0, i10, L10 , i1, i11, L11):
	global i_ix
	seq=0
	
	ii10=binaersuche_rekursiv(i_ix, 0, L10, 0, len(i_ix)-1)
	ii11=binaersuche_rekursiv(i_ix, 0, L11, 0, len(i_ix)-1)
	
	for em in i_ix[ii10][1]:
		if indices[em][2]>seq:
			seq=indices[em][2]
		if indices[em][1]==i10:
			indices[em][1]=i0

	for em in i_ix[ii11][1]:
		if indices[em][1]==i11:
			indices[em][1]=i1	

	return [ii10,seq]

def draw(poly,points):
	fig, ax = plt.subplots()
	Path = mpath.Path
	path_data2 = []
	#print "#####"
	#print poly[0]
	#print "#####"
	for em1 in poly:
		#print em1[0]
		path_data2.append((Path.MOVETO, em1[0]))
		for ix,em2 in enumerate(em1,start=0):
			if ix == 0:
				continue
			#print str(ix) + ": " + str(em2)
			path_data2.append((Path.LINETO, em2))
		path_data2.append((Path.CLOSEPOLY, em1[0]))
		#print em1[0]
		#print "------------"
	codes, verts = zip(*path_data2)
	path = mpath.Path(verts, codes)

	# plot control points and connecting lines
	x, y = zip(*path.vertices)
	line, = ax.plot(x, y, 'g.-')
	
	pointx = []
	pointy = []
	for em in points:
		if em != None:
			pointx.append(em[0])
			pointy.append(em[1])

	ax.plot(pointx, pointy, 'o')
	ax.grid()
	ax.axis('equal')
	plt.show()

def color(c):
    global config_farbe
    #CF_ID,R,G,B,CF_BEZ
    for em in config_farbe:
        if em[4] == c:
            return em[0]

    cf_id = len(config_farbe)
    config_farbe.append([cf_id,1,0,0,c])
    config_farbe.sort(key=lambda x: x[0])
    
    return cf_id
	
                        
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

def test():
    g_x = 200000.0
    g_y = 20000.0

    global vertex
    vertex = []
    vertex.append([100, 0.0,0.0])
    vertex.append([101, 0.3,0.0])
    vertex.append([102, 0.2,-0.2])
    vertex.append([103, 0.3,0.2])
    
    global v_id
    v_id = 10000
    
    global indices2n
    indices2n = []
    #(W_L_ID,W_V_ID,I_SEQ1,I_SEQ2,W_R_LON,W_R_LAT,W_SEQ)
    indices2n.append([1, 100, None, None, None, None, 0])
    indices2n.append([1, 101, None, None, None, None, 1])
    #indices2n.append([1, 101, None, None, None, None, 2])
    #indices2n.append([1, 102, None, None, None, None, 3])
    #indices2n.append([1, 102, None, None, None, None, 4])
    #indices2n.append([1, 103, None, None, None, None, 5])

    global lines3
    lines3 = []
    #(L_ID,L_COUNT,L_COUNT2,L_CF_ID,L_LVL)
    lines3.append((1, "asd", 3))
    #lines.append((2, "asd", 3))
    #lines.append((3, "asd", 3))

    for em in vertex:
	em[1] = em[1] + g_x
	em[2] = em[2] + g_y

#draw([],(1,2))
print "Polygone/Wege"
start = timer()
p = OSMParser(concurrency=1, ways_callback=myways, relations_callback=myrel) #ways_tag_filter=tag_filter,
p.parse(PBF)
#p = OSMParser(concurrency=1, relations_callback=myrel) #ways_tag_filter=tag_filter,
#p.parse(PBF)
end = timer()
print str(round(end - start,1))+"s"


start = timer()
#vertex[] erzeugen
tmp.sort()
old = -1

for em in tmp:
    if em != old:
        vertex.append((em,None,None))
    old = em
v_id = tmp[len(tmp)-1]+1
tmp = None

#test()

verts = float(len(vertex))
p = OSMParser(concurrency=1, coords_callback=coords_callback)
p.parse(PBF)
end = timer()
print str(round(end - start,1))+"s"

if len(indices2) > 0:
	start = timer()
	vbvb4()
	end = timer()
	print str(round(end - start,1))+"s"

#vertex_ix erzeugen
start = timer()
#sortiert nach X
vertex.sort(key=lambda x: x[1])
for n,em in enumerate(vertex,start=0):
    insertVIX(int(em[1])>>RSHIFT, int(em[2])>>RSHIFT, n)
    progressbar("v_ix",(n+1)/verts)
#sortiert nach V_ID
vertex.sort(key=lambda x: x[0])
end = timer()
print str(round(end - start,1))+"s"

start = timer()
vbvb1()
end = timer()
print str(round(end - start,1))+"s"
 
#sortiert nach W_V_ID
indices2n.sort(key=lambda x: x[1])

#sortiert nach I_L_ID
indices3.sort(key=lambda x: x[0])



count = 0
old_em = [-1,-1]
x2 = []
x3 = []
x4 = []
#index,gh in enumerate(x2,start=1):
for index,em in enumerate(indices2n,start=0):
	if old_em == em[1]:
		count = count + 1
	else:
		if count == 1:
			x2.append(old_em)
		elif count == 2:
			x3.append(old_em)
			print "asd"
		#elif count == 3:
			#x4.append(old_em)
		count = 0
	old_em = em[1]

i_ix = createIX(indices3,0)
vbvb2_neu(x2)
vbvb3_neu(x3)

#start = timer()
#vbvb3_neu(x3)
#end = timer()
#print str(round(end - start,1))+"s"

start = timer()
for i,em in enumerate(lines2):
    lines2[i][1] = color(em[1])
for i,em in enumerate(lines3):
    lines3[i][1] = color(em[1])
end = timer()
print str(round(end - start,1))+"s"


fillDB("sit2d_6.db",vertex,indices3,indices2,indices2n,config_farbe,lines3,lines2)

copyfile("sit2d_6.db", "sit2d_6_lvl3.db")
copyfile("sit2d_6.db", "sit2d_6_lvl2.db")
copyfile("sit2d_6.db", "sit2d_6_lvl1.db")

trDB("sit2d_6_lvl1.db", 1)
trDB("sit2d_6_lvl2.db", 2)
trDB("sit2d_6_lvl3.db", 3)
