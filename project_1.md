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
```
네트워크 카드 셋팅 priv1/priv2/nat(패키지 설치용)

[root@web1 ~]# ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.123.20  netmask 255.255.255.0  broadcast 192.168.123.255
        inet6 fe80::6dbd:f017:df7f:e685  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:e3:0d:f3  txqueuelen 1000  (Ethernet)
        RX packets 638  bytes 49706 (48.5 KiB)
        RX errors 0  dropped 4  overruns 0  frame 0
        TX packets 204  bytes 33046 (32.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth1: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.124.20  netmask 255.255.255.0  broadcast 192.168.124.255
        inet6 fe80::f2e1:bf7d:9f14:8648  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:cc:3d:f1  txqueuelen 1000  (Ethernet)
        RX packets 430  bytes 28460 (27.7 KiB)
        RX errors 0  dropped 4  overruns 0  frame 0
        TX packets 15  bytes 1078 (1.0 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

eth2: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.122.161  netmask 255.255.255.0  broadcast 192.168.122.255
        inet6 fe80::79ef:caf3:994:57e9  prefixlen 64  scopeid 0x20<link>
        ether 52:54:00:76:fa:54  txqueuelen 1000  (Ethernet)
        RX packets 2721  bytes 3369851 (3.2 MiB)
        RX errors 0  dropped 4  overruns 0  frame 0
        TX packets 751  bytes 52479 (51.2 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0




httpd 설치

# yum install httpd
[root@web1 www]# firewall-cmd --add-service=http --permanent
success

마운트
# yum install nfs-utils

[root@web1 www]# firewall-cmd --reload
success
[root@web1 www]# mount 192.168.124.30:/webcontent /var/www
[root@web1 www]# dh -f
-bash: dh: command not found
[root@web1 www]# df -h
Filesystem                  Size  Used Avail Use% Mounted on
devtmpfs                    908M     0  908M   0% /dev
tmpfs                       919M     0  919M   0% /dev/shm
tmpfs                       919M  8.6M  911M   1% /run
tmpfs                       919M     0  919M   0% /sys/fs/cgroup
/dev/mapper/centos-root      17G  1.4G   16G   8% /
/dev/vda1                  1014M  194M  821M  20% /boot
tmpfs                       184M     0  184M   0% /run/user/0
192.168.124.30:/webcontent  5.0G   32M  5.0G   1% /var/www



mariadb client 설치
wordpress 설치

clone web2

or

네트워크 카드 셋팅 priv1/priv2/nat(패키지 설치용)
clone web2
마운트
httpd 설치
mariadb client 설치
wordpress 설치




```

3. storage 서버 구축
네트워크 카드 셋팅 priv2/nat(패키지 설치용)
```
//nat는 패키지 설치용으로 마지막에 삭제 예정
[root@storage ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: ens11: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 52:54:00:2a:a7:94 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.89/24 brd 192.168.122.255 scope global noprefixroute dynamic ens11
       valid_lft 3542sec preferred_lft 3542sec
    inet6 fe80::1f43:de81:13f7:9f64/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 52:54:00:cf:ef:fc brd ff:ff:ff:ff:ff:ff
    inet 192.168.124.30/24 brd 192.168.124.255 scope global noprefixroute eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::6dbd:f017:df7f:e685/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
[root@storage ~]# 

```
storage 추가1 vdb 5G
```
[root@storage ~]# lsblk
NAME            MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0              11:0    1  4.5G  0 rom  
vda             252:0    0   20G  0 disk 
├─vda1          252:1    0    1G  0 part /boot
└─vda2          252:2    0   19G  0 part 
  ├─centos-root 253:0    0   17G  0 lvm  /
  └─centos-swap 253:1    0    2G  0 lvm  [SWAP]
vdb             252:16   0    5G  0 disk 
vdc             252:32   0    5G  0 disk 

[root@storage ~]# fdisk /dev/vdb
Welcome to fdisk (util-linux 2.23.2).

Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table
Building a new DOS disklabel with disk identifier 0x8e0a07ff.

Command (m for help): n
Partition type:
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p
Partition number (1-4, default 1): 
First sector (2048-10485759, default 2048): 
Using default value 2048
Last sector, +sectors or +size{K,M,G} (2048-10485759, default 10485759): 
Using default value 10485759
Partition 1 of type Linux and of size 5 GiB is set

Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.
Syncing disks.
[root@storage ~]# mkfs.xfs /dev/vdb1
meta-data=/dev/vdb1              isize=512    agcount=4, agsize=327616 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=0, sparse=0
data     =                       bsize=4096   blocks=1310464, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0 ftype=1
log      =internal log           bsize=4096   blocks=2560, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0

[root@storage ~]# blkid
/dev/vda1: UUID="8c180607-f8a5-48c8-96c2-5ea698aa0d71" TYPE="xfs" 
/dev/vda2: UUID="s3wucg-GL9o-Zpza-cNLe-vMIq-IP12-1Rbu5V" TYPE="LVM2_member" 
/dev/vdb1: UUID="e1f36be1-debf-4a06-bba7-5d55906a0087" TYPE="xfs" 
/dev/sr0: UUID="2020-04-22-00-54-00-00" LABEL="CentOS 7 x86_64" TYPE="iso9660" PTTYPE="dos" 
/dev/mapper/centos-root: UUID="83c57337-8973-4f70-9344-e892e0a40b43" TYPE="xfs" 
/dev/mapper/centos-swap: UUID="01705b68-f5fb-40e3-a98e-47469f951324" TYPE="swap" 
[root@storage ~]# mkdir /webcontent
[root@storage ~]# vi /etc/fstab
[root@storage ~]# mount -a
[root@storage ~]# df -h
Filesystem               Size  Used Avail Use% Mounted on
devtmpfs                 908M     0  908M   0% /dev
tmpfs                    919M     0  919M   0% /dev/shm
tmpfs                    919M  8.6M  911M   1% /run
tmpfs                    919M     0  919M   0% /sys/fs/cgroup
/dev/mapper/centos-root   17G  1.4G   16G   8% /
/dev/vda1               1014M  194M  821M  20% /boot
tmpfs                    184M     0  184M   0% /run/user/0
/dev/vdb1                5.0G   33M  5.0G   1% /webcontent
[root@storage ~]# 

# yum install -y nfs-utils
# systemctl start nfs   // nfs 서비스 시작


# vi /etc/exports
[root@storage ~]# exportfs -rva
exporting 192.168.124.0/24:/webcontent
[root@storage ~]# 

# firewall-cmd --add-service=nfs --permanent
# firewall-cmd --add-service=rpc-bind --permanent
# firewall-cmd --add-service=mountd --permanent
# firewall-cmd --reload

# chmod 755 /var/www



```

/webcontent - web1 : /var/www
/webcontent - web2 : /var/www
storage 추가2 vdc 5G
iscsi /target








4. database 서버 구축





