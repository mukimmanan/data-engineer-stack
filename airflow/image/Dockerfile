FROM apache/airflow:3.1.3

# Switch to root to install OS-level build dependencies required by some
# packages (for example: sasl, thrift-sasl, cryptography, etc.). Then
# switch back to the airflow user to keep file ownership consistent.
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY image/requirements.txt /tmp/requirements.txt
COPY config/airflow.cfg /opt/airflow/config/airflow.cfg

# Upgrade packaging tools first (helps building wheels) then install
# Python requirements. Keep --no-cache-dir to reduce image size.
USER airflow

RUN pip install --upgrade pip setuptools wheel \
	&& pip install --no-cache-dir "apache-airflow==3.1.3" -r /tmp/requirements.txt


ENTRYPOINT [ "airflow" ]