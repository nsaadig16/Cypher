FROM astral/uv:python3.12-alpine

ADD uv.lock uv.lock
ADD pyproject.toml pyproject.toml
ADD .python-version .python-version

RUN ["uv", "sync"]

COPY . .

CMD [ "uv", "run", "main.py" ]