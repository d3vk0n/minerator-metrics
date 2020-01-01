#Sets up the ubuntu firewall to allow remote access to grafana
#Run as root

ufw allow 3000/tcp #grafana
ufw allow 9090/tcp #prometheus.. handy for testing
ufw allow 80/tcp #for allmine web interface
ufw allow 22/tcp #ssh
ufw enable

#some systems have this too
if type firewall-cmd  &> /dev/null ; then
	firewall-cmd --add-port=3000/tcp --permanent
	firewall-cmd --add-port=22/tcp --permanent
	firewall-cmd --add-port=80/tcp --permanent
	firewall-cmd --add-port=9090/tcp --permanent
	firewall-cmd --reload
fi
