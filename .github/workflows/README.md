# GitHub Workflows

This directory contains the GitHub Actions workflows for the DVSwitch project. The workflows have been refactored to use reusable components for better maintainability and consistency.

## 🏗️ Workflow Structure

### **Reusable Workflows**
- **`unit-tests.yaml`**: Runs unit tests (fast, no containers)
- **`integration-tests.yaml`**: Runs integration tests (full stack testing)

### **Main Workflows**
- **`pull-request.yaml`**: Triggered on pull requests
- **`main.yaml`**: Triggered on pushes to main branch
- **`release.yaml`**: Triggered on release publication

## 🔄 Workflow Dependencies

### **Pull Request Workflow**
```
unit-tests → integration-tests → test-report
```

### **Main Workflow**
```
unit-tests → integration-tests → build-and-push
                    ↓
              test-report
```

### **Release Workflow**
```
unit-tests → integration-tests → build-and-push
                    ↓
              test-report
```

## 🧪 Test Execution Flow

### **1. Unit Tests (`unit-tests.yaml`)**
- **Purpose**: Fast configuration validation
- **Execution Time**: < 1 second
- **Dependencies**: Python, test requirements
- **Output**: Unit test results artifact

### **2. Integration Tests (`integration-tests.yaml`)**
- **Purpose**: Full stack end-to-end testing
- **Execution Time**: 2-5 minutes
- **Dependencies**: Docker, Docker Compose, unit tests
- **Output**: Integration test results artifact

### **3. Build and Push (Main/Release only)**
- **Purpose**: Build and push Docker images
- **Dependencies**: Both test suites must pass
- **Output**: Docker images tagged and pushed

### **4. Test Report**
- **Purpose**: Generate test reports and GitHub integration
- **Dependencies**: Both test suites must complete
- **Output**: Test results in PRs and releases

## 🔧 Workflow Configuration

### **Reusable Workflow Inputs**

#### **`unit-tests.yaml`**
```yaml
inputs:
  python-version:
    description: 'Python version to use for testing'
    required: false
    default: '3.11'
    type: string
```

#### **`integration-tests.yaml`**
```yaml
inputs:
  python-version:
    description: 'Python version to use for testing'
    required: false
    default: '3.11'
    type: string
  docker-compose-file:
    description: 'Docker Compose file to use'
    required: false
    default: 'compose/docker-compose.ci.yaml'
    type: string
```

### **Workflow Outputs**
```yaml
outputs:
  test-results:
    description: 'Path to test results'
    value: 'test-results/'
```

## 🚀 Benefits of Refactoring

### **1. Maintainability**
- **Single Source of Truth**: Test logic defined once in reusable workflows
- **Easy Updates**: Changes to test logic automatically apply to all workflows
- **Consistent Behavior**: All workflows use identical test execution

### **2. Performance**
- **Parallel Execution**: Unit and integration tests can run in parallel
- **Caching**: Test dependencies and results are cached between workflows
- **Efficient Resource Usage**: Tests only run when needed

### **3. Quality Assurance**
- **Mandatory Testing**: All workflows require tests to pass before proceeding
- **Consistent Coverage**: Same test suite runs across all environments
- **Early Failure Detection**: Issues caught before deployment

### **4. Developer Experience**
- **Clear Dependencies**: Workflow dependencies are explicit and visible
- **Easy Debugging**: Test failures are isolated and easy to identify
- **Fast Feedback**: Unit tests provide immediate validation

## 📊 Test Results

### **Artifacts**
- **`unit-test-results`**: Unit test results and HTML reports
- **`integration-test-results`**: Integration test results and HTML reports

### **GitHub Integration**
- **Test Reporter**: Results shown in PRs and releases
- **Status Checks**: Test status visible in GitHub UI
- **Failure Details**: Detailed logs and error information

## 🔄 Workflow Triggers

### **Pull Request**
- **Trigger**: `pull_request` event
- **Purpose**: Validate changes before merge
- **Actions**: Run tests, report results

### **Main Branch**
- **Trigger**: Push to `main` branch
- **Purpose**: Build and deploy development images
- **Actions**: Run tests, build images, push to registry

### **Release**
- **Trigger**: Release publication
- **Purpose**: Build and deploy production images
- **Actions**: Run tests, build images, push versioned tags

## 🚨 Failure Handling

### **Test Failures**
- **Unit Tests**: Build pipeline stops immediately
- **Integration Tests**: Build pipeline stops immediately
- **Test Reports**: Generated even on failure for debugging

### **Build Failures**
- **Dependencies**: Only occurs after tests pass
- **Logs**: Detailed Docker build logs available
- **Artifacts**: Test results preserved for analysis

## 🤝 Contributing

### **Adding New Tests**
1. **Unit Tests**: Add to `tests/unit/` directory
2. **Integration Tests**: Add to `tests/integration/` directory
3. **Workflow Updates**: Modify reusable workflows as needed

### **Modifying Workflows**
1. **Reusable Workflows**: Update `unit-tests.yaml` or `integration-tests.yaml`
2. **Main Workflows**: Update job dependencies and calls
3. **Testing**: Verify changes work across all workflow types

### **Best Practices**
- **Keep Tests Fast**: Unit tests should complete in < 1 second
- **Isolate Dependencies**: Tests should not depend on external services
- **Clear Naming**: Use descriptive test and workflow names
- **Documentation**: Update this README for workflow changes
