#!/bin/sh
set -eu

CONFIG_DIR="/etc/dvswitch"
CONFIG_FILE="${CONFIG_DIR}/Analog_Reflector.json"
SAMPLE_FILE="/usr/share/dvswitch/Analog_Reflector.sample.json"

if [ ! -f "${CONFIG_FILE}" ]; then
  mkdir -p "${CONFIG_DIR}"
  if [ -f "/config/Analog_Reflector.json" ]; then
    cp "/config/Analog_Reflector.json" "${CONFIG_FILE}"
  else
    [ -f "${SAMPLE_FILE}" ] && cp "${SAMPLE_FILE}" "${CONFIG_FILE}" || true
    MOBILE_PORT_VAL=${MOBILE_PORT:-12345}
    USRP_HOST_VAL=${USRP_PEER_HOST:-analog_bridge}
    USRP_PORT_VAL=${USRP_PEER_PORT:-32001}
    CLIENT_TOKEN_VAL=${CLIENT_TOKEN:-}
    cat > "${CONFIG_FILE}" <<EOF
{
  "general": {
    "logLevel": 1
  },
  "network": {
    "mobilePort": ${MOBILE_PORT_VAL},
    "clientToken": "${CLIENT_TOKEN_VAL}"
  },
  "usrp": {
    "peerHost": "${USRP_HOST_VAL}",
    "peerPort": ${USRP_PORT_VAL}
  }
}
EOF
  fi
fi

echo "Using config: ${CONFIG_FILE}"
exec "$@"

