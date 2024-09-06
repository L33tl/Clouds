# 1
FROM ubuntu:22.04

# 2
RUN apt-get update && apt-get install nginx

# 3
COPY ./lab/static/index.html /home/lab/

# 4  & 5
COPY ./lab/requirements.txt /home/lab/requirements.txt
WORKDIR /home/lab/
RUN pip install -r requirements.txt
COPY ./lab/ /home/lab/

# 6
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# 7
FROM python:3.11
