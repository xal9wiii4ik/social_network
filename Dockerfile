FROM  python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/social_network

COPY requirements.txt /usr/src/social_network/requirements.txt
RUN pip install -r /usr/src/social_network/requirements.txt

COPY . /usr/src/social_network

EXPOSE 8000
