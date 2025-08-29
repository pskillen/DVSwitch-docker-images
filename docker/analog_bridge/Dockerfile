FROM debian:bookworm-slim

LABEL org.opencontainers.image.title="DVSwitch Analog_Bridge" \
      org.opencontainers.image.description="Analog_Bridge packaged for Docker with env-driven config" \
      org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive TZ=UTC

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates bash curl git build-essential cmake pkg-config \
       libssl-dev libasound2-dev libconfig++-dev libjsoncpp-dev iproute2 procps \
       libsndfile1 python3 python3-jinja2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/build
RUN git clone --depth 1 https://github.com/DVSwitch/Analog_Bridge.git \
    && cd Analog_Bridge/bin \
    && install -m 0755 Analog_Bridge.amd64 /usr/local/bin/Analog_Bridge \
    && cd / \
    && rm -rf /tmp/build

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
CMD ["/usr/local/bin/Analog_Bridge", "/etc/dvswitch/Analog_Bridge.ini"]

