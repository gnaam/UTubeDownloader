import sys
from pytube import YouTube
from PyQt4.QtCore import *
from PyQt4.QtGui import *
## to do
# create file
##
class UTubeDownloader(QWidget):
	def __init__(self):
		super(UTubeDownloader, self).__init__()
		self.initUI()	

	def initUI(self):
		self.setGeometry(10,10,500,400)
		self.search_button = QPushButton('Copy Link', self)
		self.search_button.move(20,20)
		self.search_button.clicked.connect(self.takeInput)
		self.vbox = QVBoxLayout()
		self.vbox.addWidget(self.search_button)
		self.vbox.addStretch()
		self.setLayout(self.vbox)
		self.setWindowTitle("UTube Downloader")
		self.show()

	def takeInput(self):
		text, ok = QInputDialog.getText(self,'Link','Paste link here')
		if ok:
			if str(text).startswith('http'):
				self.link = text;
				self.listVideos()
			else:
				print("Enter valid link")

	def listVideos(self):
		try:
			self.yt = YouTube(str(self.link));
			self.videos = self.yt.get_videos();
			s = 1
			checkb_list = []
			for vid in self.videos:
				obj = 'cb'+str(s)
				obj = QPushButton((str(s)+". "+str(vid)), self)
				checkb_list.append((obj,s))
				obj.setCheckable(False)
				self.vbox.addWidget(obj)
				s+=1
			self.pbar = QProgressBar(self)
			self.pbar.setRange(0,100)
			self.pbar.setValue(0)
			self.vbox.addStretch()
			self.vbox.addWidget(self.pbar)
			for (cbox,s) in checkb_list:
				cbox.clicked[bool].connect(self.saveVideo)

		except Exception as e:
			raise e
		
	def saveVideo(self):
		sender = self.sender()
		n = int(sender.text()[0])
		video = self.videos[n-1]
		video.download("/home/naam", on_progress=self.print_status)

	def print_status(self,progress,file_size,start):
		percent = progress * 100. / file_size
		self.pbar.setValue(percent)
		#print percent

if __name__ == '__main__':
	app = QApplication(sys.argv)
	icon_images = QIcon()
	icon_images.addFile("img/icon1616.png",QSize(16,16))
	icon_images.addFile("img/icon3232.png",QSize(32,32))
	icon_images.addFile("img/icon4848.png",QSize(48,48))
	icon_images.addFile("img/icon9696.png",QSize(96,96))
	icon_images.addFile("img/icon144144.png",QSize(144,144))
	#app.setWindowIcon(QIcon("./img/icon.png"))
	app.setWindowIcon(icon_images)
	yd = UTubeDownloader()
	sys.exit(app.exec_())