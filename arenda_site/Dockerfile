FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV AWS_ACCESS_KEY_ID abc123!
ENV AWS_SECRET_ACCESS_KEY 123abc!
WORKDIR /usr/src/
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*
# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here


# install environment dependencies
RUN pip3 install --upgrade pip 


# Install project dependencies
COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

# copy project to working dir
COPY . /usr/src/
RUN python manage.py collectstatic --noinput

# run gunicorn
CMD gunicorn arenda_site.wsgi:application --bind 0.0.0.0:$PORT