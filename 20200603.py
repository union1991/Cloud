Day 14.

## 목차
 
### 8. 리눅스 핵심 운영 가이드

> #### 8.6 SMB 스토리지


------------
 
 
## 8. 리눅스 핵심 운영 가이드
 
 
최신 리눅스 시스템의 핵심 기술과 원리를 배우며 서버 관리자, 시스템 엔지니어, 클라우드 관리자, 개발자, DBA, 데브옵스 등 다양한 IT 관리자 및 개발자들에게 기본이 되는 기술을 습득한다.



 ------------

 
 #### 8.6 SMB 스토리지

* 윈도우 계열 시스템에서 파일을 공유하는 서비스
* SMB 프로토콜 사용
* SMB 데몬 
> * smbd
> * nmbd
>   + 윈도우 기반에서 SMB/CIFS에 생성된 NetBIOS 이름 서비스 요청에 대해 인식/응답
> * winbindd
>   + 사용자와 그룹 정보를 리눅스가 이해할 수 있게 변환

*smb 실습
> * samba server 설치 및 환경 설정
```
# yum install samba samba-client
# mkdir -m 777 -p /samba/smb1
# useradd -s /sbin/nologin smb1     // samba 계정은 로그인이 필요없는 서비스 계정이다. 따라서 로그인 불가로 계정 생성
# smbpasswd -a smb1     // samba 계정 패스워드 설정
# pdbedit -L    //samba 계정 확인
# vi /etc/samba/smb.conf

[print$]
        comment = Printer Drivers
        path = /var/lib/samba/drivers
        write list = @printadmin root
        force group = @printadmin
        create mask = 0664
        directory mask = 0775

[first]
        comment = Hello world
        path = /samba/smb1
        valid user = smb1
        vrowseable = no
        write list = smb1

:wq!

# systemctl start smb nmb
# systemctl enable smb nmb
# systemctl start smb nmb
# firewall-cmd --add-service=samba --permanent
# firewall-cmd --reload

```


> * samba client 설정
```
# sudo yum install -y cifs-utils
# mkdir /mnt/smb1
# mount //192.168.122.200/first
# mount -o username=smb1 //192.168.122.200/first /mnt/smb1
Password for smb1@//192.168.122.200/first:  // smb1 입력

# vi /etc/fstab

#
# /etc/fstab
# Created by anaconda on Fri May 22 14:34:12 2020
#
# Accessible filesystems, by reference, are maintained under '/dev/disk'
# See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
#
/dev/mapper/centos-root /                       xfs     defaults        0 0
UUID=923745de-1bfd-4c7e-89a1-5895651ee0ec /boot                   xfs     defaults        0 0
/dev/mapper/centos-swap swap                    swap    defaults        0 0
//192.168.122.200/first /mnt/smb1       cifs    credentials=/root/credsmb1      0 0  // 추가

:wq!


#vi /root/credsmb1

username=smb1
password=smb1

:wq!


```
