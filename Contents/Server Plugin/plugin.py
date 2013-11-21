#! /usr/bin/env python

import httplib, urllib2, smtplib, sys, os
try:
	import xml.etree.cElementTree as ET
except ImportError:
	import xml.etree.ElementTree as ET

from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

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

		hostname = dev.pluginProps['ipaddress']
		username = dev.pluginProps['username']
		password = dev.pluginProps['password']

		# create a password manager
		password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()

		# Add the username and password.
		# If we knew the realm, we could use it instead of None.
		password_mgr.add_password(None, hostname, username, password)

		handler = urllib2.HTTPBasicAuthHandler(password_mgr)

		# create "opener" (OpenerDirector instance)
		opener = urllib2.build_opener(handler)

		requestUrl = "http://"+hostname+path

		req = urllib2.Request(url=requestUrl)
		self.debugLog(u"request URL: "+requestUrl)
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

	def disable(self, pluginAction, dev):

		# Disable audio and video streams
		self.debugLog(u"disable called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		path = "/set_forbidden.cgi?schedule_enable=-1&schedule_sun_0=-1&schedule_sun_1=-1&schedule_sun_2=-1&schedule_mon_0=-1&schedule_mon_1=-1&schedule_mon_2=-1&schedule_tue_0=-1&schedule_tue_1=-1&schedule_tue_2=-1&schedule_wed_0=-1&schedule_wed_1=-1&schedule_wed_2=-1&schedule_thu_0=-1&schedule_thu_1=-1&schedule_thu_2=-1&schedule_fri_0=-1&schedule_fri_1=-1&schedule_fri_2=-1&schedule_sat_0=-1&schedule_sat_1=-1&schedule_sat_2=-1"

		self.xmitToCamera(path, dev)

	def enable(self, pluginAction, dev):

		# Enable audio and video streams
		self.debugLog(u"enable called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		path = "/set_forbidden.cgi?schedule_enable=0&schedule_sun_0=0&schedule_sun_1=0&schedule_sun_2=0&schedule_mon_0=0&schedule_mon_1=0&schedule_mon_2=0&schedule_tue_0=0&schedule_tue_1=0&schedule_tue_2=0&schedule_wed_0=0&schedule_wed_1=0&schedule_wed_2=0&schedule_thu_0=0&schedule_thu_1=0&schedule_thu_2=0&schedule_fri_0=0&schedule_fri_1=0&schedule_fri_2=0&schedule_sat_0=0&schedule_sat_1=0&schedule_sat_2=0"

		self.xmitToCamera(path, dev)

	def motionAlarmOn(self, pluginAction, dev):

		#Enable email alerts when motion sensed
		self.debugLog(u"motionAlarmOn called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		sensitivity = pluginAction.props['sensitivity']
		if sensitivity is None:
			self.debugLog(u"setting default sensitivity of max")
			sensitivity = 0

		path = "/set_alarm.cgi?motion_armed=1&motion_sensitivity="+sensitivity+"&motion_compensation=1&mail=1"

		self.xmitToCamera(path, dev)

	def motionAlarmOff(self, pluginAction, dev):

		#Enable email alerts when motion sensed
		self.debugLog(u"motionAlarmOff called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		path = "/set_alarm.cgi?motion_armed=0"

		self.xmitToCamera(path, dev)

	def irOn(self, pluginAction, dev):

		self.debugLog(u"irOn called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		path = "/decoder_control.cgi?command=95"

		self.xmitToCamera(path, dev)

	def irOff(self, pluginAction, dev):

		self.debugLog(u"irOn called")

		if dev is None:
			self.debugLog(u"no device defined")
			return

		path = "/decoder_control.cgi?command=94"

		self.xmitToCamera(path, dev)

	def snap(self, pluginAction, dev):

		self.debugLog(u"snap called")

		if dev is None:
			self.debugLog(u"no device defined")

		username = dev.pluginProps['username']
		password = dev.pluginProps['password']

		path = "/snapshot.cgi?user="+username+"&pwd="+password
		resp = self.xmitToCamera(path, dev)
		snapimg = resp.read()

		# todo: serialize filename, pass to sendViaEmail
		snappath = "/tmp/snap.jpg"
		f = open(snappath, 'w')

		f.write(snapimg)
		f.close()

		self.sendViaEmail(pluginAction, dev)

	def sendViaEmail(self, pluginAction, dev):
		
		# Create the container (outer) email message.
		msg = MIMEMultipart()
		msg['Subject'] = pluginAction.props['subject']
		msg['From'] = self.pluginPrefs['sender']
		msg['To'] = pluginAction.props['recipient']
		msg.preamble = 'cam snap test'

		# Open the files in binary mode.  Let the MIMEImage class automatically
		# guess the specific image type.
		fp = open('/tmp/snap.jpg', 'rb')
		img = MIMEImage(fp.read())
		fp.close()
		msg.attach(img)

		s = smtplib.SMTP(self.pluginPrefs['smtphost'],int(self.pluginPrefs['smtpport']))
		s.ehlo()
		s.starttls()
		s.ehlo
		s.login(self.pluginPrefs['smtpuser'], self.pluginPrefs['smtppass'])
		s.sendmail(self.pluginPrefs['sender'], pluginAction.props['recipient'], msg.as_string())
		s.quit()
