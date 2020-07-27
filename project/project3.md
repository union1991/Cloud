#



### 도커 이미지 다운로드
```
ps> docker login 
ps> docker pull wordpress
ps> docker pull mysql:5.6
```


---


#### pv 구현
* MySQL과 Wordpress는 각각 데이터를 저장할 퍼시스턴트볼륨이 필요하다. 퍼시스턴트볼륨클레임은 배포 단계에 생성된다. 많은 클러스터 환경에서 설치된 기본 스토리지클래스(StorageClass)가 있다. 퍼시스턴트볼륨클레임에 스토리지클래스를 지정하지 않으면 클러스터의 기본 스토리지클래스를 사용한다. 퍼시스턴트볼륨클레임이 생성되면 퍼시스턴트볼륨이 스토리지클래스 설정을 기초로 동적으로 프로비저닝된다.

* MySQL PV(Persistent Volume) 및 PVC(Persistent Volume Claim) 생성
> * MySQL PV 및 PVC Yaml 파일 생성
```
# vi mysql-pv.yaml

kind: PersistentVolume
apiVersion: v1
metadata:
  name: mysql-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
```


> * MySQL PV 및 PVC 배포
```
# kubectl create -f mysql-pv.yaml
```


* Wordpress PV(Persistent Volume) 및 PVC(Persistent Volume Claim) 생성
> * Wordpress PV 및 PVC Yaml 파일 생성
```
# vi wordpress-pv.yaml
kind: PersistentVolume
apiVersion: v1
metadata:
  name: wordpress-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 20Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data2"
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: wordpress-pv-claim
spec:
  storageClassName: manual
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 20Gi
```


> * MySQL PV 및 PVC 배포
```
# kubectl create -f wordpress-pv.yaml 
```


---


#### MySQL 구현
* MySQL Pod Yaml 생성
> * MySQL 이 설치된 Pod 를 배포하면서 Database , User, User password를 설정 
```
# vi mysql.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
        - image: mysql:5.6
          name: mysql
          env:
            - name: MYSQL_ROOT_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: mysql-password
                  key: password
            - name: MYSQL_DATABASE # 구성할 database명
              value: wordpress
            - name: MYSQL_USER # database에 권한이 있는 user
              value: wordadmin
            - name: MYSQL_ROOT_HOST # 접근 호스트
              value: '%'  
            - name: MYSQL_PASSWORD # database에 권한이 있는 user의 패스워드
              value: dkagh1.
          ports:
            - containerPort: 3306
              name: mysql
          volumeMounts:
            - name: mysql-pv-volume
              mountPath: /var/lib/mysql
      volumes:
        - name: mysql-pv-volume
          persistentVolumeClaim:
            claimName: mysql-pv-claim
```

> * MySQL Pod 배포
```
# kubectl create -f mysql.yaml
```

* MySQL Root 패스워드 저장(다른 방법)
> * mysql root 패스워드를 mysql-password라는 secret object에 저장
```
# kubectl create secret generic mysql-password --from-literal=password=dkagh1.
# kubectl describe secret mysql-password
Name:         mysql-password
Namespace:    default
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
password:  9 bytes 
```


* MySQL 서비스 생성
> * MySQL 컨테이너를 노출하여 Wordpress가 접근할 수 있도록 서비스를 생성
```
# vi mysql-service.yaml

apiVersion: v1

kind: Service
metadata:
  name: mysql
  labels:
    app: mysql
spec:
  type: ClusterIP
  ports:
    - port: 3306
  selector:
    app: mysql 
```

> * MySQL 서비스 배포
```
# kubectl create -f mysql-service.yaml
```

---


#### Wordpress 구현
* Wordpress Pod 생성
> * Wordpress Pod Yaml에는 MySQL에 접근하기 위한 정보가 포함되어 있음
> * Wordpress Yaml 생성
```
# vi wordpress.yaml

apiVersion: apps/v1

kind: Deployment
metadata:
  name: wordpress
  labels:
    app: wordpress
spec:
  replicas: 1
  selector:
    matchLabels:
      app: wordpress
  template:
    metadata:
      labels:
        app: wordpress
    spec:
      containers:
        - image: wordpress
          name: wordpress
          env:
          - name: WORDPRESS_DB_HOST
            value: mysql:3306
          - name: WORDPRESS_DB_NAME
            value: wordpress
          - name: WORDPRESS_DB_USER
            value: wordadmin
          - name: WORDPRESS_DB_PASSWORD
            value: dkagh1.
          ports:
            - containerPort: 80
              name: wordpress
          volumeMounts:
            - name: wordpress-pv-volume
              mountPath: /var/www/html
      volumes:
        - name: wordpress-pv-volume
          persistentVolumeClaim:
            claimName: wordpress-pv-claim
```


> * wordpress 배포 실행
```
# kubectl create -f wordpress.yaml
```


* Wordpress 서비스 생성
> * 외부에서 접근 가능하도록 서비스를 생성
> * Wordpress 서비스 Yaml 생성
```
# vi wordpress-service.yaml

apiVersion: v1
kind: Service
metadata:
  labels:
    app: wordpress
  name: wordpress
spec:
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      protocol: TCP
  selector:
    app: wordpress

```


> * Wordpress 서비스 배포 실행
```
# kubectl create -f wordpress-service.yaml
```

---


#### 설치 확인

* Pod 확인
```
# kubectl get po
NAME                         READY   STATUS    RESTARTS   AGE
mysql-f4c9b9f9f-j289j        1/1     Running   0          114m
wordpress-65f59d5556-44mpb   1/1     Running   0          107m
```


* Service 확인
```
# kubectl get service
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP        167m
mysql        ClusterIP   10.109.66.81   <none>        3306/TCP       128m
wordpress    NodePort    10.96.181.47   <none>        80:30449/TCP   125m
```


* Wordpress 서비스 IP 확인
```
# minikube service wordpress --url
http://192.168.99.101:30449
```





