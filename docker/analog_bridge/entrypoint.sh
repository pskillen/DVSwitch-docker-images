#!/bin/sh
set -eu

CONFIG_DIR="/etc/dvswitch"
CONFIG_FILE="${CONFIG_DIR}/Analog_Bridge.ini"
SAMPLE_FILE="/usr/share/dvswitch/Analog_Bridge.sample.ini"

USRP_RX_PORT_DEFAULT=32001
USRP_TX_PORT_DEFAULT=32002

if [ ! -f "${CONFIG_FILE}" ]; then
  mkdir -p "${CONFIG_DIR}"
  if [ -f "/config/Analog_Bridge.ini" ]; then
    cp "/config/Analog_Bridge.ini" "${CONFIG_FILE}"
  else
    [ -f "${SAMPLE_FILE}" ] && cp "${SAMPLE_FILE}" "${CONFIG_FILE}" || true
    {
      echo "[GENERAL]"
      echo "logLevel=1"
      echo "
[USRP]"
      echo "bindPort=${USRP_RX_PORT:-$USRP_RX_PORT_DEFAULT}"
      echo "remotePort=${USRP_TX_PORT:-$USRP_TX_PORT_DEFAULT}"
      echo "remoteAddress=${USRP_REMOTE_HOST:-analog_reflector}"
      echo "
[AMBE]"
      echo "vocoder=${VOCODER_MODE:-SOFT}"
      echo "audioSampleRate=${AUDIO_RATE:-8000}"
    } > "${CONFIG_FILE}"
  fi
fi

echo "Using config: ${CONFIG_FILE}"
exec "$@"

