# 🚀 Selenium-PyTest-Framework

A production-ready, enterprise-grade test automation framework built with Selenium WebDriver and Pytest. This framework implements industry best practices including Page Object Model, parallel execution, Docker containerization, and CI/CD integration.

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![Selenium](https://img.shields.io/badge/selenium-4.x-green)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/pytest-7.x-orange)](https://pytest.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Running Tests](#-running-tests)
- [Parallel Execution](#-parallel-execution)
- [Docker Support](#-docker-support)
- [CI/CD Integration](#-cicd-integration)
- [Reporting](#-reporting)
- [Project Structure](#-project-structure)
- [Best Practices](#-best-practices)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- **🎯 Page Object Model (POM)** - Clean separation of test logic and page elements
- **⚡ Parallel Execution** - Run tests concurrently using pytest-xdist
- **🐳 Docker Support** - Fully containerized execution environment
- **🔄 CI/CD Ready** - Pre-configured GitHub Actions workflows
- **📊 Rich Reporting** - Allure and HTML reports with screenshots
- **🔧 Flexible Configuration** - Multi-environment support (dev, staging, prod)
- **📸 Auto Screenshots** - Captures screenshots on test failures
- **📝 Detailed Logging** - Comprehensive execution logs
- **🎲 Data-Driven Testing** - JSON-based test data management
- **🔍 Custom Waits** - Smart waiting strategies for better stability
- **🌐 Cross-Browser Support** - Chrome, Firefox, Edge, Safari
- **📦 Reusable Components** - Modular utilities and helpers

---

## 🏗️ Architecture

This framework follows the **Page Object Model (POM)** design pattern with clear separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│                   Test Layer                        │
│  (test_*.py - Business logic & assertions)          │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│                   Page Layer                        │
│  (page objects - Element locators & actions)        │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│                   Core Layer                        │
│  (base classes, browser factory, utilities)         │
└─────────────────┬───────────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────────┐
│               Selenium WebDriver                    │
└─────────────────────────────────────────────────────┘
```

---

## 📦 Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)
- **Chrome/Firefox/Edge** browser installed
- **Docker** (optional, for containerized execution)
- **Git**

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourprofile/selenium-pytest-framework.git
cd selenium-pytest-framework
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download WebDriver (Automatic)

Selenium 4.x includes WebDriver Manager, so drivers are downloaded automatically.

---

## ⚙️ Configuration

### Environment Configuration

Edit `config/environments.json` to add your test environments:

```json
{
  "dev": {
    "base_url": "https://dev.example.com",
    "timeout": 10
  },
  "staging": {
    "base_url": "https://staging.example.com",
    "timeout": 15
  },
  "prod": {
    "base_url": "https://example.com",
    "timeout": 20
  }
}
```

### Pytest Configuration

Modify `pytest.ini` for custom settings:

```ini
[pytest]
markers =
    smoke: Quick smoke tests
    regression: Full regression suite
    critical: Critical path tests
```

---

## 💻 Usage

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run tests with specific marker
pytest -m smoke

# Run with verbose output
pytest -v
```

### Running with Different Browsers

```bash
# Chrome (default)
pytest --browser=chrome

# Firefox
pytest --browser=firefox

# Edge
pytest --browser=edge

# Headless mode
pytest --browser=chrome --headless
```

### Running with Different Environments

```bash
pytest --env=dev
pytest --env=staging
pytest --env=prod
```

---

## ⚡ Parallel Execution

Run tests in parallel using pytest-xdist:

```bash
# Run with 4 parallel workers
pytest -n 4

# Run with auto-detection of CPU cores
pytest -n auto

# Parallel execution with specific markers
pytest -n 4 -m regression
```

---

## 🐳 Docker Support

### Build Docker Image

```bash
docker build -t selenium-pytest-framework -f docker/Dockerfile .
```

### Run Tests in Docker

```bash
# Run all tests
docker-compose -f docker/docker-compose.yml up

# Run specific tests
docker run --rm selenium-pytest-framework pytest tests/test_login.py

# Run with parallel execution
docker run --rm selenium-pytest-framework pytest -n 4
```

### Docker Compose for Multiple Browsers

```bash
docker-compose -f docker/docker-compose.yml up --scale chrome=2 --scale firefox=2
```

---

## 🔄 CI/CD Integration

### GitHub Actions

This framework includes pre-configured GitHub Actions workflows:

- **`.github/workflows/ci.yml`** - Runs on every push/PR
- **`.github/workflows/docker-build.yml`** - Builds and pushes Docker images

### Jenkins Integration

```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'pytest -n auto --alluredir=reports/allure'
            }
        }
        stage('Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'reports/allure']]
            }
        }
    }
}
```

---

## 📊 Reporting

### HTML Reports

```bash
pytest --html=reports/report.html --self-contained-html
```

### Allure Reports

```bash
# Generate Allure results
pytest --alluredir=reports/allure

# Serve Allure report
allure serve reports/allure
```

### Screenshot on Failure

Screenshots are automatically captured on test failures and saved to `screenshots/` directory.

---

## 📁 Project Structure

```
selenium-pytest-framework/
│
├── config/              # Configuration files
├── core/                # Core framework components
├── pages/               # Page Object classes
├── tests/               # Test cases
├── utils/               # Utility functions
├── test_data/           # Test data files
├── reports/             # Generated reports
├── screenshots/         # Failure screenshots
├── docker/              # Docker configuration
└── docs/                # Documentation
```

---

## 🎯 Best Practices

1. **Follow POM Pattern** - Keep page logic separate from test logic
2. **Use Meaningful Names** - Clear, descriptive names for tests and methods
3. **DRY Principle** - Avoid code duplication, use utilities
4. **Independent Tests** - Each test should run independently
5. **Use Fixtures** - Leverage pytest fixtures for setup/teardown
6. **Add Waits** - Use explicit waits instead of sleep()
7. **Log Everything** - Comprehensive logging for debugging
8. **Tag Your Tests** - Use markers for test categorization

---

## 📚 Example Test

```python
import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.smoke
def test_successful_login(driver):
    """Verify user can login with valid credentials"""
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)
    
    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    
    assert dashboard_page.is_displayed()
    assert dashboard_page.get_welcome_message() == "Welcome, standard_user"
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📞 Contact

**Your Name** - [your.email@example.com](mailto:your.email@example.com)

**Project Link:** [https://github.com/yourprofile/selenium-pytest-framework](https://github.com/yourprofile/selenium-pytest-framework)

---

## 🙏 Acknowledgments

- [Selenium](https://www.selenium.dev/) - Web automation framework
- [Pytest](https://pytest.org/) - Testing framework
- [Allure](https://docs.qameta.io/allure/) - Reporting framework
- [Docker](https://www.docker.com/) - Containerization platform

---

## 📈 Roadmap

- [ ] Add support for mobile testing (Appium)
- [ ] Integrate with BrowserStack/Sauce Labs
- [ ] Add visual regression testing
- [ ] API testing integration
- [ ] Performance testing hooks
- [ ] Add more example tests and page objects

---

**⭐ If you find this framework useful, please consider giving it a star!**