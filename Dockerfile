FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update                          && \
    apt-get install -y --no-install-recommends nano  && \
    rm -rf /var/lib/apt/lists/* \
    --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir -r requirements.txt 

COPY app.py vm.py tf.py .

EXPOSE 8080

ENV GREETING="Hello"
#ENV APP_HOST=0.0.0.0
#ENV APP_PORT=8080

CMD ["python", "app.py"]
