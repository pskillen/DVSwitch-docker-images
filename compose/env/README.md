# DVSwitch Environment Configuration

This directory contains environment configuration files for the DVSwitch Docker services.

## File Structure

- `common.env.example` - Shared configuration values used by all services
- `mmdvm_bridge.env.example` - MMDVM_Bridge specific configuration
- `analog_bridge.env.example` - Analog_Bridge specific configuration  
- `analog_reflector.env.example` - Analog_Reflector specific configuration

## Setup Instructions

1. **Copy the example files to create your actual configuration:**

```bash
# Copy the common configuration
cp common.env.example .env.common

# Copy service-specific configurations
cp mmdvm_bridge.env.example .env.mmdvm_bridge
cp analog_bridge.env.example .env.analog_bridge
cp analog_reflector.env.example .env.analog_reflector
```

2. **Edit `.env.common` with your actual values:**

```bash
# Essential settings to change:
MY_CALLSIGN=YOUR_CALLSIGN
MY_DMR_ID=YOUR_DMR_ID
BM_MASTER_HOST=YOUR_BM_MASTER
BM_PASSWORD=YOUR_BM_PASSWORD
```

3. **Edit service-specific files if needed:**

Most settings are inherited from the common file, but you can override them in the service-specific files if needed.

## Environment File Loading Order

The docker-compose file loads environment files in this order:

1. `.env.common` - Shared values (loaded first)
2. Service-specific file (e.g., `.env.mmdvm_bridge`) - Service-specific values (loaded second, can override common values)

## Security Notes

- **Never commit `.env.*` files to version control** (they contain sensitive information)
- Only the `.env.*.example` files should be committed
- The `.env.*` files are already in `.gitignore`

## Key Configuration Sections

### Radio Identity
- `MY_CALLSIGN` - Your amateur radio callsign
- `MY_DMR_ID` - Your 7-digit DMR ID
- `MY_ESSID` - Your 2-digit ESSID (usually 01)

### DMR Network
- `BM_MASTER_HOST` - BrandMeister master server
- `BM_MASTER_PORT` - BrandMeister port (usually 62031)
- `BM_PASSWORD` - Your BrandMeister password
- `DEFAULT_TALKGROUP` - Default talkgroup
- `DEFAULT_SLOT` - Default timeslot

### Network Ports
- `USRP_RX_PORT` / `USRP_TX_PORT` - USRP communication ports
- `AMBE_RX_PORT` / `AMBE_TX_PORT` - AMBE communication ports
- `MOBILE_PORT` - Analog_Reflector mobile app port

## Troubleshooting

If you need to override a shared value for a specific service, uncomment and modify the override section in the service-specific environment file.

For example, in `.env.mmdvm_bridge`:
```bash
# Uncomment to override the common value
# MY_CALLSIGN=DIFFERENT_CALL
```
