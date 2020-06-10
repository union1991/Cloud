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
```
# yum -y install targetcli
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
 * base: mirror.opensourcelab.co.kr
 * extras: mirror.opensourcelab.co.kr
 * updates: ftp.kaist.ac.kr
Resolving Dependencies
--> Running transaction check
---> Package targetcli.noarch 0:2.1.fb49-1.el7 will be installed
--> Processing Dependency: python-rtslib >= 2.1.fb41 for package: targetcli-2.1.fb49-1.el7.noarch
--> Processing Dependency: python-ethtool for package: targetcli-2.1.fb49-1.el7.noarch
--> Processing Dependency: python-configshell for package: targetcli-2.1.fb49-1.el7.noarch
--> Running transaction check
---> Package python-configshell.noarch 1:1.1.fb25-1.el7 will be installed
--> Processing Dependency: python-urwid for package: 1:python-configshell-1.1.fb25-1.el7.noarch
--> Processing Dependency: python-six for package: 1:python-configshell-1.1.fb25-1.el7.noarch
--> Processing Dependency: pyparsing for package: 1:python-configshell-1.1.fb25-1.el7.noarch
---> Package python-ethtool.x86_64 0:0.8-8.el7 will be installed
--> Processing Dependency: libnl.so.1()(64bit) for package: python-ethtool-0.8-8.el7.x86_64
---> Package python-rtslib.noarch 0:2.1.fb69-3.el7 will be installed
--> Processing Dependency: python-kmod for package: python-rtslib-2.1.fb69-3.el7.noarch
--> Running transaction check
---> Package libnl.x86_64 0:1.1.4-3.el7 will be installed
---> Package pyparsing.noarch 0:1.5.6-9.el7 will be installed
---> Package python-kmod.x86_64 0:0.9-4.el7 will be installed
---> Package python-six.noarch 0:1.9.0-2.el7 will be installed
---> Package python-urwid.x86_64 0:1.1.1-3.el7 will be installed
--> Finished Dependency Resolution

Dependencies Resolved

==============================================================================================================================
 Package                             Arch                    Version                              Repository             Size
==============================================================================================================================
Installing:
 targetcli                           noarch                  2.1.fb49-1.el7                       base                   68 k
Installing for dependencies:
 libnl                               x86_64                  1.1.4-3.el7                          base                  128 k
 pyparsing                           noarch                  1.5.6-9.el7                          base                   94 k
 python-configshell                  noarch                  1:1.1.fb25-1.el7                     base                   68 k
 python-ethtool                      x86_64                  0.8-8.el7                            base                   34 k
 python-kmod                         x86_64                  0.9-4.el7                            base                   57 k
 python-rtslib                       noarch                  2.1.fb69-3.el7                       base                  102 k
 python-six                          noarch                  1.9.0-2.el7                          base                   29 k
 python-urwid                        x86_64                  1.1.1-3.el7                          base                  654 k

Transaction Summary
==============================================================================================================================
Install  1 Package (+8 Dependent packages)

Total download size: 1.2 M
Installed size: 5.1 M
Downloading packages:
(1/9): python-ethtool-0.8-8.el7.x86_64.rpm                                                             |  34 kB  00:00:00     
(2/9): pyparsing-1.5.6-9.el7.noarch.rpm                                                                |  94 kB  00:00:00     
(3/9): libnl-1.1.4-3.el7.x86_64.rpm                                                                    | 128 kB  00:00:00     
(4/9): python-six-1.9.0-2.el7.noarch.rpm                                                               |  29 kB  00:00:00     
(5/9): python-configshell-1.1.fb25-1.el7.noarch.rpm                                                    |  68 kB  00:00:00     
(6/9): python-rtslib-2.1.fb69-3.el7.noarch.rpm                                                         | 102 kB  00:00:00     
(7/9): targetcli-2.1.fb49-1.el7.noarch.rpm                                                             |  68 kB  00:00:00     
(8/9): python-kmod-0.9-4.el7.x86_64.rpm                                                                |  57 kB  00:00:00     
(9/9): python-urwid-1.1.1-3.el7.x86_64.rpm                                                             | 654 kB  00:00:00     
------------------------------------------------------------------------------------------------------------------------------
Total                                                                                         4.0 MB/s | 1.2 MB  00:00:00     
Running transaction check
Running transaction test
Transaction test succeeded
Running transaction
  Installing : python-six-1.9.0-2.el7.noarch                                                                              1/9 
  Installing : pyparsing-1.5.6-9.el7.noarch                                                                               2/9 
  Installing : python-kmod-0.9-4.el7.x86_64                                                                               3/9 
  Installing : python-rtslib-2.1.fb69-3.el7.noarch                                                                        4/9 
  Installing : libnl-1.1.4-3.el7.x86_64                                                                                   5/9 
  Installing : python-ethtool-0.8-8.el7.x86_64                                                                            6/9 
  Installing : python-urwid-1.1.1-3.el7.x86_64                                                                            7/9 
  Installing : 1:python-configshell-1.1.fb25-1.el7.noarch                                                                 8/9 
  Installing : targetcli-2.1.fb49-1.el7.noarch                                                                            9/9 
  Verifying  : python-urwid-1.1.1-3.el7.x86_64                                                                            1/9 
  Verifying  : libnl-1.1.4-3.el7.x86_64                                                                                   2/9 
  Verifying  : python-ethtool-0.8-8.el7.x86_64                                                                            3/9 
  Verifying  : python-kmod-0.9-4.el7.x86_64                                                                               4/9 
  Verifying  : targetcli-2.1.fb49-1.el7.noarch                                                                            5/9 
  Verifying  : 1:python-configshell-1.1.fb25-1.el7.noarch                                                                 6/9 
  Verifying  : python-rtslib-2.1.fb69-3.el7.noarch                                                                        7/9 
  Verifying  : python-six-1.9.0-2.el7.noarch                                                                              8/9 
  Verifying  : pyparsing-1.5.6-9.el7.noarch                                                                               9/9 

Installed:
  targetcli.noarch 0:2.1.fb49-1.el7                                                                                           

Dependency Installed:
  libnl.x86_64 0:1.1.4-3.el7            pyparsing.noarch 0:1.5.6-9.el7        python-configshell.noarch 1:1.1.fb25-1.el7    
  python-ethtool.x86_64 0:0.8-8.el7     python-kmod.x86_64 0:0.9-4.el7        python-rtslib.noarch 0:2.1.fb69-3.el7         
  python-six.noarch 0:1.9.0-2.el7       python-urwid.x86_64 0:1.1.1-3.el7    

Complete!
[root@storage ~]# vgcreate target_vg /dev/sdc
  Device /dev/sdc not found.
[root@storage ~]# cd /dev
[root@storage dev]# ls
autofs           dm-0       log                 ptmx      tty    tty20  tty33  tty46  tty59  uinput   vcsa   vga_arbiter
block            dm-1       loop-control        pts       tty0   tty21  tty34  tty47  tty6   urandom  vcsa1  vhci
bsg              dri        mapper              random    tty1   tty22  tty35  tty48  tty60  usbmon0  vcsa2  vhost-net
btrfs-control    fb0        mcelog              raw       tty10  tty23  tty36  tty49  tty61  usbmon1  vcsa3  virtio-ports
bus              fd         mem                 rtc       tty11  tty24  tty37  tty5   tty62  usbmon2  vcsa4  vport1p1
cdrom            full       mqueue              rtc0      tty12  tty25  tty38  tty50  tty63  usbmon3  vcsa5  vport1p2
centos           fuse       net                 sg0       tty13  tty26  tty39  tty51  tty7   usbmon4  vcsa6  zero
char             hidraw0    network_latency     shm       tty14  tty27  tty4   tty52  tty8   vcs      vda
console          hpet       network_throughput  snapshot  tty15  tty28  tty40  tty53  tty9   vcs1     vda1
core             hugepages  null                snd       tty16  tty29  tty41  tty54  ttyS0  vcs2     vda2
cpu              hwrng      nvram               sr0       tty17  tty3   tty42  tty55  ttyS1  vcs3     vdb
cpu_dma_latency  initctl    oldmem              stderr    tty18  tty30  tty43  tty56  ttyS2  vcs4     vdb1
crash            input      port                stdin     tty19  tty31  tty44  tty57  ttyS3  vcs5     vdc
disk             kmsg       ppp                 stdout    tty2   tty32  tty45  tty58  uhid   vcs6     vfio
[root@storage dev]# lsblk
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
[root@storage dev]# vgcreate target_vg /dev/vdc
  Physical volume "/dev/vdc" successfully created.
  Volume group "target_vg" successfully created
[root@storage dev]# vgremove /dev/vdc
  Volume group "vdc" not found
  Cannot process volume group vdc
[root@storage dev]# vgremove target_vg
  Volume group "target_vg" successfully removed
[root@storage dev]# lsblk
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
[root@storage dev]# vgcreate l^Cdev/vdc
[root@storage dev]# e
-bash: e: command not found
[root@storage dev]# w
 14:31:36 up  1:06,  1 user,  load average: 0.00, 0.01, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
root     pts/0    192.168.124.1    13:25    0.00s  0.11s  0.04s w
[root@storage dev]# ksh
-bash: ksh: command not found
[root@storage dev]# pvcreate /dev/vdc
  Physical volume "/dev/vdc" successfully created.
[root@storage dev]# vgcreate db_vg /dev/vdc
  Volume group "db_vg" successfully created
[root@storage dev]# vgremove db_vg 
  Volume group "db_vg" successfully removed
[root@storage dev]# vgcreate vg_db /dev/vdc
  Volume group "vg_db" successfully created
[root@storage dev]# lvcreate -n lv_db 100%FREE vg_db
  No command with matching syntax recognised.  Run 'lvcreate --help' for more information.
[root@storage dev]# lvcreate -n lv_db -l 100%FREE vg_db
  Logical volume "lv_db" created.
[root@storage dev]# targetcli
Warning: Could not load preferences file /root/.targetcli/prefs.bin.
targetcli shell version 2.1.fb49
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.

/> cd /backstres
No such path /backstres
/> cd /backstores/
/backstores> block/ cre
/backstores> exit
Global pref auto_save_on_exit=true
Configuration saved to /etc/target/saveconfig.json
[root@storage dev]# lsblk
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
└─vg_db-lv_db   253:2    0    5G  0 lvm  
[root@storage dev]# targetcli
targetcli shell version 2.1.fb49
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.

/backstores> block/ crate block1 /dev/vg_db/lv_db
Command not found crate
/backstores> block/ create block1 /dev/vg_db/lv_db
Created block storage object block1 using /dev/vg_db/lv_db.
/backstores> exit
Global pref auto_save_on_exit=true
Last 10 configs saved in /etc/target/backup/.
Configuration saved to /etc/target/saveconfig.json
[root@storage dev]# ls
autofs           dm-0       kmsg                ppp       stdout  tty2   tty32  tty45  tty58  uhid     vcs6   vfio
block            dm-1       log                 ptmx      tty     tty20  tty33  tty46  tty59  uinput   vcsa   vga_arbiter
bsg              dm-2       loop-control        pts       tty0    tty21  tty34  tty47  tty6   urandom  vcsa1  vg_db
btrfs-control    dri        mapper              random    tty1    tty22  tty35  tty48  tty60  usbmon0  vcsa2  vhci
bus              fb0        mcelog              raw       tty10   tty23  tty36  tty49  tty61  usbmon1  vcsa3  vhost-net
cdrom            fd         mem                 rtc       tty11   tty24  tty37  tty5   tty62  usbmon2  vcsa4  virtio-ports
centos           full       mqueue              rtc0      tty12   tty25  tty38  tty50  tty63  usbmon3  vcsa5  vport1p1
char             fuse       net                 sg0       tty13   tty26  tty39  tty51  tty7   usbmon4  vcsa6  vport1p2
console          hidraw0    network_latency     shm       tty14   tty27  tty4   tty52  tty8   vcs      vda    zero
core             hpet       network_throughput  snapshot  tty15   tty28  tty40  tty53  tty9   vcs1     vda1
cpu              hugepages  null                snd       tty16   tty29  tty41  tty54  ttyS0  vcs2     vda2
cpu_dma_latency  hwrng      nvram               sr0       tty17   tty3   tty42  tty55  ttyS1  vcs3     vdb
crash            initctl    oldmem              stderr    tty18   tty30  tty43  tty56  ttyS2  vcs4     vdb1
disk             input      port                stdin     tty19   tty31  tty44  tty57  ttyS3  vcs5     vdc
[root@storage dev]# ls
autofs           dm-0       kmsg                ppp       stdout  tty2   tty32  tty45  tty58  uhid     vcs6   vfio
block            dm-1       log                 ptmx      tty     tty20  tty33  tty46  tty59  uinput   vcsa   vga_arbiter
bsg              dm-2       loop-control        pts       tty0    tty21  tty34  tty47  tty6   urandom  vcsa1  vg_db
btrfs-control    dri        mapper              random    tty1    tty22  tty35  tty48  tty60  usbmon0  vcsa2  vhci
bus              fb0        mcelog              raw       tty10   tty23  tty36  tty49  tty61  usbmon1  vcsa3  vhost-net
cdrom            fd         mem                 rtc       tty11   tty24  tty37  tty5   tty62  usbmon2  vcsa4  virtio-ports
centos           full       mqueue              rtc0      tty12   tty25  tty38  tty50  tty63  usbmon3  vcsa5  vport1p1
char             fuse       net                 sg0       tty13   tty26  tty39  tty51  tty7   usbmon4  vcsa6  vport1p2
console          hidraw0    network_latency     shm       tty14   tty27  tty4   tty52  tty8   vcs      vda    zero
core             hpet       network_throughput  snapshot  tty15   tty28  tty40  tty53  tty9   vcs1     vda1
cpu              hugepages  null                snd       tty16   tty29  tty41  tty54  ttyS0  vcs2     vda2
cpu_dma_latency  hwrng      nvram               sr0       tty17   tty3   tty42  tty55  ttyS1  vcs3     vdb
crash            initctl    oldmem              stderr    tty18   tty30  tty43  tty56  ttyS2  vcs4     vdb1
disk             input      port                stdin     tty19   tty31  tty44  tty57  ttyS3  vcs5     vdc
[root@storage dev]# cd /webcontent/
[root@storage webcontent]# ls
cgi-bin  html
[root@storage webcontent]# systemctl status nfs
● nfs-server.service - NFS server and services
   Loaded: loaded (/usr/lib/systemd/system/nfs-server.service; disabled; vendor preset: disabled)
  Drop-In: /run/systemd/generator/nfs-server.service.d
           └─order-with-mounts.conf
   Active: inactive (dead)
[root@storage webcontent]# systemctl start nfs
[root@storage webcontent]# targetcli
targetcli shell version 2.1.fb49
Copyright 2011-2013 by Datera, Inc and others.
For help on commands, type 'help'.

/backstores> ls
o- backstores .......................................................................................................... [...]
  o- block .............................................................................................. [Storage Objects: 1]
  | o- block1 ............................................................. [/dev/vg_db/lv_db (5.0GiB) write-thru deactivated]
  |   o- alua ............................................................................................... [ALUA Groups: 1]
  |     o- default_tg_pt_gp ................................................................... [ALUA state: Active/optimized]
  o- fileio ............................................................................................. [Storage Objects: 0]
  o- pscsi .............................................................................................. [Storage Objects: 0]
  o- ramdisk ............................................................................................ [Storage Objects: 0]
/backstores> cd ..
/> ls
o- / ................................................................................................................... [...]
  o- backstores ........................................................................................................ [...]
  | o- block ............................................................................................ [Storage Objects: 1]
  | | o- block1 ........................................................... [/dev/vg_db/lv_db (5.0GiB) write-thru deactivated]
  | |   o- alua ............................................................................................. [ALUA Groups: 1]
  | |     o- default_tg_pt_gp ................................................................. [ALUA state: Active/optimized]
  | o- fileio ........................................................................................... [Storage Objects: 0]
  | o- pscsi ............................................................................................ [Storage Objects: 0]
  | o- ramdisk .......................................................................................... [Storage Objects: 0]
  o- iscsi ...................................................................................................... [Targets: 0]
  o- loopback ................................................................................................... [Targets: 0]
/> cd /iscsi 
/iscsi> create iqn.2020-06.com.example:storage
Created target iqn.2020-06.com.example:storage.
Created TPG 1.
Global pref auto_add_default_portal=true
Created default portal listening on all IPs (0.0.0.0), port 3260.
/iscsi> ls
o- iscsi ........................................................................................................ [Targets: 1]
  o- iqn.2020-06.com.example:storage ............................................................................... [TPGs: 1]
    o- tpg1 ........................................................................................... [no-gen-acls, no-auth]
      o- acls ...................................................................................................... [ACLs: 0]
      o- luns ...................................................................................................... [LUNs: 0]
      o- portals ................................................................................................ [Portals: 1]
        o- 0.0.0.0:3260 ................................................................................................. [OK]
/iscsi> cd 
<                                 >                                 @last                             
iqn.2020-06.com.example:storage/  path=                             
/iscsi> cd 
<                                 >                                 @last                             
iqn.2020-06.com.example:storage/  path=                             
/iscsi> cd iqn.2020-06.com.example:storage/tpg1/
/iscsi/iqn.20...:storage/tpg1> set attribute authentication=0
Parameter authentication is now '0'.
/iscsi/iqn.20...:storage/tpg1> set attribute generate_node_acls=1
Parameter generate_node_acls is now '1'.
/iscsi/iqn.20...:storage/tpg1> set attribute demo_mode_write_protect=0
Parameter demo_mode_write_protect is now '0'.
/iscsi/iqn.20...:storage/tpg1> ls
o- tpg1 ......................................................................................... [gen-acls, no-auth]
  o- acls ................................................................................................. [ACLs: 0]
  o- luns ................................................................................................. [LUNs: 0]
  o- portals ........................................................................................... [Portals: 1]
    o- 0.0.0.0:3260 ............................................................................................ [OK]
/iscsi/iqn.20...:storage/tpg1> cd ..
/iscsi/iqn.20...ample:storage> cd ..
/iscsi> ls
o- iscsi ............................................................................................... [Targets: 1]
  o- iqn.2020-06.com.example:storage ...................................................................... [TPGs: 1]
    o- tpg1 ..................................................................................... [gen-acls, no-auth]
      o- acls ............................................................................................. [ACLs: 0]
      o- luns ............................................................................................. [LUNs: 0]
      o- portals ....................................................................................... [Portals: 1]
        o- 0.0.0.0:3260 ........................................................................................ [OK]
/iscsi> cd ..
/> ls
o- / .......................................................................................................... [...]
  o- backstores ............................................................................................... [...]
  | o- block ................................................................................... [Storage Objects: 1]
  | | o- block1 .................................................. [/dev/vg_db/lv_db (5.0GiB) write-thru deactivated]
  | |   o- alua .................................................................................... [ALUA Groups: 1]
  | |     o- default_tg_pt_gp ........................................................ [ALUA state: Active/optimized]
  | o- fileio .................................................................................. [Storage Objects: 0]
  | o- pscsi ................................................................................... [Storage Objects: 0]
  | o- ramdisk ................................................................................. [Storage Objects: 0]
  o- iscsi ............................................................................................. [Targets: 1]
  | o- iqn.2020-06.com.example:storage .................................................................... [TPGs: 1]
  |   o- tpg1 ................................................................................... [gen-acls, no-auth]
  |     o- acls ........................................................................................... [ACLs: 0]
  |     o- luns ........................................................................................... [LUNs: 0]
  |     o- portals ..................................................................................... [Portals: 1]
  |       o- 0.0.0.0:3260 ...................................................................................... [OK]
  o- loopback .......................................................................................... [Targets: 0]
/> cd iscsi/iqn.2020-06.com.example:storage/tpg1/acls 
/iscsi/iqn.20...age/tpg1/acls> create iqn.2020-06.com.example:database
Created Node ACL for iqn.2020-06.com.example:database
/iscsi/iqn.20...age/tpg1/acls> ls
o- acls ................................................................................................... [ACLs: 1]
  o- iqn.2020-06.com.example:database .............................................................. [Mapped LUNs: 0]
/iscsi/iqn.20...age/tpg1/acls> cd ..
/iscsi/iqn.20...:storage/tpg1> ls
o- tpg1 ......................................................................................... [gen-acls, no-auth]
  o- acls ................................................................................................. [ACLs: 1]
  | o- iqn.2020-06.com.example:database ............................................................ [Mapped LUNs: 0]
  o- luns ................................................................................................. [LUNs: 0]
  o- portals ........................................................................................... [Portals: 1]
    o- 0.0.0.0:3260 ............................................................................................ [OK]
/iscsi/iqn.20...:storage/tpg1> cd ..
/iscsi/iqn.20...ample:storage> ls
o- iqn.2020-06.com.example:storage ........................................................................ [TPGs: 1]
  o- tpg1 ....................................................................................... [gen-acls, no-auth]
    o- acls ............................................................................................... [ACLs: 1]
    | o- iqn.2020-06.com.example:database .......................................................... [Mapped LUNs: 0]
    o- luns ............................................................................................... [LUNs: 0]
    o- portals ......................................................................................... [Portals: 1]
      o- 0.0.0.0:3260 .......................................................................................... [OK]
/iscsi/iqn.20...ample:storage> cd ..
/iscsi> cd /
/> ls
o- / .......................................................................................................... [...]
  o- backstores ............................................................................................... [...]
  | o- block ................................................................................... [Storage Objects: 1]
  | | o- block1 .................................................. [/dev/vg_db/lv_db (5.0GiB) write-thru deactivated]
  | |   o- alua .................................................................................... [ALUA Groups: 1]
  | |     o- default_tg_pt_gp ........................................................ [ALUA state: Active/optimized]
  | o- fileio .................................................................................. [Storage Objects: 0]
  | o- pscsi ................................................................................... [Storage Objects: 0]
  | o- ramdisk ................................................................................. [Storage Objects: 0]
  o- iscsi ............................................................................................. [Targets: 1]
  | o- iqn.2020-06.com.example:storage .................................................................... [TPGs: 1]
  |   o- tpg1 ................................................................................... [gen-acls, no-auth]
  |     o- acls ........................................................................................... [ACLs: 1]
  |     | o- iqn.2020-06.com.example:database ...................................................... [Mapped LUNs: 0]
  |     o- luns ........................................................................................... [LUNs: 0]
  |     o- portals ..................................................................................... [Portals: 1]
  |       o- 0.0.0.0:3260 ...................................................................................... [OK]
  o- loopback .......................................................................................... [Targets: 0]
/> cd iscsi/iqn.2020-06.com.example:storage/tpg1/luns 
/iscsi/iqn.20...age/tpg1/luns>  create /backstores/block/block1
Created LUN 0.
Created LUN 0->0 mapping in node ACL iqn.2020-06.com.example:database
/iscsi/iqn.20...age/tpg1/luns> ls
o- luns ................................................................................................... [LUNs: 1]
  o- lun0 ...................................................... [block/block1 (/dev/vg_db/lv_db) (default_tg_pt_gp)]
/iscsi/iqn.20...age/tpg1/luns> cd /
/> ls
o- / .......................................................................................................... [...]
  o- backstores ............................................................................................... [...]
  | o- block ................................................................................... [Storage Objects: 1]
  | | o- block1 .................................................... [/dev/vg_db/lv_db (5.0GiB) write-thru activated]
  | |   o- alua .................................................................................... [ALUA Groups: 1]
  | |     o- default_tg_pt_gp ........................................................ [ALUA state: Active/optimized]
  | o- fileio .................................................................................. [Storage Objects: 0]
  | o- pscsi ................................................................................... [Storage Objects: 0]
  | o- ramdisk ................................................................................. [Storage Objects: 0]
  o- iscsi ............................................................................................. [Targets: 1]
  | o- iqn.2020-06.com.example:storage .................................................................... [TPGs: 1]
  |   o- tpg1 ................................................................................... [gen-acls, no-auth]
  |     o- acls ........................................................................................... [ACLs: 1]
  |     | o- iqn.2020-06.com.example:database ...................................................... [Mapped LUNs: 1]
  |     |   o- mapped_lun0 ................................................................. [lun0 block/block1 (rw)]
  |     o- luns ........................................................................................... [LUNs: 1]
  |     | o- lun0 .............................................. [block/block1 (/dev/vg_db/lv_db) (default_tg_pt_gp)]
  |     o- portals ..................................................................................... [Portals: 1]
  |       o- 0.0.0.0:3260 ...................................................................................... [OK]
  o- loopback .......................................................................................... [Targets: 0]
/> exit
Global pref auto_save_on_exit=true
Last 10 configs saved in /etc/target/backup/.
Configuration saved to /etc/target/saveconfig.json
[root@storage webcontent]# 
[root@storage webcontent]# 
[root@storage webcontent]# firewall-cmd --permanent --add-port=3260/tcp
success
[root@storage webcontent]# 
[root@storage webcontent]#  firewall-cmd --reload
success
[root@storage webcontent]# systemctl restart target.service
[root@storage webcontent]# 
[root@storage webcontent]# 
```









4. database 서버 구축





