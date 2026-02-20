# climate_data_exchange
python script to push aggregated data from Nepali Calendar to ISO Calendar 

Python Script to Auto sync Climet data from nepalhmis to dhis2 instance

# add flask for create web-app for DHIS2
## install

sudo apt install python3-pip

pip install flask requests python-dotenv

pip install --upgrade certifi

pip install --upgrade requests certifi urllib3

pip install flask-cors

pip install python-dotenv

pip install psycopg2-binary

pip install clickhouse-connect

pip install nepali-date_converter

pip install npdatetime

pip install datetime

#https://pypi.org/project/nepali-calendar-utils/

pip install nepali-calendar-utils

pip install nepali

pip install nepali-datetime


-- 
sudo apt update

sudo apt install python3-full python3-venv -y

-- Create virtual environment

cd /home/mithilesh/climet_data_exchange

python3 -m venv venv

-- Activate it

source venv/bin/activate

then

pip install nepali-datetime

pip install --upgrade requests certifi urllib3

pip install python-dotenv


-- now add cron inside that

-- Create virtual environment
cd /home/mithilesh/ippf_uin_orgunit_sync
python3 -m venv venv
-- Activate it
source venv/bin/activate

then
pip install python-dotenv
pip install --upgrade requests certifi urllib3
-- for run on putty
(venv) root@localhost:/home/mithilesh/ippf_uin_orgunit_sync# python main.py
cd /home/mithilesh/ippf_uin_orgunit_sync && /home/mithilesh/ippf_uin_orgunit_sync/venv/bin/python main.py

chmod +x /home/mithilesh/ippf_uin_orgunit_sync/main.py

chmod 755 /home/mithilesh/ippf_uin_orgunit_sync/logs
-- final schedular

55 11 * * * cd /home/mithilesh/ippf_uin_orgunit_sync && /home/mithilesh/ippf_uin_orgunit_sync/venv/bin/python main.py >> /home/mithilesh/ippf_uin_orgunit_sync/cronlogs_ippf_uin_orgunit_sync.log 2>&1


###############

this application Auto Sync/create the Organisationunit in new DHIS2 instance based on trackedentityinstance attribute value

and update the trackedentityinstance attribute value