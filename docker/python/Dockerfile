FROM python:3.10-slim
ENV PYTHONBUFFERD=1

RUN pip install --upgrade pip

WORKDIR /workspace/src

RUN pip install poetry
COPY pyproject.toml /workspace/
RUN poetry config virtualenvs.create false && poetry install

CMD ["bin/bash"]
