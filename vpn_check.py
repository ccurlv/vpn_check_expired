#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import re
import smtplib as sl
import logging
from OpenSSL import crypto as c
from email.MIMEText import MIMEText as mt

mailname = "VPN Checker"
mailsrv = "10.10.10.10"
mailsrvport = 25
mailsubject  = "Openvpn key file will expire soon , please check !!"
undovpn=['xxx.crt','yyy.crt']
adminmail = 'your@mail'
key_path='/etc/openvpn/keys/'
expired=30
logging.basicConfig( filename='/var/log/chkvpn.log', format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO )
logger = logging.getLogger( "chkvpn.py:" + __name__ )

def mailto(exp_arr):
    s=sl.SMTP()
    try:
        s.connect( mailsrv , mailsrvport )
        s.ehlo( mailsrv )
    except sl.SMTPException:
        logger.info( "Error: unable connect mail server" )
    finfo = " about to expire openvpn crt file : "
    for exp in exp_arr:
        finfo = finfo + "\n" + exp
    msg = mt( finfo )
    msg['Subject'] = mailsubject
    msg['From'] = mailname
    msg['To'] = adminmail
    try:
        s.sendmail( mailname , adminmail, msg.as_string() )
        logger.info( "Successfully sent email: " + adminmail )
    except sl.SMTPException:
        logger.info( "Error: unable to send email: " + adminmail )
    s.quit()

crtlist = [f for f in os.listdir(key_path) if re.match(r'.*\.crt', f)]
exp_arr = []
ts_now=datetime.datetime.now()
for key_name in crtlist:
    if not  key_name in undovpn:
        cert=c.load_certificate(c.FILETYPE_PEM,file(key_path+key_name).read())
        crtime=cert.get_notAfter()
        ts_after=datetime.datetime.strptime(crtime,'%Y%m%d%H%M%SZ')
        if (ts_after-ts_now).days < expired :
            exp_arr.append( key_name+" : "+str((ts_after-ts_now).days)+" days expired ("+ts_after.strftime("%Y-%m-%d %H:%M ")+")" )

if len(exp_arr) > 0 :
    mailto(exp_arr)
