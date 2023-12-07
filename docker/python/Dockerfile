FROM python:3.10-slim
ENV PYTHONBUFFERD=1

# Install scienceplots requirements
# Install LaTeX
RUN apt-get update && apt-get install -y dvipng texlive-latex-extra texlive-luatex texlive-lang-japanese texlive-fonts-recommended cm-super
RUN apt update && apt install -y fonts-noto-cjk texlive-pictures

# Install Python requirements
RUN pip install --upgrade pip

WORKDIR /workspace/src

RUN pip install poetry
COPY pyproject.toml /workspace/
RUN poetry config virtualenvs.create false && poetry install

CMD ["bin/bash"]
