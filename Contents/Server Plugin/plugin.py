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

	def directions = {
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

	def xmitToCamera(self, path):

		if path is None:
			self.debugLog("no path defined")

		ip = dev.pluginProps['ipaddress']
		user = dev.pluginProps['user']
		password = dev.pluginProps['password']

		req = urllib2.Request(
			url="http://#{user}:#{password}@#{ip}/#{path}"
		)
		return urllib2.urlopen(req)


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

		path = "/decoder_control.cgi?command=#{directions[#direction]}"

		self.xmitToCamera(path)
		self.stop(pluginAction, dev)

	def stop(self, pluginAction, dev):

		# stop camera movement
		self.debugLog(u"stop called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		path = "/decoder_control.cgi?command=#{directions['stop']}"

		self.xmitToCamera(path)
