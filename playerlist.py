#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

from nbt import nbt
import xlsxwriter

import subprocess

import time
from sys import exit
import os

servers = "/root/of/spigot/servers"
sharePath = "/where/to/save/reports/"
def findUsers():
	subprocess.call('rm %s*' %(sharePath), shell=True)
	for dir in os.listdir(servers):
		serverName = ""	
		if os.path.isfile(servers + dir + '/server.properties'):
			with open(servers + dir + '/server.properties') as conf:
				for line in conf:
					if "=" in line:
						name, value = line.split("=", 1)
						if name == "server-name":
							serverName = value
							break
			try:
				workBook = xlsxwriter.Workbook(sharePath + '%s.xlsx' %(serverName.replace('\n', '').replace('\r', '')))
				for world in os.listdir(servers + dir):
					if not os.path.isdir(servers + dir + "/" + world):
						continue
					if os.path.isfile(servers + dir + "/" + world + "/level.dat"):
						if world != "world":
							continue
						row = 0
						col = 0
						workSheet = workBook.add_worksheet(world)
							
						workSheet.set_column(col, 3, 40)
						workSheet.write(row, col, "UUID")
						workSheet.set_column(col+1, 3, 30)
						workSheet.write(row, col+1, "Nickname")
						workSheet.set_column(col+2, 3, 30)
						workSheet.write(row, col+2, "First login")
						workSheet.set_column(col+3, 3, 30)
						workSheet.write(row, col+3, "Last login")
						path = servers + dir + "/" + world + "/playerdata/"
						for file in os.listdir(path):
							user = nbt.NBTFile(path + file,'rb')
							if not "bukkit" in user:
								continue
							row += 1
							workSheet.write(row, col, file[:-4])
							
							workSheet.write(row, col+1, str(user["bukkit"]["lastKnownName"]))
							print "Found user: " + str(user["bukkit"]["lastKnownName"])
							
							unix_timestamp  = int(str(user["bukkit"]["firstPlayed"]))/1000
							local_time = time.localtime(unix_timestamp)
							workSheet.write(row, col+2, time.strftime("%d-%m-%Y %H:%M:%S", local_time))
							
							unix_timestamp  = int(str(user["bukkit"]["lastPlayed"]))/1000
							local_time = time.localtime(unix_timestamp)
							workSheet.write(row, col+3, time.strftime("%d-%m-%Y %H:%M:%S", local_time))
							
				workBook.close()
			except KeyboardInterrupt:
				workBook.close()
				print "Interrupted by user"
				exit(0)
			
findUsers()
exit(0)
