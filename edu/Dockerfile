FROM python:3.12

WORKDIR /code
ENV HF_HOME=/data/.huggingface

COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

COPY . /code
CMD ["python", "server.py"]