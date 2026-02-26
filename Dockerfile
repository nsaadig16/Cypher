FROM astral/uv:python3.12-alpine

WORKDIR /app

ADD uv.lock uv.lock
ADD pyproject.toml pyproject.toml
ADD .python-version .python-version

RUN uv sync --no-install-project

COPY . .
RUN uv sync

CMD [ "uv", "run", "python", "-m", "cypher.main" ]