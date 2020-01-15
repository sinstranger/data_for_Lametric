# data_for_Lametric
Server application for fetching data from finolog.ru and represent it for Lametric in json

##### How to build docker image

```
sudo docker build -t lametric:v1 .
```

##### How to build docker image with env parameters, biz_1 is beer, biz_2 is development

``` 
docker build \
--build-arg api_key="dkv6uaV7ON2fEThB18318e4d73b5a02e35a526cc0fa39defnzLed5sqZyV775ua" \
--build-arg biz_1="28618" \
--build-arg biz_2="28615" \
 -t lametric:v1 . 
```

##### How to run and daemonize container with TCP port 8123 

```
sudo docker run -d -p 8123:8088 lametric:v1
```

