FROM python:3.9-slim
COPY . /opt/zemnir
WORKDIR /opt/zemnir/
RUN pip install -r /opt/zemnir/requirements.txt
CMD ["bash","-c","/opt/zemnir/run_gunicorn.sh"]