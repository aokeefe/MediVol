#!/bin/bash

echo "Updating apt-get...";
sudo apt-get update;

echo "Installing vim...";
sudo apt-get install vim -y;

echo "Installing apache2...";
sudo apt-get install apache2 -y;

echo "Installing php5...";
sudo apt-get install php5 -y;

echo "Installing mysql-server...";
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password password root';
sudo debconf-set-selections <<< 'mysql-server-5.5 mysql-server/root_password_again password root';
sudo apt-get install mysql-server -y;

echo "Installing phpMyAdmin...";
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
