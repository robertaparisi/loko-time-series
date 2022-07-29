FROM python:3.6-slim
ARG user
ARG password
ADD requirements.lock /
RUN pip install --upgrade --extra-index-url https://$user:$password@distribution.livetech.site -r /requirements.lock
ADD . /ds4biz-time-series
ENV PYTHONPATH=$PYTHONPATH:/ds4biz-time-series
WORKDIR /ds4biz-time-series/ds4biz_time_series/services
CMD python services.py
