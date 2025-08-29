#!/bin/sh
set -eu

CONFIG_DIR="/etc/dvswitch"
CONFIG_FILE="${CONFIG_DIR}/Analog_Bridge.ini"
MACRO_FILE="${CONFIG_DIR}/dvsm.macro"
TEMPLATE_FILE="/usr/share/dvswitch/Analog_Bridge.ini.j2"
MACRO_TEMPLATE="/usr/share/dvswitch/dvsm.macro.j2"

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

# Generate macro file from template
python3 -c "
import os
from jinja2 import Template
with open('${MACRO_TEMPLATE}', 'r') as f:
    template = Template(f.read())
with open('${MACRO_FILE}', 'w') as f:
    f.write(template.render(**os.environ))
"

echo "Using config: ${CONFIG_FILE}"
exec "$@"

