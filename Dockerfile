FROM ubuntu

RUN apt update
RUN apt install python3 python3-pip -y

COPY . /sneaker-sales-parser

RUN pip3 install -r /sneaker-sales-parser/requirements.txt

CMD python3 /sneaker-sales-parser/main.py