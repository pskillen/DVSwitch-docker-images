FROM python:alpine3.18

LABEL org.opencontainers.image.title="HBlink3 (DMR Master for tests)" \
      org.opencontainers.image.description="Lightweight HBlink3 master for CI integration tests" \
      org.opencontainers.image.licenses="MIT"

ENV PYTHONUNBUFFERED=1 \
    DMR_MASTER_PORT=62031 \
    DMR_MASTER_PASSWORD=passw0rd

# Add non-root user and install dependencies
RUN adduser -D -u 54000 radio && \
    apk update && \
    apk add --no-cache git gcc musl-dev iproute2 && \
    pip install --upgrade pip && \
    pip cache purge && \
    cd /opt && \
    git clone --depth 1 https://github.com/ShaYmez/hblink3 && \
    cd /opt/hblink3 && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del git gcc musl-dev && \
    chown -R radio: /opt/hblink3

# Copy our custom config files
COPY hblink.cfg /opt/hblink3/hblink.cfg
COPY rules.py /opt/hblink3/rules.py
COPY entrypoint.sh /entrypoint

# Set ownership and permissions
RUN chown radio: /opt/hblink3/hblink.cfg /opt/hblink3/rules.py /entrypoint && \
    chmod +x /entrypoint

USER radio

EXPOSE 62031/udp

HEALTHCHECK --interval=15s --timeout=5s --retries=20 CMD sh -c "ss -lun | grep -q ":${DMR_MASTER_PORT}""

ENTRYPOINT ["/entrypoint"]
