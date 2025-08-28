#!/bin/sh
set -eu

CONFIG_DIR="/etc/dvswitch"
CONFIG_FILE="${CONFIG_DIR}/mmdvm_bridge.ini"
SAMPLE_FILE="/usr/share/dvswitch/mmdvm_bridge.sample.ini"

# Allow mounted config to override
if [ ! -f "${CONFIG_FILE}" ]; then
  mkdir -p "${CONFIG_DIR}"
  if [ -f "/config/mmdvm_bridge.ini" ]; then
    cp "/config/mmdvm_bridge.ini" "${CONFIG_FILE}"
  else
    # Render a minimal config from env or sample
    if [ -f "${SAMPLE_FILE}" ]; then
      cp "${SAMPLE_FILE}" "${CONFIG_FILE}"
    fi
    {
      echo "[General]"
      echo "Daemon=0"
      echo "RptProtocol=USRP"
      echo "Callsign=${CALLSIGN:-NOCALL}"
      echo "Id=${DMR_ID:-0000000}${ESSID:-00}"
      echo "Timeout=180"
      echo "
[DMR Network]"
      echo "Enable=1"
      echo "Address=${MASTER_HOST:-master.example.org}"
      echo "Port=${MASTER_PORT:-62031}"
      echo "Password=${BM_PASSWORD:-passw0rd}"
      echo "Slot=2"
      echo "TG=${TALKGROUP:-91}"
      echo "Options=StartRef=4000;RelinkTime=30;Userlink=1;TS2_1=91;TS2_2=9"
    } > "${CONFIG_FILE}"
  fi
fi

echo "Using config: ${CONFIG_FILE}"
if [ "${DUMMY_MODE:-false}" = "true" ]; then
  echo "DUMMY_MODE enabled: skipping network connectivity checks."
fi

exec "$@"

