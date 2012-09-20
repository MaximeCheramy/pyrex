# coding=utf-8

from distutils.core import setup
import py2exe 

setup(
	windows=[{"script":"pyrex.py"}],
	options={"py2exe":{"includes":["sip", "PyQt4.QtCore", "PyQt4._qt"]}}
)
