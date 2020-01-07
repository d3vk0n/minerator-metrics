
GRAFANA="http://localhost:3000"

#Setup the datasource
KEY=$1
if ! [ -n "$KEY" ] ; then
	echo "Usage:"
	echo "setup_grafana.sh API_KEY"
	echo "API key must be generated through grafana web interface"
	exit 1

fi
curl -d '{"isDefault": true, "name": "local_prometheus","type": "prometheus", "url": "http://localhost:9090", "access": "proxy", "basicAuth": false}' -H "Content-Type: application/json" -H "Authorization: Bearer $KEY" -X POST $GRAFANA/api/datasources


#Now add the dashboards

