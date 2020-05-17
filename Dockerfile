FROM python:3.7.2-alpine


RUN pip install --upgrade pip

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

# Get Input from environment variables
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_ROUTE53_HZ_ARN=""
ENV AWS_ROUTE53_RECORDS=""
ENV AWS_ROUTE53_TTL="120"
ENV LOOP_TIME="120"
ENV DEBUG="False"

CMD python code/main.py