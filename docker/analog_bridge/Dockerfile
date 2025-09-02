FROM debian:bookworm-slim

LABEL org.opencontainers.image.title="DVSwitch Analog_Bridge" \
      org.opencontainers.image.description="Analog_Bridge packaged for Docker with env-driven config" \
      org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive TZ=UTC

# Add DVSwitch apt repository and install packages
# Stub systemctl to satisfy package postinst scripts in minimal containers
RUN printf '#!/bin/sh\nexit 0\n' > /bin/systemctl \
    && chmod +x /bin/systemctl \
    && apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates bash curl gnupg \
    && curl -fsSL http://dvswitch.org/DVSwitch_Repository/dvswitch.gpg.key | gpg --dearmor -o /usr/share/keyrings/dvswitch-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/dvswitch-keyring.gpg] http://dvswitch.org/DVSwitch_Repository bookworm hamradio" > /etc/apt/sources.list.d/dvswitch.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       analog-bridge \
       libsndfile1 \
       iproute2 \
       procps \
       python3 \
       python3-jinja2 \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -r -u 1000 -g nogroup -d /var/lib/dvswitch -s /usr/sbin/nologin dvswitch \
    && mkdir -p /var/lib/dvswitch /etc/dvswitch /config \
    && chown -R dvswitch:nogroup /var/lib/dvswitch /etc/dvswitch /config

# Note: Build context is pinned as the dir containing the Dockerfile. Do not change.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY Analog_Bridge.ini.j2 /usr/share/dvswitch/Analog_Bridge.ini.j2
COPY dvsm.macro.j2 /usr/share/dvswitch/dvsm.macro.j2
RUN chmod +x /usr/local/bin/entrypoint.sh

USER dvswitch
WORKDIR /var/lib/dvswitch

EXPOSE 32001/udp 32002/udp
HEALTHCHECK --interval=15s --timeout=5s --retries=20 CMD sh -c 'ss -lunpt | grep -E ":${USRP_RX_PORT:-32001}|:${USRP_TX_PORT:-32002}" >/dev/null' || exit 1

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/opt/Analog_Bridge/Analog_Bridge", "/etc/dvswitch/Analog_Bridge.ini"]

