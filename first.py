import sys
from PyQt5 import QtCore, QtGui, uic,QtWidgets
from PyQt5.QtCore import Qt,QObject
from PyQt5.QtCore import QPoint
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter,QFont
from PyQt5.QtGui import QColor 
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QPushButton,QDesktopWidget
from BulletGo import Bullet
import random,GLOBAL

qtCreatorFile="ui.ui"

Ui_MainWindow, QtBaseClass=uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
	mouseLeaveTimer=0

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		#自己有__init__函数时,不会默认调用基类的__init__函数
		# 因为这里重写了__init__将基类的覆盖掉了,故需要主动调用之
		super(MyApp,self).__init__()
		# 	Get the Screen size
		self.screenWidth=QDesktopWidget().availableGeometry().width()
		self.screenHeight=QDesktopWidget().availableGeometry().height()
		#  ColorSetting
		self.bgColor=QColor(66,66,66,88)
		
		#
		self.setupUi(self)
		self.initUI();
		#用来控制半透明的bg面板自动消失
		self.timer=QTimer()
		self.timer.start(30)
		self.setGeometry(0,30,self.screenWidth,self.screenHeight/4)

		self.creatConnections()
		#Flags
		self.IsMouseHover=False
		self.MouseOver=False
		#变量初始化
		GLOBAL.WINDOWWIDTH=self.width()
		GLOBAL.WINDOWHEIGHT=self.height()
		self.bullets=[]
		self.dragPos=QPoint(22,22)

	def fireBtn(self):
		txt=self.plainTextEdit.toPlainText()
		tmpbullet=Bullet(txt,GLOBAL.ORANGE,random.randrange(16,22,2))
		self.bullets.append(tmpbullet)
		tmpbullet.prepare()
		print(len(self.bullets))

	def creatConnections(self):
		self.timer.timeout.connect(self.update)
		self.btnFire.clicked.connect(self.fireBtn)

	def initUI(self):
		#构建托盘

		self.setWindowTitle("BulletGo")
		sizeGrip=QtWidgets.QSizeGrip(self)
		self.setWindowFlags(Qt.FramelessWindowHint\
			|Qt.WindowStaysOnTopHint|Qt.Window)
		#Plan A
		self.setAttribute(Qt.WA_TranslucentBackground,True)
		#Plan B  失败
		# palette=QPalette()
		# color=QColor(190, 230, 250)
		# color.setAlphaF(0.6)
		# palette.setBrush(self.backgroundRole(), color)
		# self.setPalette(palette)
		# self.setAutoFillBackground(True)
		# self.setBackgroundRole(QPalette.Window)
	
	def mousePressEvent(self,e):
		if e.button()==Qt.LeftButton: 
			# self.dragPos=e.globalPos()-self.frameGeometry().topLeft()
			self.dragPos=e.pos()#效果同上,鼠标相对窗口左上角的位置
			e.accept()

	def mouseMoveEvent(self,e):
		if e.buttons()&Qt.LeftButton:
			self.move(e.globalPos()-self.dragPos)
			e.accept();

	def enterEvent(self,e):
		self.MouseOver=True
		self.IsMouseHover=True
		return super(MyApp,self).enterEvent(e)

	def setMouseHoverFalse(self):
		if(not self.MouseOver):
			self.IsMouseHover=False

	def leaveEvent(self,e):
		QTimer.singleShot(800,self.setMouseHoverFalse)
		self.MouseOver=False
		return super(MyApp,self).leaveEvent(e)

	def resizeEvent(self,e):
		GLOBAL.WINDOWWIDTH=self.width()
		GLOBAL.WINDOWHEIGHT=self.height()
		self.repaint()
		e.accept()

	def paintEvent(self,e):
		# Get the Painter
		painter=QPainter(self)
		#Draw a semi-Transparent rect whose size is the same with this window
		if(self.IsMouseHover):
			painter.fillRect(0,0,GLOBAL.WINDOWWIDTH,GLOBAL.WINDOWHEIGHT\
				,self.bgColor)
		# painter.setBackground(QBrush(QColor(123,222,123,122)))
		#画所有bullet
		for b in self.bullets:
			if(b.draw(painter)):
				self.bullets.remove(b)
				# pass
		# painter.drawText(30,100,"Hello this is a PyQt5 App我也会说中文")
		return super(MyApp,self).paintEvent(e)

if __name__=="__main__":
	app=QtWidgets.QApplication(sys.argv)
	window=MyApp()
	window.show()
	sys.exit(app.exec_())