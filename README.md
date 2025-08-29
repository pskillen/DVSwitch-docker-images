DVSwitch Server (MB/AB/AR) — Dockerized

Dockerized server-side DVSwitch stack with MMDVM_Bridge, Analog_Bridge, and Analog_Reflector. Includes Dockerfiles, local compose for testing, and GitHub Actions CI/CD to GHCR.

### Quickstart (local)

1. Copy example envs and edit as needed:
   - `cp compose/env/*.example compose/env/`
   - Edit `compose/env/*.env` for your local values (keep placeholders for CI).
2. Build and start:
   - `docker compose -f compose/docker-compose.local.yml up -d --build`
3. Point DVSwitch Mobile to AR:
   - Host: `tcp://localhost:12345`

### Architecture

```
DVSwitch Mobile ⇄ (TCP) Analog_Reflector ⇄ (USRP/PCM) Analog_Bridge ⇄ (AMBE) MMDVM_Bridge ⇄ BrandMeister
```

### Notes

- No real credentials are included. Provide your own `.env` files outside git.
- Defaults are local-only; only `Analog_Reflector` publishes `mobilePort` to host.
- CI does not require live BrandMeister; MB supports a dummy start mode.
