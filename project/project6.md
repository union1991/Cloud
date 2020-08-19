# AWX를 이용한 Haproxy 서비스 2티어 구성

## 목차

## 0. 과제 개요
> ### 0.1 과제 내용
> ### 0.2 시스템 구성
> ### 0.3 네트워크 구조


## 1. AWX 및 Ansible Tower
> ### 1.1 AWX 및 Ansibel Tower 소개
> ### 1.2 AWX 설치 
> ### 1.3 AWX 사용 

## 2. Playbook


---

## 문서 수정 이력


|수정 날짜|내용|기타|
|:--|:--|:--|
|20.08.14|최초 작성||
|20.08.17|과제 환경설정, Playbook||


---

## 0. 과제 개요


본 과제의 목적은 AWX를 이용하여 '(로드밸런스) - (웹 - 데이터베이스)' 환경을 구성하여 자동화 기술과 웹 서비스의 본질을 이해하는 것이다.  



### 0.1 과제 내용


#### 본 과제의 구성도는 아래와 같다.


![test (2)](https://user-images.githubusercontent.com/56064985/90222442-05d34e80-de47-11ea-83d4-1097c4f98917.png)



### 0.2 과제 환경 설정

#### 본 과제의 환경 설정은 아래와 같다.


#### [시스템]
|서버|메모리|운영체제|
|:--|:--|:--|
|Controller|2048 MiB|Linux controller 3.10.0-1127.el7.x86_64 #1 SMP x86_64 x86_64 x86_64 GNU|
|Haproxy(node1)|2048 MiB|Linux node1 3.10.0-1127.el7.x86_64 #1 SMP x86_64 x86_64 x86_64 GNU|
|WEB1(node2)|2048 MiB|Linux node2 3.10.0-1127.el7.x86_64 #1 SMP x86_64 x86_64 x86_64 GNU|
|WEB2(node3)|2048 MiB|Linux node3 3.10.0-1127.el7.x86_64 #1 SMP x86_64 x86_64 x86_64 GNU|
|DB1(node4)|2048 MiB|Linux node4 3.10.0-1127.el7.x86_64 #1 SMP x86_64 x86_64 x86_64 GNU|
|DB2(node5)|2048 MiB|Linux node5 3.10.0-1127.el7.x86_64 #1 SMP x86_64 x86_64 x86_64 GNU|




#### 과제 성취도 평가

1. 구성도를 확인하여 서버를 구성할 수 있는가?
2. AWS를 이용한 자동화 서비스를 이해하였는가?
3. Playbook을 작성하고 서비스 배포가 가능한가?



---



## 1. AWX 및 Ansible Tower


### 1.1 AWX 및 Ansibel Tower 소개 


![image](https://user-images.githubusercontent.com/56064985/90197669-3fd22f80-de0a-11ea-80a6-3c8a6713cde8.png)


```Ansible Tower```는 REST API, 웹 서비스 및 웹 기반의 대시보드로 Ansible을 한층 더 유용하게 사용할 수 있도록 도와준다. ```Ansible Tower```는 RedHat, INC.에서 지원하는 사용 제품이며 ```AWX```는 2017년 9월 오픈소스로 공개된 버전이다. 




#### AWX의 특징

* 대시보드 사용
* 실시간 작업 상태 확인
* 멀티 플레이북 워크플로우
* 실행 작업 기록(Who ran what job when)
* 역할기반 접근 제어(RBAC)
* 타워 클러스터를 사용하여 스케일 조절
* 통합 알림
* 작업 스케줄링
* 인벤토리 관리 및 추적
* 간단한 셀프 서비스 방식
* 원격 명령 실행
* RESTful API




#### AWX 구성 방법

* AWX와 데이터베이스를 같은 서버에 구성
* AWX와 데이터베이스를 다른 서버에 구성
* AWX 클러스터 구성




#### 최소 시스템 요구사항

* AWX 8.0.0 버전 기준의 요구사항

|항목|요구사항|
|:--|:--|
|운영체제|RedHat:7.4 이상, Ubuntu: 14 이상|
|CPU|최소 2개|
|메모리|최소 4GB|
|디스크|20GB|
|PostgreSQL|9.6.X 필요|
|Ansible|2.2 이상|




#### 소프트웨어 요구사항

* Ansible 2.4 이상
* Docker
* Docker 및 Docker-compose Python 모듈
* GNU Make
* Git 1.84 이상
* Node 6.X LTS 버전
* NPM 3.X LTS 


### 1.2 AWX 설치 

#### 레포지토리 및 패키지 설치

* Ansible 버전을 사용하기 위한 EPEL 레포지토리 추가
```
# yum -y install epel-release.noarch
# yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```


* 소프트웨어 요구사항에 따라 필요한 패키지 설치
```
# yum -y install docker-ce docker-ce-cli containerd.io
# yum -y install ansible make git nodejs npm python-pip
# yum -y update python
# sudo pip install docker docker-compose
```


* AWX Git 레포지토리를 홈 디렉토리 및 적절한 디렉토리에 클론
```
# git clone https://github.com/ansible/awx.git
```


* Inventory 파일에서 변수를 적절하게 설정
```
# cd awx/installer
# vi inventory

...
postgres_data_dir=/var/lib/pgdocker        // 주석을 제거하여 postgres_data_dir의 경로를 지정한다
...
admin_password=<password>                 // <password>를 변경하여 admin 계정 로그인 패스워드를 지정
...
docker_compose_dir=/var/lib/awxcompose
...

```


* install.yml 플레이북을 실행시켜 설치
```
# ansible=playbook -i inventory install.yml
```



### 1.3 AWX 사용 



#### 본 과제의 AWX 서비스는 다음과 같다.


![test2](https://user-images.githubusercontent.com/56064985/90228658-9020b000-de51-11ea-8b8f-3cd7c11f6a99.png)



### AWX 서비스 시작

* 로그인 페이지(Default 정보)
> user: admin
> Password: password


<img src="https://user-images.githubusercontent.com/56064985/90206711-5767e300-de1f-11ea-981c-0c2a2f3baf7d.png" width="70%"></img>


* AWX 대시보드


<img src="https://user-images.githubusercontent.com/56064985/90206714-5931a680-de1f-11ea-8678-4a19585e69df.png" width="70%"></img>



### 대시보드를 이용한 자동화


#### 프로젝트(Projects)


AWX의 ```프로젝트```는 플레이북의 모임이다.


* 프로젝트 생성
> * 플레이북이 존재하는 디렉토리 경로를 지정하려면 해당 서버에 직접 원격 접속하여 디렉토리를 생성해야함
```
# mkdir /var/lib/awx/projects/awx-project
```

> * [RESOURCES] - [Projects] - [ + ] 
```
1.NAME(필수): AWX-project
2.DESCRIPTION(선택):
3.ORGANIZATION(필수): Default
4.SCM TYPE(필수): Manual
5.PROJECT BASE PATH(자동입력): /var/lib/awx/projects
6.PLATBOOK DIRECTORY(필수): awx-project
```



#### 자격증명(Credentials)


```자격증명```은 컨트롤 머신에서 관리 노드에 접근할 때 사용하는 인증 값이다. 만약 연결 유형이 SSH라면 사용자의 아이디와 패스워드 또는 개인키를 지정해야 한다. ```자격증명``` 유형으로는 클라우드 기반, 일반적인 머신 기반 등 다영하게 존대한다.


> * Control 서버에 직접 원격 로그인 하여 SSH PRIVATE KEY를 복사
```
# cat .ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAqF6VsMa9k0vzE320Yv+QRn+HToTfpfFNdIpvNgdqpbythJ5M
tNWCVgtUwUWbnPM7TWQQ9DjynKtVTZjo5DHzAk+rvuzYHonJ2blr5X7E2+r1zxx5
Shc86ZA7qvWTs47jeq7p8RkD3iVxxIZ5ekUC0VjiOuCk57RitrgycasrtJCg2aYa
mlNwykdan2LvL2jUY6BcPgkLJsJCx8MhmrIQAVSIAh4XQ24qVij+3EmjoYncjV6t
xRnkAOj0fLtAPwnOOG55Aox2WOdLkyOdMjR07U7PbiAZ5rIBz1FGuH3TMAX+m1V4
OHA0Cf4mlLYFcsM0Vi6X7EiJSShAhhgmFSY+hQIDAQABAoIBAGaVSmrsi/DE45NK
ka+HumXZqZ0DhChc/y40clHe7vGQJcCZmm7Lb5/xQ3CGcquL3uPmRhYm5FrkYRLo
SW1PqZoM5L1tHLhuh1dqi/zF4jeDzsSjupqT0f8Ua+ZbveQ2+Q50qADHlv2wnsJ4
lGcUyQS4PQ5WdOLfmw1s6P8spXJbdz/HQuwgCWr5wU9AHBmbVlQCAHHhl8d4BKS3
fXsXIhPKyNp/Kk8G1Qblda7nHF2E/UL/A776z+UwKqzxMaluRV1HNncqRyKTZOVm
CupYYaOnVoZEizzqieN3T7M42eU1G3zADUsEjAxrg3pnVyfI1KbzieiN8aA0hnsy
V7/gYoECgYEA0wHLxefUhfqV0lNwUHFECFHlaNwRIaX3B3/G6YwJ+qbbtJc0MNX2
T0WBICGBxqWoSjw1v0HMFQ6hs8CWAn1CyBRh5vw+EjghW79F8HfVjKgMXeg5RODV
UJFV/XX53AVHzUchuYy677GOuqlEY6bSFiC69YEPm9kmqHX4DP7caHUCgYEAzEVX
I9W5xnC8XZQkTGLTcG51xU/6cLjD3uqcgtI4cZrcWXfQG+ilY0raimTkE8hxD/1m
5dUH1KpK8lTZRvjmyvshBhqPl1+zy+TgEgxmf4/xqTNbVwh3amKiHIgf/p3OGdOI
Kt9YVf7pajcAUqzL1yKqZMFQLGUODZHRrsZaO9ECgYEAw415jXtSIazfpuH/R/4A
v/kuNCUnl1iZfRC1hwJqySpUmaQ8ETpqIINYrS+Ad1pVgh8U7KCNA8Lgp5dHLx1p
g8YoCYsh936fo8i7h6V3evjPJUSvtp7r8tQOrmzk2Dzok11l6vF62eNjVKjEodob
/7frrNUkYxo30o4qCdk06XUCgYBiVM7J1UyElihW88U1cC1QZhwTS5jHQmonmNCW
uROqvF1uRBrOFIPo9FOXY1HXpBmpFNa/tHj8iq1hUi7110NiWtle0tJkkBFBCYBD
r+x3Y5d1V9+UWeMCN1DKY0zjiJt6GzXlTXZ8jyVVl/xzz/KgMXPM5LHvbQYCyjsh
4yH0wQKBgQC/gRtmsdd/FGG3hQ6ClA0MsKK6YUXuY0Wg4Zug8yIbn/1cw0yK599z
U2PJ7aLHW8cuCAE4ohjRR70ljzWf8WSF9C0zg7a7M4f0HUIzqb8wuc6gn8R4EbEJ
lGbuzzOmI5X/3eP6so1g70ZYnLeVUizrfcI1QMTWav8i+yQSAkd97Q==
-----END RSA PRIVATE KEY-----
```


> * [RESOURCES] - [Credentials] - [ + ] 
```
1.NAME(필수): AWX-credential
2.DESCRIPTION(선택):
3.ORGANIZATION(필수): Default
4.CREDENTIAL TYPE(필수): Machine
5.USERNAME: student
6.PASSWORD: dkagh1.
7.PRIVILEGE ESCALATION METHOD : sudo
8.SSH PRIVATE KEY:
cat .ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAqF6VsMa9k0vzE320Yv+QRn+HToTfpfFNdIpvNgdqpbythJ5M
tNWCVgtUwUWbnPM7TWQQ9DjynKtVTZjo5DHzAk+rvuzYHonJ2blr5X7E2+r1zxx5
Shc86ZA7qvWTs47jeq7p8RkD3iVxxIZ5ekUC0VjiOuCk57RitrgycasrtJCg2aYa
mlNwykdan2LvL2jUY6BcPgkLJsJCx8MhmrIQAVSIAh4XQ24qVij+3EmjoYncjV6t
xRnkAOj0fLtAPwnOOG55Aox2WOdLkyOdMjR07U7PbiAZ5rIBz1FGuH3TMAX+m1V4
OHA0Cf4mlLYFcsM0Vi6X7EiJSShAhhgmFSY+hQIDAQABAoIBAGaVSmrsi/DE45NK
ka+HumXZqZ0DhChc/y40clHe7vGQJcCZmm7Lb5/xQ3CGcquL3uPmRhYm5FrkYRLo
SW1PqZoM5L1tHLhuh1dqi/zF4jeDzsSjupqT0f8Ua+ZbveQ2+Q50qADHlv2wnsJ4
lGcUyQS4PQ5WdOLfmw1s6P8spXJbdz/HQuwgCWr5wU9AHBmbVlQCAHHhl8d4BKS3
fXsXIhPKyNp/Kk8G1Qblda7nHF2E/UL/A776z+UwKqzxMaluRV1HNncqRyKTZOVm
CupYYaOnVoZEizzqieN3T7M42eU1G3zADUsEjAxrg3pnVyfI1KbzieiN8aA0hnsy
V7/gYoECgYEA0wHLxefUhfqV0lNwUHFECFHlaNwRIaX3B3/G6YwJ+qbbtJc0MNX2
T0WBICGBxqWoSjw1v0HMFQ6hs8CWAn1CyBRh5vw+EjghW79F8HfVjKgMXeg5RODV
UJFV/XX53AVHzUchuYy677GOuqlEY6bSFiC69YEPm9kmqHX4DP7caHUCgYEAzEVX
I9W5xnC8XZQkTGLTcG51xU/6cLjD3uqcgtI4cZrcWXfQG+ilY0raimTkE8hxD/1m
5dUH1KpK8lTZRvjmyvshBhqPl1+zy+TgEgxmf4/xqTNbVwh3amKiHIgf/p3OGdOI
Kt9YVf7pajcAUqzL1yKqZMFQLGUODZHRrsZaO9ECgYEAw415jXtSIazfpuH/R/4A
v/kuNCUnl1iZfRC1hwJqySpUmaQ8ETpqIINYrS+Ad1pVgh8U7KCNA8Lgp5dHLx1p
g8YoCYsh936fo8i7h6V3evjPJUSvtp7r8tQOrmzk2Dzok11l6vF62eNjVKjEodob
/7frrNUkYxo30o4qCdk06XUCgYBiVM7J1UyElihW88U1cC1QZhwTS5jHQmonmNCW
uROqvF1uRBrOFIPo9FOXY1HXpBmpFNa/tHj8iq1hUi7110NiWtle0tJkkBFBCYBD
r+x3Y5d1V9+UWeMCN1DKY0zjiJt6GzXlTXZ8jyVVl/xzz/KgMXPM5LHvbQYCyjsh
4yH0wQKBgQC/gRtmsdd/FGG3hQ6ClA0MsKK6YUXuY0Wg4Zug8yIbn/1cw0yK599z
U2PJ7aLHW8cuCAE4ohjRR70ljzWf8WSF9C0zg7a7M4f0HUIzqb8wuc6gn8R4EbEJ
lGbuzzOmI5X/3eP6so1g70ZYnLeVUizrfcI1QMTWav8i+yQSAkd97Q==
-----END RSA PRIVATE KEY-----
```



#### 인벤토리(Inventory)


AWX의 ```인벤토리```는 Ansible에서의 인벤토리와 같다. AWX에서는 인벤토리를 그래픽으로 관리할 수 있다.


> * [RESOURCES] - [Inventories] - [ + ] - [Inventory]
```
[DETAILS]
1.NAME(필수): AWX-inventory
2.DESCRIPTION(선택):
3.ORGANIZATION(필수): Default

[HOSTS] - [ + ]
1.HOST NAME(필수): node1
2.DESCRIPTION(선택):
3. VARIABLES
---
ansible_host: 192.168.123.60
```



#### 템플릿(Template)


```템플릿```은 ansible-playbook 명령으로 플레이북을 실행하는 형태를 정의해 놓은 객체이다.


> * [RESOURCES] - [Templates] - [ + ] - [Inventory]
```
[DETAILS]
1.NAME(필수): AWX-inventory
2.DESCRIPTION(선택):
3.JOB TYPE(필수): Run
4.INVENTORY: AWX-inventory
5.PROJECT: AWX-project
6.PLAYBOOK: hello-world.yaml
```


---

## 2. Playbook

#### ansible.cfg
* INI 형식의 설정 파일
* 우선 순위
> ANSIBLE_CONFIG 환경 변수에 지정한 파일
> 현재 디렉토리에 있는 ansible.cfg 파일
> 사용자 홈 디렉토리에 .ansible.cfg 파일
> /etc/ansible/ansible.cfg 파일(글로벌한 기본 설정)

```
[defaults]
inventory = inventory.ini
callback_whitelist = profile_tasks
```

#### inventory.ini
* 어떤 시점에 어떤 목적을 수행할지에 따라 결정되어진 시스템의 묶음 단위로 나누어 대괄호로 지정된 그룹 이름별로 나누는것이 가능
```
node1 ansible_host=192.168.123.51
node2 ansible_host=192.168.123.52
node3 ansible_host=192.168.123.53
node4 ansible_host=192.168.123.54
node5 ansible_host=192.168.123.55 ansible_python_interpreter=/usr/bin/python2.7

[wp-lb]
node5

[wp-web]
node2
node3

[wp-db]
node4

[wp-nfs]
node4

[wp:children]
wp-lb
wp-web
wp-db
wp-nfs
```


#### site.yaml
* 각 roles 의 hosts 권한 부여
```
- hosts: wp
  become: yes
  roles: 
    - common

- hosts: wp-nfs
  become: yes
  roles: 
    - nfs

- hosts: wp-db
  become: yes
  roles: 
    - mariadb

- hosts: wp-web
  become: yes
  roles: 
    - apache

- hosts: wp-lb
  become: yes
  roles: 
    - haproxy
```


#### group_vars
* 변수 파일을 정의
> wp/apache.yaml
```
apache:
  port: 80    # apache port를 80으로 정의

php:
  repo: 
    pkg: "https://rpms.remirepo.net/enterprise/remi-release-7.rpm "     # php.repo.pkg의 주소를 다음으로 정의
```


> wp/haproxy.yaml
```
haproxy:
  frontend:
    port: 80      # haproxy.frontend.port를 80으로 정의
  backend:
    name: wordpress
    balance_type: roundrobin          # haproxy 서비스를 RR 방식으로 지정
    wordpress1:
      port: 80        # web1 서버의 haproxy 포트를 80으로 지정
    wordpress2:
      port: 80        # web2 서버의 haproxy 포트를 80으로 지정
```

> wp/mariadb.yaml
```
mariadb:
  repo:       # mariadb 레포지토리 정의
    baseurl: http://mirror.yongbok.net/mariadb/yum/10.5/centos7-amd64
    gpgkey: http://mirror.yongbok.net/mariadb/yum/RPM-GPG-KEY-MariaDB 
  wp:
    name: wordpress_db              # db 추가
    user: admin                        # db계정 추가
    pwd: dkagh1.                       # db계정 패스워드 지정
    priv: wordpress_db.*:ALL,GRANT          # 신규 db에 신규 admin 계정 권한 부여
    host: '192.168.123.%'                   # 접근 허용 주소 
  port: 3306                           # mariadb 포트 지정
```     


> wp/nfs.yaml
```
nfs:
  exports:
    directory: /wordpress               # db 서버에서 web 서버로 공유할 파일 서버 경로(wordpress 파일)
    subnet: 192.168.123.0/24            # nfs 서비스를 제공할 네트워크 정의
    options: rw,sync,no_root_squash               # 읽기/쓰기, 동기화, no_root_squash(root 권한이 없어도 사용 가능)
  block:
    #device: /dev/vdb
    fs_type: ext4
```

> wp/wordpress.yaml
```
wordpress:                     # wordpress 설치 시, 패키지 빌드 버전 정의
  source:
    version: 5.3.4
    language: ko_KR
  db:                         # wp-config에 필요한 요소 정의
    name: wordpress_db            
    username: admin
    password: dkagh1.
    host: 192.168.123.54
```

#### roles/apache/handlers/main.yml
```
---
- name: Restart httpd
  service:                        # apache 핸들러 파일(restart를 요구하는 이벤트 발생 때, 실행) 
    name: httpd                 
    state: restarted
```

#### wp-role/roles/apache/tasks/main.yml
```
---
- name: Install nfs-utils
  yum:                                               # yum 명령어를 통한 nfs-utils 서비스 설치
    name: nfs-utils
    state: latest
- name: Install httpd     
  yum:                                               # yum 명령어를 통한 httpd 서비스 설치 
    name: httpd 
    state: latest
- name: Copy configuration
  template:
    src: apache.conf.j2                                   # controller 서버에 미리 작성해 놓은 apache.conf.j2의 템플릿에 따라 아래의 경로의 파일 생성
    dest: /etc/httpd/conf/httpd.conf
  notify:
  - Restart httpd                                         # wp-role/roles/apache/tasks/main.yml 에 지정되어 있는 서비스 실행
- name: Delegate collecting facts for mariadb
  setup:
  delegate_to: node4
- name: Set facts for mariadb private ip
  set_fact:
    db_private_ip: "{{ ansible_eth1.ipv4.address }}"              # ansible 명령어를 통한 eth1.ipv4 주소
- name: Mount nfs share
  mount:
    path: /var/www/html
    src: "{{ db_private_ip }}:{{ nfs['exports']['directory'] }}"          # group_vars/wp/nfs.yaml 에 정의있는 변수
    fstype: nfs
    state: mounted
- name: Open http port
  firewalld: 
    port: "{{ apache['port'] }}/tcp"
    permanent: yes 
    state: enabled 
    immediate: yes
- name: Active seboolean for httpd                          # selinux 설정으로 인해 막힌 httpd, mariadb 서비스 오픈
  seboolean:
    name: "{{ item }}"                                      # 하단의 with_items 리스트의 값들을 순차로 입력
    state: yes
    persistent: yes
  with_items: "{{ sebool_httpd_lists }}"                    # roles/apache/vars/main.yaml 에 선언된 리스트 참조
- name: Install remi-release-7 for php74
  yum: 
    name: "{{ php['repo']['pkg'] }}"
    state: latest
- name: Install php and php-mysql                           # wordpress 설치에 필요한 php7.2 이상 버전 설치
  yum: 
    name: php,php-mysql 
    enablerepo: remi-php74 
    state: latest
- name: Install nfs-utils for mount
  yum:
    name: nfs-utils
    state: latest
- name: Start httpd
  service: 
    name: httpd 
    state: started 
    enabled: true
```



#### roles/apache/templates/apache.conf.j2
* jinja2(j2): 서버 구성에 필요한 파일을 템플릿으로 작성하여 타겟서버에 복사
* web 서버의 apache 설정 파일을 템플릿
```
Listen {{ ansible_eth1.ipv4.address }}:{{ apache['port'] }}

Include conf.modules.d/*.conf

User apache
Group apache

ServerAdmin root@localhost

<Directory />
    AllowOverride none
    Require all denied
</Directory>

DocumentRoot "/var/www/html"

<Directory "/var/www">
    AllowOverride None
    # Allow open access:
    Require all granted
</Directory>

<Directory "/var/www/html">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>

<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>

<Files ".ht*">
    Require all denied
</Files>

ErrorLog "logs/error_log"

LogLevel warn

<IfModule log_config_module>
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common

    <IfModule logio_module>
      # You need to enable mod_logio.c to use %I and %O
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
    </IfModule>
    CustomLog "logs/access_log" combined
</IfModule>

<IfModule alias_module>
    ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"
</IfModule>

<Directory "/var/www/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>

<IfModule mime_module>
    TypesConfig /etc/mime.types
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    AddType text/html .shtml
    AddOutputFilter INCLUDES .shtml
</IfModule>

AddDefaultCharset UTF-8

<IfModule mime_magic_module>
    MIMEMagicFile conf/magic
</IfModule>

EnableSendfile on

IncludeOptional conf.d/*.conf
```


#### roles/apache/vars/main.yaml
* selinux 서비스를 통제하기 위한 변수를 지정
```
---
sebool_httpd_lists:
  - httpd_can_network_connect
  - httpd_can_network_connect_db
  - httpd_use_nfs
```



#### roles/common/tasks/main.yml

```
---
- block:                                  # task를 block 단위로 묶어서 조건절(when)에 부합해야 해당 block 실행
  - name: Install epel-release
    yum: 
      name: epel-release 
      state: latest
  - name: Install libsemanage-python for seboolean
    yum: 
      name: libsemanage-python 
      state: latest
  when: ansible_distribution == 'CentOS'          # OS가 'centos'일 경우 해당 블록 실행

- block:
  - name: Update apt cache
    apt:                                          # ubuntu apt 활성화
      update_cache: yes
  when: ansible_distribution == 'Ubuntu'          # OS가 'ubuntu'일 경우 해당 블록 실행
```


#### roles/haproxy/handlers/main.yml
```
---
- name: Restart haproxy service
  service:
    name: haproxy
    state: restarted
```


#### roles/haproxy/tasks/main.yml
* 조건절(when)을 사용하여 해당 OS에 맞게 haproxy 
```
---
- name: Deploy to CentOS
  block:
  - name: Install haproxy
    yum:
      name: haproxy
      state: latest
  - name: Open http port                                                # http Port 방화벽 오픈
    firewalld: 
      port: "{{ haproxy['frontend']['port'] }}/tcp" 
      permanent: yes 
      state: enabled                                                    # 서버가 부팅되더라도 서비스 자동 실행
      immediate: yes                                                    # 즉시 반영
  - name: Active seboolean for httpd                                    # selinux httpd 서비스 제어 Off 
    seboolean: 
      name: haproxy_connect_any
      state: yes 
      persistent: yes
  - name: Set facts for haproxy public ip
    set_fact:
      haproxy_public_ip: "{{ ansible_eth0.ipv4.address }}"              # haproxy 서비스 외부 주소 지정
  - name: Delegate collecting facts for wordpress1
    setup:
    delegate_to: node2
  - name: Set facts for wordpress1 private ip
    set_fact:
      wordpress1_private_ip: "{{ ansible_eth1.ipv4.address }}"
  - name: Delegate collecting facts for wordpress2
    setup:
    delegate_to: node3
  - name: Set facts for wordpress2 private ip
    set_fact:
      wordpress2_private_ip: "{{ ansible_eth1.ipv4.address }}"
  - name: Copy haproxy configuration
    template:
      src: centos/haproxy.cfg.j2
      dest: /etc/haproxy/haproxy.cfg
    notify:
    - Restart haproxy service
  when: ansible_distribution == "CentOS"                               # 조건절(when)을 이용하여 타겟 서버가 centos일 경우 해당 block을 실행

- name: Deploy to Ubuntu
  block:
  - name: Install haproxy
    apt:
      name: haproxy
      state: latest
      update_cache: yes
  - name: Set facts for haproxy public ip
    set_fact:
      haproxy_public_ip: "{{ ansible_ens3.ipv4.address }}"
  - name: Delegate collecting facts for wordpress1
    setup:
    delegate_to: node2
  - name: Set facts for wordpress1 private ip
    set_fact:
      wordpress1_private_ip: "{{ ansible_eth1.ipv4.address }}"
  - name: Delegate collecting facts for wordpress2
    setup:
    delegate_to: node3
  - name: Set facts for wordpress2 private ip
    set_fact:
      wordpress2_private_ip: "{{ ansible_eth1.ipv4.address }}"
  - name: Copy haproxy configuration
    template:
      src: ubuntu/haproxy.cfg.j2
      dest: /etc/haproxy/haproxy.cfg
    notify:
    - Restart haproxy service  
  when: ansible_distribution == "Ubuntu"                               # 조건절(when)을 이용하여 타겟 서버가 Ubuntu일 경우 해당 block을 실행

- name: Start haproxy service                                          
  service:
    name: haproxy
    enabled: true
    state: started
```


#### roles/haproxy/templates/centos/haproxy.cfg.j2
* centos haproxy 서버에서 사용될 haproxy  
```
global
    log         127.0.0.1 local2

    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon
    stats socket /var/lib/haproxy/stats
defaults
    mode                    http
    log                     global
    option                  httplog
    option                  dontlognull
    option http-server-close
    option forwardfor       except 127.0.0.0/8
    option                  redispatch
    retries                 3
    timeout http-request    10s
    timeout queue           1m
    timeout connect         10s
    timeout client          1m
    timeout server          1m
    timeout http-keep-alive 10s
    timeout check           10s
    maxconn                 3000

frontend  main {{ haproxy_public_ip }}:{{ haproxy['frontend']['port'] }}                         # httpd port 지정
    acl url_static       path_beg       -i /static /images /javascript /stylesheets
    acl url_static       path_end       -i .jpg .gif .png .css .js

    #use_backend static          if url_static
    default_backend              {{ haproxy['backend']['name'] }}

backend static
    balance     roundrobin
    server      static 127.0.0.1:4331 check

backend {{ haproxy['backend']['name'] }}
    balance     {{ haproxy['backend']['balance_type'] }}
    server  web1 {{ wordpress1_private_ip }}:{{ haproxy['backend']['wordpress1']['port'] }} check         # web1 서버 주소
    server  web2 {{ wordpress2_private_ip }}:{{ haproxy['backend']['wordpress2']['port'] }} check         # web2 서버 주소
```


#### roles/haproxy/templates/ubuntu/haproxy.cfg.j2
* ubuntu haproxy 서버에서 사용될 haproxy  
```
global
        log /dev/log    local0
        log /dev/log    local1 notice
        chroot /var/lib/haproxy
        stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners
        stats timeout 30s
        user haproxy
        group haproxy
        daemon

        # Default SSL material locations
        ca-base /etc/ssl/certs
        crt-base /etc/ssl/private

        # Default ciphers to use on SSL-enabled listening sockets.
        # For more information, see ciphers(1SSL). This list is from:
        #  https://hynek.me/articles/hardening-your-web-servers-ssl-ciphers/
        # An alternative list with additional directives can be obtained from
        #  https://mozilla.github.io/server-side-tls/ssl-config-generator/?server=haproxy
        ssl-default-bind-ciphers ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:RSA+AESGCM:RSA+AES:!aNULL:!MD5:!DSS
        ssl-default-bind-options no-sslv3

defaults
        log     global
        mode    http
        option  httplog
        option  dontlognull
        timeout connect 5000
        timeout client  50000
        timeout server  50000
        errorfile 400 /etc/haproxy/errors/400.http
        errorfile 403 /etc/haproxy/errors/403.http
        errorfile 408 /etc/haproxy/errors/408.http
        errorfile 500 /etc/haproxy/errors/500.http
        errorfile 502 /etc/haproxy/errors/502.http
        errorfile 503 /etc/haproxy/errors/503.http
        errorfile 504 /etc/haproxy/errors/504.http

frontend  main {{ haproxy_public_ip }}:{{ haproxy['frontend']['port'] }}                              # httpd port 지정
    acl url_static       path_beg       -i /static /images /javascript /stylesheets
    acl url_static       path_end       -i .jpg .gif .png .css .js

    #use_backend static          if url_static
    default_backend              {{ haproxy['backend']['name'] }}

backend {{ haproxy['backend']['name'] }}
    balance     {{ haproxy['backend']['balance_type'] }}
    server  web1 {{ wordpress1_private_ip }}:{{ haproxy['backend']['wordpress1']['port'] }} check        # web1 서버 주소
    server  web2 {{ wordpress2_private_ip }}:{{ haproxy['backend']['wordpress2']['port'] }} check        # web2 서버 주소
```


#### roles/nfs/handlers/main.yml
```
---
- name: Re-export all directories
  command: exportfs -ar
```


#### roles/nfs/tasks/main.yml
```
---
- name: Install nfs-utils
  yum:
    name: nfs-utils
    state: latest
- name: Create a directory for nfs exports
  file:
    path: "{{ nfs['exports']['directory'] }}"
    state: directory
    mode: '0775'
- block:
  - name: Create a new primary partition for LVM
    parted:
      device: "{{ nfs['block']['device'] }}"
      number: 1
      flags: [ lvm ]
      state: present
      part_start: 5GiB
  - name: Create a filesystem
    filesystem:
      fstype: "{{ nfs['block']['fs_type'] }}"
      dev: "{{ nfs['block']['device'] }}1"
  - name: mount /dev/vdb1 on /wordpress
    mount:
      path: "{{ nfs['exports']['directory'] }}"
      src: "{{ nfs['block']['device'] }}1"
      fstype: "{{ nfs['block']['fs_type'] }}"
      state: mounted
  when: nfs['block']['device'] is defined
- name: Create exports to webserver
  template:
    src: exports.j2
    dest: /etc/exports
  notify:
  - Re-export all directories
- name: Set wordpress url
  set_fact:
    wp_url: "https://ko.wordpress.org/wordpress-{{ wordpress['source']['version'] }}-{{ wordpress['source']['language'] }}.tar.gz"
    wp_filename: "wordpress-{{ wordpress['source']['version'] }}-{{ wordpress['source']['language'] }}.tar.gz"
- name: Download wordpress sources
  get_url: 
    url: "{{ wp_url }}"
    dest: "/tmp/{{ wp_filename }}"
- name: Unarchive wordpress archive
  unarchive: 
    src: "/tmp/{{ wp_filename }}"
    dest: "{{ nfs['exports']['directory'] }}"
    remote_src: yes 
    owner: root 
    group: root
- name: Copy wp-config.php
  template:
    src: wp-config.php.j2
    dest: "{{ nfs['exports']['directory'] }}/wordpress/wp-config.php"
- name: Start nfs service
  service:
    name: nfs
    enabled: true
    state: started
- name: Allow port for nfs, rpc-bind, mountd
  firewalld:
    service: "{{ item }}"
    permanent: yes
    state: enabled
    immediate: yes
  with_items: "{{ firewall_nfs_lists }}"
```


#### roles/nfs/templates/exports.j2
```
{{ nfs['exports']['directory'] }} {{ nfs['exports']['subnet'] }}({{ nfs['exports']['options'] }})
```


#### roles/nfs/templates/wp-config.php.j2
```
<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the
 * installation. You don't have to use the web site, you can
 * copy this file to "wp-config.php" and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * MySQL settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/support/article/editing-wp-config-php/
 *
 * @package WordPress
 */

// ** MySQL settings - You can get this info from your web host ** //
/** The name of the database for WordPress */
define( 'DB_NAME', '{{ wordpress['db']['name'] }}' );

/** MySQL database username */
define( 'DB_USER', '{{ wordpress['db']['username'] }}' );

/** MySQL database password */
define( 'DB_PASSWORD', '{{ wordpress['db']['password'] }}' );

/** MySQL hostname */
define( 'DB_HOST', '{{ wordpress['db']['host'] }}' );

/** Database Charset to use in creating database tables. */
define( 'DB_CHARSET', 'utf8' );

/** The Database Collate type. Don't change this if in doubt. */
define( 'DB_COLLATE', '' );

/**#@+
 * Authentication Unique Keys and Salts.
 *
 * Change these to different unique phrases!
 * You can generate these using the {@link https://api.wordpress.org/secret-key/1.1/salt/ WordPress.org secret-key service}
 * You can change these at any point in time to invalidate all existing cookies. This will force all users to have to log in again.
 *
 * @since 2.6.0
 */
define( 'AUTH_KEY',         'put your unique phrase here' );
define( 'SECURE_AUTH_KEY',  'put your unique phrase here' );
define( 'LOGGED_IN_KEY',    'put your unique phrase here' );
define( 'NONCE_KEY',        'put your unique phrase here' );
define( 'AUTH_SALT',        'put your unique phrase here' );
define( 'SECURE_AUTH_SALT', 'put your unique phrase here' );
define( 'LOGGED_IN_SALT',   'put your unique phrase here' );
define( 'NONCE_SALT',       'put your unique phrase here' );

/**#@-*/

/**
 * WordPress Database Table prefix.
 *
 * You can have multiple installations in one database if you give each
 * a unique prefix. Only numbers, letters, and underscores please!
 */
$table_prefix = 'wp_';

/**
 * For developers: WordPress debugging mode.
 *
 * Change this to true to enable the display of notices during development.
 * It is strongly recommended that plugin and theme developers use WP_DEBUG
 * in their development environments.
 *
 * For information on other constants that can be used for debugging,
 * visit the documentation.
 *
 * @link https://wordpress.org/support/article/debugging-in-wordpress/
 */
define( 'WP_DEBUG', false );

/* That's all, stop editing! Happy publishing. */

/** Absolute path to the WordPress directory. */
if ( ! defined( 'ABSPATH' ) ) {
	define( 'ABSPATH', __DIR__ . '/' );
}

/** Sets up WordPress vars and included files. */
require_once ABSPATH . 'wp-settings.php';
```


#### roles/nfs/vars/main.yaml
```
---
firewall_nfs_lists:
  - nfs
  - rpc-bind
  - mountd
```








```
[mysqld]
binlog_format=ROW
default-storage-engine=innodb
innodb_autoinc_lock_mode=2
bind-address={{ db1_ip }}
[galera]
wsrep_on=1
wsrep_provider=/usr/lib64/galera-4/libgalera_smm.so
wsrep_cluster_name="wp_wsrep_cluster"
wsrep_cluster_address="gcomm://{{ db1_ip }},{{ db2_ip }}"
wsrep_node_name={{ hostname }}
wsrep_node_address={{ db1_ip }}
wsrep_sst_method=rsync
- hosts: wp-db
  become: yes
  tasks:
  - name: Add yum_repository for mariadb
    yum_repository:
      name: MariaDB
      baseurl: http://mirror.yongbok.net/mariadb/yum/10.4/centos7-amd64
      gpgkey: http://mirror.yongbok.net/mariadb/yum/RPM-GPG-KEY-MariaDB
      gpgcheck: 1
      description: MariaDB
  - name:
    yum:
      name: MariaDB
      state: present
  - name: start mariadb service
    service:
      name: mariadb
      state: started
- hosts: db1
  tasks:
  - setup:
    delegate_to: db1
  - set_fact:
      db1_ip: "{{ ansible_eth1.ipv4.address }}"
      hostname: "{{ ansible_hostname }}"
  - setup:
    delegate_to: db2
  - set_fact:
      db2_ip: "{{ ansible_eth1.ipv4.address }}"
  - template:
      src: galera.cnf.j2
      dest: /etc/my.cnf.d/galera.cnf
- hosts: db2
  tasks:
  - setup:
    delegate_to: db1
  - set_fact:
      db1_ip: "{{ ansible_eth1.ipv4.address }}"
  - setup:
    delegate_to: db2
  - set_fact:
      db2_ip: "{{ ansible_eth1.ipv4.address }}"
      hostname2: "{{ absible_hostname }}"
  - template:
      src: galera_db2.cnf.j2
      dest: /etc/my.cnf.d/galera.cnf
- hosts: wp-db
  tasks:
  - name: Allow port for mountd
    firewalld:
      port: "{{ item }}"
      permanent: yes
      state: enabled
      immediate: yes
    with_items: "{{firewall_port}}"
  - name:
    yum:
      name: policycoreutils-python
      state: installed
  - name:
    seport:
      ports: "{{ item }}"
      proto: tcp
      setype: mysqld_port_t
      state: present
    with_items: "{{ mysql_port }}"
  - name:
    seport:
      ports: 4567
      proto: udp
      setype: mysqld_port_t
      state: present
  - name: stop mariadb service
    service:
      name: mariadb
      state: stopped
  - name:
    command: semanage permissive -a mysqld_t
  vars:
    firewall_port:
    - 3306/tcp
    - 4444/tcp
    - 4567/tcp
    - 4568/tcp
    - 4567/udp
    mysql_port:
    - 4567
    - 4568
    - 4444
- hosts: db1
  become: yes
  tasks:
  - name:
    command: galera_new_cluster
- hosts: db2
  tasks:
  - name: start mariadb service db2
    service:
      name: mariadb
      state: started
```







