FROM python:3.7-slim

ADD . /deploy

RUN cd /deploy && \
    pip install . && \
    rm -rf /build /deploy 
CMD ["publisher"]