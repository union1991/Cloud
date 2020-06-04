Day 14.

## 목차
 
### 8. 리눅스 핵심 운영 가이드

> #### 8.7 웹 서비스


------------
 
 
## 8. 리눅스 핵심 운영 가이드
 
 
최신 리눅스 시스템의 핵심 기술과 원리를 배우며 서버 관리자, 시스템 엔지니어, 클라우드 관리자, 개발자, DBA, 데브옵스 등 다양한 IT 관리자 및 개발자들에게 기본이 되는 기술을 습득한다.



 ------------

 
 #### 8.7 웹 서비스

* 웹 서비스 특징
> * HTTP프로토콜에 의해 내용이 전송
> * HTTP프로토콜에 의해 내용이 전송
> * http(80/tcp),https(443/tcp)
* httpd 서비스 시작
```
# yum install httpd
# systemctl enable httpd
# systemctl start httpd
# firewall-cmd --add-service=http --permanent

# firewall-cmd --reload
# /usr/share/httpd          // 에러 메시지
# cd /etc/httpd             // 서비스 파일을 가지고 있음
```

* httpd 설정 변경
```
# vi /etc/httpd/conf/httpd.conf     // 설정 변경 가능

#Listen 80
Listen 8080             // 포트 번호 변경

...

#DocumentRoot "/var/www/html"
DocumentRoot "/var/www/html2"          // Default root 디렉토리 변경

#
# Relax access to content within /var/www.
#
<Directory "/var/www">
    AllowOverride None
    # Allow open access:
    Require all granted
</Directory>

/*
<Directory "/var/www">
    AllowOverride None
    # Allow open access:
    Require all granted
</Directory>
*/


:wq!

# firewall-cmd --add-port=8080/tcp --permanent
# firewall-cmd --reload
# systemctl restart httpd
# setenforce 0


```

```


# yum install bind*
# vi /etc/named.conf

options {
        listen-on port 53 { any;  };
        listen-on-v6 port 53 {none; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        recursing-file  "/var/named/data/named.recursing";
        secroots-file   "/var/named/data/named.secroots";
        allow-query     { any; };



zone "20200604.co.kr" IN {
        type master;
        file "data/20200604.co.kr.zone";
};



:wq!

# systemctl start named


# vi ./data/20200604.co.kr.zone

 $TTL 3H
@       IN SOA  ns.20200604.co.kr root.20200604.co.kr. (
                                        0       ; serial
                                        1D      ; refresh
                                        1H      ; retry
                                        1W      ; expire
                                        3H )    ; minimum
@       IN      NS      ns.cccr.co.kr.
        IN      A       192.168.122.200
ns      IN      A       192.168.122.200
www     IN      A       192.168.122.200 
first      IN      CNAME       www
second     IN      CNAME       www

```

```
#vi /etc/httpd/conf.d/virtualhost.conf
<VirtualHost 192.168.122.200:8080>
  DocumentRoot "/var/www/html"
  ServerName  "first.20200604.co.kr"
</VirtualHost>

<VirtualHost 192.168.122.200:8080>
  DocumentRoot "/var/www/html2"
  ServerName  "second.20200604.co.kr"
</VirtualHost>

:wq!

# systemctl restart httpd
