from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QElapsedTimer 
from PyQt5.QtGui import QColor,QFont
from PyQt5.QtGui import QPainter ,QPen
from PyQt5 import QtCore
import GLOBAL,random



class Bullet:
	"""Bullet contains:
		1 StartPosition
		2 EndPosition
		3 Color
		4 Text( A String)
		5 Duration
		It uses the "window"  to draw it selft
	"""
	#这个叫做  类的属性  
	Count=0# 通过类名Bullet.bullet访问,就是一个静态变量
	Height=GLOBAL.BULLETFONTSIZE+6 #一个Bullet占用的像素高度
	def __init__(self, Text, Color,Duration):
		Bullet.Count+=1
		#这个里面self给定的内容则只属于当前对象
		self.Text=Text
		self.Color=Color
		self.Duration=Duration*1000 #单位是毫秒,输入的是秒
		self.IsExpired=False

	"""this method must be called when this 
		bullet is ready to shoot at the first time
	"""
	def prepare(self):
		self.elapsedTimer=QElapsedTimer()
		self.elapsedTimer.start() #start time
		self.StartPosition=QPoint(GLOBAL.WINDOWWIDTH+random.randrange(200,500,20),\
			(Bullet.Height+(Bullet.Count%(GLOBAL.WINDOWHEIGHT//Bullet.Height))*Bullet.Height))
		self.EndPosition=QPoint(-2000 ,self.StartPosition.y())
	"""Draw this bullet at position x,y ,use painter
		Returns True indicates this bullet is out of screen
	"""
	def draw(self,painter):
		ratio=self.elapsedTimer.elapsed()/self.Duration
		if(ratio>0.9):
			self.IsExpired=True
		# pos=ratio*self.EndPosition+(1-ratio)*self.StartPosition
		pos=QPoint(ratio*self.EndPosition.x()+(1-ratio)*self.StartPosition.x(),self.StartPosition.y())
		#这里需要插入绘制字体阴影的代码
		#
		# font.setFixedPitch(True)
		# painter.setFont(font)
		painter.save()
		painter.drawText(pos+QPoint(2,2),self.Text)
		painter.setPen(QPen(self.Color))
		painter.drawText(pos,self.Text)
		painter.restore()

	# def __del__(self):
		# Count-=1
		# print ("刚刚自动Delete了一个bullet\n")