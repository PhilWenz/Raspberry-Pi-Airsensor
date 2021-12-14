
sudo apt-get install python3-venv -y
python3 -m venv ~/my_venv
source ~/my_venv/bin/activate
pip install -r requirements.txt

#wierd stuff for DHT Sensor
git clone https://github.com/coding-world/Python_DHT.git
cd Python_DHT
sudo python3 setup.py install
cd ..
sudo pip3 install adafruit-circuitpython-dht
sudo apt-get install libgpiod2