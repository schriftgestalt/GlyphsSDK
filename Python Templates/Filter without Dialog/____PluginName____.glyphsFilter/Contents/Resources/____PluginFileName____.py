# encoding: utf-8

from plugin import *
from AppKit import *

class ____PluginClassName____(FilterWithoutDialog):
	
	def settings(self):
		self.menuName = 'My Filter'
		self.keyboardShortcut = None # With Cmd+Shift

	def filter(self, layer, inEditView, customParameters):
		
		# Apply your filter code here
		
		print layer, inEditView, customParameters
