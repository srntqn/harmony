FROM python:3.8
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY pyproject.toml ./
RUN adduser --disabled-password --gecos "" harmony && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev
COPY harmony/ ./harmony
RUN  chown -R harmony:harmony /app
USER harmony
ENTRYPOINT ["python", "-m", "harmony", "run"]