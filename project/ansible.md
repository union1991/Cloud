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
```핸들러```는 변화에 대한 동작을 실행


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




