     
def vbvb3_neu(x3):
	# wie vbvb3
	# p[0-2]_d: 0 -> 1 durch wechsel der a's
	global i_ix
        global vertex
        ttt = [0]
        #sql_update = "update indices set i_v_id=? where i_l_id=? and i_v_id=?"
	#x = sqc.execute("SELECT w_v_id FROM indices2n group by w_v_id having count(*)=3").fetchall()
	
	verts = float(len(x3))
	for index,gh in enumerate(x3,start=1):
                #progressbar("vbvb3",index/verts)
	        punkt = vertex[binaersuche_rekursiv(vertex, 0, gh[1], 0, len(vertex)-1)][1:]
                
           	i2n = []
		i1 = []
		i2 = []
		v = []
		p2 = []
		tmp =[]

		i2n.append(binaersuche_rekursiv(indices2n,1,gh[1],0,len(indices2n)-1))
		if indices2n[i2n[0]+1][1] == gh[1]:
			i2n.append(i2n[0]+1)
		if indices2n[i2n[0]-1][1] == gh[1]:
			i2n.append(i2n[0]-1)
		if indices2n[i2n[0]+2][1] == gh[1]:
			i2n.append(i2n[0]+2)
		if indices2n[i2n[0]-2][1] == gh[1]:
			i2n.append(i2n[0]-2)
		
		tmp.append(indices2n[i2n[0]])
		tmp.append(indices2n[i2n[1]])
		tmp.append(indices2n[i2n[2]])
		tmp.sort(key=lambda x: (x[0],x[6]))		
		
	        p0_d = tmp[0][6] % 2
                p1_d = tmp[1][6] % 2
                p2_d = tmp[2][6] % 2
		
		p0 = [punkt[0]+tmp[0][4],punkt[1]+tmp[0][5]]
		p1 = [punkt[0]+tmp[1][4],punkt[1]+tmp[1][5]]
                p2 = [punkt[0]+tmp[2][4],punkt[1]+tmp[2][5]]
                                
		t1 = aufLinie(p0, punkt, p1)
                t2 = aufLinie(p1, punkt, p2)
                t3 = aufLinie(p0, punkt, p2)
	
                if t1 == 0 or t2 == 0 or t3 == 0:
                    continue
                if t1 == 0 and t2 == 0:
                    continue
                if t2 == 0 and t3 == 0:
                    continue
                if t1 == 0 and t3 == 0:
                    continue
               
		p08=binaersuche_rekursiv(i_ix, 0, tmp[0][0], 0, len(i_ix)-1)
		for em in i_ix[p08][1]:
			if indices[em][2] == tmp[0][2]:
				i1.append(em)
			if indices[em][2] == tmp[0][3]:
				i2.append(em)
		p18=binaersuche_rekursiv(i_ix, 0, tmp[1][0], 0, len(i_ix)-1)
		for em in i_ix[p18][1]:
			if indices[em][2] == tmp[1][2]:
				i1.append(em)
			if indices[em][2] == tmp[1][3]:
				i2.append(em)
		p28=binaersuche_rekursiv(i_ix, 0, tmp[2][0], 0, len(i_ix)-1)
		for em in i_ix[p28][1]:
			if indices[em][2] == tmp[2][2]:
				i1.append(em)
			if indices[em][2] == tmp[2][3]:
				i2.append(em)
		######################
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[1]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[1]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[2]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[2]][1],0,len(vertex)-1)])

		p = []
		p.append([indices[i1[0]][1], indices[i2[0]][1], v[0][1], v[0][2], v[2][1], v[2][2], tmp[0][4], tmp[0][5], tmp[0][0],tmp[0][6]])
		p.append([indices[i1[1]][1], indices[i2[1]][1], v[1][1], v[1][2], v[3][1], v[3][2], tmp[1][4], tmp[1][5], tmp[1][0],tmp[1][6]])
		p.append([indices[i1[2]][1], indices[i2[2]][1], v[4][1], v[4][2], v[5][1], v[5][2], tmp[2][4], tmp[2][5], tmp[2][0],tmp[2][6]])
                #################################
		if p0_d == 0:
	                a3 = [p[0][2],p[0][3],p[0][0]]
	                a1 = [p[0][4],p[0][5],p[0][1]]
		else:
	                a1 = [p[0][2],p[0][3],p[0][0]]
	                a3 = [p[0][4],p[0][5],p[0][1]]

                a2 = [a1[0]+p[0][6],a1[1]+p[0][7]]
                a4 = [a3[0]+p[0][6],a3[1]+p[0][7]]

		if p1_d == 0:
		        a7 = [p[1][2],p[1][3],p[1][0]]
		        a5 = [p[1][4],p[1][5],p[1][1]]                        
		else:
	                a5 = [p[1][2],p[1][3],p[1][0]]
		        a7 = [p[1][4],p[1][5],p[1][1]]   
     
                a6 = [a5[0]+p[1][6],a5[1]+p[1][7]]
                a8 = [a7[0]+p[1][6],a7[1]+p[1][7]]
       
		if p2_d == 0:
	                a9  = [p[2][2],p[2][3],p[2][0]]
        	        a11 = [p[2][4],p[2][5],p[2][1]]
		else:
	                a11 = [p[2][2],p[2][3],p[2][0]]
        	        a9  = [p[2][4],p[2][5],p[2][1]]

		a10 = [a9[0]+p[2][6],a9[1]+p[2][7]]                
                a12 = [a11[0]+p[2][6],a11[1]+p[2][7]]
                                        
		if t1 > 0 and t2 > 0 and t3 < 0:
                        s1 = sp(a1, a2, a7, a8)
                        i1 = insertV(s1[0], s1[1])

			s2 = sp(a3, a4, a11, a12)
                        i2 = insertV(s2[0], s2[1])

			s3 = sp(a5, a6, a9, a10)
                        i3 = insertV(s3[0], s3[1])

			[c,seq] = update_indices(i_ix, i2, a3[2], p[0][8], i2, a11[2], p[2][8])
			[c,seq] = update_indices(i_ix, i3, a5[2], p[1][8], i3,  a9[2], p[2][8])
			[c,seq] = update_indices(i_ix, i1, a1[2], p[0][8], i1,  a7[2], p[1][8])
                elif t1 < 0 and t2 < 0 and t3 > 0:
			s1 = sp(a7, a8, a11, a12)
                        i1 = insertV(s1[0], s1[1])

			s2 = sp(a3, a4, a5, a6)
                        i2 = insertV(s2[0], s2[1])

			s3 = sp(a1, a2, a9, a10)
                        i3 = insertV(s3[0], s3[1])

			[c,seq] = update_indices(i_ix, i2, a5[2], p[1][8], i2, a3[2], p[0][8])
			[c,seq] = update_indices(i_ix, i3, a5[2], p[1][8], i3, a9[2], p[2][8])
			[c,seq] = update_indices(i_ix, i1, a11[2], p[2][8], i1, a7[2], p[1][8])
		if 1==1:
			print gh

			print p0_d
	                print p1_d
	                print p2_d
			
	                print punkt
               
			print p0
			print p1
			print p2
			print "t1: " + str(t1) + " t2: " + str(t2) + " t3: " + str(t3)
	
			print "###"
                	print a1
			print a2
			print a3
			print a4
			print "###"
                	print a5
			print a6
			print a7
			print a8
			print "###"
			print a9
			print a10
			print a11
			print a12
			print "###"

                #print '######################'

def vbvb3(x3):
	global i_ix
        global vertex
        ttt = [0]
        #sql_update = "update indices set i_v_id=? where i_l_id=? and i_v_id=?"
	#x = sqc.execute("SELECT w_v_id FROM indices2n group by w_v_id having count(*)=3").fetchall()
	
	verts = float(len(x3))
	for index,gh in enumerate(x3,start=1):
                print "###########"
                #progressbar("vbvb3",index/verts)
	
                punkt = vertex[binaersuche_rekursiv(vertex, 0, gh[1], 0, len(vertex)-1)][1:]
                
		print gh
		
           	i2n = []
		i1 = []
		i2 = []
		v = []
		p2 = []
		tmp =[]

		i2n.append(binaersuche_rekursiv(indices2n,1,gh[1],0,len(indices2n)-1))
		if indices2n[i2n[0]+1][1] == gh[1]:
			i2n.append(i2n[0]+1)
		if indices2n[i2n[0]-1][1] == gh[1]:
			i2n.append(i2n[0]-1)
		if indices2n[i2n[0]+2][1] == gh[1]:
			i2n.append(i2n[0]+2)
		if indices2n[i2n[0]-2][1] == gh[1]:
			i2n.append(i2n[0]-2)
		
		tmp.append(indices2n[i2n[0]])
		tmp.append(indices2n[i2n[1]])
		tmp.append(indices2n[i2n[2]])
				
		#tmp.sort(key=lambda x: (x[0],x[6]))

                p0_d = tmp[0][6] % 2
                p1_d = tmp[1][6] % 2
                p2_d = tmp[2][6] % 2
		print p0_d
                print p1_d
                print p2_d
		print '-->'
		if p0_d == 0 and p1_d == 1 and p2_d == 0:
			swap = tmp[0]
			tmp[0] = tmp[1]
			tmp[1] = swap
		elif p0_d == 0 and p1_d == 0 and p2_d == 1:
			swap = tmp[0]
			tmp[0] = tmp[2]
			tmp[2] = swap

		p0_d = tmp[0][6] % 2
                p1_d = tmp[1][6] % 2
                p2_d = tmp[2][6] % 2
                
                print p0_d
                print p1_d
                print p2_d
		
                print punkt
		p0 = [punkt[0]+tmp[0][4],punkt[1]+tmp[0][5]]
		p1 = [punkt[0]+tmp[1][4],punkt[1]+tmp[1][5]]
                p2 = [punkt[0]+tmp[2][4],punkt[1]+tmp[2][5]]
                
		print p0
		print p1
		print p2
                
		t1 = aufLinie(p0, punkt, p1)
                t2 = aufLinie(p1, punkt, p2)
                t3 = aufLinie(p0, punkt, p2)
	
                if t1 == 0 and t2 == 0 and t3 == 0:
                    continue
                if t1 == 0 and t2 == 0:
                    continue
                if t2 == 0 and t3 == 0:
                    continue
                if t1 == 0 and t3 == 0:
                    continue
               
              
		print "t1: " + str(t1) + " t2: " + str(t2) + " t3: " + str(t3)
		
                p08=binaersuche_rekursiv(i_ix, 0, tmp[0][0], 0, len(i_ix)-1)
		for em in i_ix[p08][1]:
			if indices[em][2] == tmp[0][2]:
				i1.append(em)
			if indices[em][2] == tmp[0][3]:
				i2.append(em)
		p18=binaersuche_rekursiv(i_ix, 0, tmp[1][0], 0, len(i_ix)-1)
		for em in i_ix[p18][1]:
			if indices[em][2] == tmp[1][2]:
				i1.append(em)
			if indices[em][2] == tmp[1][3]:
				i2.append(em)
		p28=binaersuche_rekursiv(i_ix, 0, tmp[2][0], 0, len(i_ix)-1)
		for em in i_ix[p28][1]:
			if indices[em][2] == tmp[2][2]:
				i1.append(em)
			if indices[em][2] == tmp[2][3]:
				i2.append(em)
		######################
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[1]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[1]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[2]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[2]][1],0,len(vertex)-1)])

		p = []
		p.append([indices[i1[0]][1], indices[i2[0]][1], v[0][1], v[0][2], v[2][1], v[2][2], tmp[0][4], tmp[0][5], tmp[0][0],tmp[0][6]])
		p.append([indices[i1[1]][1], indices[i2[1]][1], v[1][1], v[1][2], v[3][1], v[3][2], tmp[1][4], tmp[1][5], tmp[1][0],tmp[1][6]])
		p.append([indices[i1[2]][1], indices[i2[2]][1], v[4][1], v[4][2], v[5][1], v[5][2], tmp[2][4], tmp[2][5], tmp[2][0],tmp[2][6]])
                #################################
                a1 = [p[0][2],p[0][3],p[0][0]]
                a2 = [p[0][2]+p[0][6],p[0][3]+p[0][7]]
                a3 = [p[0][4],p[0][5],p[0][1]]
                a4 = [p[0][4]+p[0][6],p[0][5]+p[0][7]]
                print "###"
                print a1
		print a2
		print a3
		print a4
		print "###"
                a5 = [p[1][2],p[1][3],p[1][0]]
                a6 = [p[1][2]+p[1][6],p[1][3]+p[1][7]]
                a7 = [p[1][4],p[1][5],p[1][1]]
                a8 = [p[1][4]+p[1][6],p[1][5]+p[1][7]]
                print a5
		print a6
		print a7
		print a8
		print "###"
		if p2_d == 0:
	                a9  = [p[2][2],p[2][3],p[2][0]]
        	        a11 = [p[2][4],p[2][5],p[2][1]]
		else:
	                a11 = [p[2][2],p[2][3],p[2][0]]
        	        a9  = [p[2][4],p[2][5],p[2][1]]


		a10 = [a9[0]+p[2][6],a9[1]+p[2][7]]                
                a12 = [a11[0]+p[2][6],a11[1]+p[2][7]]
                print a9
		print a10
		print a11
		print a12
		print "###"
                                        
                t1 = aufLinie(p0, punkt, p1)
                t2 = aufLinie(p1, punkt, p2)
                t3 = aufLinie(p0, punkt, p2)

                if not((p0_d == 1 and p1_d == 0 and p2_d == 0) or (p0_d == 1 and p1_d == 0 and p2_d == 1)or(p0_d == 1 and p1_d == 0 and p2_d == 1)):
			print "next"
			continue
               
                if t1 == 0:
                        if t2 < 0:
                            s1 = sp(a3, a4, a9, a10)
                            i1 = insertV(s1[0], s1[1])
                            
                            s2 = sp(a3, a4, a11, a12)
                            i2 =  insertV(s2[0], s2[1])
                            
                            seq = update_indices(i_ix, i1, a9[2], p[2][8], i2, a11[2], p[2][8])
                        else:
                            s1 = sp(a1, a2, a9, a10)
                            i1 =  insertV(s1[0], s1[1])
                            
                            s2 = sp(a1, a2, a11, a12)
                            i2 =  insertV(s2[0], s2[1])
                            
                            seq = update_indices(i_ix, i1, a9[2], p[2][8], i2, a11[2], p[2][8])
	        elif t2 == 0:
                        if t1 > 0:
			    s1 = sp(a1, a2, a5, a6)
                            i1 =  insertV(s1[0], s1[1])
                            
                            s2 = sp(a3, a4, a5, a6)
                            i2 =  insertV(s2[0], s2[1])
                            
                            seq = update_indices(i_ix, i1, a1[2], p[0][8], i2, a3[2], p[0][8])
                        else:
			    s1 = sp(a1, a2, a7, a8)
                            i1 =  insertV(s1[0], s1[1])
                            
                            s2 = sp(a3, a4, a7, a8)
                            i2 =  insertV(s2[0], s2[1])
                            
                            seq = update_indices(i_ix, i1, a1[2], p[0][8], i2, a3[2], p[0][8])
                elif t3 == 0:
                        if t2 < 0:
                            s1 = sp(a1, a2, a7, a8)
                            i1 = insertV(s1[0], s1[1])
                            
                            s2 = sp(a5, a6, a9, a10)
                            i2 =  insertV(s2[0], s2[1])
                            
                            seq = update_indices(i_ix, i2, a5[2], p[1][8], i1, a7[2], p[1][8])
                        else:
                            s1 = sp(a3, a4, a5, a6)
                            i1 =  insertV(s1[0], s1[1])
                            
                            s2 = sp(a7, a8, a11, a12)
                            i2 =  insertV(s2[0], s2[1])
                            
                            seq = update_indices(i_ix, i1, a5[2], p[1][8], i2, a7[2], p[1][8])
                elif (t1 < 0 and t2 < 0 and t3 > 0) or (t1 < 0 and t2 > 0 and t3 > 0):
                        # neu
			print "(t1 < 0 and t2 < 0 and t3 > 0) or (t1 < 0 and t2 > 0 and t3 > 0)"
                        s1 = sp(a3, a4, a7, a8)
                        i1 = insertV(s1[0], s1[1])

			s2 = sp(a1, a2, a9, a10)
                        i2 = insertV(s2[0], s2[1])

			s3 = sp(a5, a6, a11, a12)
                        i3 = insertV(s3[0], s3[1])

			[c,seq] = update_indices(i_ix, i2, a1[2], p[0][8], i2, a9[2], p[2][8])
			[c,seq] = update_indices(i_ix, i3, a5[2], p[1][8], i3, a11[2], p[2][8])
			[c,seq] = update_indices(i_ix, i1, a3[2], p[0][8], i1, a7[2], p[1][8])
                
			# Keil
			#l_indices = len(indices)
			#i_ix[c][1].append(l_indices)
			#i_ix[c][1].append(l_indices+1)
			#i_ix[c][1].append(l_indices+2)
			#indices.append([p[0][8], i1, seq+1])
			#indices.append([p[0][8], i2, seq+2])
			#indices.append([p[0][8], i3, seq+3])    
		elif (t1 > 0 and t2 > 0) or (t1 < 0 and t2 < 0):
			#neu	
			print "(t1 > 0 and t2 > 0) or (t1 < 0 and t2 < 0)"	  
			s1 = sp(a1, a2, a5, a6)
                        i1 = insertV(s1[0], s1[1])

			s2 = sp(a3, a4, a11, a12)
                        i2 = insertV(s2[0], s2[1])

			s3 = sp(a7, a8, a9, a10)
                        i3 = insertV(s3[0], s3[1])

			[c,seq] = update_indices(i_ix, i2, a3[2], p[0][8], i2, a11[2], p[2][8])
			[c,seq] = update_indices(i_ix, i3, a7[2], p[1][8], i3, a9[2], p[2][8])
			[c,seq] = update_indices(i_ix, i1, a1[2], p[0][8], i1, a5[2], p[1][8])

			# Keil
			#l_indices = len(indices)
			#i_ix[c][1].append(l_indices)
			#i_ix[c][1].append(l_indices+1)
			#i_ix[c][1].append(l_indices+2)
			#indices.append([p[0][8], i1, seq+1])
			#indices.append([p[0][8], i2, seq+2])
			#indices.append([p[0][8], i3, seq+3])
                else:
			print "else"
                #print '######################'


def vbvb2(x2):
	global i_ix
        
	verts = float(len(x2))
	#print "gh: " + str(len(x2))
	#for em in x2:
	#	print em
	for index,gh in enumerate(x2,start=1):
		#if index != 2:
		#	continue
		#print "##############"
		a1 = None
		a2 = None
		a3 = None
		a4 = None
		a5 = None
		a6 = None
		a7 = None
		a8 = None
                
             	i2n = []	
		i2n.append(binaersuche_rekursiv(indices2n,1,gh[1],0,len(indices2n)-1))
		if indices2n[i2n[0]+1][1] == gh[1]:
			i2n.append(i2n[0]+1)
		else:
			i2n.append(i2n[0]-1)                        
                
                p0_d = indices2n[i2n[0]][6] % 2
                p1_d = indices2n[i2n[1]][6] % 2
                #print p0_d
                #print p1_d
                                
                
                if p1_d == 0 and p0_d == 1:
                    tmp = i2n[0]
                    i2n[0] = i2n[1]
                    i2n[1] = tmp
                    p0_d = indices2n[i2n[0]][6] % 2
                    p1_d = indices2n[i2n[1]][6] % 2
                    #print "swap"
                    
                #print p0_d
                #print p1_d
                
                #print indices2n[i2n[0]]
                #print indices2n[i2n[1]]       
                
		punkt = vertex[binaersuche_rekursiv(vertex, 0, gh[1], 0, len(vertex)-1)][1:]
		p0 = [punkt[0]+indices2n[i2n[0]][4],punkt[1]+indices2n[i2n[0]][5]]
		p1 = [punkt[0]+indices2n[i2n[1]][4],punkt[1]+indices2n[i2n[1]][5]]
		
		#print p0
		#print punkt
		#print p1
                                              
                t = aufLinie(p0, punkt, p1)		
                
		if t == 0:
			continue

		#print t

		i1 = []
		i2 = []
		p08=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[0]][0], 0, len(i_ix)-1)
		for em in i_ix[p08][1]:
			if indices[em][2] == indices2n[i2n[0]][2]:
				i1.append(em)
			if indices[em][2] == indices2n[i2n[0]][3]:
				i2.append(em)
		p18=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[1]][0], 0, len(i_ix)-1)
		for em in i_ix[p18][1]:
			if indices[em][2] == indices2n[i2n[1]][2]:
				i1.append(em)
			if indices[em][2] == indices2n[i2n[1]][3]:
				i2.append(em)
		
		v = []
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[1]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[1]][1],0,len(vertex)-1)])

		p = []
		p.append([indices[i1[0]][1], indices[i2[0]][1], v[0][1], v[0][2], v[2][1], v[2][2], indices2n[i2n[0]][4], indices2n[i2n[0]][5], indices2n[i2n[0]][0],indices2n[i2n[0]][6]])
		p.append([indices[i1[1]][1], indices[i2[1]][1], v[1][1], v[1][2], v[3][1], v[3][2], indices2n[i2n[1]][4], indices2n[i2n[1]][5], indices2n[i2n[1]][0],indices2n[i2n[1]][6]])
		#print p[0]
		#print p[1]
		if p0_d + p1_d == 2:
			a3 = [p[0][2],p[0][3],p[0][0]]
        	       	a1 = [p[0][4],p[0][5],p[0][1]]
		else:
			a1 = [p[0][2],p[0][3],p[0][0]]
        	       	a3 = [p[0][4],p[0][5],p[0][1]]

		a2 = [a1[0]+p[0][6],a1[1]+p[0][7]]
               	a4 = [a3[0]+p[0][6],a3[1]+p[0][7]]                	

		#print ""                
		#print a1
		#print a2
		#print a3
		#print a4

		if p0_d + p1_d == 0:
	              	a7 = [p[1][2],p[1][3],p[1][0]]
	              	a5 = [p[1][4],p[1][5],p[1][1]]

		else:
	              	a5 = [p[1][2],p[1][3],p[1][0]]
	              	a7 = [p[1][4],p[1][5],p[1][1]]

                a6 = [a5[0]+p[1][6],a5[1]+p[1][7]]
                a8 = [a7[0]+p[1][6],a7[1]+p[1][7]]
		#print a5
		#print a6
		#print a7
		#print a8
                #print ""
               
                #if p0_d + p1_d == 0:
                #    print "next"
                #    continue
                try:                           
		    if t < 0:
			s = sp(a1, a2, a5, a6)
			i = insertV(s[0], s[1])
			                        
                        [asd,seq] = update_indices(i_ix, i, a1[2], p[0][8], i, a5[2], p[1][8])
                        
			# Keil
			l_indices = len(indices)
			i_ix[asd][1].append(l_indices)
			i_ix[asd][1].append(l_indices+1)
			i_ix[asd][1].append(l_indices+2)
			indices.append([p[0][8], i, seq+1])
			indices.append([p[0][8], a3[2], seq+2])
			indices.append([p[0][8], a7[2], seq+3])
                    elif t > 0:
			s = sp(a3, a4, a7, a8)
			i = insertV(s[0], s[1])
                        
                        [asd,seq] = update_indices(i_ix, i, a3[2], p[0][8], i, a7[2], p[1][8])

                        # Keil
			l_indices = len(indices)
			i_ix[asd][1].append(l_indices)
			i_ix[asd][1].append(l_indices+1)
			i_ix[asd][1].append(l_indices+2)
			indices.append([p[0][8], i, seq+1])
			indices.append([p[0][8], a1[2], seq+2])
			indices.append([p[0][8], a5[2], seq+3])
		except:
			raise
			#continue
                #for em in indices:
                #    print em
		
		progressbar("vbvb2",index/verts)
			
def vbvb2_neu(x2):
	global i_ix
        
	verts = float(len(x2))
	print "gh: " + str(len(x2))
	for em in x2:
		print em
	for index,gh in enumerate(x2,start=1):
		print index
		print gh
		return
		#if index != 2:
		#	continue
		#print "##############"
		a1 = None
		a2 = None
		a3 = None
		a4 = None
		a5 = None
		a6 = None
		a7 = None
		a8 = None
                
             	i2n = []	
		i2n.append(binaersuche_rekursiv(indices2n,1,gh[1],0,len(indices2n)-1))
		if indices2n[i2n[0]+1][1] == gh[1]:
			i2n.append(i2n[0]+1)
		else:
			i2n.append(i2n[0]-1)                        
                
                p0_d = indices2n[i2n[0]][6] % 2
                p1_d = indices2n[i2n[1]][6] % 2
                #print p0_d
                #print p1_d
                                
                
                if p1_d == 0 and p0_d == 1:
                    tmp = i2n[0]
                    i2n[0] = i2n[1]
                    i2n[1] = tmp
                    p0_d = indices2n[i2n[0]][6] % 2
                    p1_d = indices2n[i2n[1]][6] % 2
                    #print "swap"
                    
                #print p0_d
                #print p1_d
                
                #print indices2n[i2n[0]]
                #print indices2n[i2n[1]]       
                
		punkt = vertex[binaersuche_rekursiv(vertex, 0, gh[1], 0, len(vertex)-1)][1:]
		p0 = [punkt[0]+indices2n[i2n[0]][4],punkt[1]+indices2n[i2n[0]][5]]
		p1 = [punkt[0]+indices2n[i2n[1]][4],punkt[1]+indices2n[i2n[1]][5]]
		
		#print p0
		#print punkt
		#print p1
                                              
                t = aufLinie(p0, punkt, p1)		
                
		if t == 0:
			continue

		#print t

		i1 = []
		i2 = []
		p08=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[0]][0], 0, len(i_ix)-1)
		for em in i_ix[p08][1]:
			if indices[em][2] == indices2n[i2n[0]][2]:
				i1.append(em)
			if indices[em][2] == indices2n[i2n[0]][3]:
				i2.append(em)
		p18=binaersuche_rekursiv(i_ix, 0, indices2n[i2n[1]][0], 0, len(i_ix)-1)
		for em in i_ix[p18][1]:
			if indices[em][2] == indices2n[i2n[1]][2]:
				i1.append(em)
			if indices[em][2] == indices2n[i2n[1]][3]:
				i2.append(em)
		
		v = []
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i1[1]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[0]][1],0,len(vertex)-1)])
		v.append( vertex[binaersuche_rekursiv(vertex,0,indices[i2[1]][1],0,len(vertex)-1)])

		p = []
		p.append([indices[i1[0]][1], indices[i2[0]][1], v[0][1], v[0][2], v[2][1], v[2][2], indices2n[i2n[0]][4], indices2n[i2n[0]][5], indices2n[i2n[0]][0],indices2n[i2n[0]][6]])
		p.append([indices[i1[1]][1], indices[i2[1]][1], v[1][1], v[1][2], v[3][1], v[3][2], indices2n[i2n[1]][4], indices2n[i2n[1]][5], indices2n[i2n[1]][0],indices2n[i2n[1]][6]])
		#print p[0]
		#print p[1]
		if p0_d + p1_d == 2:
			a3 = [p[0][2],p[0][3],p[0][0]]
        	       	a1 = [p[0][4],p[0][5],p[0][1]]
		else:
			a1 = [p[0][2],p[0][3],p[0][0]]
        	       	a3 = [p[0][4],p[0][5],p[0][1]]

		a2 = [a1[0]+p[0][6],a1[1]+p[0][7]]
               	a4 = [a3[0]+p[0][6],a3[1]+p[0][7]]                	

		#print ""                
		#print a1
		#print a2
		#print a3
		#print a4

		if p0_d + p1_d == 0:
	              	a7 = [p[1][2],p[1][3],p[1][0]]
	              	a5 = [p[1][4],p[1][5],p[1][1]]

		else:
	              	a5 = [p[1][2],p[1][3],p[1][0]]
	              	a7 = [p[1][4],p[1][5],p[1][1]]

                a6 = [a5[0]+p[1][6],a5[1]+p[1][7]]
                a8 = [a7[0]+p[1][6],a7[1]+p[1][7]]
		#print a5
		#print a6
		#print a7
		#print a8
                #print ""
               
                #if p0_d + p1_d == 0:
                #    print "next"
                #    continue
                try:                           
#		    if t < 0:
			s1 = sp(a1, a2, a5, a6)
			i1 = insertV(s1[0], s1[1])
		                        
			s2 = sp(a3, a4, a7, a8)
			i2 = insertV(s2[0], s2[1])

                        [asd,seq] = update_indices(i_ix, i1, a1[2], p[0][8], i1, a5[2], p[1][8])
                        [asd,seq] = update_indices(i_ix, i2, a3[2], p[0][8], i2, a7[2], p[1][8])

			# Keil
			#l_indices = len(indices)
			#i_ix[asd][1].append(l_indices)
			#i_ix[asd][1].append(l_indices+1)
			#i_ix[asd][1].append(l_indices+2)
			#indices.append([p[0][8], i, seq+1])
			#indices.append([p[0][8], a3[2], seq+2])
			#indices.append([p[0][8], a7[2], seq+3])
                    #elif t > 0:
			#s = sp(a3, a4, a7, a8)
			#i = insertV(s[0], s[1])
                        
                       # [asd,seq] = update_indices(i_ix, i, a3[2], p[0][8], i, a7[2], p[1][8])

                        # Keil
			#l_indices = len(indices)
			#i_ix[asd][1].append(l_indices)
			#i_ix[asd][1].append(l_indices+1)
			#i_ix[asd][1].append(l_indices+2)
			#indices.append([p[0][8], i, seq+1])
			#indices.append([p[0][8], a1[2], seq+2])
			#indices.append([p[0][8], a5[2], seq+3])
		except:
			raise
			#continue
                #for em in indices:
                #    print em
		
		progressbar("vbvb2",index/verts)
