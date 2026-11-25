FROM jenkins/jenkins:2.541.3-lts-jdk17

USER root

# Python, para que el pipeline pueda construir y probar la app
RUN apt-get update \
 && apt-get install -y --no-install-recommends python3 python3-venv curl \
 && rm -rf /var/lib/apt/lists/*

# Dos herramientas de seguridad: bandit revisa el código, pip-audit las dependencias
RUN python3 -m venv /opt/sec \
 && /opt/sec/bin/pip install --no-cache-dir bandit==1.9.4 pip-audit==2.10.1 \
 && ln -s /opt/sec/bin/bandit /opt/sec/bin/pip-audit /usr/local/bin/

USER jenkins
