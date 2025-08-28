FROM debian:bookworm-slim

LABEL org.opencontainers.image.title="DVSwitch Analog_Reflector" \
      org.opencontainers.image.description="Analog_Reflector packaged for Docker with env-driven config" \
      org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive TZ=UTC

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates bash curl git build-essential cmake pkg-config \
       libssl-dev libasound2-dev libconfig++-dev libjsoncpp-dev iproute2 procps \
       netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/build
RUN git clone --depth 1 https://github.com/DVSwitch/Analog_Reflector.git \
    && cd Analog_Reflector \
    && make -j"$(nproc)" \
    && install -m 0755 Analog_Reflector /usr/local/bin/Analog_Reflector \
    && strip /usr/local/bin/Analog_Reflector || true \
    && cd / \
    && rm -rf /tmp/build

RUN useradd -r -u 1000 -g nogroup -d /var/lib/dvswitch -s /usr/sbin/nologin dvswitch \
    && mkdir -p /var/lib/dvswitch /etc/dvswitch /config \
    && chown -R dvswitch:nogroup /var/lib/dvswitch /etc/dvswitch /config

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY config/Analog_Reflector.json /usr/share/dvswitch/Analog_Reflector.sample.json
RUN chmod +x /usr/local/bin/entrypoint.sh

USER dvswitch
WORKDIR /var/lib/dvswitch

EXPOSE 12345/tcp 32001/udp 32002/udp
HEALTHCHECK --interval=15s --timeout=5s --retries=20 CMD sh -c 'nc -z localhost ${MOBILE_PORT:-12345}' || exit 1

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/usr/local/bin/Analog_Reflector", "/etc/dvswitch/Analog_Reflector.json"]

