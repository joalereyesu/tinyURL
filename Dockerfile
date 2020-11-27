FROM python:3-alpine

COPY requierments.txt /tmp/

RUN pip install -r /tmp/requierments.txt

WORKDIR /app/

COPY . ./

CMD ["python", "app.py"]

EXPOSE 5000