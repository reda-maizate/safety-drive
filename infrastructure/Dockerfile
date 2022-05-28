FROM ubuntu:latest

# Update and upgrade
RUN apt-get update -y && apt-get upgrade -y
RUN apt install wget -y && apt install curl -y
RUN apt install zip -y

# Uninstall Python 3.10
RUN apt autoremove python3 -y
RUN apt autoremove python3-pip -y

# Install Python 3.8
RUN apt update && apt upgrade -y
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update
RUN DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt-get -y install tzdata
RUN apt install python3.8 -y
RUN apt install python3.8-distutils -y

# Install pip for Python 3.8
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.8 get-pip.py

# Launch the install script
COPY utils/install.sh /install.sh
COPY src/ /src/
RUN chmod u+x /install.sh

CMD /install.sh $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_DEFAULT_REGION $AWS_BUCKET