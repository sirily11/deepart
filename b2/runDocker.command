docker run -it -v "$(pwd)/":/usr/src/app/flask/ -p 5000:5000 --name myflaskapp flaskapp
sudo docker run -it -v "$(pwd)/":/usr/src/app/flask/ -p 80:80 --name myflaskapp flaskapp
http://52.207.147.141/