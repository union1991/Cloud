

#### 3. web서버와 database 서버가 부팅되지 않는 경우가 발생한다.
* 1 storage 서버가 켜져있지 않은 경우, mount 정보를 읽어오지 못하여 부팅이 안된다. 따라서 storage 서버를 먼저 부팅하고 진행한다.
* 2 storage의 nfs 또는 iscsci 서비스가 켜져있지 않은 경우, mount 정보를 읽어오지 못하여 부팅이 안된다. 따라서 storage 서버의 다음 명령어를 입력한다.
```
# systemctl start nfs
# systemctl start target
```

