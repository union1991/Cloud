Day 00.

# <Helm 패키지 관리자를 이용한 Harbor Repository>


## 목차


## 1. Helm 개요

> ### 1.1 
> ### 1.2

## 2. Harbor 개요

> ### 1.1 
> ### 1.2
------------
 
## 1. Helm 개요

### 1.1 Helm 패키지 관리자


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


* Helm 허브 저장소 검색
> Helm 허브에서 mysql 차트 검색하는 명령
```
# helm search hub mysql
URL                                                     CHART VERSION   APP VERSION     DESCRIPTION                                       
https://hub.helm.sh/charts/appscode/stash-mysql         8.0.14          8.0.14          stash-mysql - MySQL database backup and restore...
https://hub.helm.sh/charts/wso2/mysql-am                3.1.0-3         5.7             A Helm chart for MySQL based deployment of WSO2...
https://hub.helm.sh/charts/wso2/mysql-ob                1.4.0-1         5.7             A Helm chart for WSO2 Open Banking Datasources    
https://hub.helm.sh/charts/wso2/mysql-ei                6.6.0-1         5.7             A Helm chart for WSO2 Enterprise Integrator Dat...
https://hub.helm.sh/charts/wso2/mysql-is                5.10.0-1        5.7             A Helm chart for the deployment of WSO2 IAM dat...
https://hub.helm.sh/charts/banzaicloud-stable/m...      0.1.0           0.2.0           A Helm chart for deploying the Oracle MySQL Ope...
https://hub.helm.sh/charts/banzaicloud-stable/p...      0.2.4           v0.11.0         A Helm chart for prometheus mysql exporter with...
https://hub.helm.sh/charts/banzaicloud-stable/tidb      0.0.2                           A TiDB Helm chart for Kubernetes                  
https://hub.helm.sh/charts/choerodon/create-mys...      0.1.0           1.0             A Helm chart for Kubernetes                       
https://hub.helm.sh/charts/choerodon/mysql              0.1.4           0.1.4           mysql for Choerodon                               
https://hub.helm.sh/charts/choerodon/mysqld-exp...      0.1.0           1.0             A Helm chart for Kubernetes                       
https://hub.helm.sh/charts/choerodon/mysql-client       0.1.1           0.1.1           mysql Ver 15.1 Distrib 10.1.32-MariaDB, for Lin...
https://hub.helm.sh/charts/t3n/mysql-backup             2.0.0                                                                             
https://hub.helm.sh/charts/t3n/cloudsql-proxy           2.0.0           1.16            Google Cloud SQL Proxy                            
https://hub.helm.sh/charts/cetic/adminer                0.1.4           4.7.6           Adminer is a full-featured database management ...
...

```


> Helm repo 에서 mysql 찯트 검색하는 명령
```
# helm search repo mysql
NAME                                    CHART VERSION   APP VERSION     DESCRIPTION                                       
stable/mysql                            1.6.6           5.7.30          Fast, reliable, scalable, and easy to use open-...
stable/mysqldump                        2.6.0           2.4.1           A Helm chart to help backup MySQL databases usi...
stable/prometheus-mysql-exporter        0.7.0           v0.11.0         A Helm chart for prometheus mysql exporter with...
stable/percona                          1.2.1           5.7.26          free, fully compatible, enhanced, open source d...
stable/percona-xtradb-cluster           1.0.5           5.7.19          free, fully compatible, enhanced, open source d...
stable/phpmyadmin                       4.3.5           5.0.1           DEPRECATED phpMyAdmin is an mysql administratio...
stable/gcloud-sqlproxy                  0.6.1           1.11            DEPRECATED Google Cloud SQL Proxy                 
stable/mariadb                          7.3.14          10.3.22         DEPRECATED Fast, reliable, scalable, and easy t...
```


* Helm 차트 저장소 추가/제거
> 구글에서 제공하는 저장소 추가
```
# helm repo add stable https://kubernetes-charts.storage.googleapis.com
"stable" has been added to your repositories
# helm repo update
Hang tight while we grab the latest from your chart repositories...
...Successfully got an update from the "stable" chart repository
Update Complete. ⎈ Happy Helming!⎈ 
# helm repo list
NAME    URL                                             
stable  https://kubernetes-charts.storage.googleapis.com
```


> 저장소 제거
```
# helm repo remove stable
"stable" has been removed from your repositoies
```



* 차트 정보 확인
> stable/mysql 차트 확인
```
# helm show chart stable/mysql
apiVersion: v1
appVersion: 5.7.30
description: Fast, reliable, scalable, and easy to use open-source relational database
  system.
home: https://www.mysql.com/
icon: https://www.mysql.com/common/logos/logo-mysql-170x115.png
keywords:
- mysql
- database
- sql
maintainers:
- email: o.with@sportradar.com
  name: olemarkus
- email: viglesias@google.com
  name: viglesiasce
name: mysql
sources:
- https://github.com/kubernetes/charts
- https://github.com/docker-library/mysql
version: 1.6.6
```


> values(변수 정보 확인)
```
# helm show values stable/mysql

## mysql image version
## ref: https://hub.docker.com/r/library/mysql/tags/
##
image: "mysql"
imageTag: "5.7.30"

...

## Init container resources defaults
initContainer:
  resources:
    requests:
      memory: 10Mi
      cpu: 10m
```


* Helm 차트 기본 설치
> mydb 릴리즈 이름으로 stable 저장소의 mysql 설치
```
# helm install mydb stable/mysql
NAME: mydb
LAST DEPLOYED: Mon Aug  3 02:10:48 2020
NAMESPACE: default
STATUS: deployed
REVISION: 1
NOTES:
MySQL can be accessed via port 3306 on the following DNS name from within your cluster:
mydb-mysql.default.svc.cluster.local

To get your root password run:

    MYSQL_ROOT_PASSWORD=$(kubectl get secret --namespace default mydb-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo)

To connect to your database:

1. Run an Ubuntu pod that you can use as a client:

    kubectl run -i --tty ubuntu --image=ubuntu:16.04 --restart=Never -- bash -il

2. Install the mysql client:

    $ apt-get update && apt-get install mysql-client -y

3. Connect using the mysql cli, then provide your password:
    $ mysql -h mydb-mysql -p

To connect to your database directly from outside the K8s cluster:
    MYSQL_HOST=127.0.0.1
    MYSQL_PORT=3306

    # Execute the following command to route the connection:
    kubectl port-forward svc/mydb-mysql 3306

    mysql -h ${MYSQL_HOST} -P${MYSQL_PORT} -u root -p${MYSQL_ROOT_PASSWORD}

# kubectl get secret --namespace default mydb-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo
RkCOgXko86
```


* Helm 차트의 root 패스워드 구성 수정 및 배포
> yaml 파일을 이용한 values 옵션
```
# echo "mysqlRootPassword: P@ssw0rd" > custom.yaml
# helm install mydb-custom stable/mysql --values custom.yaml
# kubectl get secret --namespace default mydb-mysql -o jsonpath="{.data.mysql-root-password}" | base64 --decode; echo
P@ssw0rd
```


> 차트 내용 수정
```
# helm upgrade mydb-custom stable/mysql --set service.port=3306
```



## 2. Harbor 개요

### 2.1 프라이빗 이미지 저장소 개요


프라이빗 이미지 저장소는 기업이 사내에 구축하여 내부 또는 외부에서 사용할 수 있도록 만든 이미지 저장소이다.


#### Harbor 
> Harbor는 RBAC 기반으로 CNCF에서 관리하는 오픈소스 컨테이너 이미지 레지스트리다. 웹 인터페이스, 이미지 취약점 스캐닝, 이미지 서명, 복제 등의 기능을 제공한다. 또한 다양한 서드파티 제품들과 호환되기 때문에 편리하다.


* 사전 요구사항
|Resource|Minimum|Recommended|
|: |: |: |
|CPU|2CPU|4CPU|
|Memory|4GB|8GB|
|Disk|40GB|160GB|


















