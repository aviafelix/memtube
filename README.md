# memtube

Запоминаем просмотренные видео на youtube
Подробнее здесь:

http://habrahabr.ru/post/255549/

### Демо-версия
Чтобы смотреть видео на ютюбе с разных устройств и быть не привязанным к локальному компу, я выложил flask-сайт в онлайн:

http://memtube.com

И смотрю все оттуда. 
У кого есть желание, пожалуйста, присоединяйтесь. На сайте в любой момент можно скачать Excel файл с историей просмотров:

![alt text](http://habrastorage.org/files/6b9/b45/11b/6b9b4511ba284656b7ce3b381967d990.png "Logo Title Text 1")

#### P.S.

Это сингл-юзер версия приложения. Данные о пользователе, так же как и Youtube
API key задаются в файле settings.conf. Например:
```
[Main]
api_key = s0me-1etters-and-nUmbers
username = your_user_name
password = your_password
```

#### Запоминаем просмотренные видео на youtube

Процесс обновления:

  /etc/init.d/memtube stop

  cd /home/memtube/
  
  cp video.db /home/video.db
  
  cp .htpasswd /home/.htpasswd
  
  cd /home/
  
  rm -r memtube
  
  git clone https://github.com/cema93/memtube
  
  cp video.db /home/memtube/video.db
  
  cp .htpasswd /home/memtube/.htpasswd
  
  rm video.db
  
  /etc/init.d/memtube start
