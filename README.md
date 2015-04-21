# memtube
Запоминаем просмотренные видео на youtube


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
