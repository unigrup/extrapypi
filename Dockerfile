FROM python:3.8.7

# Set working directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Update
RUN echo nameserver 8.8.8.8 > /etc/resolv.conf && apt-get -y update && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN echo nameserver 8.8.8.8 > /etc/resolv.conf && pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN echo nameserver 8.8.8.8 > /etc/resolv.conf && pip install -r requirements.txt

# Install uwsgi
RUN echo nameserver 8.8.8.8 > /etc/resolv.conf && pip install uwsgi

# Add project files
ADD . /usr/src/app

# Environment variables
ENV PYTHONPATH .
ENV EXTRAPYPI_CONFIG config.cfg

# Start project
CMD ["uwsgi", "--http", "0.0.0.0:80", "--module", "extrapypi.wsgi:app"]