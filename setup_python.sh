#run from minerator-metric root dir (not setup)

DIR=/var/local/minerator-metrics/
apt-get install -y python3 python3-venv python3.6-venv
pyvenv-3.6 ${DIR}/venv
${DIR}/venv/bin/pip install prometheus_client requests
