FROM /python:3.6
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt -i http://pypi.douban.com/simple --trusted-host pypi.douban.com

EXPOSE 80
COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8099", "--reload"]
