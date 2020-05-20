#!/usr/bin/env python3

# a small, non-parallel brute-force password file cracker

from sys import argv
#import hashlib # -- doesnt work on mac os!
from passlib.hash import sha512_crypt, sha256_crypt, md5_crypt
from string import ascii_lowercase, ascii_uppercase
from pynput import keyboard
import base64

isRunning = True
pwd=[]
saltdic={}
discovered={}
s=''


def algo(n, f):
	if n=='1':
		#return hashlib.md5
		return md5_crypt.hash
	elif n=='5':
		#return hashlib.sha256
		return sha256_crypt.hash
	elif n=='6':
		#return hashlib.sha512
		return sha512_crypt.hash
	else:
		print("unrecognized hash algorithm")
		f.close()
		exit()
	"""elif n=='2a' or n=='2y':
		return hashlib.blowfish"""

def parsePWD(filename):
	global pwd, saltdic
	print("hello")
	f = open(filename, 'r')
	for pw in f.readlines():
		l = pw.split('$')
		uname=l[0]
		alg=algo(l[1], f)
		salt=l[2]
		password=l[3].strip()
		entry = {'uname':uname, 'algo':alg, 'salt':salt, 'password':password}
		pwd.append(entry)
		if not salt in saltdic:
			saltdic[salt] = [entry]
		else:
			saltdic[salt].append(entry)
	f.close()

def addOne(word, chars):
	if word=='':
		return chars[0]
	elif word[-1]==chars[-1]:
		return addOne(word[:-1],chars)+chars[0]
	else:
		ind = chars.index(word[-1])
		return word[:-1]+chars[ind+1]

def brute_force(start):
	global s, isRunning
	s = start
	print("starting from {0}".format(s))
	chars = ascii_lowercase
	#chars = ascii_lowercase+ascii_uppercase
	"""for i in range(0,10):
		print(i)
		chars+=str(i)"""
	#chars+='!'+'@'+'#'+'$'+'%'+'^'+'&'+'*'+'('+')'+'-'+'_'+'+'+'=' # there is more, doesn't matter right now
	while isRunning:
		for c in chars:
			for salt in saltdic:
				for e in saltdic[salt]:
					h=e['algo'](s+c, salt=e['salt'], rounds=5000).split('$')[-1] # shadow files hash 5000 rounds
					#h=e['algo']((s+c+e['salt']).encode('utf-8')).hexdigest()
					if h==e['password']:
						print("username: {0} password: {1}".format(e['uname'], e['password']))
						discovered[e['uname']]=s+c
			#a=hashlib.sha256((s+c).encode('utf-8')).hexdigest()
		s = addOne(s, chars)
		#print(s)

def on_press(key):
	global s
	#print('key {0} pressed'.format(key))
	try:
		#print('key {0} pressed'.format(key.char))
		kc=key.char
		print("\b\b\b\b\b\b\b",end="", flush="True"),
		if kc == "w":
			print(s)
			print("\b",end="", flush="True"),
		if kc== "q":
			quit()
	except AttributeError:
		print("\b\b\b\b\b\b\b",end="", flush="True"),
		if key== keyboard.Key.esc:
			quit()
		#print('special key {0} pressed'.format(key))
		#pass

def quit():
	global isRunning
	if len(discovered)!=0:
		print("Cracked passwords:")
		for d in discovered:
			print("{0}: {1}".format(d, discovered[d]))
	else:
		print("No passwords cracked.")
	print("exiting")
	isRunning=False

def on_release(key):
	#print("hello")
	#do nothing
	pass

def main(start=''):
	print("enter w to see current word, esc to quit")
	listener = keyboard.Listener(
		on_press=on_press,
		on_release=on_release)
	listener.start()
	brute_force(start)
	#listener.join()
	
	return
	"""with keyboard.Listener(
		on_press=on_press,
		on_release=on_release) as listener:
		listener.start()
		brute_force()"""

def start_listener():
	#keyboard.Listener.start
	#parsePWD("pwd")
	main()


if __name__=="__main__":
	#sha512_crypt.hash("soccer", salt="NShHCRTL", rounds=5000)
	if len(argv)!=2 and len(argv)!=3:
		print("error")
		exit()
	filename = argv[1]
	start=''
	if len(argv)==3:
		start=argv[2]
	parsePWD(filename)
	main(start)
