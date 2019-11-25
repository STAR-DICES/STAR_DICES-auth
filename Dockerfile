FROM ubuntu:latest
MAINTAINER Stefano Duo <duostefano93@gmail.com>
RUN apt-get update
RUN apt-get install -y git python3.6 python3-pip
RUN git clone -q https://github.com/STAR-DICES/STAR_DICES-auth.git
WORKDIR /STAR_DICES-auth
RUN pip3 install -r requirements.txt
RUN python3 setup.py develop
ENV LANG C.UTF-8
WORKDIR /STAR_DICES-auth/auth
EXPOSE 5000
CMD ["python3", "app.py"]
