FROM python:3.8 as builder
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

FROM python:3.8
COPY --from=builder /app /app
WORKDIR /app
COPY harmony/ ./harmony
RUN adduser --disabled-password --gecos "" harmony && \
    chown -R harmony:harmony /app
USER harmony
ENTRYPOINT ["python", "-m", "harmony", "run"]