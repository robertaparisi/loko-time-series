FROM node:16.15.0 AS builder
ADD ./frontend/package.json /frontend/package.json
WORKDIR /frontend
RUN yarn install
ADD ./frontend /frontend
RUN yarn build --base="/routes/ds4biz-time-series/web/"

FROM python:3.10-slim
ARG user
ARG password
EXPOSE 8080
ADD ./requirements.lock /
RUN pip install --upgrade --extra-index-url https://piplivetech:pip2018@distribution.livetech.site -r /requirements.lock
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
COPY --from=builder /frontend/dist /frontend/dist
WORKDIR /plugin/ds4biz_time_series/services
CMD python services.py
