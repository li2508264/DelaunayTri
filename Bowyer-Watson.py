import numpy as np
import cv2
import pdb
def drawline(x,y,bg):
	if(abs(x[0]-y[0])>abs(x[1]-y[1])):
		dd = 1
		if x[0]>y[0]:
			dd = -1
		for i in range(x[0],y[0],dd):
			j = int((i-x[0])/(y[0]-x[0])*(y[1]-x[1]))+x[1]
			bg[i,j,0:2] = 0
	else:
		dd = 1
		if x[1]>y[1]:
			dd = -1
		for i in range(x[1],y[1],dd):
			j = int((i-x[1])/(y[1]-x[1])*(y[0]-x[0]))+x[0]
			bg[j,i,0:2] = 0
	return bg
def dis(a,b):
	return np.sqrt(np.sum(np.power(a-b,2)))
def wjCircle(tri):
	x1 = tri[0,0]
	y1 = tri[0,1]
	x2 = tri[1,0]
	y2 = tri[1,1]
	x3 = tri[2,0]
	y3 = tri[2,1]
	a=((y2-y1)*(y3*y3-y1*y1+x3*x3-x1*x1)-(y3-y1)*(y2*y2-y1*y1+x2*x2-x1*x1))/(2.0*((x3-x1)*(y2-y1)-(x2-x1)*(y3-y1)));
	b=((x2-x1)*(x3*x3-x1*x1+y3*y3-y1*y1)-(x3-x1)*(x2*x2-x1*x1+y2*y2-y1*y1))/(2.0*((y3-y1)*(x2-x1)-(y2-y1)*(x3-x1)));
	r = dis(np.asarray([a,b]),tri[0])
	return np.asarray([a,b]),r

for tnum in range(100):
			
	xy  = np.random.randint(180,390,(30,2))

	for i in range(xy.shape[0]-1):
		for j in range(i,xy.shape[0]-1):
			if(xy[j,1]>xy[j+1,1]):
				tmp = xy[j,:].copy()
				xy[j,:] = xy[j+1,:].copy()
				xy[j+1,:] = tmp
	#求最大外接包围盒
	lt = np.min(xy,0)
	br = np.max(xy,0)

	#求斜率
	k = 1
	b = br[1]-k*lt[0]+3
	##计算外接三角形x123
	x3 = br[0]+3
	y3 = k*x3+b
	x2 = x3
	y2 = y3 - 2*(y3-(br[1]+lt[1])/2)
	y1 = (br[1]+lt[1])/2
	x1 = (y1-b)/k
	tc = [[x1,y1],[x2,y2],[x3,y3]]#剔出超级三角形
	tmpTri = []
	Tris = []#最终保存的三角形
	tri = np.asarray([[x1,y1],[x2,y2],[x3,y3]])
	tmpTri.append(tri)
	ps =[i for i in range(xy.shape[0])]
	edges = []

	bg = np.ones((700,700,3))*255
	for i in range(xy.shape[0]):
		bg[xy[i,0]:xy[i,0]+2,xy[i,1]:xy[i,1]+2,2] = 0
	while len(ps)!=0:#对所有点进行检查
		newtmpTri=[]
		delind =[]#待删除的三角形下标
		p = xy[ps[0],:]#插入最左侧点
		edge_buffer = []
		for i in range(len(tmpTri)):
			tri = tmpTri[i]
			cxy,r = wjCircle(tri)
			d = dis(p,cxy)
			if d<r:
				tmp1 = [[tri[0,0],tri[0,1]],[tri[1,0],tri[1,1]]]
				tmp2 = [[tri[1,0],tri[1,1]],[tri[2,0],tri[2,1]]]
				tmp3 = [[tri[2,0],tri[2,1]],[tri[0,0],tri[0,1]]]
				delind.append(i)
				edge_buffer.append(tmp1)
				edge_buffer.append(tmp2)
				edge_buffer.append(tmp3)

		print("----",edge_buffer)
		d_ind = []
		for i in range(len(edge_buffer)):
			if i in d_ind:
				continue
			for j in range(i+1,len(edge_buffer)):
				if j in d_ind:
					continue
				if (edge_buffer[i][0]==edge_buffer[j][0] and edge_buffer[i][1]==edge_buffer[j][1]) or(edge_buffer[i][0]==edge_buffer[j][1] and edge_buffer[i][1]==edge_buffer[j][0]):
					if i not in d_ind:
						d_ind.append(i)
					if j not in d_ind:
						d_ind.append(j)
		
		d_ind.sort()
		for i in range(len(d_ind)-1,-1,-1):
			del edge_buffer[d_ind[i]]

		for i in range(len(edge_buffer)):
			newtmpTri.append(np.asarray([[p[0],p[1]],edge_buffer[i][0],edge_buffer[i][1]]))
		print(delind)
		for i in range(len(delind)-1,-1,-1):
			del tmpTri[delind[i]]
		newtmpTri.extend(tmpTri)
		tmpTri = newtmpTri
		del ps[0]
	for tri in tmpTri:
		Tris.append(tri)
	for tri in Tris:
		if [tri[0,0],tri[0,1]] in tc or [tri[0,1],tri[0,0]] in tc:
			continue
		if [tri[1,0],tri[1,1]] in tc or [tri[1,1],tri[1,0]] in tc:
			continue
		if [tri[2,0],tri[2,1]] in tc or [tri[2,1],tri[2,0]] in tc:
			continue
		edges.append([tri[0],tri[1]])
		edges.append([tri[1],tri[2]])
		edges.append([tri[2],tri[0]])
	# print(x1,y1,x2,y2,x3,y3)
	# pdb.set_trace()

	for i in range(xy.shape[0]):
		bg[xy[i,0],xy[i,1],2] = 0

	# bg = drawline([int(x1),int(y1)],[int(x2),int(y2)],bg)
	# bg = drawline([int(x2),int(y2)],[int(x3),int(y3)],bg)
	# bg = drawline([int(x3),int(y3)],[int(x1),int(y1)],bg)
	print(edges)
	for i in range(len(edges)):

		e1 = edges[i][0].astype('int32')
		e2 = edges[i][1].astype('int32')

		print(e1,e2)
		bg  = drawline([e1[0],e1[1]],[e2[0],e2[1]],bg)
	bg = bg.astype('uint8')
	bg = cv2.resize(bg,(800,800))
	cv2.imshow('test',bg)
	cv2.waitKey(2000) 


