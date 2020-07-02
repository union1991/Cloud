#!/bin/bash
yum -y install php
yum clean all
yum repolist update
yum -y install epel-release
rpm -Uvh "https://mirror.webtatic.com/yum/el7/webtatic-release.rpm"
yum -y install httpd
yum -y install wget 
yum -y install php72w-cli php72w-bcmath php72w-gd php72w-mbstring php72w-mysqlnd php72w-pear php72w-xml php72w-xmlrpc php72w-process mod_php72w
wget "http://wordpress.org/latest.tar.gz"
tar -xvzf /latest.tar.gz -C /var/www/html
rm -rf /wordpress.org
chown -R apache: /var/www/html/wordpress
systemctl start httpd
systemctl enable httpd

