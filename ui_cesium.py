# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_cesium.ui'
#
# Created: Fri Aug 22 14:20:39 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_cesium(object):
    def setupUi(self, cesium):
        cesium.setObjectName(_fromUtf8("cesium"))
        cesium.resize(720, 646)
        self.buttonBox = QtGui.QDialogButtonBox(cesium)
        self.buttonBox.setGeometry(QtCore.QRect(360, 600, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.webView = QtWebKit.QWebView(cesium)
        self.webView.setGeometry(QtCore.QRect(10, 10, 701, 581))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))

        self.retranslateUi(cesium)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), cesium.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), cesium.reject)
        QtCore.QMetaObject.connectSlotsByName(cesium)

    def retranslateUi(self, cesium):
        cesium.setWindowTitle(_translate("cesium", "cesium", None))

from PyQt4 import QtWebKit
