Crontab 
at
lsblk
fdisk
gdisk
partprobe

file system 생성
mkfs.ext4 /dev/sdb1

장치 마운트
  mount /dev/sdb1 /mnt/disk1
  lsblk -f
  ls
  touch /mnt/disk1/file1
  ls
  sync
  umount /dev/sdb1
  ls


  282  sudo fdisk /dev/sdb
  283  free
  284  mkswap /dev/sdb4
  285  sudo mkswap /dev/sdb4
  286  swapon /dev/sdb4
  287  sudo swapon /dev/sdb4

실습 해보세요
gdisk 사용
parted
확장 파티션
163 스왑 파일생성
-------------------------------------------
재부팅 후에도 상태가 유지되어야함
1. 10기가 디스크 추가 (1개)
2. 5G(xfs, read only, 실행파일 실행 허용), 
   1G(ext4, 읽기 쓰기전용 파일시스템 ), 
   500MB(ext4, 입출력 동기 방식 sync(잘될지는 모르겠음.)), 
   2G(xfs,)
3. 200MB swap 영역 구축(파티션으로)
재부팅 후에도 상태가 유지되어야함
1. 10기가 디스크 추가 (1개)
2. 5G(xfs, read only, 실행파일 실행 허용), 
   1G(ext4, 읽기 쓰기전용 파일시스템 ), 
   500MB(ext4, 입출력 동기 방식 sync(잘될지는 모르겠음.)), 
   2G(xfs,)
3. 200MB swap 영역 구축(파티션으로)

sol)-----------------------------------------------------
tail -5 /etc/fstab
UUID=865bdf6f-1429-4d5f-9fda-c83edca05291 /mnt/disk1 xfs ro,exec 0 0
UUID=2aa3ed7a-af2b-42dd-8088-acb1d2b19c74 /mnt/disk2 ext4 rw 0 0
UUID=f4b384cc-9325-4c95-b72b-a2f5aeb79e5c /mnt/disk3 ext4 sync 0 0
UUID=31b68a2a-4a40-435d-bc0a-09d23a51dc79 /mnt/disk4 xfs defaults 0 0
UUID=a5f8ef7d-5606-447f-9aff-92d790fbf187 swap swap defaults 0 0


df -Th
Filesystem              Type      Size  Used Avail Use% Mounted on
devtmpfs                devtmpfs  1.9G     0  1.9G   0% /dev
tmpfs                   tmpfs     1.9G     0  1.9G   0% /dev/shm
tmpfs                   tmpfs     1.9G  8.7M  1.9G   1% /run
tmpfs                   tmpfs     1.9G     0  1.9G   0% /sys/fs/cgroup
/dev/mapper/centos-root xfs       8.6G  1.5G  7.1G  18% /
/dev/sdc5               xfs       2.0G   33M  2.0G   2% /mnt/disk4
/dev/sdc1               xfs       5.0G  224K  5.0G   1% /mnt/disk1
/dev/sdc2               ext4      976M  2.6M  907M   1% /mnt/disk2
/dev/sdc3               ext4      454M  2.3M  424M   1% /mnt/disk3
/dev/sda1               xfs      1014M  150M  865M  15% /boot

lsblk -f /dev/sdc
NAME   FSTYPE LABEL UUID                                 MOUNTPOINT
sdc                                                      
├─sdc1 xfs          865bdf6f-1429-4d5f-9fda-c83edca05291 /mnt/disk1
├─sdc2 ext4         2aa3ed7a-af2b-42dd-8088-acb1d2b19c74 /mnt/disk2
├─sdc3 ext4         f4b384cc-9325-4c95-b72b-a2f5aeb79e5c /mnt/disk3
├─sdc4                                                   
├─sdc5 xfs          31b68a2a-4a40-435d-bc0a-09d23a51dc79 /mnt/disk4
└─sdc6 swap         a5f8ef7d-5606-447f-9aff-92d790fbf187 [SWAP]
-------------------------------------------------------

논리 볼륨
- 이전 : 파티션을 사용해 디스크를 관리함 -> 크기의 유연함이 떨어짐
- 논리볼륨 : 원하는 크기로 생성가능, 확장 가능, 디스크를 제거하는것도 가능, RAID0,1,2,3.. 적용가능

논리 볼륨 구성 단계
fdisk 파티션 생성 -> partprobe -> 물리볼륨 생성 -> 볼륨 그룹 생성 -> 논리 볼륨 생성 -> 파일 시스템 생성 -> mount
fdisk -> partprobe -> pvcreate -> vgcreate -> lvcreate -> mkfs -> mount 

물리볼륨

볼륨그룹 
- 물리 볼륨 집합으롷 구성
- PE 크기를 지정 (기본 4MB)

논리 볼륨

물리볼륨 1G, 논리볼륨 500M 생성


  417  fdisk /dev/sdc 
  418  partprobe
  419  lsblk -f
  420  pvcreate /dev/sdc1
  421  pvdisplay
  422  pvscan 
  423  vgcreate vg0 /dev/sdc1
  424  vgdisplay 
  426  lvcreate --help
  427  lvcreate vg0 -n lv1 -L 500M
  428  lvdisplay 
  429  lsblk -f
  430  mkfs.xfs /dev/vg0/lv1
  431  lsblk -f
  432  mount /dev/vg0/lv1 /mnt/disk1/
  433  lsblk -f
-----------------------------------------


  --- Volume group ---
  VG Name               vg1
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  1
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                0
  Open LV               0
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               2.98 GiB
  PE Size               8.00 MiB
  Total PE              382
  Alloc PE / Size       0 / 0   
  Free  PE / Size       382 / 2.98 GiB
  VG UUID               H6AsdP-Eq8x-zifM-ue9U-pBR0-DK6Z-cU6


vgextend vg1 /dev/sdc5


 VG Name               vg1
  System ID             
  Format                lvm2
  Metadata Areas        3
  Metadata Sequence No  4
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                1
  Open LV               0
  Max PV                0
  Cur PV                3
  Act PV                3
  VG Size               <8.98 GiB
  PE Size               8.00 MiB
  Total PE              1149
  Alloc PE / Size       333 / 2.60 GiB
  Free  PE / Size       816 / <6.38 GiB
  VG UUID               H6AsdP-Eq8x-zifM-ue9U-pBR0-DK6Z-cU6LBr

[root@localhost user]# vgdisplay vg1
  --- Volume group ---
  VG Name               vg1
  System ID             
  Format                lvm2
  Metadata Areas        3
  Metadata Sequence No  4
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                1
  Open LV               0
  Max PV                0
  Cur PV                3
  Act PV                3
  VG Size               <8.98 GiB
  PE Size               8.00 MiB
  Total PE              1149
  Alloc PE / Size       333 / 2.60 GiB
  Free  PE / Size       816 / <6.38 GiB
  VG UUID               H6AsdP-Eq8x-zifM-ue9U-pBR0-DK6Z-cU6LBr
   
[root@localhost user]# lvextend -L 5G /dev/vg1/lv3^C
[root@localhost user]# lvdisplay /dev/vg1/lv3
  --- Logical volume ---
  LV Path                /dev/vg1/lv3
  LV Name                lv3
  VG Name                vg1
  LV UUID                iXXfkz-hxfi-KmGt-HM8U-yT2V-7PV2-WR4Cge
  LV Write Access        read/write
  LV Creation host, time localhost.localdomain, 2020-05-27 11:44:53 +0900
  LV Status              available
  # open                 0
  LV Size                2.60 GiB
  Current LE             333
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:4
   
[root@localhost user]# lvextend -L 5G /dev/vg1/lv3
  Size of logical volume vg1/lv3 changed from 2.60 GiB (333 extents) to 5.00 GiB (640 extents).
  Logical volume vg1/lv3 successfully resized.
[root@localhost user]# lvdisplay /dev/vg1/lv3
  --- Logical volume ---
  LV Path                /dev/vg1/lv3
  LV Name                lv3
  VG Name                vg1
  LV UUID                iXXfkz-hxfi-KmGt-HM8U-yT2V-7PV2-WR4Cge
  LV Write Access        read/write
  LV Creation host, time localhost.localdomain, 2020-05-27 11:44:53 +0900
  LV Status              available
  # open                 0
  LV Size                5.00 GiB
  Current LE             640
  Segments               3
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     8192
  Block device           253:4


논리볼륨 확장
물리볼륨 생성 -> 볼륨그룹에 추가 -> 논리볼륨 확장 -> 파일시스템 확장
파일시스템 확장: xfs_growfs, resize2fs
or 
논리볼륨 확장 + 파일시스템 확장 : lvextend -L <용량> <위치> -r 

-------------------------------------------------------
systemd
- init프로세스에 대한 호환성 제공
- 시스템 부팅시 서비스를 병렬로 시작
- 마운트 포인트와 자동 마운트 관리
- unit 단위로 서비스를 관리한다.
    - http : 서비스 유닛
    - sshd : 소캣유닛 

- unit : 유닛의 conf파일 존재
      유닛을 시작 -> conf파일을 읽어옴(메모리에 올라감) -> 실행됨
                   설정만 변경 -> 실행 
-----------------------------------------------------
리눅스 부트 프로세스
1) 부팅
POST
부트로더를 메모리에 적재후 -> grub2 적재 -> 부팅가능한 커널 목록을 출력
-> 커널선택 -> systemd 실행한다. -> target(unit중에 하나) -> default target 

멀티유저 타겟 (총 로그인을 4명까지 가능하게만들어준다.ctrl+alt+f1~f4)
-> 그래픽 타겟
멀티1 -> 그래픽 타겟
멀티2
멀티3
멀티4

-----------------------------------------------------------
CentOS타겟 변경
최소 설치 되어있기 때문에 Xwindow를 설치 해야한다. 
yum groupinstall "GNOME Desktop"
systemctl isolate graphical.target 입력(일시적으로 타겟 변경)
systemctl set-default graphical.target
systemctl set-default multi-user.target
VBOX 화면확인

target 의 종류
emergency : 최소한의 환경만 제공
            부팅중 문제가 발생했을때.
            루트파일 시스템(/) : 읽기 전용
            파일 내용을 수정할떄는 읽기-쓰기로 다시 마운트 해야됨
rescue : 단일 사용자 환경 복구쉘
        / : 읽기 쓰기로 마운트됨
        네트워크 인터페이스는 비활성화
multi-user : CLI 제공 사용자 4명까지 가능 
graphical : GUI
            multiuser  target 다음 단계에 실행된다.
            별도 설치 필요

--------------------------------------------
root password 복구
grub -> e
UTF-8 rd.break
mount -o rw,remount /sysroot
chroot /sysroot
passw 
exit
reboot

------------------------------------------
rescue 모드
grub -> e
UTF-8 systemd.unit=emergency.target
---

로그관리
- 이벤트의 기록

시스템 이벤트 -> systemd-journald -> rsyslogd  /etc/rsyslog.conf -> /var/log
                               -> journal : 모든 로그파일을 생성, /run/log/journal/
systemd-journald : 부팅 순간부터 모든 로그를 수집

/etc/rsyslog.conf
[facility].[level] [action]
[facility]: 무엇을 남길 것인가, 어디에서 발생한 메세지를 남길것인가
[Level] : 저장되는 로그 레벨
[Action] : 저장되는 장소
---------------------------------------------
로그 순환
/etc/rsyslog.conf
*.info;mail.none;authpriv.none;cron.none                /var/log/testlog.log

systemctl restart rsyslogd.service
로그가 생성됨
------------------------------------
vi /etc/logrotate.d/testlog
/var/log/testlog.log{
  size=3k
  create 600 root root
  rotate 3
  nodateext
}
------------------------------------
로그를 발생 
logger "homehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehomehome"
3k이상 로그가 발생되면

logrotate 실행 
logrotate -f /etc/logrotate.d/testlog

소프트웨어 패키지
RPM 패키지 관리도구
- 종속성 문제가 발생함

YUM/DNF
- RPM의 종속성 문제를 해결함
- 패키지를 설치할때 종속성 문제를 해결해 의존성 패키지들을 함께 설치해 준다.
- Ubuntu 의 apt or apt-get 과 사용법은 비슷하다.

 yum 저장소(repository)
 - 패키지들을 저장해놓은 하나의 서버(웹서버)
 - 패키지를 다운받을수 있고, 패키지에 대한 정보도 다운받을수 있다.
 - YUM 저장소는 웹서버, repofile 


 http://mirror.kakao.com/centos/
 
curl https://rpmfind.net/linux/opensuse/ports/riscv/tumbleweed/repo/oss/riscv64/vim-8.2.0701-5.1.riscv64.rpm -o ./vim.rpm
rpm -i ./vim.rpm

예제
mc 패키지 설치

--------------------------------------
repo 추가
 echo '[base]
name=CentOS-$releasever - Base
baseurl=http://ftp.daumkakao.com/centos/$releasever/os/$basearch/
gpgcheck=0 
[updates]
name=CentOS-$releasever - Updates
baseurl=http://ftp.daumkakao.com/centos/$releasever/updates/$basearch/
gpgcheck=0
[extras]
name=CentOS-$releasever - Extras
baseurl=http://ftp.daumkakao.com/centos/$releasever/extras/$basearch/
gpgcheck=0' > /etc/yum.repos.d/Daum.repo
  130  cd /etc/yum.repos.d/
  131  ls
  133  yum repolist
  134  cat Daum.repo 
  135  yum update

http://ftp.kaist.ac.kr/CentOS/7.8.2003/os/x86_64/

vim /etc/yum.repos.d/kaist.repo
[ftp.kaist.ac.kr_CentOS_7.8.2003_os_x86_64_]
name=added from: http://ftp.kaist.ac.kr/CentOS/7.8.2003/os/x86_64/
baseurl=http://ftp.kaist.ac.kr/CentOS/7.8.2003/os/x86_64/
enabled=1
gpgcheck=0

  158  rm -rf *.repo
  160  yum clean all
  161  yum update
  162  yum repolist all
  164  yum-config-manager --add-repo="http://ftp.kaist.ac.kr/CentOS/7.8.2003/os/x86_64/"



---------------------------------------------------------
SSH
Telnet -> SSH
암호화 알고리즘
대칭키 기반
    같은 키를 사용해서 데이터를 암호화 한다.
    키(암호화 알고리즘) : a -> 1
    apple ->  key1 : 암호화(a -> 1) -> 1pple -> key1 : 복호화(a->1) -> apple 
비대칭키 기반
    key1 과 key2가 동시에 생성된다. 
    개인키와 공개키 라고 한다.
    공개키 : 외부에 공개된키로 누구나 공개키를 가지고 있어도 된다.
    개인키 : 키를 만든 생성자만 갖고 있는키다.
    공개키는 데이터를 암호화 해서 전달. -> 개인키를 이용해서 복호화 한다.
    사람1: apple -> key1 (공개키): 암호화 (a -> 1) -> 1pple -> key2(개인키) : 복호화(a->1) -> apple : 사람2

SSH 구성1
client -> server 접속요청
server -> 공개키를 전달 -> client
client -> client 의 공개키를 server의 공개키로 암호화 -> server의 개인키로 복호화 -> client의 공개키 -> Server

SSH 구성
client -> server 접속요청
server -> 공개키를 전달 -> client
client -> 대칭키를 만든다(비밀키) -> server 의 공개키로 암호화 -> server의 개인키로 복호화 -> client가 만든 비밀키 -> server
client <-비밀키-> server
------------------------------------------------------
sudo apt-get install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
sudo adduser $USER kvm
sudo apt-get install -y virt-manager
sudo virt-manager
---------------------------------------------------------
client
ip 192.168.122.100/24
gateway 192.168.122.1
dns 8.8.8.8
hostname client.cccr.co.kr

server
ip 192.168.122.200/24
gateway 192.168.122.1
dns 8.8.8.8
hostname server.cccr.co.kr

yum install -y bash-completion net-tools
nmcli connection add con-name eth0-client type ethernet ifname eth0
nmcli connection modify eth0-client ipv4.addresses 192.168.122.100/24
nmcli connection modify eth0-client ipv4.gateway 192.168.122.1
nmcli connection modify eth0-client ipv4.dns 8.8.8.8
nmcli connection modify eth0-client ipv4.method manual
nmcli connection modify eth0-client autoconnect yes
hostnamectl set-hostname client.cccr.co.kr
nmcli connection up eth0-client

yum install -y bash-completion net-tools
nmcli connection add con-name eth0-server type ethernet ifname eth0
nmcli connection modify eth0-server ipv4.addresses 192.168.122.200/24
nmcli connection modify eth0-server ipv4.gateway 192.168.122.1
nmcli connection modify eth0-server ipv4.dns 8.8.8.8
nmcli connection modify eth0-server ipv4.method manual
nmcli connection modify eth0-server autoconnect yes
hostnamectl set-hostname server.cccr.co.kr
nmcli connection up eth0-server

client : AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAdtLqgM7RfNOiT8ZqC72qrDf7vTopXPuog/QcwMt1FzoAQZ38VRJ1PbWEFZmxozfeOPGD4hwn+EviacKU863PQ=
server : AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBAdtLqgM7RfNOiT8ZqC72qrDf7vTopXPuog/QcwMt1FzoAQZ38VRJ1PbWEFZmxozfeOPGD4hwn+EviacKU863PQ= 
--------------------------------------------
open ssh 설치(서버설치)
yum install openssh-server

서버&클라이언트 설치
yum install ssh

서버의 key가 저장되어 있는 위치는 
/etc/ssh/~~~.pub
클라이언트의 key 저장되어 있는 위치는
/home/user/.ssh/know_hosts
--------------------------------------------
x-11 포워딩
ssh -X student@192.168.0.175
gedit aaaa.txt
firefox www.google.com

인증관련
- 특정사용자만 로그인
vi /etc/sshd/sshd_config
AllowUsers userssh
- root 로그인 되지 않게
vi /etc/sshd/sshd_config
PermitRootLogin no 
-키기반 인증
vi /etc/sshd/sshd_config
PasswordAuthentication no 
   28  ssh-keygen -t ecdsa
   29  ssh-copy-id user@192.168.122.200
   30  ssh user@192.168.122.200





가상머신 스냅샷 찍어두세요
ova 파일도 만들어 두세요.

사용자 : 로그인 하는 대상
그룹 : 사용자의 집합
    - 기본그룹 : 처음 생성할때 속한 그룹
    - 보조그룹 : 생성 이후 추가적으로 속하는 그룹

가상머신 초기화 하세요

30분까지 쉬세요.
가상머신 고치세요

set uid
chmod u+s
chmod u-s
chmod 4xxx
파일 : 소유자 권한으로 실행
디렉토리 : 영향x

set gid 
chmod g+s
chmod g-s
chmod 2xxx
파일 : 소유 그룹의 권한으로 실행
디렉토리 : 새로운파일 생성 -> 해당 디렉토리와 동일한 소유그룹으로 지정된다.

sticky bit
chmod o+t
chmod o-t
chmod 1xxx
파일 : 영향x
디렉토리 : 해당 디렉토리에서 파일 삭제시 본인 소유의 파일만 삭제가능

ACL
파일소유자
ACL등록사용자
소유그룹
ACL등록그룹
other











?  ~ getfacl roster.txt 
# file: roster.txt
# owner: user
# group: user02
user::rwx
user:1005:rwx
user:james:---
group::rwx
group:sudor:r--
group:2210:rwx
mask::rwx
other::---

   35  touch file1.txt
   36  ls -al file1.txt
   37  getfacl file1.txt
   38  setfacl --help
   39  getfacl file1.txt
   41  setfacl -m user:user01:rwx file1.txt
   42  getfacl file1.txt
   43  setfacl -b file1.txt
   44  getfacl file1.txt
   45  setfacl -m user:user01:-wx file1.txt
   46  getfacl file1.txt

   54  setfacl -b user:user01:-wx file1.txt
   57  setfacl -x mask file1.txt
   58  getfacl file1.txt
   59  setfacl -m user:user01:-wx file1.txt
   60  getfacl file1.txt
   61  setfacl -m mask::-wx file1.txt
   62  getfacl file1.txt
   63  setfacl -m mask::--x file1.txt
   64  getfacl file1.txt

------------------------------------------------
dir1 : acl 사용자 적용 -> dir1/dir1-1 생성 ACL확인
dir2 : acl default 사용자 적용 -> dir2/dir2-1 생성 ACL 확인





