# Ansible 활용

## 목차

### 1. 플레이북 기본

### 2. Become(권한 상승)

### 3. 변수

### 4. 포함(Include)

### 5. 템플릿

### 6. 조건문

### 7. 반복문

### 8. 블록

---

### 1. 플레이북 기본

#### 플레이북이란

```플레이북```은 구성 관리와 멀티 머신 배포 시스템을 단순하게 구성할 수 있는 기반이며, 복잡한 응용 프로그램을 배포하는데 매우 적합하다.


```플레이북 언어```는 yaml을 사용하며 프로그래밍 언어 또는 스크립트가 아닌 구성 또는 프로세스 모델을 시도하는 최소한의 구문을 사용한다.


```호스트와 그룹``` 플레이북에서 플레이 할 때마다 인프라에서 대상으로 지정할 머신과 작업을 수행하는 원격 사용자를 선택할 수 있다.


```핸들러```는 변화에 대한 대응할 수 있는 기본 이벤트 시스템이다. ```notify``` 액션은 플레이에서 각 작업 블록이 끝날 때 시작되며, 여러 작업으로부터 알림을 받아도 한 번만 트리거 된다.



* 플레이북 예시
```
---
- hosts: webservers
  vars:
    http_port: 80
    max_clients: 200
  remote_user: root
  tasks:
  - name: ensure apache is at the latest version
    yum: name=httpd state=latest
  - name: write the apache config file
    template: src=/srv/httpd.j2 dest=/etc/httpd.conf
    notify:
    - restart apache
  - name: ensure apache is running (and enable it at boot)
    service: name=httpd state=started enabled=yes
  handlers:
  - name: restart apache
    service: name=httpd state=restarted    
```


* 플레이북 실행
> f 옵션: fork로 한 번에 처리 될 host 개수를 정함 
```
# ansible-playbook playbook.yml -f 10
```



### 2. Become(권한 상승)


#### 권한 상승


```Ansible```을 사용하면 시스템에 로그인한 사용자(원격 사용자)와 다른 사용자로 작업을 수행할 수 있습니다. ```sudo, su, pfexec, doas, pbrun, dzdo, ksu``` 등과 같은 기존 권한 상승 도구를 사용하여 수행된다.


* 지시자


```become``` 권한 상승을 활성화하기 위해 ```true``` 또는 ```yes```로 설정


```become_user``` 권한을 상승해서 되고자 하는 사용자를 지정


```become_method``` 플레이 또는 작업 레벨에서 ```ansible.cfg```에서의 설정을 덮어씀


```become_flags``` 플레이 또는 작업 레벨에서 작업 또는 역할을 위한 지정된 플래그 사용을 허락


* become 예시
```
- name: Ensure the httpd service is running
  service:
    name: httpd
    state: started
  become: true
```


### 3. 변수


```변수 이름```은 문자, 숫자 및 밑줄로 이루어지며 숫자로 시작하거나 숫자로만 이루어질 수 없다.


```등록된 변수``` 변수의 주요 사용은 명령을 실행하고 그 명령의 결과를 사용하여 결과를 변수에 저장하는 것이가. 결과는 모듈마다 다르며 플레이북을 실행할 때 -v 옵션을 사용하면 결과에 값이 표시된다.


* Register(등록변수) 예시
```
- host: web_servers
  tasks:
  - shell: /usr/bin/foo
    register: foo_result
    ignore_errors: True
  - shell: /usr/bin/bar
    when: foo_result.rc == 5
```


```변수 파일``` 변수를 비공개로 유지하면서 플레이북 소스를 공개할 수 있는 방법으로 특정 정보를 메인 플레이북과 다른 파일에 보관할 수 있다.


* 변수파일 예시
```
---
- host: web_servers
  remote_user: root
  vars:
    favcolor: blue
  vars_files:
  - /vars/external_vars.yml
  tasks:
  - name: this is just a placeholder
    command: /bin/echo foo
```







