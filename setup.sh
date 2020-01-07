add-apt-repository universe
apt-get -y install prometheus curl

#Configure prometheus
p_config=/etc/prometheus/prometheus.yml
if ! grep -q minerator $p_config ; then
	cat prometheus_target.yml >> $p_config
fi

systemctl restart prometheus

##Install Grafana
curl https://packages.grafana.com/gpg.key | apt-key add -
add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update
sudo apt-get -y install grafana

systemctl daemon-reload
systemctl enable grafana-server

#Configure grafana?
#Install grafana plugs
grafana-cli plugins install yesoreyeram-boomtable-panel 1.0.0
grafana-cli plugins install natel-discrete-panel 0.0.9

systemctl start grafana-server


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


