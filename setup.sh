add-apt-repository universe
apt-get -y install prometheus curl

#Configure prometheus
p_config=/etc/prometheus/prometheus.yml
if ! grep -q minerator $p_config ; then
	cat prometheus_target.yml >> $p_config
fi

systemctl restart prometheus


#Configure firewall
#Allow user to do this themselves
#./setup_network.sh


mkdir /var/local/minerator-metrics
cp minerator_metrics.py /var/local/minerator-metrics/
./setup_python.sh

./setup_service.sh


echo """
minerator-metrics installation complete.
If you want to access grafana from another computer you _may_ need to run setup_network.sh (as root)
This will configure and enable to ubuntu firewall
"""


