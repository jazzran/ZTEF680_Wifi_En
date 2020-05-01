import urllib2, urllib,hashlib,random,re

#do logout
def logout (address,SID, session):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1 SID= '+SID))
    url = 'http://'+address
    data = urllib.urlencode({'logout':'1','_SESSION_TOKEN':session})
    #print data
    req = urllib2.Request(url, data)
    response = opener.open(req)

    d= response.read();
    
    #print d;
    
    opener.close()
    return

def getSessionToken(address,SID):

    #opener = urllib2.build_opener()
    #opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1 SID='+value))
    #url = 'http://192.168.1.1/start.ghtml'
    #req = urllib2.Request(url)
    #response = opener.open(req)
    #print d


    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1 SID='+SID))
    opener.addheaders.append(('Referer', 'http://'+address+'/start.ghtml'))
    url = 'http://'+address+'/template.gch'
    req = urllib2.Request(url)
    response = opener.open(req)
    d = response.read()
    
    opener.close()

    try:
        session_token = re.search('var session_token = "(.+?)";', d).group(1)
    except AttributeError:   
        session_token = '' # apply your error handling

    if (session_token == ''):
        print "No session token found"
        exit()

    #print session_token
    return session_token
    
    
##get frm_logintToken    
def getLoginToken(address):   
    opener = urllib2.build_opener()
    url = 'http://'+address+'/'
    response = opener.open(url)
    d = response.read()
    opener.close()
    try:
        loginToken = re.search('\("Frm_Logintoken", "(.+?)"\),', d).group(1)
    except AttributeError:   
        loginToken = '' # apply your error handling

    if (loginToken == ''):
        print "No login token found"
        exit()
    
    return loginToken;
    
    
def getSID(address,user,password,loginToken):

    #login
    randNumber = round(random.random()*89999999,0)+10000000;
    #print str (randNumber)[:8]
    password = hashlib.sha256(b'Angel666'+str(randNumber)[:8]).hexdigest()
    #print password


    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
        cookie = ''
        def http_error_302(self, req, fp, code, msg, headers):
            #print "Cookie Manip Right Here"
            self.cookie=headers['Set-Cookie']
            #print cookie
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302


    cookieprocessor = urllib2.HTTPCookieProcessor()
    redirecthandler = MyHTTPRedirectHandler()
    opener = urllib2.build_opener(redirecthandler,cookieprocessor)
    #print redirecthandler.cookie

    opener.addheaders.append(('Host', address))
    opener.addheaders.append(('Origin', 'http://'+address))
    opener.addheaders.append(('Referer', 'http://'+address))
    opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1'))
    opener.addheaders.append(('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'))
    url = 'http://'+address+'/'
    data = urllib.urlencode({'action' : 'login' , 'Username' : user, 'Password' : password, 'Frm_Logintoken' : loginToken ,'UserRandomNum' : str(randNumber)[:8], 'port' : ''})
    #print data
    req = urllib2.Request(url, data)
    response = opener.open(req)
    d = response.read()
    opener.close()

    splitData = redirecthandler.cookie.split(';')

    value = None

    for x in splitData:
      if x.find("SID") !=-1:
        value = (x.split('='))[1]
        
    if value is None:
        print "SID value not found"
        exit()
        
    #print "Request session"+value
        
    return value
    


def enable2G (address,SID, session_token):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1 SID='+SID))
    url = 'http://'+address+'/getpage.gch?pid=1002&nextpage=net_wlanm_conf1_t.gch'
    data = urllib.urlencode({"IF_ACTION":"apply","IF_ERRORSTR":"SUCC","IF_ERRORPARAM":"SUCC","IF_ERRORTYPE":"-1","IF_CONFIGTAG":"Y","SettingStatus":"NULL","CardIsIn":"NULL","MaxInterface":"NULL","DeviceMode":"NULL","CardMode":"NULL","CardRev":"NULL","Class":"NULL","PID":"NULL","VID":"NULL","ValidIf":"NULL","Enable":"NULL","RadioStatus":"1","Standard":"NULL","BeaconInterval":"75","RtsCts":"2347","Fragment":"2346","DTIM":"1","TxPower":"100%","CountryCode":"esI","TxRate":"NULL","Channel":"NULL","ESSID":"NULL","ESSIDPrefix":"NULL","ACLPolicy":"NULL","BeaconType":"NULL","WEPAuthMode":"NULL","WEPEncryptionLevel":"NULL","WEPKeyIndex":"NULL","WPAAuthMode":"NULL","WPAEncryptType":"NULL","WPAGroupRekey":"NULL","WPAEAPServerIp":"NULL","RadiusPort":"NULL","RadiusServerPort":"NULL","WPAEAPSecret":"NULL","PossibleChannels":"NULL","BasicDataRates":"1,2,5.5,11","OpDataRates":"1,2,5.5,11,6,9,12,18,24,36,48,54","PossibleTxRates":"NULL","OOBAccessEnabled":"NULL","BeaconEnabled":"NULL","ESSIDHideEnable":"NULL","RegulatoryDomain":"NULL","WlanMode":"NULL","DistanceFromRoot":"NULL","PeerBSSID":"NULL","AuthServiceMode":"NULL","QosType":"WMM","Priority":"NULL","UAPSDEnabled":"NULL","AutoChannelEnabled":"1","ChannelsInUse":"NULL","11iAuthMode":"NULL","11iEncryptType":"NULL","MaxUserNum":"NULL","SSIDIsolationEnable":"0","VapIsolationEnable":"NULL","Band":"NULL","11nMode":"1","BandWidth":"Auto","SideBand":"NULL","11nRate":"NULL","SGIEnabled":"1","GreenField":"0","WdsMode":"WDS_Disable","11acMode":"0","DynamicChannelSelection":"0","cnI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","cnI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","cnI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","caI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11","caI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11","caI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11","egI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","egI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","egI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","usI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11","usI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11","usI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11","country_1,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","_SESSION_TOKEN":session_token})
    #print data
    req = urllib2.Request(url, data)
    response = opener.open(req)
    d = response.read()
    #print d
    opener.close()
    return
    
    
def disable2G (address,SID, session_token):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1 SID='+SID))
    url = 'http://'+address+'/getpage.gch?pid=1002&nextpage=net_wlanm_conf1_t.gch'
    data = urllib.urlencode({"IF_ACTION":"apply","IF_ERRORSTR":"SUCC","IF_ERRORPARAM":"SUCC","IF_ERRORTYPE":"-1","IF_CONFIGTAG":"Y","SettingStatus":"NULL","CardIsIn":"NULL","MaxInterface":"NULL","DeviceMode":"NULL","CardMode":"NULL","CardRev":"NULL","Class":"NULL","PID":"NULL","VID":"NULL","ValidIf":"NULL","Enable":"NULL","RadioStatus":"0","Standard":"NULL","BeaconInterval":"75","RtsCts":"2347","Fragment":"2346","DTIM":"1","TxPower":"100%","CountryCode":"esI","TxRate":"NULL","Channel":"NULL","ESSID":"NULL","ESSIDPrefix":"NULL","ACLPolicy":"NULL","BeaconType":"NULL","WEPAuthMode":"NULL","WEPEncryptionLevel":"NULL","WEPKeyIndex":"NULL","WPAAuthMode":"NULL","WPAEncryptType":"NULL","WPAGroupRekey":"NULL","WPAEAPServerIp":"NULL","RadiusPort":"NULL","RadiusServerPort":"NULL","WPAEAPSecret":"NULL","PossibleChannels":"NULL","BasicDataRates":"1,2,5.5,11","OpDataRates":"1,2,5.5,11,6,9,12,18,24,36,48,54","PossibleTxRates":"NULL","OOBAccessEnabled":"NULL","BeaconEnabled":"NULL","ESSIDHideEnable":"NULL","RegulatoryDomain":"NULL","WlanMode":"NULL","DistanceFromRoot":"NULL","PeerBSSID":"NULL","AuthServiceMode":"NULL","QosType":"WMM","Priority":"NULL","UAPSDEnabled":"NULL","AutoChannelEnabled":"1","ChannelsInUse":"NULL","11iAuthMode":"NULL","11iEncryptType":"NULL","MaxUserNum":"NULL","SSIDIsolationEnable":"0","VapIsolationEnable":"NULL","Band":"NULL","11nMode":"1","BandWidth":"Auto","SideBand":"NULL","11nRate":"NULL","SGIEnabled":"1","GreenField":"0","WdsMode":"WDS_Disable","11acMode":"0","DynamicChannelSelection":"0","cnI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","cnI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","cnI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","caI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11","caI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11","caI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11","egI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","egI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","egI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","usI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11","usI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11","usI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11","country_1,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","_SESSION_TOKEN":session_token})
    #print data
    req = urllib2.Request(url, data)
    response = opener.open(req)
    d = response.read()
    #print d
    opener.close()
    return


def enable5G (address,SID, session_token):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1 SID='+SID))
    url = 'http://'+address+'/getpage.gch?pid=1002&nextpage=net_wlanm_conf2_t.gch'
    data = urllib.urlencode({"IF_ACTION":"apply","IF_ERRORSTR":"SUCC","IF_ERRORPARAM":"SUCC","IF_ERRORTYPE":"-1","IF_CONFIGTAG":"Y","SettingStatus":"NULL","CardIsIn":"NULL","MaxInterface":"NULL","DeviceMode":"NULL","CardMode":"NULL","CardRev":"NULL","Class":"NULL","PID":"NULL","VID":"NULL","ValidIf":"NULL","Enable":"NULL","RadioStatus":"1","Standard":"NULL","BeaconInterval":"75","RtsCts":"2347","Fragment":"2346","DTIM":"1","TxPower":"80%","CountryCode":"esI","TxRate":"NULL","Channel":"100","ESSID":"NULL","ESSIDPrefix":"NULL","ACLPolicy":"NULL","BeaconType":"NULL","WEPAuthMode":"NULL","WEPEncryptionLevel":"NULL","WEPKeyIndex":"NULL","WPAAuthMode":"NULL","WPAEncryptType":"NULL","WPAGroupRekey":"NULL","WPAEAPServerIp":"NULL","RadiusPort":"NULL","RadiusServerPort":"NULL","WPAEAPSecret":"NULL","PossibleChannels":"NULL","BasicDataRates":"1,2,5.5,11,6,9,12,18,24","OpDataRates":"1,2,5.5,11,6,9,12,18,24,36,48,54","PossibleTxRates":"NULL","OOBAccessEnabled":"NULL","BeaconEnabled":"NULL","ESSIDHideEnable":"NULL","RegulatoryDomain":"NULL","WlanMode":"NULL","DistanceFromRoot":"NULL","PeerBSSID":"NULL","AuthServiceMode":"NULL","QosType":"WMM","Priority":"NULL","UAPSDEnabled":"NULL","AutoChannelEnabled":"0","ChannelsInUse":"NULL","11iAuthMode":"NULL","11iEncryptType":"NULL","MaxUserNum":"NULL","SSIDIsolationEnable":"0","VapIsolationEnable":"NULL","Band":"NULL","11nMode":"1","BandWidth":"80MHz","SideBand":"NULL","11nRate":"NULL","SGIEnabled":"1","GreenField":"0","WdsMode":"WDS_Disable","11acMode":"1","DynamicChannelSelection":"NULL","cnI,5G,20MHz":"36,40,44,48,52,56,60,64,149,153,157,161,165","cnI,5G,40MHz":"36,40,44,48,52,56,60,64,149,153,157,161","cnI,5G,80MHz":"36,40,44,48,52,56,60,64,149,153,157,161","cnI,5G,Auto":"36,40,44,48,52,56,60,64,149,153,157,161","auI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","auI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","auI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","auI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","brI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","brI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","brI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","brI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","caI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","caI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","caI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","caI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","egI,5G,20MHz":"36,40,44,48,52,56,60,64,149,153,157,161,165","egI,5G,40MHz":"36,40,44,48,52,56,60,64,149,153,157,161","egI,5G,80MHz":"36,40,44,48,52,56,60,64,149,153,157,161","egI,5G,Auto":"36,40,44,48,52,56,60,64,149,153,157,161","frI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","frI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","frI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","frI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","deI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","deI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","deI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","deI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","grI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","grI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","grI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","grI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","hkI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","hkI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","hkI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","hkI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","itI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","itI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","itI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","itI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","krI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161","krI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","krI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","krI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","esI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","esI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,132,136","esI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112","esI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112","gbI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","gbI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","gbI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","gbI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","usI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","usI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","usI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","usI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","country_1,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165,34,38,42,46","_SESSION_TOKEN":session_token})
    #print data
    req = urllib2.Request(url, data)
    response = opener.open(req)
    d = response.read()
    #print d
    opener.close()
    return

def disable5G (address,SID, session_token):
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie', '_TESTCOOKIESUPPORT=1 SID='+SID))
    url = 'http://'+address+'/getpage.gch?pid=1002&nextpage=net_wlanm_conf2_t.gch'
    data = urllib.urlencode({"IF_ACTION":"apply","IF_ERRORSTR":"SUCC","IF_ERRORPARAM":"SUCC","IF_ERRORTYPE":"-1","IF_CONFIGTAG":"Y","SettingStatus":"NULL","CardIsIn":"NULL","MaxInterface":"NULL","DeviceMode":"NULL","CardMode":"NULL","CardRev":"NULL","Class":"NULL","PID":"NULL","VID":"NULL","ValidIf":"NULL","Enable":"NULL","RadioStatus":"0","Standard":"NULL","BeaconInterval":"75","RtsCts":"2347","Fragment":"2346","DTIM":"1","TxPower":"80%","CountryCode":"esI","TxRate":"NULL","Channel":"100","ESSID":"NULL","ESSIDPrefix":"NULL","ACLPolicy":"NULL","BeaconType":"NULL","WEPAuthMode":"NULL","WEPEncryptionLevel":"NULL","WEPKeyIndex":"NULL","WPAAuthMode":"NULL","WPAEncryptType":"NULL","WPAGroupRekey":"NULL","WPAEAPServerIp":"NULL","RadiusPort":"NULL","RadiusServerPort":"NULL","WPAEAPSecret":"NULL","PossibleChannels":"NULL","BasicDataRates":"1,2,5.5,11,6,9,12,18,24","OpDataRates":"1,2,5.5,11,6,9,12,18,24,36,48,54","PossibleTxRates":"NULL","OOBAccessEnabled":"NULL","BeaconEnabled":"NULL","ESSIDHideEnable":"NULL","RegulatoryDomain":"NULL","WlanMode":"NULL","DistanceFromRoot":"NULL","PeerBSSID":"NULL","AuthServiceMode":"NULL","QosType":"WMM","Priority":"NULL","UAPSDEnabled":"NULL","AutoChannelEnabled":"0","ChannelsInUse":"NULL","11iAuthMode":"NULL","11iEncryptType":"NULL","MaxUserNum":"NULL","SSIDIsolationEnable":"0","VapIsolationEnable":"NULL","Band":"NULL","11nMode":"1","BandWidth":"80MHz","SideBand":"NULL","11nRate":"NULL","SGIEnabled":"1","GreenField":"0","WdsMode":"WDS_Disable","11acMode":"1","DynamicChannelSelection":"NULL","cnI,5G,20MHz":"36,40,44,48,52,56,60,64,149,153,157,161,165","cnI,5G,40MHz":"36,40,44,48,52,56,60,64,149,153,157,161","cnI,5G,80MHz":"36,40,44,48,52,56,60,64,149,153,157,161","cnI,5G,Auto":"36,40,44,48,52,56,60,64,149,153,157,161","auI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","auI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","auI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","auI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","brI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","brI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","brI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","brI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","caI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","caI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","caI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","caI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","egI,5G,20MHz":"36,40,44,48,52,56,60,64,149,153,157,161,165","egI,5G,40MHz":"36,40,44,48,52,56,60,64,149,153,157,161","egI,5G,80MHz":"36,40,44,48,52,56,60,64,149,153,157,161","egI,5G,Auto":"36,40,44,48,52,56,60,64,149,153,157,161","frI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","frI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","frI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","frI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","deI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","deI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","deI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","deI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","grI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","grI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","grI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","grI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","hkI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","hkI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","hkI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","hkI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","itI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","itI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","itI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","itI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","krI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161","krI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","krI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","krI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","esI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","esI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,132,136","esI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112","esI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112","gbI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","gbI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","gbI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","gbI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","usI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","usI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","usI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","usI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","country_1,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165,34,38,42,46","_SESSION_TOKEN":session_token})
    #print data
    req = urllib2.Request(url, data)
    response = opener.open(req)
    d = response.read()
    #print d
    opener.close()
    return
    
#Enable 2G
#'http://192.168.1.1/getpage.gch?pid=1002&nextpage=net_wlanm_conf1_t.gch'
#{"IF_ACTION":"apply","IF_ERRORSTR":"SUCC","IF_ERRORPARAM":"SUCC","IF_ERRORTYPE":"-1","IF_CONFIGTAG":"Y","SettingStatus":"NULL","CardIsIn":"NULL","MaxInterface":"NULL","DeviceMode":"NULL","CardMode":"NULL","CardRev":"NULL","Class":"NULL","PID":"NULL","VID":"NULL","ValidIf":"NULL","Enable":"NULL","RadioStatus":"1","Standard":"NULL","BeaconInterval":"75","RtsCts":"2347","Fragment":"2346","DTIM":"1","TxPower":"100%","CountryCode":"esI","TxRate":"NULL","Channel":"NULL","ESSID":"NULL","ESSIDPrefix":"NULL","ACLPolicy":"NULL","BeaconType":"NULL","WEPAuthMode":"NULL","WEPEncryptionLevel":"NULL","WEPKeyIndex":"NULL","WPAAuthMode":"NULL","WPAEncryptType":"NULL","WPAGroupRekey":"NULL","WPAEAPServerIp":"NULL","RadiusPort":"NULL","RadiusServerPort":"NULL","WPAEAPSecret":"NULL","PossibleChannels":"NULL","BasicDataRates":"1,2,5.5,11","OpDataRates":"1,2,5.5,11,6,9,12,18,24,36,48,54","PossibleTxRates":"NULL","OOBAccessEnabled":"NULL","BeaconEnabled":"NULL","ESSIDHideEnable":"NULL","RegulatoryDomain":"NULL","WlanMode":"NULL","DistanceFromRoot":"NULL","PeerBSSID":"NULL","AuthServiceMode":"NULL","QosType":"WMM","Priority":"NULL","UAPSDEnabled":"NULL","AutoChannelEnabled":"1","ChannelsInUse":"NULL","11iAuthMode":"NULL","11iEncryptType":"NULL","MaxUserNum":"NULL","SSIDIsolationEnable":"0","VapIsolationEnable":"NULL","Band":"NULL","11nMode":"1","BandWidth":"Auto","SideBand":"NULL","11nRate":"NULL","SGIEnabled":"1","GreenField":"0","WdsMode":"WDS_Disable","11acMode":"0","DynamicChannelSelection":"0","cnI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","cnI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","cnI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","auI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","brI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","caI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11","caI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11","caI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11","egI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","egI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","egI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","frI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","deI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","grI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","hkI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","itI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","krI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","esI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","gbI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11,12,13","usI,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11","usI,2.4G,40MHz":"1,2,3,4,5,6,7,8,9,10,11","usI,2.4G,Auto":"1,2,3,4,5,6,7,8,9,10,11","country_1,2.4G,20MHz":"1,2,3,4,5,6,7,8,9,10,11,12,13","_SESSION_TOKEN":session_token}

#Enable 5G
#'http://192.168.1.1/getpage.gch?pid=1002&nextpage=net_wlanm_conf2_t.gch'
#{"IF_ACTION":"apply","IF_ERRORSTR":"SUCC","IF_ERRORPARAM":"SUCC","IF_ERRORTYPE":"-1","IF_CONFIGTAG":"Y","SettingStatus":"NULL","CardIsIn":"NULL","MaxInterface":"NULL","DeviceMode":"NULL","CardMode":"NULL","CardRev":"NULL","Class":"NULL","PID":"NULL","VID":"NULL","ValidIf":"NULL","Enable":"NULL","RadioStatus":"1","Standard":"NULL","BeaconInterval":"75","RtsCts":"2347","Fragment":"2346","DTIM":"1","TxPower":"80%","CountryCode":"esI","TxRate":"NULL","Channel":"100","ESSID":"NULL","ESSIDPrefix":"NULL","ACLPolicy":"NULL","BeaconType":"NULL","WEPAuthMode":"NULL","WEPEncryptionLevel":"NULL","WEPKeyIndex":"NULL","WPAAuthMode":"NULL","WPAEncryptType":"NULL","WPAGroupRekey":"NULL","WPAEAPServerIp":"NULL","RadiusPort":"NULL","RadiusServerPort":"NULL","WPAEAPSecret":"NULL","PossibleChannels":"NULL","BasicDataRates":"1,2,5.5,11,6,9,12,18,24","OpDataRates":"1,2,5.5,11,6,9,12,18,24,36,48,54","PossibleTxRates":"NULL","OOBAccessEnabled":"NULL","BeaconEnabled":"NULL","ESSIDHideEnable":"NULL","RegulatoryDomain":"NULL","WlanMode":"NULL","DistanceFromRoot":"NULL","PeerBSSID":"NULL","AuthServiceMode":"NULL","QosType":"WMM","Priority":"NULL","UAPSDEnabled":"NULL","AutoChannelEnabled":"0","ChannelsInUse":"NULL","11iAuthMode":"NULL","11iEncryptType":"NULL","MaxUserNum":"NULL","SSIDIsolationEnable":"0","VapIsolationEnable":"NULL","Band":"NULL","11nMode":"1","BandWidth":"80MHz","SideBand":"NULL","11nRate":"NULL","SGIEnabled":"1","GreenField":"0","WdsMode":"WDS_Disable","11acMode":"1","DynamicChannelSelection":"NULL","cnI,5G,20MHz":"36,40,44,48,52,56,60,64,149,153,157,161,165","cnI,5G,40MHz":"36,40,44,48,52,56,60,64,149,153,157,161","cnI,5G,80MHz":"36,40,44,48,52,56,60,64,149,153,157,161","cnI,5G,Auto":"36,40,44,48,52,56,60,64,149,153,157,161","auI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","auI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","auI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","auI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","brI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","brI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","brI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","brI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","caI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","caI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","caI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","caI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","egI,5G,20MHz":"36,40,44,48,52,56,60,64,149,153,157,161,165","egI,5G,40MHz":"36,40,44,48,52,56,60,64,149,153,157,161","egI,5G,80MHz":"36,40,44,48,52,56,60,64,149,153,157,161","egI,5G,Auto":"36,40,44,48,52,56,60,64,149,153,157,161","frI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","frI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","frI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","frI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","deI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","deI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","deI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","deI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","grI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","grI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","grI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","grI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","hkI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","hkI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","hkI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","hkI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","itI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","itI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","itI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","itI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","krI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161","krI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","krI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","krI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","esI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","esI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,132,136","esI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112","esI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112","gbI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140","gbI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136","gbI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","gbI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128","usI,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165","usI,5G,40MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,149,153,157,161","usI,5G,80MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","usI,5G,Auto":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,149,153,157,161","country_1,5G,20MHz":"36,40,44,48,52,56,60,64,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165,34,38,42,46","_SESSION_TOKEN":session_token}