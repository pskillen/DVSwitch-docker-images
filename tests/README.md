# DVSwitch Testing Framework

This directory contains the comprehensive testing framework for the DVSwitch stack, including unit tests, integration tests, and CI/CD integration.

## 🏗️ Test Structure

```
tests/
├── conftest.py                 # Pytest configuration and fixtures
├── unit/                       # Unit tests (fast, no containers)
│   └── test_configuration.py   # Configuration validation tests
├── integration/                # Integration tests (full stack)
│   └── test_dvswitch_stack.py # End-to-end stack tests
└── README.md                   # This file
```

## 🧪 Test Types

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components without external dependencies
- **Speed**: Fast execution (< 1 second)
- **Scope**: Configuration validation, file structure, template syntax
- **Dependencies**: None (pure Python)

### Integration Tests (`tests/integration/`)
- **Purpose**: Test the complete DVSwitch stack end-to-end
- **Speed**: Slower execution (2-5 minutes)
- **Scope**: Container health, network connectivity, service communication
- **Dependencies**: Docker, Docker Compose, full stack running

## 🚀 Running Tests

### Prerequisites
- Python 3.11+
- Docker and Docker Compose
- `netcat` (for port testing)

### Quick Start
```bash
# Run all tests (recommended for first time)
./scripts/run-tests.sh

# Or run manually:
pip install -r requirements-test.txt
./compose/env/setup-env.sh
pytest tests/ -v
```

### Individual Test Suites
```bash
# Unit tests only (fast)
pytest tests/unit/ -v

# Integration tests only (requires running stack)
pytest tests/integration/ -v

# Specific test file
pytest tests/integration/test_dvswitch_stack.py -v

# Specific test method
pytest tests/integration/test_dvswitch_stack.py::TestDVSwitchStack::test_container_health -v
```

### Test Options
```bash
# Run with detailed output
pytest tests/ -v --tb=long

# Run with timeout (default: 300s)
pytest tests/ --timeout=600

# Generate HTML reports
pytest tests/ --html=test-results/report.html --self-contained-html

# Run tests in parallel (unit tests only)
pytest tests/unit/ -n auto
```

## 🔧 Test Configuration

### Pytest Configuration (`pytest.ini`)
- **Timeout**: 300 seconds for integration tests
- **HTML Reports**: Generated in `test-results/`
- **Markers**: `@pytest.mark.integration`, `@pytest.mark.unit`, `@pytest.mark.slow`
- **Warnings**: Deprecation warnings suppressed

### Test Fixtures (`conftest.py`)
- **`test_environment`**: Session-scoped fixture that starts/stops the full stack
- **`service_ports`**: Port configuration for all services
- **`service_hosts`**: Host configuration for testing
- **`docker_client`**: Docker client for container management

## 📊 Test Results

### Local Execution
- **HTML Reports**: `test-results/unit-report.html`, `test-results/integration-report.html`
- **Console Output**: Detailed test results with emojis and status indicators
- **Exit Codes**: 0 for success, 1 for failure

### CI/CD Integration
- **Artifacts**: Test results uploaded to GitHub Actions
- **Test Reporter**: Dorny test reporter shows results in PRs
- **Failure Handling**: Detailed logs and container state on failure

## 🐳 Integration Test Details

### Test Environment Setup
1. **Environment Files**: Automatically generated from examples
2. **Container Startup**: All services built and started
3. **Health Checks**: Waits for all containers to be healthy
4. **Network Setup**: Docker network with proper service discovery

### Test Coverage
- **Container Health**: All services must be healthy
- **Port Accessibility**: TCP/UDP ports must be accessible
- **Service Communication**: Inter-service connectivity verified
- **Configuration Generation**: Jinja2 templates properly rendered
- **Performance**: Basic throughput and concurrency testing

### Test Data
- **Simulated Mobile App**: UDP packets sent to test connectivity
- **Network Testing**: Port scanning and connectivity verification
- **Configuration Validation**: JSON/INI structure verification

## 🚨 Troubleshooting

### Common Issues
1. **Port Conflicts**: Ensure ports 12345, 32001-32004 are available
2. **Docker Permissions**: Run with appropriate Docker permissions
3. **Python Environment**: Use virtual environment for dependencies
4. **Service Health**: Check container logs if health checks fail

### Debug Mode
```bash
# Run with maximum verbosity
pytest tests/ -vvv --tb=long

# Show container logs
docker compose -f compose/docker-compose.ci.yaml logs

# Check container status
docker compose -f compose/docker-compose.ci.yaml ps
```

### Test Isolation
- Each test run starts with a clean environment
- Containers are automatically cleaned up after tests
- Environment files are regenerated for each run

## 🔄 CI/CD Integration

### Pull Request Workflow
- **Trigger**: On every PR
- **Actions**: Build, test, report results
- **Artifacts**: Test results and reports
- **Test Reporter**: Results shown in PR comments

### Main Branch Workflow
- **Trigger**: On push to main
- **Actions**: Build, test, push images
- **Images**: Tagged as `:dev`
- **Test Results**: Uploaded as artifacts

### Release Workflow
- **Trigger**: On release publication
- **Actions**: Build, test, push images
- **Images**: Tagged with version and `:latest`
- **Quality Gate**: Tests must pass before release

## 📈 Performance Metrics

### Test Execution Times
- **Unit Tests**: < 1 second total
- **Integration Tests**: 2-5 minutes total
- **Container Startup**: 1-2 minutes
- **Health Checks**: 15-30 seconds

### Resource Usage
- **Memory**: ~2GB total for all containers
- **CPU**: Moderate usage during tests
- **Disk**: Minimal (containers are ephemeral)
- **Network**: Local Docker network only

## 🤝 Contributing

### Adding New Tests
1. **Unit Tests**: Add to `tests/unit/` for configuration/validation
2. **Integration Tests**: Add to `tests/integration/` for end-to-end testing
3. **Fixtures**: Add to `conftest.py` if shared across tests
4. **Documentation**: Update this README for new test types

### Test Guidelines
- **Naming**: Use descriptive test names (`test_analog_reflector_mobile_port`)
- **Assertions**: Use specific assertions with helpful error messages
- **Cleanup**: Ensure proper cleanup in `finally` blocks
- **Timeouts**: Use appropriate timeouts for network operations

### Test Data
- **Realistic Values**: Use realistic DMR IDs, callsigns, ports
- **Edge Cases**: Test boundary conditions and error scenarios
- **Performance**: Include basic performance and stress tests
