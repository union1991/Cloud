Day 00.

# <Helm 패키지 관리자를 이용한 Harbor Repository>


## 목차


## 1. 

> ### 1.1 
> ### 1.2

## 2. Helm/harvor 개요

> ### 1.1 Helm 패키지 관리자
> ### 1.2 Harvor 프라이빗 저장소
------------
 
## 2. Helm/harvor 개요

### 2.1 Helm 패키지 관리자


Helm은 Helm 차트라는 구성으로 여러 YAML 오브젝트 리소스를 하나의 패키지로 구성, 배포 및 관리를 쉽게할 수 있다.


#### Helm 설치


Helm은 Kubectl 명령과 적절한 Kubeconfig 파일이 있는 호스트에 설치해야 한다.


* 바이너리
> * 각 운영체제의 Helm 바이너리는 https://get.helm.sh/ 에서 받을 수 있음
```
# wget https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz
# tar xf helm-v3.2.4-linux-amd64.tar.gz 
# cd ./linux-amd64/
# sudo cp ./helm /usr/local/bin/
# helm version
version.BuildInfo{Version:"v3.2.4", GitCommit:"0ad800ef43d3b826f31a5ad8dfbb4fe05d143688", GitTreeState:"clean", GoVersion:"go1.13.12"}
```


#### Helm 사용


* Helm 사용 조건
> 접근 가능한 쿠버네티스 클러스터
> Helm이 설치될 시스템에 Kubectl이 설치되어 있어야 함
> Kubectl은 적절한 kubeconfig(~/.kube/config)파일로 쿠버네티스 클러스터에 접근할 수 있어야 함




### 2.2 Harbor 프라이빗 저장소


프라이빗 이미지 저장소는 기업이 사내에 구축하여 내부 또는 외부에서 사용할 수 있도록 만든 이미지 저장소이다.


#### Harbor 
> Harbor는 RBAC 기반으로 CNCF에서 관리하는 오픈소스 컨테이너 이미지 레지스트리다. 웹 인터페이스, 이미지 취약점 스캐닝, 이미지 서명, 복제 등의 기능을 제공한다. 또한 다양한 서드파티 제품들과 호환되기 때문에 편리하다.


* 사전 요구사항
> 하드웨어
|Resource|Minimum|Recommended|
|:---|:---|:---|
|CPU|2CPU|4CPU|
|Memory|4GB|8GB|
|Disk|40GB|160GB|


> 소프트웨어
|SoftWare|Version|
|:---|:---|
|Docker engine|Version 17.06.0-ce |
|Docker Compose|Version 1.18.0 이상|
|Openssl|최신버전 선호|




## 3. 프로젝트 구현


### helm 설치

```
# wget https://get.helm.sh/helm-v3.2.4-linux-amd64.tar.gz
# tar xf helm-v3.2.4-linux-amd64.tar.gz 
# cd ./linux-amd64/
# sudo cp ./helm /usr/local/bin/
# helm version
version.BuildInfo{Version:"v3.2.4", GitCommit:"0ad800ef43d3b826f31a5ad8dfbb4fe05d143688", GitTreeState:"clean", GoVersion:"go1.13.12"}
```


### harbor 설치 

```
# helm repo add harbor https://helm.goharbor.io
# helm install my-release harbor/harbor
```

 <img src="https://user-images.githubusercontent.com/56064985/89282274-416f5b00-d686-11ea-98c5-dac03c797e47.png" width="80%"></img>


https://core.harbor.domain
ID: admin
PW: Harbor12345


키 다운로드


 <img src="https://user-images.githubusercontent.com/56064985/89282281-43391e80-d686-11ea-8e94-ef3092436fc4.png" width="80%"></img>


 <img src="https://user-images.githubusercontent.com/56064985/89282289-4502e200-d686-11ea-9056-248952acc605.png" width="800%"></img>

* 유저 PC(ubuntu)에서 ca키 확인
```
student@kickseed:~/Downloads$ cat ca.crt 
-----BEGIN CERTIFICATE-----
MIIC9DCCAdygAwIBAgIQOeA1dpEcuy7xZ1SddihCujANBgkqhkiG9w0BAQsFADAU
MRIwEAYDVQQDEwloYXJib3ItY2EwHhcNMjAwODA0MDQ0ODUwWhcNMjEwODA0MDQ0
ODUwWjAUMRIwEAYDVQQDEwloYXJib3ItY2EwggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDo6RaHNadn2vUnxY459lw5ai7iniE9kIj7E/0KKSt81QUWRfg9
9VlNqFfMywUiu/2/BzHC7KO+/vsW2ee/vaW8bdZZqVe+Hn8nboEm/XvydQKZ7Yam
icJc0i8uMv5T9h/OjB0HIerMtvW9yqh/phaz6b3D06JRNZ1Ct2ZNCOvLCaEzMDXY
mgqJjZx9FzeGEkOTVc2ibCTpjh6IN2yoBQ4eJkVgOZELIDeHePwgVZtP+S7pfzkI
nrGy8eLtZsJWGpmNMlnLpQGPKLkcl2AP52cjCg9N+rKla/1tzLuc4tOw4r41t8rC
jbJ2k3NW93sg7RovHicLgeGzJHiplWBxxnpHAgMBAAGjQjBAMA4GA1UdDwEB/wQE
AwICpDAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDwYDVR0TAQH/BAUw
AwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAyKL4X/cu+tZCynuaTo1mkarj3LVnJqeT
YqUjNQ1/aCHO81DsR64E/8+v9cSTgIq38xs5pftAHDtIr8ufOJndQPee8k4TPu46
4Ah0UmN8gXiehfqqSIuNPvTJIXAdjTVHelYSYiUTfsOH4POBG4W7BLZWZ8c4Grkn
+d1uQS9Qd3XUBrNKCfj65yMYKF2BAg7RE8kgzxon4P2Sjx7VZE6lPWHqE4KliHG/
/AIsadIFyolI35Wz6/2xczT/2VpdbxJam13cAbw5osj2OLaBTHtuDWqJfNlPMKZg
Fyj14gNSWxQXJ3VSb0OByoenOwj3KoXecq4i8snZLoOcf05Ll9sTlA==
-----END CERTIFICATE-----
```

* kube-Master 및 모든 노드 ca.crt 저장
```
# mkdir -p /etc/docker/certs.d/core.harbor.domain
# vi /etc/docker/certs.d/core.harbor.domain/ca.crt
-----BEGIN CERTIFICATE-----
MIIC9DCCAdygAwIBAgIQOeA1dpEcuy7xZ1SddihCujANBgkqhkiG9w0BAQsFADAU
MRIwEAYDVQQDEwloYXJib3ItY2EwHhcNMjAwODA0MDQ0ODUwWhcNMjEwODA0MDQ0
ODUwWjAUMRIwEAYDVQQDEwloYXJib3ItY2EwggEiMA0GCSqGSIb3DQEBAQUAA4IB
DwAwggEKAoIBAQDo6RaHNadn2vUnxY459lw5ai7iniE9kIj7E/0KKSt81QUWRfg9
9VlNqFfMywUiu/2/BzHC7KO+/vsW2ee/vaW8bdZZqVe+Hn8nboEm/XvydQKZ7Yam
icJc0i8uMv5T9h/OjB0HIerMtvW9yqh/phaz6b3D06JRNZ1Ct2ZNCOvLCaEzMDXY
mgqJjZx9FzeGEkOTVc2ibCTpjh6IN2yoBQ4eJkVgOZELIDeHePwgVZtP+S7pfzkI
nrGy8eLtZsJWGpmNMlnLpQGPKLkcl2AP52cjCg9N+rKla/1tzLuc4tOw4r41t8rC
jbJ2k3NW93sg7RovHicLgeGzJHiplWBxxnpHAgMBAAGjQjBAMA4GA1UdDwEB/wQE
AwICpDAdBgNVHSUEFjAUBggrBgEFBQcDAQYIKwYBBQUHAwIwDwYDVR0TAQH/BAUw
AwEB/zANBgkqhkiG9w0BAQsFAAOCAQEAyKL4X/cu+tZCynuaTo1mkarj3LVnJqeT
YqUjNQ1/aCHO81DsR64E/8+v9cSTgIq38xs5pftAHDtIr8ufOJndQPee8k4TPu46
4Ah0UmN8gXiehfqqSIuNPvTJIXAdjTVHelYSYiUTfsOH4POBG4W7BLZWZ8c4Grkn
+d1uQS9Qd3XUBrNKCfj65yMYKF2BAg7RE8kgzxon4P2Sjx7VZE6lPWHqE4KliHG/
/AIsadIFyolI35Wz6/2xczT/2VpdbxJam13cAbw5osj2OLaBTHtuDWqJfNlPMKZg
Fyj14gNSWxQXJ3VSb0OByoenOwj3KoXecq4i8snZLoOcf05Ll9sTlA==
-----END CERTIFICATE-----

# update-ca-certificates
```


* 저장소 추가
```
# helm repo add --ca-file /etc/docker/certs.d/core.harbor.domain/ca.crt --username=admin --password=Harbor12345 myrepo https://core.harbor.domain/chartrepo/library
```




* 저장소 인증 정보용 시크릿 생성
```
# kubectl create secret docker-registry myrepo --docker-username=admin --docker-password=Harbor12345 --docker-server=https://core.harbor.domain/library

```


* 저장소 로그인
```
# sudo docker login -u admin -p Harbor12345 https://core.harbor.domain/library
```


* push 설치
```
# helm plugin install https://github.com/chartmuseum/helm-push.git
```


* 차트 push
```
# helm package myweb
# helm push myweb-0.1.0.tgz myrepo
```
