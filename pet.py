from PySide6 import QtCore, QtWidgets, QtGui, QtMultimedia
import sys
import os
import time
import random as rd

class Player(QtWidgets.QWidget):
    def __init__(self, parent=None, name=None):
        # Basic settings
        super().__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint|QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.Tool|QtCore.Qt.X11BypassWindowManagerHint)
        self.setAutoFillBackground(False)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        self.imagePath = os.path.join(self.bundle_dir, f'images\\{name}')
        self.audioPath = os.path.join(self.bundle_dir, f'audio\\{name}')
        self.isFollowMouse = False
        self.dragPosition = 0
        self.image = QtWidgets.QLabel(self)
        self.size = self.screen().availableGeometry()
        self.setGeometry(rd.randint(0, self.size.width()-100), rd.randint(0, self.size.height()-100), 100, 100)
        
        # Let me talk!
        self.isLetMeTalk = False
        self.audioPlayer = QtMultimedia.QMediaPlayer()
        self.audioOutput = QtMultimedia.QAudioOutput()
        self.audioPlayer.setAudioOutput(self.audioOutput)
        
        # Walking animation
        self.autoChangeDirection = False
        self.isWalking = True
        self.restoreWalking = False
        self.faceDirection = "right" if rd.random() > 0.5 else "left"
        self.currentIndex = 1
        self.walkingSpeed = 10
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.walk)
        self.timer.start(100)  # 1000 ms = 1 second
        self.walk()  # Initial update
        
    
    def switchIsWalking(self):
        self.isWalking = not self.isWalking
    
    def switchLetMeTalk(self):
        self.isLetMeTalk = not self.isLetMeTalk
    
    def switchFaceDirection(self):
        if self.faceDirection == "right":
            self.faceDirection = "left"
        else:
            self.faceDirection = "right"
            
    def switchAutoChangeDirection(self):
        self.autoChangeDirection = not self.autoChangeDirection
    
    def setSpeed(self, speed):
        self.walkingSpeed = speed
        
    def walk(self):
        if self.isLetMeTalk:
            self.image.setPixmap(QtGui.QPixmap(f"{self.imagePath}/{name}_{self.faceDirection}_letmetalk_2.png"))
            return
        if not self.isWalking:
            self.image.setPixmap(QtGui.QPixmap(f"{self.imagePath}/{name}_{self.faceDirection}_stand.png"))
            return
        self.image.setPixmap(QtGui.QPixmap(f"{self.imagePath}/{name}_{self.faceDirection}_walk_{self.currentIndex}.png"))
        if self.faceDirection == "right":
            if self.x() > self.size.width() - 100: # Minus the width of the player
                self.faceDirection = "left"
            self.move(self.x() + self.walkingSpeed, self.y())
        elif self.faceDirection == "left":
            if self.x() < 0:
                self.faceDirection = "right"
            self.move(self.x() - self.walkingSpeed, self.y())
        self.currentIndex += 1
        if self.currentIndex == 3 or self.currentIndex == 5:
            self.image.setPixmap(QtGui.QPixmap(f"{self.imagePath}/{name}_{self.faceDirection}_stand.png"))
            if rd.random() > 0.95:
                self.switchIsWalking()
                self.timer.singleShot(3000, self.switchIsWalking)
            if self.autoChangeDirection and rd.random() > 0.95:
                self.switchFaceDirection()
                self.switchIsWalking()
                self.timer.singleShot(3000, self.switchIsWalking)
            if self.currentIndex == 5:
                self.currentIndex = 1
                
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.setMinimumWidth(150)
        menu.addSeparator()
        movement = QtGui.QAction('走動／停止', self)
        movement.triggered.connect(self.switchIsWalking)
        menu.addAction(movement)
        
        changeSpeed = QtWidgets.QMenu(f'改變速度（目前為 {self.walkingSpeed}）', self)
        speedSubActions = []
        for speed in range(5, 35, 5):
            action = QtGui.QAction(f'{speed}', self)
            action.triggered.connect(lambda _, speed=speed: self.setSpeed(speed))
            speedSubActions.append(action)
        changeSpeed.addActions(speedSubActions)
        menu.addMenu(changeSpeed)
        menu.addSeparator()
        changeDirection = QtGui.QAction('手動轉向', self)
        changeDirection.triggered.connect(self.switchFaceDirection)
        menu.addAction(changeDirection)
        if self.autoChangeDirection:
            autoChangeDirection = QtGui.QAction('自動轉向（已啟用）', self)
        else:
            autoChangeDirection = QtGui.QAction('自動轉向（已停用）', self)
        autoChangeDirection.triggered.connect(self.switchAutoChangeDirection)
        menu.addAction(autoChangeDirection)
        menu.addSeparator()
        
        if name == "debruyne":
            letMeTalk = QtGui.QAction('Let me talk!', self)
            letMeTalk.triggered.connect(self.letMeTalk)
            menu.addAction(letMeTalk)
            menu.addSeparator()
        quit = QtGui.QAction('退出', self)
        quit.triggered.connect(self.quit)
        menu.addAction(quit)
        menu.addSeparator()
        menu.exec_(event.globalPos())

    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.isFollowMouse = True
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
            event.accept()
            
    def mouseMoveEvent(self, event):
        if self.isFollowMouse:
            if self.isWalking:
                self.restoreWalking = True
            self.isWalking = False
            self.image.setPixmap(QtGui.QPixmap(f"{self.imagePath}/{name}_{self.faceDirection}_stand.png"))
            self.move(event.globalPos() - self.dragPosition)
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.isFollowMouse = False
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            if self.restoreWalking:
                self.isWalking = True
                self.restoreWalking = False
    
    def letMeTalk(self):
        self.isLetMeTalk = True
        self.image.setPixmap(QtGui.QPixmap(f"{self.imagePath}/{name}_{self.faceDirection}_letmetalk_2.png"))
        file = rd.sample(os.listdir(self.audioPath), 1)[0]
        self.audioPlayer.setSource(QtCore.QUrl.fromLocalFile(f"{self.audioPath}/{file}"))
        self.audioOutput.setVolume(50)
        self.audioPlayer.play()
        self.timer.singleShot(1000, self.switchLetMeTalk)
            
    def quit(self):
        self.close()
        sys.exit()
print(sys.argv)
playerApp = QtWidgets.QApplication([])
name = sys.argv[1]
player = Player(None, name)
player.resize(100, 100)
player.show()
sys.exit(playerApp.exec())