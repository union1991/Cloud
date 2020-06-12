# 과제 1. 웹서비스 환경 구성하기

## 목차.

### 1. 과제 목표 
### 2. 과제 내용 
### 3. 환경 설정 
### 4. 과제 절차 
### 5. 추가 정리


-----------------


### 1. 과제 목표


 본 과제의 목적은 (로드밸런스) - (웹 - 스토리지 - 데이터베이스) 환경을 구성하여 네트워크의 구성을 이해하며, 각각의 서버에 설치되는 패키지를 연동하며 웹 서비스의 본질을 이해하는 것이다.  


#### 과제 성취도 평가

1. 구성도를 확인하여 서버를 구성할 수 있는가?
2. NFS, ISCSI를 이해하고 서버와 클라이언트를 연결시킬 수 있는가?
3. 각각의 서버에 설치되는 패키지(MariaDB, PHP 7.2 등)를 이해하고 설정 및 연동할 수 있는가?
4. 웹 서비스를 이해하였는가?



---



### 2. 과제 내용


#### 2.1 구성도
 본 과제의 구성도는 아래와 같다.


<img src="https://user-images.githubusercontent.com/56064985/84450874-6a79fd80-ac8c-11ea-860b-becc698805f9.png" width="90%"></img>



#### 2.2 서비스
 과제에 앞서 알아야 할 서비스들의 개념을 정리한다.
 
 
* iscsi 
> * iSCSI(Internet Small Computer System Interface)는 컴퓨팅 환경에서 데이터 스토리지 시설을 이어주는 IP 기반의 스토리지 네트워킹 표준이다. iSCSI는 IP 망을 통해 SCSI 명령을 전달함으로써 인트라넷을 거쳐 데이터 전송을 쉽게 하고 먼 거리에 걸쳐 스토리지를 관리하는 데 쓰인다. iSCSI는 근거리 통신망과 원거리 통신망, 아니면 인터넷을 통해 데이터를 전송하는 데 쓰이며 위치에 영향을 받지 않는 데이터 보관과 복구를 사용할 수 있게 한다.


* NFS
> * 네트워크 파일 시스템(Network File System, NFS)은 1984년에 썬 마이크로시스템즈가 개발한 프로토콜이다.클라이언트 컴퓨터의 사용자가 네트워크 상의 파일을 직접 연결된 스토리지에 접근하는 방식과 비슷한 방식으로 접근하도록 도와준다. 


* Load Balancing
> * 부하분산 또는 로드 밸런싱(load balancing)은 컴퓨터 네트워크 기술의 일종으로 둘 혹은 셋이상의 중앙처리장치 혹은 저장장치와 같은 컴퓨터 자원들에게 작업을 나누는 것을 의미한다. 이로써 가용성 및 응답시간을 최적화 시킬 수 있다. 


---


### 3. 환경 설정


 본 과제의 서버 환경에 대해 설명한다.  


### [서버]
* storage 서버 : Linux database 3.10.0-1127.10.1.el7.x86_64
* webserver 서버 : Linux database 3.10.0-1127.10.1.el7.x86_64
* database 서버 : Linux database 3.10.0-1127.10.1.el7.x86_64
* loadbalance 서버 : Linux database 3.10.0-1127.10.1.el7.x86_64


### [네트워크]

* loadbalance 서버
> * eth0(NAT) : ipv4(192.168.122.10/24), gw(192.168.122.1),dns(8.8.8.8) 
> * eth1(Priv1) : ipv4(192.168.122.10/24)


* web1 서버
> * eth0(Priv1) : ipv4(192.168.123.20/24)
> * eth1(Priv2) : ipv4(192.168.124.20/24)


* web2 서버
> * eth0(Priv1) : ipv4(192.168.123.21/24)
> * eth1(Priv2) : ipv4(192.168.124.21/24)


* storage 서버
> * eth0(Priv2) : ipv4(192.168.124.30/24)


* database 서버
> * eth0(Priv2) : ipv4(192.168.124.40/24)


### [storage]
* storage 서버
> * VirtIO Disk 1(5G) 추가
> * VirtIO Disk 2(5G) 추가

---


### 4. 과제 절차


 본 과제의 서버 환경에 대해 설명한다. 


(스토리지 서버 - > web 서버 -> 데이터 베이스 -> 로드밸런스)
(nfs -> iscsi -> database 설치 -> http 설치 -> wordpress 설치 -> 로드밸런스)


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


# yum install wget
# wget "http://wordpress.org/latest.tar.gz"
# tar -xvzf latest.tar.gz -C /var/www/html
# chown -R apache: /var/www/html/wordpress




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
```
# lsblk
NAME            MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sr0              11:0    1  4.5G  0 rom  
vda             252:0    0   20G  0 disk 
├─vda1          252:1    0    1G  0 part /boot
└─vda2          252:2    0   19G  0 part 
  ├─centos-root 253:0    0   17G  0 lvm  /
  └─centos-swap 253:1    0    2G  0 lvm  [SWAP]
vdb             252:16   0    5G  0 disk 
└─vdb1          252:17   0    5G  0 part /webcontent
vdc             252:32   0    5G  0 disk 
[root@storage ~]# yum install targetcli
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.opensourcelab.co.kr
 * extras: mirror.opensourcelab.co.kr
 * updates: ftp.kaist.ac.kr
base                                                                                          | 3.6 kB  00:00:00     
extras                                                                                        | 2.9 kB  00:00:00     
updates                                                                                       | 2.9 kB  00:00:00     
Resolving Dependencies
--> Running transaction check
---> Package targetcli.noarch 0:2.1.fb49-1.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=====================================================================================================================
 Package                     Arch                     Version                           Repository              Size
=====================================================================================================================
Installing:
 targetcli                   noarch                   2.1.fb49-1.el7                    base                    68 k

Transaction Summary
=====================================================================================================================
Install  1 Package

Total download size: 68 k
Installed size: 233 k
Is this ok [y/d/N]: y
Downloading packages:
targetcli-2.1.fb49-1.el7.noarch.rpm                                                           |  68 kB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : targetcli-2.1.fb49-1.el7.noarch                                                                   1/1 
  Verifying  : targetcli-2.1.fb49-1.el7.noarch                                                                   1/1 

Installed:
  targetcli.noarch 0:2.1.fb49-1.el7                                                                                  

Complete!
[root@storage ~]# 
[root@storage ~]# 
[root@storage ~]# 
[root@storage ~]# targetli
-bash: targetli: command not found
[root@storage ~]# targetcli
targetcli shell version 2.1.fb49
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.

/> 
/> 
/> 
/> ls
o- / .......................................................................................................... [...]
  o- backstores ............................................................................................... [...]
  | o- block ................................................................................... [Storage Objects: 0]
  | o- fileio .................................................................................. [Storage Objects: 0]
  | o- pscsi ................................................................................... [Storage Objects: 0]
  | o- ramdisk ................................................................................. [Storage Objects: 0]
  o- iscsi ............................................................................................. [Targets: 0]
  o- loopback .......................................................................................... [Targets: 0]
/> cd backstores/block 
/backstores/block> create block1 /dev/vdc
Created block storage object block1 using /dev/vdc.
/backstores/block> ls
o- block ....................................................................................... [Storage Objects: 1]
  o- block1 .............................................................. [/dev/vdc (5.0GiB) write-thru deactivated]
    o- alua ........................................................................................ [ALUA Groups: 1]
      o- default_tg_pt_gp ............................................................ [ALUA state: Active/optimized]
/backstores/block> cd /
/> cd /iscsi 
/iscsi> create iqn.2020-06.com.example:storage
Created target iqn.2020-06.com.example:storage.
Created TPG 1.
Global pref auto_add_default_portal=true
Created default portal listening on all IPs (0.0.0.0), port 3260.
/iscsi> ls
o- iscsi ............................................................................................... [Targets: 1]
  o- iqn.2020-06.com.example:storage ...................................................................... [TPGs: 1]
    o- tpg1 .................................................................................. [no-gen-acls, no-auth]
      o- acls ............................................................................................. [ACLs: 0]
      o- luns ............................................................................................. [LUNs: 0]
      o- portals ....................................................................................... [Portals: 1]
        o- 0.0.0.0:3260 ........................................................................................ [OK]
/iscsi> cd ./iqn.2020-06.com.example:storage/tpg1/acls 
/iscsi/iqn.20...age/tpg1/acls> create iqn.2020-06.com.example:database
Created Node ACL for iqn.2020-06.com.example:database
/iscsi/iqn.20...age/tpg1/acls> ls
o- acls ................................................................................................... [ACLs: 1]
  o- iqn.2020-06.com.example:database .............................................................. [Mapped LUNs: 0]
/iscsi/iqn.20...age/tpg1/acls> cd /
/> ls
o- / .......................................................................................................... [...]
  o- backstores ............................................................................................... [...]
  | o- block ................................................................................... [Storage Objects: 1]
  | | o- block1 .......................................................... [/dev/vdc (5.0GiB) write-thru deactivated]
  | |   o- alua .................................................................................... [ALUA Groups: 1]
  | |     o- default_tg_pt_gp ........................................................ [ALUA state: Active/optimized]
  | o- fileio .................................................................................. [Storage Objects: 0]
  | o- pscsi ................................................................................... [Storage Objects: 0]
  | o- ramdisk ................................................................................. [Storage Objects: 0]
  o- iscsi ............................................................................................. [Targets: 1]
  | o- iqn.2020-06.com.example:storage .................................................................... [TPGs: 1]
  |   o- tpg1 ................................................................................ [no-gen-acls, no-auth]
  |     o- acls ........................................................................................... [ACLs: 1]
  |     | o- iqn.2020-06.com.example:database ...................................................... [Mapped LUNs: 0]
  |     o- luns ........................................................................................... [LUNs: 0]
  |     o- portals ..................................................................................... [Portals: 1]
  |       o- 0.0.0.0:3260 ...................................................................................... [OK]
  o- loopback .......................................................................................... [Targets: 0]
/> cd /iscsi/iqn.2020-06.com.example:storage/tpg1/luns 
/iscsi/iqn.20...age/tpg1/luns> create /backstores/block/block1 
Created LUN 0.
Created LUN 0->0 mapping in node ACL iqn.2020-06.com.example:database
/iscsi/iqn.20...age/tpg1/luns> ls
o- luns ................................................................................................... [LUNs: 1]
  o- lun0 .............................................................. [block/block1 (/dev/vdc) (default_tg_pt_gp)]
/iscsi/iqn.20...age/tpg1/luns> exit
Global pref auto_save_on_exit=true
Last 10 configs saved in /etc/target/backup/.
Configuration saved to /etc/target/saveconfig.json
[root@storage ~]# systemctl enable target
Created symlink from /etc/systemd/system/multi-user.target.wants/target.service to /usr/lib/systemd/system/target.service.
[root@storage ~]# systemctl start target



```





4. database 서버 구축

```
iscsi 마운트
# yum install iscsi*
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.opensourcelab.co.kr
 * extras: mirror.opensourcelab.co.kr
 * updates: mirror.opensourcelab.co.kr
Resolving Dependencies
--> Running transaction check
---> Package iscsi-initiator-utils.x86_64 0:6.2.0.874-17.el7 will be installed
---> Package iscsi-initiator-utils-devel.x86_64 0:6.2.0.874-17.el7 will be installed
---> Package iscsi-initiator-utils-iscsiuio.x86_64 0:6.2.0.874-17.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

=====================================================================================================================
 Package                                    Arch               Version                        Repository        Size
=====================================================================================================================
Installing:
 iscsi-initiator-utils                      x86_64             6.2.0.874-17.el7               base             423 k
 iscsi-initiator-utils-devel                x86_64             6.2.0.874-17.el7               base              91 k
 iscsi-initiator-utils-iscsiuio             x86_64             6.2.0.874-17.el7               base              93 k

Transaction Summary
=====================================================================================================================
Install  3 Packages

Total download size: 607 k
Installed size: 2.9 M
Is this ok [y/d/N]: y
Downloading packages:
(1/3): iscsi-initiator-utils-iscsiuio-6.2.0.874-17.el7.x86_64.rpm                             |  93 kB  00:00:00     
(2/3): iscsi-initiator-utils-6.2.0.874-17.el7.x86_64.rpm                                      | 423 kB  00:00:00     
(3/3): iscsi-initiator-utils-devel-6.2.0.874-17.el7.x86_64.rpm                                |  91 kB  00:00:00     
---------------------------------------------------------------------------------------------------------------------
Total                                                                                1.4 MB/s | 607 kB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : iscsi-initiator-utils-iscsiuio-6.2.0.874-17.el7.x86_64                                            1/3 
  Installing : iscsi-initiator-utils-6.2.0.874-17.el7.x86_64                                                     2/3 
  Installing : iscsi-initiator-utils-devel-6.2.0.874-17.el7.x86_64                                               3/3 
  Verifying  : iscsi-initiator-utils-devel-6.2.0.874-17.el7.x86_64                                               1/3 
  Verifying  : iscsi-initiator-utils-6.2.0.874-17.el7.x86_64                                                     2/3 
  Verifying  : iscsi-initiator-utils-iscsiuio-6.2.0.874-17.el7.x86_64                                            3/3 

Installed:
  iscsi-initiator-utils.x86_64 0:6.2.0.874-17.el7            iscsi-initiator-utils-devel.x86_64 0:6.2.0.874-17.el7  
  iscsi-initiator-utils-iscsiuio.x86_64 0:6.2.0.874-17.el7  

Complete!
[root@database ~]# vi /etc/iscsi/i
initiatorname.iscsi  iscsid.conf          
[root@database ~]# vi /etc/iscsi/i
initiatorname.iscsi  iscsid.conf          
[root@database ~]# vi /etc/iscsi/i
initiatorname.iscsi  iscsid.conf          
[root@database ~]# vi /etc/iscsi/i
initiatorname.iscsi  iscsid.conf          
[root@database ~]# vi /etc/iscsi/i
initiatorname.iscsi  iscsid.conf          
[root@database ~]# vi /etc/iscsi/initiatorname.iscsi 
[root@database ~]# systemctl enable iscsi
[root@database ~]# systemctl start iscsi
[root@database ~]# iscsiadm -m iscsiadm -m discovery -t sendtargets -p 192.168.124.30
192.168.124.30:3260,1 iqn.2020-06.com.example:storage
[root@database ~]# iscsiadm -m node -T "iqn.2020-06.com.example:storage" -p 192.168.124.30:3260 -l
[root@database ~]# iscsiadm -m node -T "iqn.2020-06.com.example:storage" -p 192.168.124.30:3260 -u
Logging out of session [sid: 1, target: iqn.2020-06.com.example:storage, portal: 192.168.124.30,3260]
Logout of [sid: 1, target: iqn.2020-06.com.example:storage, portal: 192.168.124.30,3260] successful.
[root@database ~]# iscsiadm -m node -T "iqn.2020-06.com.example:storage" -p 192.168.124.30:3260 -l
Logging in to [iface: default, target: iqn.2020-06.com.example:storage, portal: 192.168.124.30,3260] (multiple)
Login to [iface: default, target: iqn.2020-06.com.example:storage, portal: 192.168.124.30,3260] successful.
[root@database ~]# lsblk
NAME            MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda               8:0    0    5G  0 disk 
sr0              11:0    1  4.5G  0 rom  
vda             252:0    0   20G  0 disk 
├─vda1          252:1    0    1G  0 part /boot
└─vda2          252:2    0   19G  0 part 
  ├─centos-root 253:0    0   17G  0 lvm  /
  └─centos-swap 253:1    0    2G  0 lvm  [SWAP]
[root@database ~]# iscsiadm -m node -T "iqn.2020-06.com.example:storage" -p 192.168.124.30:3260 -l^C
[root@database ~]# 

[root@database ~]# pvcreate /dev/sda
  Physical volume "/dev/sda" successfully created.
[root@database ~]# vgcreate vg_db /dev/sda
  Volume group "vg_db" successfully created
[root@database ~]# lvcreate lv_db -l 100%FREE vg_db
  Volume group "lv_db" not found
  Cannot process volume group lv_db
[root@database ~]# lvcreate -n lv_db -l 100%FREE vg_db
  Logical volume "lv_db" created.
[root@database ~]# lsblk
NAME            MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda               8:0    0    5G  0 disk 
└─vg_db-lv_db   253:2    0    5G  0 lvm  
sr0              11:0    1  4.5G  0 rom  
vda             252:0    0   20G  0 disk 
├─vda1          252:1    0    1G  0 part /boot
└─vda2          252:2    0   19G  0 part 
  ├─centos-root 253:0    0   17G  0 lvm  /
  └─centos-swap 253:1    0    2G  0 lvm  [SWAP]
[root@database ~]# 
```


db 설치

```
# mysql -u root -p
MariaDB [(none)]> create database wordpress default CHARACTER SET UTF8;
MariaDB [(none)]> use wordpress;
MariaDB [(wordpress)]> create user 'wordadmin'@'%' identified by 'toor';  // 
MariaDB [(none)]> grant all privileges on wordpress.* to wordadmin
MariaDB [(none)]> flush privileges;   // refresh


```
