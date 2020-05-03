#!/usr/bin/python

import sys, getopt

from ZTE import *


def printHelp():
    print ('wifichange.py  -p <password> [ -i <address> -u <user> -t <technology> -e <state> ]')
    print ('password: router password. Mandatory parameter')
    print ('user(optional): router user, default: 1234')
    print ('address(optional): router address, default: 192.168.1.1')
    print ('technology (optional): 0-> all(default), 1-> 2G, 2-> 5G')
    print ('state (optional): 0-> disable, 1-> enable(default)')
    return

    
def changeStatus( ipAddress, user, password, enable, technologies):

    SID = getSID (ipAddress,user,password,getLoginToken(ipAddress))

    session_token = getSessionToken(ipAddress,SID)

    if (technologies == '0') : #All
        if (enable == '1'):
            #print ('enable All')
            enable5G(ipAddress,SID,session_token)
            logout(ipAddress,SID,session_token)
            SID = getSID (ipAddress,user,password,getLoginToken(ipAddress))
            session_token = getSessionToken(ipAddress,SID)
            enable2G(ipAddress,SID,session_token)
        else:

            disable5G(ipAddress,SID,session_token)
            logout(ipAddress,SID,session_token)
            SID = getSID (ipAddress,user,password,getLoginToken(ipAddress))
            session_token = getSessionToken(ipAddress,SID)
            disable2G(ipAddress,SID,session_token)

    if (technologies == '1') : #2G
        if (enable == '1'):
            #print ('enable 2G')
            enable2G(ipAddress,SID,session_token)
        else:
            #print ('disable 2G')
            disable2G(ipAddress,SID,session_token)
            
    if (technologies == '2') : #5G
        if (enable =='1'):
            #print ('enable 5G')
            enable5G(ipAddress,SID,session_token)
        else:
            #print ('disable 5G')
            disable5G(ipAddress,SID,session_token)

    #disable2G(ipAddress,SID,session_token)
    #enable2G(ipAddress,SID,session_token)
    #disable5G(ipAddress,SID,session_token)
    #enable5G(ipAddress,SID,session_token)

    logout(ipAddress,SID,session_token)
    return




def main(argv):
   techno = '0' # default all
   enable = '1' #default enable
   ipAddress = '192.168.1.1'
   user = '1234'
   password = None
   try:
      opts, args = getopt.getopt(argv,"ht:e:i:u:p:",["techno=","enable=","ip==","user==","pass=="])
   except getopt.GetoptError:
      printHelp()
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         printHelp()
         sys.exit()
      elif opt in ("-t", "--techno"):
         techno = arg
      elif opt in ("-e", "--enable"):
         enable = arg
      elif opt in ("-i", "--ip"):
         ipAddress = arg
      elif opt in ("-u", "--user"):
         user = arg
      elif opt in ("-p", "--pass"):
         password = arg
   
   if (password == None):
    print ("Error password is a mandatory parameter")
    printHelp()
    sys.exit()
   
   
   changeStatus(ipAddress,user, password, enable,techno)

if __name__ == "__main__":
   main(sys.argv[1:])

















