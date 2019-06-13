#Sets up the ubuntu firewall to allow remote access to grafana
#Run as root
ufw allow 3000/tcp
ufw enable

#some systems have this too
if type firewall-cmd  &> /dev/null ; then
	firewall-cmd --add-port=3000/tcp --permanent
	firewall-cmd --reload
fi
