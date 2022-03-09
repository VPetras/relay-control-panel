# relay-control-panel
web app for controling relays with raspberry pi

# install

`./install.sh `

# running

`./app.py `

# using

Open your browser. Type ip adress with port 8000 (for example: http://192.168.0.1:8000) and click on buttons :D

# setup systemd service
Copy service file into /etc/system/systemd:
`sudo cp relay-control.service /etc/systemd/system/.`
Enable systemd service:
`sudo systemctl enable relay-control.service`
Start systemd service:
`sudo systemctl start relay-control.service`
