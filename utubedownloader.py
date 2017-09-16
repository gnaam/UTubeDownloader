import sys, os
from pytube import YouTube
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class UTubeDownloader(QWidget):
	def __init__(self):
		super(UTubeDownloader, self).__init__()
		self.initUI()	

	def initUI(self):
		self.setGeometry(10,10,500,400)
		self.setAutoFillBackground(False)
		#self.setStyleSheet("background-image:url(./img/background.jpg)")
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
				#if there is already a message, remove from widget
				if hasattr(self,'link_error'):
					self.link_error.clear()
				#if there is already a message, remove from widget
				if hasattr(self,'videos') and len(self.videos)!=0:
					if hasattr(self,'checkb_list') and len(self.checkb_list)!=0:
						for (obj,s) in self.checkb_list:
							obj.deleteLater()
						self.checkb_list = []
						self.videos = []
				#remove movie title, if there is
				if hasattr(self,'video_title'):
					self.video_title.clear()
				if hasattr(self,'pbar') and self.pbar!=None:
					self.pbar.deleteLater()
					self.pbar=None
				self.link = text
				self.listVideos()
			else:
				# displaying the message
				if hasattr(self,'link_error') is False:
					self.link_error = QLabel("Enter valid link")
					self.link_error.setAlignment(Qt.AlignCenter);
					self.vbox.addWidget(self.link_error)
					# remove video names, video title, progress bas from widget
					if hasattr(self,'videos'):
						for (obj,s) in self.checkb_list:
							obj.deleteLater()
						self.checkb_list=[]
						self.videos = []
					if hasattr(self,'video_title'):
						self.video_title.clear()
					if hasattr(self,'pbar'):
						self.pbar.deleteLater()
						self.pbar=None

	def listVideos(self):
		try:
			self.yt = YouTube(str(self.link));
			self.videos = self.yt.get_videos();
			self.video_title = QLabel(self.yt.filename)
			self.video_title.setAlignment(Qt.AlignCenter)
			self.vbox.addWidget(self.video_title)
			self.vbox.addStretch()
			s = 1
			self.checkb_list = []
			for vid in self.videos:
				obj = 'cb'+str(s)
				obj = QPushButton((str(s)+". "+str(vid)), self)
				self.checkb_list.append((obj,s))
				obj.setCheckable(False)
				self.vbox.addWidget(obj)
				s+=1
			self.pbar = QProgressBar(self)
			self.pbar.setRange(0,100)
			self.pbar.setValue(0)
			self.vbox.addStretch()
			self.vbox.addWidget(self.pbar)
			for (cbox,s) in self.checkb_list:
				cbox.clicked[bool].connect(self.saveVideo)

		except Exception as e:
			if hasattr(self,'link_error'):
				self.link_error.clear()
				self.link_error = QLabel(str(e))
				self.link_error.setAlignment(Qt.AlignCenter);
				self.vbox.addWidget(self.link_error)
			else:
				self.link_error = QLabel(str(e))
				self.link_error.setAlignment(Qt.AlignCenter);
				self.vbox.addWidget(self.link_error)
	def createDirectory(self):
		destination = os.environ['HOME']+'/Videos'
		os.chdir(destination)
		if 'UTube' not in os.listdir(destination):
			os.mkdir('UTube')
		destination = os.environ['HOME']+'/Videos/UTube'
		return destination

	def saveVideo(self):
		sender = self.sender()
		n = int(sender.text()[0])
		video = self.videos[n-1]
		# change directory
		destination = self.createDirectory()
		video.download(destination, on_progress=self.print_status)

	def print_status(self,progress,file_size,start):
		percent = progress * 100. / file_size
		self.pbar.setValue(percent)
		#print percent

app = QApplication(sys.argv)
icon_images = QIcon()
icon_images.addFile("img/icon1616.png",QSize(16,16))
icon_images.addFile("img/icon3232.png",QSize(32,32))
icon_images.addFile("img/icon4848.png",QSize(48,48))
icon_images.addFile("img/icon9696.png",QSize(96,96))
icon_images.addFile("img/icon144144.png",QSize(144,144))
app.setWindowIcon(icon_images)
yd = UTubeDownloader()
sys.exit(app.exec_())