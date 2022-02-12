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

RUN groupadd -r harmony -g 433 && \
    useradd -u 431 -r -g harmony -s /sbin/nologin -c "Docker image user" harmony

COPY --chown=harmony:harmony --from=builder /app/ /app
COPY --chown=harmony:harmony --from=builder /venv/ /venv

WORKDIR /app

USER harmony
ENTRYPOINT ["/venv/bin/python", "-m", "harmony", "run"]
