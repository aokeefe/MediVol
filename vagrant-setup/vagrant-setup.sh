#!/bin/bash

echo "Updating apt-get...";
sudo apt-get update;

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
sudo cp /var/www/medivol_apache_conf /etc/apache2/sites-available/medivol;
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
sudo pip install Django;

printf '\nInstalling python-dev...';
sudo apt-get install python-dev -y;

printf '\nInstalling elaphe...';
sudo pip install elaphe;

printf '\nInstalling python-mysqldb...';
sudo apt-get install python-mysqldb -y;

printf '\nInstalling django-jenkins...';
sudo pip install django-jenkins;

printf '\nInstalling django_dajax...';
sudo pip install django_dajax;

printf '\nCreating database for inventory...';
mysql -u root --password=root -e 'create database MediVolDB;';

python /var/www/MediVol/syncdb_script.py;
