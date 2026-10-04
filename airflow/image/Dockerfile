FROM apache/airflow:3.3.2

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

COPY ./requirements.txt /tmp/requirements.txt

# (Note: We do NOT COPY airflow.cfg here because it is mounted at runtime via docker-compose.yaml)

# Upgrade packaging tools first (helps building wheels) then install
# Python requirements. Keep --no-cache-dir to reduce image size.
USER airflow

RUN pip install --upgrade pip setuptools wheel \
	&& pip install --no-cache-dir -r /tmp/requirements.txt
