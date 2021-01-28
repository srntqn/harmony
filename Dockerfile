FROM  python:3.7
RUN pip install kubernetes
WORKDIR /app
COPY *.py ./
ENTRYPOINT ["python", "-u", "feeder.py", "--privateRegistry"]