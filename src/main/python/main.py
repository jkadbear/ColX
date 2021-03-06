import sys
import json

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from mainwindow import Ui_MainWindow
from model import Model

class MainWindowUIClass( Ui_MainWindow ):
    def __init__( self ):
        '''Initialize the super class
        '''
        super().__init__()
        self.model = Model()


    def setupUi( self, MW ):
        ''' Setup the UI of the super class, and add here code
        that relates to the way we want our UI to operate.
        '''
        super().setupUi( MW )
        self.refreshAll()
        top_s = 'ColX @Version 1.2 @Author jkadbear @Copyright 2020'
        self.debugTextBrowser.append( top_s + '\n' + '='*60 )

        # close the lower part of the splitter to hide the
        # debug window under normal operations
        # self.splitter.setSizes([300, 0])


    def debugPrint( self, msg ):
        '''Print the message in the text edit at the bottom of the
        horizontal splitter.
        '''
        self.debugTextBrowser.append( msg )


    def refreshAll( self ):
        '''
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        '''
        self.lineEdit.setText( self.model.getFilePath() )
        self.lineEdit_4.setText( self.model.getFolder()  )
        self.lineEdit_2.setText( ','.join(self.model.getColName()) )
        self.lineEdit_3.setText( ','.join([str(i) for i in self.model.getMaxCol()]) )


    def enterOpenSlot( self ):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        filePath =  self.lineEdit.text()
        if self.model.isValid( filePath ):
            self.model.setFilePath( self.lineEdit.text() )
            self.debugPrint( 'setting file path: ' + filePath )
            self.refreshAll()
        else:
            m = QtWidgets.QMessageBox()
            m.setText("Invalid file path!\n" + filePath )
            m.setIcon(QtWidgets.QMessageBox.Warning)
            m.setStandardButtons(QtWidgets.QMessageBox.Ok
                                 | QtWidgets.QMessageBox.Cancel)
            m.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = m.exec_()
            self.lineEdit.setText( '' )
            self.refreshAll()
            self.debugPrint( 'Invalid file specified: ' + filePath )


    def enterSaveSlot( self ):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        folder = self.lineEdit_4.text()
        if self.model.isValid( folder ):
            self.model.setFolder( self.lineEdit_4.text() )
            self.debugPrint( 'setting saving folder: ' + folder )
            self.refreshAll()
        else:
            m = QtWidgets.QMessageBox()
            m.setText("Invalid folder name!\n" + folder )
            m.setIcon(QtWidgets.QMessageBox.Warning)
            m.setStandardButtons(QtWidgets.QMessageBox.Ok
                                 | QtWidgets.QMessageBox.Cancel)
            m.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            ret = m.exec_()
            self.lineEdit_4.setText( '' )
            self.refreshAll()
            self.debugPrint( 'Invalid folder specified: ' + folder  )


    def extractSlot( self ):
        ''' Called when the user presses the Extract button.
        '''
        if self.model.isValid(self.model.getFilePath()) and \
            self.model.isValid(self.model.getFolder()):
            self.model.extract()
            self.refreshAll()
            self.debugPrint( 'saving extraction results to ' + self.model.getResFilePath() )


    def browseOpenSlot( self ):
        ''' Called when the user presses the Browse button
        '''
        options = QtWidgets.QFileDialog.Options()
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
                        None,
                        'QFileDialog.getOpenFileName()',
                        '',
                        'Excel Files (*.xls *.xlsx);;All Files (*)',
                        options=options)
        if filePath:
            self.debugPrint( 'setting file path: ' + filePath )
            self.model.setFilePath( filePath )
            self.refreshAll()


    def browseSaveSlot( self ):
        ''' Called when the user presses the Browse button
        '''
        folder = QtWidgets.QFileDialog.getExistingDirectory(
                     None,
                     'Select a folder:',
                     '',
                     options=QtWidgets.QFileDialog.ShowDirsOnly)
        if folder:
            self.debugPrint( 'setting saving folder: ' + folder )
            self.model.setFolder( folder )
            self.refreshAll()


    def columnNameSlot( self, text):
        self.model.setColName( text )


    def maxColumnSlot( self, text ):
        self.model.setMaxCol( text )


if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext

    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()

    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
