useradd metrics
cp mineratormetrics.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable mineratormetrics
systemctl start mineratormetrics

