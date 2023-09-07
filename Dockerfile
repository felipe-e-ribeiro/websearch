ARG ARCH=
FROM ${ARCH}python:3.9
COPY . /opt
workdir /opt
ENV TOKEN_ID=NULL
ENV GROUP_ID=NULL
ENV LOOKUP_WORD=NULL
ENV WEB_URLS=NULL

RUN pip3.9 install -r requirements.txt
CMD python3.9 /opt/python.py
