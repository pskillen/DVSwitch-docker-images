"""
Unit tests for DVSwitch configuration
"""
import pytest
import json
from pathlib import Path

class TestConfigurationValidation:
    """Test configuration file generation and validation"""
    
    def test_analog_reflector_config_structure(self):
        """Test Analog_Reflector configuration file structure"""
        config_path = Path("docker/analog_reflector/Analog_Reflector.json.j2")
        assert config_path.exists(), "Analog_Reflector template not found"
        
        # Read template content
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Check for required sections
        assert '"general"' in content, "Missing general section"
        assert '"network"' in content, "Missing network section"
        assert '"usrp"' in content, "Missing usrp section"
        
        # Check for required fields
        assert '"mobilePort"' in content, "Missing mobilePort field"
        assert '"peerHost"' in content, "Missing peerHost field"
        assert '"peerPort"' in content, "Missing peerPort field"
    
    def test_analog_bridge_config_structure(self):
        """Test Analog_Bridge configuration file structure"""
        config_path = Path("docker/analog_bridge/Analog_Bridge.ini.j2")
        assert config_path.exists(), "Analog_Bridge template not found"
        
        # Read template content
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Check for required sections
        assert '[GENERAL]' in content, "Missing GENERAL section"
        assert '[USRP]' in content, "Missing USRP section"
        assert '[AMBE_AUDIO]' in content, "Missing AMBE_AUDIO section"
        
        # Check for required fields
        assert 'gatewayDmrId' in content, "Missing gatewayDmrId field"
        assert 'repeaterID' in content, "Missing repeaterID field"
    
    def test_mmdvm_bridge_config_structure(self):
        """Test MMDVM_Bridge configuration file structure"""
        config_path = Path("docker/mmdvm_bridge/mmdvm_bridge.ini.j2")
        assert config_path.exists(), "MMDVM_Bridge template not found"
        
        # Read template content
        with open(config_path, 'r') as f:
            content = f.read()
        
        # Check for required sections
        assert '[General]' in content, "Missing General section"
        assert '[DMR Network]' in content, "Missing DMR Network section"
        assert '[USRP]' in content, "Missing USRP section"
        
        # Check for required fields
        assert 'Callsign' in content, "Missing Callsign field"
        assert 'Id' in content, "Missing Id field"
        assert 'Address' in content, "Missing Address field"
    
    def test_environment_file_structure(self):
        """Test environment file structure and required variables"""
        env_files = [
            "compose/env/common.env.example",
            "compose/env/analog_bridge.env.example",
            "compose/env/analog_reflector.env.example",
            "compose/env/mmdvm_bridge.env.example"
        ]
        
        for env_file in env_files:
            env_path = Path(env_file)
            assert env_path.exists(), f"Environment file not found: {env_file}"
            
            # Read content
            with open(env_path, 'r') as f:
                content = f.read()
            
            # Check for required variables based on file type
            if "common" in env_file:
                assert 'MY_CALLSIGN' in content, f"Missing MY_CALLSIGN in {env_file}"
                assert 'MY_DMR_ID' in content, f"Missing MY_DMR_ID in {env_file}"
                assert 'MY_ESSID' in content, f"Missing MY_ESSID in {env_file}"
            
            elif "analog_bridge" in env_file:
                assert 'USRP_RX_PORT' in content, f"Missing USRP_RX_PORT in {env_file}"
                assert 'USRP_TX_PORT' in content, f"Missing USRP_TX_PORT in {env_file}"
                assert 'AMBE_RX_PORT' in content, f"Missing AMBE_RX_PORT in {env_file}"
                assert 'AMBE_TX_PORT' in content, f"Missing AMBE_TX_PORT in {env_file}"
            
            elif "analog_reflector" in env_file:
                assert 'MOBILE_PORT' in content, f"Missing MOBILE_PORT in {env_file}"
                assert 'USRP_PEER_HOST' in content, f"Missing USRP_PEER_HOST in {env_file}"
                assert 'USRP_PEER_PORT' in content, f"Missing USRP_PEER_PORT in {env_file}"
            
            elif "mmdvm_bridge" in env_file:
                assert 'AMBE_PEER_HOST' in content, f"Missing AMBE_PEER_HOST in {env_file}"
                assert 'AMBE_RX_PORT' in content, f"Missing AMBE_RX_PORT in {env_file}"
                assert 'AMBE_TX_PORT' in content, f"Missing AMBE_TX_PORT in {env_file}"
    
    def test_docker_compose_structure(self):
        """Test Docker Compose file structure"""
        compose_files = [
            "compose/docker-compose.local.yaml",
            "compose/docker-compose.ci.yaml"
        ]
        
        for compose_file in compose_files:
            compose_path = Path(compose_file)
            assert compose_path.exists(), f"Docker Compose file not found: {compose_file}"
            
            # Read content
            with open(compose_path, 'r') as f:
                content = f.read()
            
            # Check for required services
            assert 'mmdvm_bridge:' in content, f"Missing mmdvm_bridge service in {compose_file}"
            assert 'analog_bridge:' in content, f"Missing analog_bridge service in {compose_file}"
            assert 'analog_reflector:' in content, f"Missing analog_reflector service in {compose_file}"
            
            # Check for required sections
            assert 'networks:' in content, f"Missing networks section in {compose_file}"
            assert 'healthcheck:' in content, f"Missing healthcheck section in {compose_file}"
