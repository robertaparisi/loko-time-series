FROM python:3.10-slim
ARG user
ARG password
ADD ./requirements.lock /
RUN pip install --upgrade --extra-index-url https://piplivetech:pip2018@distribution.livetech.site -r /requirements.lock
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/ds4biz_time_series/services
CMD python services.py
