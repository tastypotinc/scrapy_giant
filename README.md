https://github.com/terryh/autotrader
https://www.quantopian.com/help#api-doco
http://docs.mongodb.org/manual/tutorial/write-a-tumblelog-application-with-django-mongodb-engine/
https://hshah19.wordpress.com/2013/08/23/setting-up-celery-for-django-using-django-celery-rabbitmq-supervisor-and-monit/
https://github.com/funningboy/django-tutorial-for-programmers/blob/master/25-deploy-to-ubuntu-server.md

vnc
https://www.howtoforge.com/how-to-install-vnc-server-on-ubuntu-14.04

openvpn
https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-14-04

ii
Mac OS setup flow
0.1 #install anaconda python
https://store.continuum.io/cshop/anaconda/

0.2 install external conda libs
```
conda install opencv
conda install gunicorn
```
0.3 install external python pkgs
```
pip install -r requirements.txt
port install tesseract
```

ubuntu setup flow
0.1 #install anaconda python
https://store.continuum.io/cshop/anaconda/

0.2 install external conda libs
```
conda install scrapy
conda install opencv
conda install mongodb
conda install -c Quantopian zipline
use latest zipline from github
https://github.com/quantopian/zipline
cd conda
conda build zipline >= 0.8.0
```
0.3 install drive libs
```
apt-get install rabbitmq-server
apt-get install nginx
apt-get install tesseract-ocr
```
0.3.1 install 3path libs
```
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
untar and cd
./configure --prefix=/usr
make 
make install
```
0.4 install python wrappers
```
easy_install TA-Lib
pip install Pillow
pip install mongoengine
#pip install zipline
pip install celery
pip install celery-with-mongodb
pip install supervisor
pip install mongodb-cache
pip install pytesseract  

#pip install mongengineform
pip install django-rest-framework-mongoengine
# for django mongodb engine used
# https://django-mongodb-engine.readthedocs.org/en/latest/topics/setup.html
pip install git+https://github.com/django-nonrel/django@nonrel-1.5
pip install git+https://github.com/django-nonrel/djangotoolbox
pip install git+https://github.com/django-nonrel/mongodb-engine
pip install django_nose
pip install django_compressor
```

0.5 normal run
broker=rabbitmq
backend=mongodb
```
sudo service supervisor start
echo_supervisord_conf > supervisord.con
sudo /root/anaconda/bin/supervisorctl -c /etc/supervisor/supervisord.conf
sudo  /usr/lib/rabbitmq/lib/rabbitmq_server-3.2.4/sbin/rabbitmq-plugins enable rabbitmq_management

rabbitmqctl cluster MASTER SLAVE
rabbitmqctl start_app
rabbitmq-server
# rabbitmq-server -detached
# rabbitmqctl stop
#sudo netstat -tulpn | grep :27017
# kill -9 <pid> if proc has running the same port
ps aux | grep celery | awk '{print $2}' | xargs kill -9
celeryctl purge
>>> from celery.task.control import discard_all
>>> discard_all()
lsof -i tcp | grep LISTEN
mongod --dbpath ./tmp --journal
export DJANGO_SETTINGS_MODULE=giant.settings 
export DJANGO_PROJECT_DIR=`pwd`
export C_FORCE_ROOT=true
# for normal mode
export ROOTPATH=./data
# for test mode
export ROOTPATH=./tmp
celery -A giant worker -B -l info -c 4 -P gevent
python manage.py syncdb
python manage.py shell
celery scheduler
scrapy crawl twsehisstock -s LOG_FILE=twsehisstock.log -s GIANT_DEBUG=1 -s GIANT_LIMIT=1 -s LOG_LEVEL=DEBUG
sudo ln -s /etc/nginx/sites-available/lunch /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo service nginx restart
sudo nginx -t
sudo fuser -k 80/tcp
```

0.6 as django unittest run
```
celery -A giant worker -B -l info
nosetests --nocapture test/test_start.py
nosetests --nocapture test/test_... 
python manage.py test bin --traceback
python manage.py test handler algorithm --traceback

sudo service supervisor start
sudo /root/anaconda/bin/supervisorctl -c /etc/supervisor/supervisord.conf
sudo service supervisor stop
```

ref:
Redis vs RabbitMQ
http://blog.langoor.mobi/django-celery-redis-vs-rabbitmq-message-broker/
run as celery task
trader/stock data align 
https://github.com/pydanny/django-mongonaut
```

TBDO
#https://eonasdan.github.io/bootstrap-datetimepicker/Installing/#minimal-requirements 

URLs:
http://127.0.0.1:8000/handler/api/hisstock_list/?opt=twse&starttime=2015/10/01&endtime=2015/10/10&stockids=2330&traderids=&algorithm=StockProfileRaw"

http://127.0.0.1:8000/handler/api/hisstock_detail/?opt=twse&starttime=2015/10/01&endtime=2015/10/10&stockids=2330&traderids=&algorithm=StockProfileRaw"

http://127.0.0.1:8000/handler/api/hisstock_detail/?opt=twse
