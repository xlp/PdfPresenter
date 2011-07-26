#!/usr/bin/env python
'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created on Jul 18, 2011

@author: Alex Passfall
'''
from __future__ import division


import QtPoppler
from PyQt4 import QtGui, QtCore
import sys
import os.path
import codecs

class QtPDFViewer(QtGui.QWidget):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.pdfImages = dict()
        self.currentPage = 0
        self.doc = None
        self.initUI()
               
        self.presenterWindow = ProjectorView(self)
        self.presenterWindow.show()
        
    
    def initUI(self):
        
        self.current = PDFView(0,self)
        #self.current.resize(500,500)
        self.next = PDFView(1,self)
                
        viewbox = QtGui.QHBoxLayout()
        viewbox.addWidget(self.current,1)
        viewbox.addWidget(self.next,1)        
        
        uhr = QtGui.QLCDNumber()
        bStart = QtGui.QPushButton('Start')
        bStop = QtGui.QPushButton('Stop')
        
        clockbox = QtGui.QVBoxLayout()
        clockbox.addWidget(uhr)
        clockbuttonbox = QtGui.QHBoxLayout()
        clockbuttonbox.addWidget(bStart)
        clockbuttonbox.addWidget(bStop)
        clockbox.addLayout(clockbuttonbox)
        
        self.notes = Notes()
        bottombox = QtGui.QHBoxLayout()
        bottombox.addLayout(clockbox)
        bottombox.addWidget(self.notes)
        
        mainbox = QtGui.QVBoxLayout()
        mainbox.addLayout(viewbox)
        mainbox.addLayout(bottombox,0)
        self.setLayout(mainbox)
        
    def renderImages(self):
        # TODO: threaded!!
        self.pdfImages = dict()
        if self.doc is not None:
            for i in range(self.doc.numPages()):
                print 'Rendering Page '+repr(i+1)+'/'+repr(self.doc.numPages())
                page = self.doc.page(i)
                if page:
                    pageSize = page.pageSize()
                    pageSize.scale(self.presenterWindow.width(), self.presenterWindow.height(), QtCore.Qt.KeepAspectRatio)
                    scale = pageSize.width()/page.pageSize().width()
                    self.pdfImages[i] = page.renderToImage(scale * 72,scale * 72)
            self.update()
            self.presenterWindow.update()
    
    def load(self, file):
        self.doc = QtPoppler.Poppler.Document.load(file)
        self.doc.setRenderHint(QtPoppler.Poppler.Document.Antialiasing and QtPoppler.Poppler.Document.TextAntialiasing)
        self.renderImages()
    
    def showFileDialog(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        if filename !='':
            self.load(filename)
            self.notes.read(filename)
            self.notes.show(self.currentPage)
        
    def prevPage(self):
        if self.currentPage > 0:
            self.currentPage -= 1
            self.update()
            self.notes.show(self.currentPage)
    
    def nextPage(self):
        if self.currentPage +1 < self.doc.numPages():
            self.currentPage +=1
            self.update()
            self.notes.show(self.currentPage)
            
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_S and (event.modifiers() & QtCore.Qt.ControlModifier ):
            self.notes.save()


class PDFView(QtGui.QWidget):
    def __init__(self,offset, parent = None):
        QtGui.QFrame.__init__(self,parent)
        self.offset = offset
    
    def sizeHint(self, *args, **kwargs):
        return QtCore.QSize(600,600)
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.parent().currentPage+self.offset in self.parent().pdfImages:
            target = QtCore.QRectF(0,0,self.width(),self.height())
            painter.drawImage(target, self.parent().pdfImages[self.parent().currentPage+self.offset])
        else:
            print 'no pixmap'


class ProjectorView(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.initUI()



    def initUI(self):            
        self.resize(640, 480)
        
        self.setWindowTitle('QtPDFPresenter - Presentation Window')
                
        #self.setFocus()
        
        
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Background, QtCore.Qt.black);
        self.setPalette(p)
   
    def resizeEvent(self, event):
        self.parent().renderImages()
        self.update()
    
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if self.parent().currentPage in self.parent().pdfImages:
            painter.drawImage((self.width()-self.parent().pdfImages[self.parent().currentPage].width())/2,
                              (self.height()-self.parent().pdfImages[self.parent().currentPage].height())/2,
                               self.parent().pdfImages[self.parent().currentPage])
            
        else:
            print 'no pixmap'
    
    
    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()


    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F11 or event.key() == QtCore.Qt.Key_F:
            self.toggleFullscreen()
        elif event.key() == QtCore.Qt.Key_O:
            self.parent().showFileDialog()
        elif event.key() == QtCore.Qt.Key_Left:
            self.parent().prevPage()
            self.update()
        elif event.key() == QtCore.Qt.Key_Right:
            self.parent().nextPage()
            self.update()

class Notes(QtGui.QTextEdit):
    def __init__(self, parent = None):
        QtGui.QTextEdit.__init__(self, parent)
        self.notes = dict()
        self.setReadOnly(1)
        self.setFontPointSize(16)
        self.current = None
        self.connect(self, QtCore.SIGNAL('textChanged()'), self.textEdited)
            
    def read(self, filename):
        self.notesfile = str(filename)+'.notes'
        self.setReadOnly(0)
        if os.path.isfile(self.notesfile):
            with codecs.open(self.notesfile, encoding='utf-8', mode='r') as f:
                print 'Reading notes...'
                for line in f:
                    if '==XXslide' in line:
                        slide = line.strip()
                        self.notes[slide] =  ''
                    else:
                        self.notes[slide] += line

    def save(self):
        if len(self.notes) > 0:
            print 'Saving notes'
            with codecs.open(self.notesfile, encoding='utf-8', mode='w') as f:
                for id in self.notes.keys():
                    f.write(id)
                    f.write('\n')
                    f.write(self.notes[id])
                    f.write('\n')
        else:
            print 'No notes to save!'

    def show(self, slide):
        self.current = '==XXslide'+str(slide)
        if self.notes.has_key(self.current):
            self.setPlainText(self.notes[self.current])
        else:
            self.setPlainText('')

    def textEdited(self):
        if self.current is not None:
            self.notes[self.current] = unicode(self.toPlainText())

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    viewer = QtPDFViewer()
    viewer.show()
    sys.exit(app.exec_())

