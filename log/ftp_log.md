docker pull fauria/vsftpd

docker run -d -p 20:20 -p 21:21 -p 21100-21110:21100-21110 -v /home/aceliuchanghong/ftpfiles:/home/vsftpd -e FTP_USER=liu -e FTP_PASS=20240113 -e PASV_ADDRESS=34.127.57.59 -e PASV_MIN_PORT=21100 -e PASV_MAX_PORT=21110 --name vsftpd --restart=always fauria/vsftpd

docker exec -i -t vsftpd bash

docker exec -i -t vsftpd bash

文件复制到自己的用户文件夹下面/home/vsftpd/${user}

ftp://34.127.57.59/
