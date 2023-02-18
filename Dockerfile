FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN pip install flask==2.2.3

ADD src /video_server/src

RUN cd /video_server/src && \
    pip3 install -r requirements.txt

EXPOSE 80 8080

WORKDIR /video_server/src
CMD ["python3", "video_server.py"]
