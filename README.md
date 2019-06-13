# minerator-metrics

Visualisations for Minerator using Prometheus/Grafana.

# Setup

For Ubuntu 18.04 systems the setup.sh script can be used (run as root).
For other systems, check the scripts to see what needs installing/configuring.

# Confirm Prometheus Installed

Prometheus is only available from the minerator system.

Goto localhost:9090 from your minerator system. You should see Prometheus web interface.
Go to Status->Targets and you should see "minerator" target, and it should be up.

# Grafana Configuration

Grafana should be up on port 3000 on your minerator box. 

Access grafana and log in with default username "admin", password "admin" and change your password.

## Add Prometheus Datasource

* Click "Add data source", select "Prometheus".
* set URL to "http://localhost:9090".
* Ensure name is "Prometheus".
* Click "Save and Test" and Prometheus should be configured with grafana

## Import Dashboards

* On the left hand side of Grafana, click the "+" symbol
* Select Import Dashboard
* Click "Upload .json File" and select Minerator-Overview.json from minerator-metrics/dashboards
* Repeat process for Device, Core, Phase, and Sysmon dashboards

# Multiple rigs

No dashboard for this, but metrics have a "rig" label that could be used to create one.












