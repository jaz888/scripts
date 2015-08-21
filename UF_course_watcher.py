#coding:utf-8
 
import httplib
import urllib
import time
import sys
import smtplib
from email.mime.text import MIMEText

HOST="www.isis.ufl.edu"
PORT=80
METHOD="POST"
REQUEST_URL="/cgi-bin/nirvana"
 
def http_request():
    #request parameters
    params=urllib.urlencode({
'MDASTRAN':'RSF-GRP   ',
'MDASKEYY':'COMPUTER & INFO SCI & ',
'REGCSE':'',
'searchby':'D',
#REGDEPT can be found in the post header of any course search request
'REGDEPT':'COMPUTER & INFO SCI & ',
'CRSEANYD':'Y',
'CRSEANYT':'Y',
#MDASSTTE and MDASCACH can be found in the page source of any course search result page
'MDASSTTE':'T0099581M0002069', 
'MDASCACH':'00081529',
    })
    #header
    headers={
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Encoding":"gzip, deflate",
"Accept-Language":"en-US,en;q=0.8",
"Cache-Control":"max-age=0",
"Connection":"keep-alive",
"Content-Length":"175",
"Content-Type":"application/x-www-form-urlencoded",
"Cookie":"myRecordStatus=block; treqStatus=none; pheadStatus=block; isiscookietest=it%20works; regStatus=block; eagAuxVal=XmN6240XlwAObEq0; _shibsession_75726e3a6564753a75666c3a70726f643a303031373175726e3a6564753a75666c3a70726f643a3030313731=_493ce472594530569c1225562fefd6f7; GSMsetBy=redirect; UF_GSM=PUxxQyhEil0W%2BsHnZRtSeQ%3D%3D; treqStatus=none; myRecordStatus=block; myAssessmentStatus=none; advisingStatus=none; elearnStatus=none; evalsStatus=none; finAidStatus=none; finSvcsStatus=block; oAcadStatus=block; oAdvisStatus=none; oFinanStatus=none; oGradStatus=none; oPersStatus=none; oSvcsStatus=none; isiscookieConfirm=yes; pheadStatus=block",
"Host":"www.isis.ufl.edu",
"Origin":"https://www.isis.ufl.edu",
"Referer":"https://www.isis.ufl.edu/cgi-bin/nirvana?MDASTRAN=RSF-RGCHK2",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.37 Safari/537.36",
    }
    conn=httplib.HTTPConnection(HOST,PORT)
    conn.request(METHOD,REQUEST_URL,params,headers)
    response=conn.getresponse()
    data=response.read()
    conn.close()
 
    return (response.status,response.reason,data)
     
if __name__=="__main__":

    while True:
        gap = 1
        status,result,data=http_request()
        #print status,result
        #print data
        if data.find('provide the number of an always existing course as a flag to determin if the system is down')==-1:
            print 'system down (',time.strftime('%H:%M',time.localtime(time.time())),')'
            time.sleep(600)
        else:
            if data.find('your desired course number')!=-1:
                gap += 10
                print '--found (',time.strftime('%H:%M',time.localtime(time.time())),')'
                msg = MIMEText("Find XX\n")
                msg['Subject'] = 'Find XX\n'
                msg['From'], msg['To'] = "your email address", "your email address"
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.ehlo()
                s.starttls()
                s.login(msg['From'], 'your email password')
                try:
                   # Python 3.2.1
                   s.send_message(msg)
                except AttributeError:
                   # Python 2.7.2
                   s.sendmail(msg['From'], [msg['To']], msg.as_string())
                s.quit()
            else:
                print 'Algo not found (',time.strftime('%H:%M',time.localtime(time.time())),')'

        time.sleep(gap*30)

