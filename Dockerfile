FROM python:alpine3.14

RUN apk add --no-cache git && \
    git clone https://github.com/dracarys18/TweetBot

WORKDIR TweetBot	
	
RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
