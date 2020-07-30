Day 00.

# <Kubernetes Native - Wordpress 애플리케이션 구축>


## 목차


## 1. 프로젝트 개요

> ### 1.1 목적
> ### 1.2 환경설정

## 2. 프로젝트 내용

> ### 2.1 구성도
> ### 2.2 서비스

## 3. 프로젝트 구현

> ### 3.1

## 4. FAQ

> ### 4.1
------------
 
## 1. 프로젝트 개요

### 1.1 목적


 본 과제의 목적은 쿠버네티스를 사용하여 2티어(Wordpress - DB)환경을 구성하고, 각 기능 구현에 사용되는 쿠버네티스 서비스를 활용하며 쿠버네티스에 대한 전반적인 시스템을 이해하는 것에 있다.
 
 
 ### 1.2 환경설정
 
 
 본 과제의 환경설정은 다음과 같다.
 
 
 #### [서버]
 * kube-master 서버
 * kube-node1 서버
 * kube-node2 서버
 * kube-node3 서버
 
 #### [네트워크]
 


---

## 2. 프로젝트 내용

### 2.1 구성도

### 2.2 서비스


과제에 앞서 알아야 할 서비스들의 개념을 정리한다.


#### Ingress TLS Termination
* Secret은 패스워드, 암호화 키/인증서, 토큰 등 소량의 민감한 데이터를 저장하고 안전하게 제공될 수 있도록 만들어 졌다.
> Base64로 인코딩하여 데이터를 저장
> 개별 오브젝트당 1MiB로 제한

* 시크릿 저장 데이터 종류
> generic: 키-값 형식의 임의 데이터
> docker-registry:
> tls: TLS 키 및 인증서

* TLS 키/인증서용 시크릿 생성 방법
```
# kubectl create secrets tls <NAME> --cert=cert-file --key=key-file
```


#### Service: ClusterIP
```

```
#### Deployment: Wordpress(Replica:2, Liveness, Readiness)


#### PVC: StorageClass(cephfs)


#### HPA: Deployment


#### Service: Headless


#### Statefulset: Mysql(Replica:2, Liveness, Readiness)


#### PVC: StorageClass(rbd)


#### HPA: Statefulset


#### PodAffinity 및  PodAntiAffinity (wp/db <-> wp/db)


11. (기타) ConfigMap, Secret 등...
전체 구성도 그림/설명
yaml 코드/설명
생성된 리소스 확인/설명(kubectl get/describe... po/rs/svc...)
동작 확인이 필요한 리소스 동작 확인/설명(Scale...)
Wordpress 동작 화면 (edited) 
```

---


## 3. 프로젝트 환경설정

### 3.1







---

## 4. 프로젝트 구현

### 4.1


 echo -n "admin" > id.txt
# echo -n "P@sswOrd" > pwd.txt
# kubectl create secret generic my-secret --from-file=id.txt --from-file=pwd.txt
# kubectl get secret my-secret
user-pass.yaml
# vi user-pass.yaml

apiVersion: v1
kind: Secret
metadata:
  name: user-pass-yaml
type: Opaque
data:
  username: YWRtaW4=
  password: UEBzc3dPcmQ=
# kubectl create -f mynapp-pod.yaml
# mkdir nginx-tls
# openssl genrsa -out nginx-tls/nginx-tls.key 2048
# openssl req -new -x509 -key nginx-tls/nginx-tls.key\
-out nginx-tls/nginx-tls.crt \
-days 3650 -subj /CN=mynapp.example.com
# kubectl create secret tls nginx-tls-secret \
--cert=nginx-tls/nginx-tls.crt \
--key=nginx-tls/nginx-tls.key 
# mkdir conf
# vi conf/nginx-tls.conf
server {
  listen 80;
  listen 443 ssl;
  server_name mynapp.example.com;
  ssl_certificate /etc/nginx/ssl/tls.crt;
  ssl_certificate_key /etc/nginx/ssl/tls.key;
  ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
  ssl_ciphers
  location / {
   root /usr/share/nginx/html;
   index index.html;
   }
}  

# kubectl create configmap nginx-tls-config --from-file=conf/nginx-tls.conf








---


## 5. FAQ

### 5.1


