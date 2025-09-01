# DVSwitch Port Configuration

This document describes the port configuration and network topology for the DVSwitch services.

## Network Topology

```
┌─────────────────┐    USRP     ┌─────────────────┐    AMBE     ┌─────────────────┐
│ Analog_Reflector│◄───────────►│  Analog_Bridge  │◄───────────►│  MMDVM_Bridge   │
│                 │  32001/32002│                 │  32003/32004│                 │
└─────────────────┘             └─────────────────┘             └─────────────────┘
         │                                │
         │                                │
         │ Mobile App                     │ PCM
         │ Port 12345                     │ Port 2222
         ▼                                ▼
```

## Port Configuration

### Analog_Reflector ↔ Analog_Bridge (USRP Protocol)
- **Analog_Reflector** listens on port `12345` (mobile app)
- **Analog_Reflector** connects to **Analog_Bridge** on port `32001` (USRP_RX_PORT)
- **Analog_Bridge** sends to **Analog_Reflector** on port `32002` (USRP_TX_PORT)

### Analog_Bridge ↔ MMDVM_Bridge (AMBE Protocol)
- **Analog_Bridge** sends to **MMDVM_Bridge** on port `32004` (AMBE_TX_PORT)
- **Analog_Bridge** listens from **MMDVM_Bridge** on port `32003` (AMBE_RX_PORT)
- **MMDVM_Bridge** connects to **Analog_Bridge** on port `32003` (Analog_Bridge AMBE_RX_PORT)

### External Ports
- **Analog_Reflector**: Port `12345` (exposed to host for mobile app)
- **Analog_Bridge**: Port `2222` (PCM audio, internal only)

## Environment Variables

### Common Variables (common.env)
- `MY_DMR_ID`: 7-digit DMR ID (e.g., `1234567`)
- `MY_ESSID`: 2-digit ESSID (e.g., `01`)

### Analog_Bridge Variables (analog_bridge.env)
- `GATEWAY_DMR_ID`: Calculated as `{{ MY_DMR_ID }}{{ MY_ESSID }}` (e.g., `123456701`)
- `REPEATER_ID`: Calculated as `{{ MY_DMR_ID }}{{ MY_ESSID }}` (e.g., `123456701`)
- `USRP_RX_PORT`: `32001` (receives from Analog_Reflector)
- `USRP_TX_PORT`: `32002` (sends to Analog_Reflector)
- `AMBE_RX_PORT`: `32003` (receives from MMDVM_Bridge)
- `AMBE_TX_PORT`: `32004` (sends to MMDVM_Bridge)
- `AMBE_PEER_HOST`: `mmdvm_bridge` (Docker service name)

### Analog_Reflector Variables (analog_reflector.env)
- `MOBILE_PORT`: `12345` (mobile app port)
- `USRP_PEER_HOST`: `analog_bridge` (Docker service name)
- `USRP_PEER_PORT`: `32001` (connects to Analog_Bridge USRP_RX_PORT)

### MMDVM_Bridge Variables (mmdvm_bridge.env)
- `AMBE_PEER_HOST`: `analog_bridge` (Docker service name)
- `AMBE_RX_PORT`: `32004` (receives from Analog_Bridge AMBE_TX_PORT)
- `AMBE_TX_PORT`: `32003` (sends to Analog_Bridge AMBE_RX_PORT)

## Health Checks

- **MMDVM_Bridge**: Checks if process is running
- **Analog_Bridge**: Checks if ports `32001` and `32002` are listening
- **Analog_Reflector**: Checks if port `12345` is listening

## Notes

1. All services communicate via Docker's internal network (`dvswitch_net`)
2. Only the Analog_Reflector mobile port (`12345`) is exposed to the host
3. Gateway and Repeater IDs are automatically calculated from `MY_DMR_ID` and `MY_ESSID`
4. Port numbers are consistent across all configuration files and templates
