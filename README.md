# data_for_Lametric
Server application for fetching data from finolog.ru and represent it for Lametric in json

How to build docker image
sudo docker build -t lametric:v1 .

How to run and daemonize container with TCP port 8123 
sudo docker run -d -p 8123:8088 lametric:v1