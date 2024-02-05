FROM python:latest
WORKDIR /app
ADD . /app
ADD main.py .
RUN pip install -r requirements.txt
CMD ["python", "./main.py"]
