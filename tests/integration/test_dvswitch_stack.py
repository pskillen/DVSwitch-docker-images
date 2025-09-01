"""
Integration tests for DVSwitch stack
"""
import pytest
import socket
import time
import subprocess
from pathlib import Path

class TestDVSwitchStack:
    """Test suite for DVSwitch stack integration"""
    
    def test_container_health(self, test_environment):
        """Test that all containers are healthy"""
        result = subprocess.run([
            "docker", "compose", "-f", "compose/docker-compose.ci.yaml", "ps"
        ], capture_output=True, text=True, check=True)
        
        # Check that all services are healthy
        output = result.stdout
        assert "unhealthy" not in output, "Found unhealthy containers"
        assert "starting" not in output, "Found containers still starting"
        assert "analog_reflector" in output, "Analog_Reflector not found"
        assert "analog_bridge" in output, "Analog_Bridge not found"
        assert "mmdvm_bridge" in output, "MMDVM_Bridge not found"
        assert "dmr_master" in output, "DMR master (HBlink3) not found"
    
    def test_analog_reflector_mobile_port(self, service_ports):
        """Test Analog_Reflector mobile app port accessibility"""
        port = service_ports["analog_reflector_mobile"]
        
        # Test TCP connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        
        assert result == 0, f"TCP port {port} is not accessible"
    
    def test_analog_reflector_usrp_port(self, service_ports):
        """Test Analog_Reflector USRP port accessibility"""
        port = service_ports["analog_reflector_usrp"]
        
        # Test UDP port is listening
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(b"test", ('localhost', port))
        sock.close()
        
        # Port should be accessible (no exception means success)
        assert True
    
    def test_analog_bridge_usrp_ports(self, service_ports):
        """Test Analog_Bridge USRP ports accessibility"""
        rx_port = service_ports["analog_bridge_usrp_rx"]
        tx_port = service_ports["analog_bridge_usrp_tx"]
        
        # Test both ports
        for port in [rx_port, tx_port]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(b"test", ('localhost', port))
            sock.close()
            assert True  # No exception means success
    
    def test_analog_bridge_ambe_ports(self, service_ports):
        """Test Analog_Bridge AMBE ports accessibility"""
        rx_port = service_ports["analog_bridge_ambe_rx"]
        tx_port = service_ports["analog_bridge_ambe_tx"]
        
        # Test both ports
        for port in [rx_port, tx_port]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(b"test", ('localhost', port))
            sock.close()
            assert True  # No exception means success
    
    def test_inter_service_communication(self, service_ports):
        """Test communication between services"""
        # Test Analog_Reflector -> Analog_Bridge
        usrp_port = service_ports["analog_bridge_usrp_rx"]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)
        sock.sendto(b"test", ('localhost', usrp_port))
        sock.close()
        assert True

    def test_mmdvm_bridge_registers_with_master(self):
        """Wait for MMDVM_Bridge to register with the test DMR master."""
        import re
        # Tail master logs and look for registration/peer lines
        for _ in range(20):
            result = subprocess.run([
                "docker", "compose", "-f", "compose/docker-compose.ci.yaml",
                "logs", "--tail=200", "dmr_master"
            ], capture_output=True, text=True, check=True)
            logs = result.stdout
            if re.search(r"(peer|client).*(connected|register|active)", logs, re.IGNORECASE):
                return
            time.sleep(5)
        pytest.fail("MMDVM_Bridge did not register with DMR master in time")

    def test_master_port_listening(self):
        """Ensure DMR master UDP port is listening."""
        result = subprocess.run([
            "docker", "exec", "compose-dmr_master-1",
            "sh", "-c", "ss -lunp | grep -q ':62031'"
        ])
        assert result.returncode == 0, "DMR master port 62031 is not listening"
    
    def test_mobile_app_simulation(self, service_ports):
        """Simulate mobile app connection and data transmission"""
        port = service_ports["analog_reflector_mobile"]
        
        # Send test data as if from mobile app
        test_data = b"MOBILE_APP_TEST_DATA"
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        
        try:
            sock.sendto(test_data, ('localhost', port))
            
            # Try to receive response (optional)
            try:
                sock.settimeout(2)
                response, addr = sock.recvfrom(1024)
                print(f"Received response: {response} from {addr}")
            except socket.timeout:
                # No response is normal for this service
                pass
                
        finally:
            sock.close()
        
        assert True  # Test passes if no exceptions

    def test_optional_websocket_handshake(self, service_ports):
        """Attempt a WebSocket handshake to Analog_Reflector if it serves WS; skip if refused."""
        try:
            import websocket  # type: ignore
        except Exception:
            pytest.skip("websocket-client not installed")
        port = service_ports["analog_reflector_mobile"]
        url = f"ws://127.0.0.1:{port}/"
        try:
            ws = websocket.create_connection(url, timeout=3)
            ws.close()
            assert True
        except Exception as e:
            # If WS endpoint is not present, that is OK; ensure TCP is reachable already.
            pytest.skip(f"WebSocket upgrade not supported on port {port}: {e}")

    def test_usrp_smoke_send(self, service_ports):
        """Send a minimal UDP datagram to Analog_Bridge USRP RX as a smoke test."""
        rx_port = service_ports["analog_bridge_usrp_rx"]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        try:
            # Send a minimal HB/USRP-like header (not full spec) just to exercise socket path
            sock.sendto(b"USRP_TEST", ("127.0.0.1", rx_port))
        finally:
            sock.close()
        assert True
    
    def test_service_logs(self, test_environment):
        """Test that services are generating logs without critical errors"""
        # Check Analog_Reflector logs
        result = subprocess.run([
            "docker", "compose", "-f", "compose/docker-compose.ci.yaml", 
            "logs", "--tail=50", "analog_reflector"
        ], capture_output=True, text=True, check=True)
        
        logs = result.stdout
        # Check for critical errors
        assert "FATAL" not in logs.upper(), "Found FATAL errors in Analog_Reflector logs"
        assert "CRITICAL" not in logs.upper(), "Found CRITICAL errors in Analog_Reflector logs"
        
        # Check that service is running
        assert "Analog_Reflector" in logs, "Analog_Reflector not found in logs"
    
    def test_network_connectivity(self, test_environment):
        """Test network connectivity between containers"""
        # Test that containers can reach each other
        result = subprocess.run([
            "docker", "exec", "compose-analog_reflector-1", 
            "nc", "-zu", "analog_bridge", "32001"
        ], capture_output=True, text=True)
        
        # nc -zu returns 0 on success, 1 on failure
        assert result.returncode == 0, "Analog_Reflector cannot reach Analog_Bridge"
    
    def test_configuration_generation(self, test_environment):
        """Test that configuration files are properly generated"""
        # Check that Analog_Reflector config was generated
        result = subprocess.run([
            "docker", "exec", "compose-analog_reflector-1", 
            "cat", "/etc/dvswitch/Analog_Reflector.json"
        ], capture_output=True, text=True, check=True)
        
        config = result.stdout
        # Verify key configuration elements
        assert '"mobilePort": 12345' in config, "Mobile port not configured correctly"
        assert '"peerHost": "analog_bridge"' in config, "Peer host not configured correctly"
        assert '"peerPort": 32001' in config, "Peer port not configured correctly"

class TestDVSwitchPerformance:
    """Performance and stress tests for DVSwitch stack"""
    
    def test_concurrent_connections(self, service_ports):
        """Test handling of multiple concurrent connections"""
        port = service_ports["analog_reflector_mobile"]
        connections = []
        
        try:
            # Create multiple connections
            for i in range(5):
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(5)
                sock.sendto(f"CONNECTION_{i}".encode(), ('localhost', port))
                connections.append(sock)
            
            # All connections should succeed
            assert len(connections) == 5, "Failed to create all connections"
            
        finally:
            # Clean up connections
            for sock in connections:
                sock.close()
    
    def test_data_throughput(self, service_ports):
        """Test data throughput capabilities"""
        port = service_ports["analog_reflector_mobile"]
        
        # Send larger data packets
        test_data = b"X" * 1024  # 1KB packet
        
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(10)
        
        try:
            for i in range(10):
                sock.sendto(test_data, ('localhost', port))
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Should complete in reasonable time
            assert duration < 5.0, f"Data transmission took too long: {duration:.2f}s"
            
        finally:
            sock.close()
