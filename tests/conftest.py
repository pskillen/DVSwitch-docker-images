"""
Pytest configuration for DVSwitch tests
"""
import os
import pytest
import subprocess
import time
from pathlib import Path

# Test configuration (override with env for local runs)
TEST_TIMEOUT = int(os.getenv("DVS_TEST_TIMEOUT", "300"))
HEALTH_CHECK_INTERVAL = int(os.getenv("DVS_HEALTHCHECK_INTERVAL", "5"))
HEALTH_CHECK_RETRIES = int(os.getenv("DVS_HEALTHCHECK_RETRIES", "60"))

@pytest.fixture(scope="session")
def docker_compose_file():
    """Path to docker-compose file for testing"""
    return Path(__file__).parent.parent / "compose" / "docker-compose.ci.yaml"

@pytest.fixture(scope="session")
def test_environment(docker_compose_file):
    """Assumes stack is already managed externally. Only wait for healthy services."""
    print("\n🔎 Verifying DVSwitch stack health (pytest will not start/stop containers)...")

    # Wait for services to be healthy
    for attempt in range(HEALTH_CHECK_RETRIES):
        result = subprocess.run([
            "docker", "compose", "-f", str(docker_compose_file), "ps"
        ], capture_output=True, text=True)

        if result.returncode == 0 and "unhealthy" not in result.stdout and "starting" not in result.stdout:
            print("✅ Services are healthy (or no healthchecks defined).")
            break

        if attempt < HEALTH_CHECK_RETRIES - 1:
            time.sleep(HEALTH_CHECK_INTERVAL)
        else:
            print(result.stdout)
            pytest.fail("Services did not become healthy in time")

    yield
    # No cleanup here; lifecycle managed by scripts/CI

@pytest.fixture
def service_ports():
    """Port configuration for services"""
    return {
        "analog_reflector_mobile": 12345,
        "analog_reflector_usrp": 12346,
        "analog_bridge_usrp_rx": 32001,
        "analog_bridge_usrp_tx": 32002,
        "analog_bridge_ambe_rx": 32003,
        "analog_bridge_ambe_tx": 32004,
        "analog_bridge_pcm": 2222
    }

@pytest.fixture
def service_hosts():
    """Host configuration for services"""
    return {
        "analog_reflector": "localhost",
        "analog_bridge": "localhost",
        "mmdvm_bridge": "localhost"
    }
