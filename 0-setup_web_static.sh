#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# update the package database
sudo apt-get -y update
# download available package updates
sudo apt-get upgrade
# install nginx web server
sudo apt-get -y install nginx

# create the folders
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# create a simple html file with simple content to test
sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
    <head></head>
    <body>Holberton School</body>
</html>" | sudo tee /data/web_static/releases/test/index.html

# create a symbolic link /data/web_static/current linked to
#   the /data/web_static/releases/test/ folder
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of the /data/ folder to the ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content
#   of /data/web_static/current/ to hbnb_static
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# restart Nginx server
sudo service nginx restart
