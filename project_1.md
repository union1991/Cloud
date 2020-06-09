1. lb 서버 구축
네트워크 카드 세팅 nat/priv1 
```
[root@localhost ~]# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.122.10  netmask 255.255.255.0  broadcast 192.168.122.255
        inet6 fe80::6dbd:f017:df7f:e685  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:d9:1c:06  txqueuelen 1000  (Ethernet)
        RX packets 2021  bytes 138092 (134.8 KiB)
        RX errors 0  dropped 5  overruns 0  frame 0
        TX packets 334  bytes 26937 (26.3 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.123.10  netmask 255.255.255.0  broadcast 192.168.123.255
        inet6 fe80::f2e1:bf7d:9f14:8648  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:9c:5d:5f  txqueuelen 1000  (Ethernet)
        RX packets 1727  bytes 112186 (109.5 KiB)
        RX errors 0  dropped 5  overruns 0  frame 0
        TX packets 27  bytes 3651 (3.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 72  bytes 6268 (6.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 72  bytes 6268 (6.1 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

haproxy 설치, 설정, 실행
```
# yum install haproxy
# cd /etc/haproxy/
# vi haproxy.cfg

#---------------------------------------------------------------------
# main frontend which proxys to the backends
#---------------------------------------------------------------------
frontend  main *:80
    acl url_static       path_beg       -i /static /images /javascript /stylesheets
    acl url_static       path_end       -i .jpg .gif .png .css .js

    use_backend static          if url_static
    default_backend             app

#---------------------------------------------------------------------
# static backend for serving up images, stylesheets and such
#---------------------------------------------------------------------
backend static
    balance     roundrobin
    server      static 127.0.0.1:4331 check

#---------------------------------------------------------------------
# round robin balancing between the various backends
#---------------------------------------------------------------------
backend app
    balance     roundrobin
    server  www1 192.168.123.20:80
    server  www2 192.168.123.21:80

:wq!

# systemctl start haproxy
```



2. web1/2 서버 구축
네트워크 카드 셋팅 priv1/priv2/nat(패키지 설치용)
httpd 설치
mariadb client 설치
wordpress 설치
마운트
clone web2

or

네트워크 카드 셋팅 priv1/priv2/nat(패키지 설치용)
clone web2
마운트
httpd 설치
mariadb client 설치
wordpress 설치





3. storage 서버 구축
네트워크 카드 셋팅 priv2/nat(패키지 설치용)
storage 추가1 vdb 5G
/webcontent - web1 : /var/www
/webcontent - web2 : /var/www
storage 추가2 vdc 5G
iscsi /target








4. database 서버 구축





