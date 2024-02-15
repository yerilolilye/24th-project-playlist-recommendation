FROM ubuntu:20.04
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
CMD ["/bin/bash"]