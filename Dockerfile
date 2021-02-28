FROM python:3.8
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY harmony/ ./harmony
COPY pyproject.toml ./
RUN adduser --disabled-password --gecos "" harmony && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev && \
    chown -R harmony:harmony /app
USER harmony
ENTRYPOINT ["python", "-u", "harmony/main.py"]