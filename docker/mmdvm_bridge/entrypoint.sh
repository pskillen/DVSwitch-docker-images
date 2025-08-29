#!/bin/sh
set -eu

CONFIG_DIR="/etc/dvswitch"
CONFIG_FILE="${CONFIG_DIR}/mmdvm_bridge.ini"
TEMPLATE_FILE="/usr/share/dvswitch/mmdvm_bridge.ini.j2"

# Generate config from template using environment variables
mkdir -p "${CONFIG_DIR}"
python3 -c "
import os
from jinja2 import Template
with open('${TEMPLATE_FILE}', 'r') as f:
    template = Template(f.read())
with open('${CONFIG_FILE}', 'w') as f:
    f.write(template.render(**os.environ))
"

echo "Using config: ${CONFIG_FILE}"
if [ "${DUMMY_MODE:-false}" = "true" ]; then
  echo "DUMMY_MODE enabled: skipping network connectivity checks."
fi

exec "$@"

