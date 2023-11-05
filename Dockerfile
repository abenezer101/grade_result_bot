FROM python:3.10
RUN apt update && apt upgrade -y
RUN apt install git -y
COPY requirements.txt /requirements.txt

RUN cd /
RUN pip install -U pip && pip install -U -r requirements.txt
WORKDIR ./

COPY . .
CMD ["python", "python_version_v2.py"]
