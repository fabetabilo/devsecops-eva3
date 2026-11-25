FROM jenkins/jenkins:2.541.3-lts-jdk17

USER root

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv curl \
 && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/sec \
 && /opt/sec/bin/pip install --no-cache-dir bandit==1.9.4 pip-audit==2.10.1 \
 && ln -s /opt/sec/bin/bandit /opt/sec/bin/pip-audit /usr/local/bin/

RUN /opt/sec/bin/pip install --no-cache-dir pipenv==2026.10.4 \
 && ln -s /opt/sec/bin/pipenv /usr/local/bin/

ARG ZAP_VERSION=2.17.0
RUN curl -sSL "https://github.com/zaproxy/zaproxy/releases/download/v${ZAP_VERSION}/ZAP_${ZAP_VERSION}_Linux.tar.gz" \
    | tar -xz -C /opt \
 && ln -s /opt/ZAP_${ZAP_VERSION}/zap.sh /usr/local/bin/zap.sh

USER jenkins
