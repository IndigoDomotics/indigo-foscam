#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2012, Chad Francis. All rights reserved.
# http://www.chadfrancis.com

import httplib, urllib2, sys, os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


class Plugin(indigo.PluginBase):

	directions = {
		'up': 0,
		'down': 2,
		'left': 6,
		'right': 4,
		'stop': 3
	}

	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		indigo.PluginBase.__init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.debug = True

	def __del__(self):
		indigo.PluginBase.__del__(self)

	def startup(self):
		self.debugLog(u"startup called")

	def shutdown(self):
		self.debugLog(u"shutdown called")

	def xmitToCamera(self, path, dev):

		if path is None:
			self.debugLog("no path defined")

		ipaddress = dev.pluginProps['ipaddress']
		username = dev.pluginProps['username']
		password = dev.pluginProps['password']

		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

		# Add the username and password.
		# If we knew the realm, we could use it instead of None.
		top_level_url = ipaddress
		password_mgr.add_password(None, top_level_url, username, password)

		handler = urllib2.HTTPBasicAuthHandler(password_mgr)

		# create "opener" (OpenerDirector instance)
		opener = urllib2.build_opener(handler)

		req = urllib2.Request(
			url="http://"+ipaddress+path
		)
		return opener.open(req)



	# actions go here
	def getStatus(self, pluginAction, dev):
		# get status from receiver, update locals
		self.debugLog(u"getStatus called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		#TODO: get device status, update states

	def move(self, pluginAction, dev):


		# move camera
		self.debugLog(u"move called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		direction = pluginAction.props['direction']

		if direction is None:
			self.debugLog(u"no direction defined")
			return

		path = "/decoder_control.cgi?command="+str(self.directions[direction])

		self.xmitToCamera(path, dev)
		self.stop(pluginAction, dev)

	def stop(self, pluginAction, dev):

		# stop camera movement
		self.debugLog(u"stop called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		path = "/decoder_control.cgi?command="+str(self.directions['stop'])

		self.xmitToCamera(path, dev)
