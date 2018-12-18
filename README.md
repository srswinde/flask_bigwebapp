# flask_bigwebapp
Flask app to display important information to user of Kuiper Telescope

## Config
This app requires a config json file with the BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD. You can pass the path of this config file as an argument or stick with the defualt.

## Installation
sudo python3 setup.py install
This will also restart the appache server to relaod the app.

## run locally
python3 __init__.py <Path to config>

## Add a module

Add a .py file with your flask stuff and import in the __init__.py. 
