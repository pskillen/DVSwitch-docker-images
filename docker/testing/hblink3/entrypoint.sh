#!/bin/sh
# HBlink3 entrypoint for CI testing

set -e

# Substitute environment variables in config
sed -i "s/\${DMR_MASTER_PASSWORD}/${DMR_MASTER_PASSWORD}/g" /opt/hblink3/hblink.cfg

# Start HBlink3 using bridge.py (not hblink.py)
cd /opt/hblink3
exec python3 -u bridge.py -c hblink.cfg -r rules.py
