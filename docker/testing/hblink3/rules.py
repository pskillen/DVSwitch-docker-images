# Permissive rules for CI testing – allow all TGs on both timeslots
# Based on rules_SAMPLE.py from HBlink3 repository

BRIDGES = {
    'DEFAULT': [
        {'SYSTEM': 'MASTER-TEST', 'TS': 1, 'TGID': 1, 'ACTIVE': True, 'TIMEOUT': 0, 'TO_TYPE': 'NONE', 'ON': [], 'OFF': [], 'RESET': []},
        {'SYSTEM': 'MASTER-TEST', 'TS': 2, 'TGID': 1, 'ACTIVE': True, 'TIMEOUT': 0, 'TO_TYPE': 'NONE', 'ON': [], 'OFF': [], 'RESET': []},
    ]
}

# Unit-to-unit call bridging
UNIT = []

if __name__ == '__main__':
    from pprint import pprint
    pprint(BRIDGES)
    print(UNIT)
