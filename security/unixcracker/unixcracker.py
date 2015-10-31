import crypt
import sys

if len(sys.argv) == 3:
	passwords, dictionary = sys.argv[1], sys.argv[2]
	if not os.path.isfile(passwords):
		print '[-] ' + passwords + ' does not exist...'
		exit(0)
	if not os.access(passwords, os.R_OK):
		print '[-] ' + passwords + ' access denied...'
		exit(0)
	if not os.path.isfile(dictionary):
		print '[-] ' + dictionary + ' does not exist...'
		exit(0)
	if not os.access(dictionary, os.R_OK):
		print '[-] ' + dictionary + ' access denied...'
		exit(0)
def testPass(cryptPass):
	salt = cryptPass[0:2]
	dictFile = open(dictionary, 'r')
	for word in dictFile.readlines():
		word = word.strip('\n')
		cryptWord = crypt.crypt(word,salt)
		if (cryptWord == cryptPass):
			print "[+] Found Password: "+word+"\n"
			return
	print "[-] Password not Found.\n"
	return



def main():
	passFile = open(passwords)
	for line in passFile.readlines():
		if ':' in line:
			user_and_password = line.split(':')
			user, cryptPass = user_and_password[0], user_and_password[1]
			print "[+] Cracking Password For: "+user"\n"
			testPass(cryptPass)

if __name__ == "__main__":
	main()