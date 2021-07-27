FROM python:3.8 as builder
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
COPY pyproject.toml ./
RUN python3 -m venv /venv && \
    . /venv/bin/activate && \
    pip install poetry && \
    poetry install --no-dev --no-root
COPY harmony/ ./harmony
RUN . /venv/bin/activate && \
    poetry install --no-dev

FROM python:3.8

ENV PATH="/venv/bin:${PATH}"

COPY --from=builder /app /app
COPY --from=builder /venv /venv

RUN adduser --disabled-password --gecos "" harmony && \
    mkdir /projects && \
    chown -R harmony:harmony /app /venv /projects
USER harmony
ENTRYPOINT ["/venv/bin/python", "-m", "harmony", "run"]