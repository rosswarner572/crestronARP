import time
import telnetlib
import smtplib, ssl

### Variables   ###

#TelNet Variables
telnetPort = 23
telnetTimeOut = 2
telnetHost = ''
#tn = telnetlib.Telnet(telnetHost)

#SMTP/Mail Variables
sslPort = 465
testport = 1025
testserver = 'localhost'
smtp_server = 'smtp.gmail.com'
password = 'Rossan0vA!'
sender_email = 'de1815crestron@gmail.com'
receiver_email = 'rwarner@incyte.com'
email_message = 'test message'
server = smtplib.SMTP(testserver, testport)

#Crestron Variables
##processorHostAddr = {
##	'Room 24141': '10.202.17.52',
##	'Room 24107': '10.202.17.58',
##	'Room 24108': '10.202.17.54',
##	'Room 24121': '10.202.17.31',
##	'Room 24130': '10.202.17.25',
##	'Room 24131': '10.202.16.11',
##	'Room 24140': '10.202.16.27',
##	'Room 24200': '10.202.16.20',
##	'Room 23118': '10.202.15.28',
##	'Room 22107': '10.202.13.28',
##	'Room 21115': '10.202.11.25',
##	'Room 21106': '10.202.10.32',
##	'Room 21101': '10.202.10.30',
##	'Town Hall': '10.202.17.77'
##	}

###     for testing only    ###
##processorHostAddr = {
##        'CP3 Timeout': '192.168.1.3',
##        'CP3 One': '192.168.1.5',
##        'CP3 Two': '192.168.1.6'
##        }


arpCompareList = [
	'192.168.1.101',
	'192.168.1.141',
	'192.168.1.142',
	'192.168.1.143',
        '172.22.248.151'
	]

#defined here so that it is global
currentConnectedProcessor = ''
arpAddresses = []
compareResults = []
noMatch = []

		
###     Functions   ###

#Jumpstart the Connection
def jumpConnect():
        tn.write(b'\r\n')
        time.sleep(1)
        tn.write(b'\r\n')
        time.sleep(1)

#send showarptable cmd to processor and give time to respond
def arpQuery():
	tn.write(b'showarptable\r\n')
	time.sleep(5)

#build the arp list from the recv'd data
def arpListBuild():
        tn_read = tn.read_very_eager()
        #print(type(tn_read))
        #print(repr(tn_read))
        tn_decode = tn_read.decode('iso8859-1')
        tn_split = tn_decode.split('Internet Address       Physical Address')
        removeFirst = tn_split.pop(0)
        for x in tn_split:
                x = x[2:17]
                x = x.replace(' ', '')
                arpAddresses.append(x)
        print(arpAddresses)
                

#compare arpAddresses to arpCompareList
def arpCompare():
        for x in arpCompareList:
                if x in arpAddresses:
                        compareResults.append('yes - ' + x)
                else:
                        compareResults.append('no - ' + x)
        print(compareResults)

#make a list of addresses that aren't showing up
def findAlerts():
        alertString = 'no'
        for missing in compareResults:
                if alertString in missing:
                        noMatch.append(missing)
        if len(noMatch) == 0:
                print(currentConnectedProcessor + ' - All Devices Connected')
        elif len(noMatch) > 0:
                sendAlert()
        #print(len(noMatch))
        print(noMatch)
        

#send alert listing offline devices
def sendAlert():
##    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
##            server.login('de1815crestron@gmail.com', password)
        #server = smtplib.SMTP(testserver, testport)
        email_message = (currentConnectedProcessor + ' has missing devices ' +str(noMatch))
        server.sendmail(sender_email, receiver_email, email_message)

def testSendAlert():
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
        #server = smtplib.SMTP(testserver, testport)
##                email_message = ('this is a test email')
                server.sendmail(sender_email, receiver_email, email_message)

#send alert that connection timed out
def timeoutAlert():
        email_message = (currentConnectedProcessor + ' is unreachable due to timeout.')
        print(email_message)
        server.sendmail(sender_email, receiver_email, email_message)

#send alert if connection was actively refused
def connectionRefusedAlert():
        email_message = (currentConnectedProcessor + ' actively refused the connection.')
        print(email_message)
        server.sendmail(sender_email, receiver_email, email_message)


###     MAIN PROG   ###
              
##for processor, addr in processorHostAddr.items():
##        try:
##                currentConnectedProcessor = processor
##                print('Connecting to ' + currentConnectedProcessor)
##                telnetHost = addr
##                tn = telnetlib.Telnet(telnetHost)
##                jumpConnect()
##                arpQuery()
##                arpListBuild()
##                arpCompare()
##                findAlerts()
##                time.sleep(5)
##                tn.close()
##                arpAddresses = []
##                compareResults = []
##                noMatch = []
##        except TimeoutError:
##                timeoutAlert()
##        except ConnectionRefusedError:
##                connectionRefusedAlert()


testSendAlert()
























