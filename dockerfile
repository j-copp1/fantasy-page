FROM python:3

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

EXPOSE 5000

COPY . .

ENTRYPOINT [ "python" ]

CMD ["./driver.py"]