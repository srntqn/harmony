FROM python:3.8
WORKDIR /app
COPY harmony/ ./harmony
COPY pyproject.toml ./
RUN adduser --disabled-password --gecos "" harmony && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    chown -R harmony:harmony /app
USER harmony
RUN mkdir ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENTRYPOINT ["python", "-u", "harmony/main.py"]