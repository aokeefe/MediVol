#!/bin/bash

echo "Updating apt-get...";
sudo apt-get update;

printf "\nInstalling fish...";
sudo apt-get install fish -y;

awk -F':' '{system("sudo usermod -s /usr/bin/fish " $1)}' /etc/passwd;

printf "\nInstalling vim...";
sudo apt-get install vim -y;

printf "\nInstalling apache2...";
sudo apt-get install apache2 -y;

printf "\nInstalling apache python mod..."; 
sudo apt-get install libapache2-mod-wsgi -y; 

printf "\nEnabling ssl on apache...";
sudo a2enmod ssl; 

if [ -f /etc/apache2/sites-available/default ];
then
printf "\nDisabling default...";
sudo a2dissite default;
sudo service apache2 reload;
sudo rm /etc/apache2/sites-available/default;
fi

if [ -f /etc/apache2/sites-available/default-ssl ];
then
printf "\nDeleting default-ssl...";
sudo rm /etc/apache2/sites-available/default-ssl;
fi

if [ ! -f /etc/apache2/sites-available/medivol ];
then
printf "\nAdding medivol config...";
sudo cp /var/www/MediVol/medivol_apache_conf /etc/apache2/sites-available/medivol;
sudo a2ensite medivol;
sudo service apache2 reload;
fi

printf "\nRestarting apache...";
sudo service apache2 restart; 

printf "\nInstalling php5...";
sudo apt-get install php5 -y;

printf "\nInstalling mysql-server...";
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password root';
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password root';
sudo apt-get install mysql-server -y;

printf "\nInstalling phpMyAdmin...";
echo 'phpmyadmin phpmyadmin/dbconfig-install boolean true' | debconf-set-selections;
echo 'phpmyadmin phpmyadmin/reconfigure-webserver multiselect apache2' | debconf-set-selections;

echo 'phpmyadmin phpmyadmin/app-password-confirm password root' | debconf-set-selections;
echo 'phpmyadmin phpmyadmin/mysql/admin-pass password root' | debconf-set-selections;
echo 'phpmyadmin phpmyadmin/password-confirm password root' | debconf-set-selections;
echo 'phpmyadmin phpmyadmin/setup-password password ' | debconf-set-selections;
echo 'phpmyadmin phpmyadmin/database-type select mysql' | debconf-set-selections;
echo 'phpmyadmin phpmyadmin/mysql/app-pass password root' | debconf-set-selections;

echo 'dbconfig-common dbconfig-common/mysql/app-pass password root' | debconf-set-selections;
echo 'dbconfig-common dbconfig-common/mysql/app-pass password' | debconf-set-selections;
echo 'dbconfig-common dbconfig-common/password-confirm password root' | debconf-set-selections;
echo 'dbconfig-common dbconfig-common/app-password-confirm password root' | debconf-set-selections;
echo 'dbconfig-common dbconfig-common/app-password-confirm password root' | debconf-set-selections;
echo 'dbconfig-common dbconfig-common/password-confirm password root' | debconf-set-selections;
sudo apt-get install phpmyadmin -y;

if [ ! -f /var/www/phpmyadmin/index.php ];
then
	echo "Making phpMyAdmin link...";
	sudo ln -s /usr/share/phpmyadmin /var/www/phpmyadmin;
fi

printf '\nInstalling python-pip...';
sudo apt-get install python-pip -y;

printf '\nInstalling Django...';
sudo pip install Django==1.5;

printf '\nInstalling python-dev...';
sudo apt-get install python-dev -y;

printf '\nInstalling elaphe...';
sudo pip install elaphe==0.6.0;
printf '\nInstalling reportlab...';
sudo pip install reportlab==2.7;

printf '\nInstalling python-mysqldb...';
sudo apt-get install python-mysqldb -y;

printf '\nInstalling django-jenkins...';
sudo pip install django-jenkins==0.14.1;

printf '\nInstalling django_dajax...';
sudo pip install django-dajax==0.9.2;
sudo pip install django-dajaxice==0.5.5;

printf '\nInstalling pytz...';
sudo pip install pytz==2013.9;

printf '\nInstalling django-haystack...';
sudo pip install django-haystack==2.1.0;

printf '\nInstalling headless jvm...';
sudo apt-get install openjdk-7-jre-headless -y;

printf '\nInstalling elasticsearch...';
sudo pip install pyelasticsearch==0.6.1;
sudo pip install elasticsearch==1.0.0;
cd /var/www/MediVol/vagrant-setup;
sudo dpkg -i elasticsearch-0.90.11.deb;
sudo service elasticsearch restart;

printf '\nInstalling Mandrill...';
sudo pip install mandrill;

printf '\nCreating database for inventory...';
mysql -u root --password=root -e 'create database MediVolDB;';

#VERY IMPROTANT DO NOT REMOVE!
printf '/nInstalling sl';
sudo apt-get install sl;

sleep 15;

python /var/www/MediVol/MediVol/syncdb_script.py;
python /var/www/MediVol/MediVol/catalog/initialize_categories.py;
python /var/www/MediVol/MediVol/inventory/CSV_Importer.py /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_1.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_2.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_3.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_4.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_5.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_6.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_7.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_8.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_9.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_10.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_11.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_12.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_13.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_14.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_15.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_16.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_17.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_18.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_19.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_20.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_21.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_22.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_23.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_24.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_25.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_26.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_27.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_28.csv /var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_29.csv \
/var/www/MediVol/MediVol/inventory/Medivol_DBImport/old_inventory_30.csv;

cd /var/www/MediVol/MediVol/;
python manage.py collectstatic --noinput;

sudo service apache2 restart;

#Leave at the end
mysql -u root --password=root -e 'use MediVolDB; select count(*) from catalog_item;';
