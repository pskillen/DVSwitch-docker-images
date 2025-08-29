FROM debian:bookworm-slim

LABEL org.opencontainers.image.source="https://github.com/${GITHUB_REPOSITORY}" \
      org.opencontainers.image.title="DVSwitch MMDVM_Bridge" \
      org.opencontainers.image.description="MMDVM_Bridge packaged for Docker with env-driven config" \
      org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive \
    MMDVM_BRIDGE_VERSION=latest \
    TZ=UTC

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       ca-certificates \
       bash \
       curl \
       git \
       build-essential \
       cmake \
       pkg-config \
       libssl-dev \
       libasound2-dev \
       libconfig++-dev \
       libjsoncpp-dev \
       iproute2 \
       procps \
       python3 \
       python3-jinja2 \
    && rm -rf /var/lib/apt/lists/*

# Install MMDVM_Bridge from pre-built binaries
WORKDIR /tmp/build
RUN git clone --depth 1 https://github.com/DVSwitch/MMDVM_Bridge.git \
    && cd MMDVM_Bridge/bin \
    && install -m 0755 MMDVM_Bridge.amd64 /usr/local/bin/MMDVM_Bridge \
    && cd / \
    && rm -rf /tmp/build

# Non-root user
RUN useradd -r -u 1000 -g nogroup -d /var/lib/dvswitch -s /usr/sbin/nologin dvswitch \
    && mkdir -p /var/lib/dvswitch /etc/dvswitch /config \
    && chown -R dvswitch:nogroup /var/lib/dvswitch /etc/dvswitch /config

# Copy entrypoint and template
# Note: Build context is pinned as the dir containing the Dockerfile. Do not change.
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
COPY mmdvm_bridge.ini.j2 /usr/share/dvswitch/mmdvm_bridge.ini.j2
RUN chmod +x /usr/local/bin/entrypoint.sh

USER dvswitch
WORKDIR /var/lib/dvswitch

# Healthcheck: ensure process is running
HEALTHCHECK --interval=15s --timeout=5s --retries=20 CMD pgrep -x MMDVM_Bridge >/dev/null || exit 1

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/usr/local/bin/MMDVM_Bridge", "/etc/dvswitch/mmdvm_bridge.ini"]

