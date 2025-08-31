"""
Pytest configuration for DVSwitch tests
"""
import pytest
import subprocess
import time
import docker
from pathlib import Path

# Test configuration
TEST_TIMEOUT = 300  # 5 minutes
HEALTH_CHECK_INTERVAL = 15
HEALTH_CHECK_RETRIES = 20

@pytest.fixture(scope="session")
def docker_compose_file():
    """Path to docker-compose file for testing"""
    return Path(__file__).parent.parent / "compose" / "docker-compose.ci.yaml"

@pytest.fixture(scope="session")
def docker_client():
    """Docker client for container management"""
    return docker.from_env()

@pytest.fixture(scope="session")
def test_environment():
    """Setup test environment and return cleanup function"""
    print("\n🚀 Setting up DVSwitch test environment...")
    
    # Start services
    compose_file = Path(__file__).parent.parent / "compose" / "docker-compose.ci.yaml"
    subprocess.run([
        "docker", "compose", "-f", str(compose_file), "up", "-d", "--build"
    ], check=True)
    
    # Wait for services to be healthy
    print("⏳ Waiting for services to be healthy...")
    for attempt in range(HEALTH_CHECK_RETRIES):
        result = subprocess.run([
            "docker", "compose", "-f", str(compose_file), "ps"
        ], capture_output=True, text=True, check=True)
        
        if "unhealthy" not in result.stdout and "starting" not in result.stdout:
            print("✅ All services are healthy!")
            break
        
        if attempt < HEALTH_CHECK_RETRIES - 1:
            print(f"⏳ Waiting for services... (attempt {attempt + 1}/{HEALTH_CHECK_RETRIES})")
            time.sleep(HEALTH_CHECK_INTERVAL)
        else:
            pytest.fail("Services did not become healthy in time")
    
    yield
    
    # Cleanup
    print("\n🧹 Cleaning up test environment...")
    subprocess.run([
        "docker", "compose", "-f", str(compose_file), "down", "-v"
    ], check=True)

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
