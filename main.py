
from cryptography.fernet import Fernet
import pymongo
from pymongo import *
from os import path
g_key = b''
uri="URL"
myclient = MongoClient(uri,tls=True,tlsAllowInvalidCertificates=True)
mydb = myclient["PASS"]
mylocal = mydb["DATA"]

def genkey():
    key = Fernet.generate_key()
    if path.exists("mykey.key"):
        file = open('mykey.key', 'rb')
        tmp = file.read()
        file.close()
        return(tmp)
    
    file = open('mykey.key', 'wb')
    file.write(key)
    file.close()
    return key
   
class Passwd:
    
    def __init__(self, password, mail, site):
        self.password = password
        self.mail = mail
        self.site = site
        self.key = genkey()
        self.encpass = b''
        if password != '':
            self.encpass = self.get_encrypted_pass()
            
    def get_encrypted_pass(self):
        f_obj = Fernet(self.key)
        f = f_obj.encrypt(self.password.encode())
        mydata = {"pass":f}
        a = mylocal.insert_one(mydata)
        print (a)
        return f
        
    def printallpass(self):
        f_obj = Fernet(self.key)
        for data in mylocal.find({},{"_id":0}):
            a = data['pass']
            print(f_obj.decrypt(a))


if (__name__ == "__main__"):
    while 42:
        print("===================")
        print("bir sercim yapin")
        print("===================")
        print("add")
        print("===================")
        print("sort")
        print("===================")
        command = input("command: ")
        # command = "sort"
        if command == "add":
            passwd = input("input a pass: ")
            mail = input("input a mail: ")
            site = input("input a site: ")
            p1 = Passwd(passwd, mail, site)
            print("OKAY")
        if command == "sort":
            p = Passwd("", "", "")
            p.printallpass()