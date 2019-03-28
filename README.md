# vpn_check_expired
# need pyopenssl
pip install pyopenssl

# config your ENV

mailname = "VPN Checker"
mailsrv = "10.10.10.10"
mailsrvport = 25
mailsubject  = "Openvpn key file will expire soon , please check !!"
undovpn=['xxx.crt','yyy.crt']
adminmail = 'your@mail'
key_path='/etc/openvpn/keys/'
expired=30

# put vpn_check.py to crontab , and get happy
