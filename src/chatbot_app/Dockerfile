FROM python:3.11-slim

WORKDIR /workdir

COPY requirements.txt /temp/requirements.txt
RUN pip install --no-cache-dir -r /temp/requirements.txt

COPY . /workdir

RUN ["chmod", "+x", "/workdir/entrypoint.sh"]
CMD ["./workdir/entrypoint.sh"]

