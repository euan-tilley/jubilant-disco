FROM mcr.microsoft.com/vscode/devcontainers/python:3.11
ENV EDITOR=vim

RUN apt-get update && export DEBIAN_FR ONTEND=noninteractive && \
    apt-get install -y vim gnupg2 && \
    pip install boto3

COPY ./.devcontainer/aws-profile.py /root/aws-profile.py

RUN echo "alias staging='eval \$(~/aws-profile.py staging)'" >> ~/.bashrc