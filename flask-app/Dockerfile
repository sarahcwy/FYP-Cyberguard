FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5123:5123

ENV NAME UserTrafficGenerator

CMD ["python", "user_traffic_generator.py"]
