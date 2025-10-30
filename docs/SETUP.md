# Setup Guide

Complete guide for setting up and running the Selenium PyTest Framework.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running Tests](#running-tests)
5. [Docker Setup](#docker-setup)
6. [IDE Configuration](#ide-configuration)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Web Browser** - Chrome, Firefox, or Edge
- **pip** - Python package manager (comes with Python)

### Optional Software

- **Docker** - For containerized execution
- **IDE** - PyCharm, VS Code, or any Python IDE
- **Allure** - For enhanced reporting

---

## Installation Steps

### 1. Clone Repository

```bash
git clone https://github.com/yourprofile/selenium-pytest-framework.git
cd selenium-pytest-framework
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python --version
pip list
pytest --version
```

### 5. Run Sample Test

```bash
pytest tests/test_login.py::TestLogin::test_successful_login_with_standard_user -v
```

---

## Configuration

### Environment Configuration

Edit `config/environments.json` to configure different environments:

```json
{
  "dev": {
    "base_url": "https://your-dev-url.com",
    "timeout": 10
  },
  "staging": {
    "base_url": "https://your-staging-url.com",
    "timeout": 15
  }
}
```

### Browser Configuration

Set browser via command line or environment variable:

```bash
# Command line
pytest --browser=chrome

# Environment variable
export BROWSER=firefox
pytest
```

### Headless Mode

```bash
# Command line
pytest --headless

# Environment variable
export HEADLESS=true
pytest
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_login.py

# Run specific test
pytest tests/test_login.py::TestLogin::test_successful_login_with_standard_user

# Run with markers
pytest -m smoke
pytest -m regression
pytest -m "smoke or critical"
```

### Advanced Options

```bash
# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Parallel execution
pytest -n 4
pytest -n auto

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# Multiple options combined
pytest -v -m smoke --browser=chrome --headless
```

### Running with Different Environments

```bash
pytest --env=dev
pytest --env=staging
pytest --env=prod
```

---

## Docker Setup

### Build Docker Image

```bash
docker build -t selenium-pytest-framework -f docker/Dockerfile .
```

### Run Tests in Docker

```bash
# Run all tests
docker run --rm selenium-pytest-framework

# Run specific tests
docker run --rm selenium-pytest-framework pytest tests/test_login.py

# Run with custom parameters
docker run --rm \
  -e BROWSER=firefox \
  -e ENV=staging \
  selenium-pytest-framework pytest -m smoke

# Mount reports directory
docker run --rm \
  -v $(pwd)/reports:/app/reports \
  selenium-pytest-framework
```

### Docker Compose

```bash
# Build services
docker-compose -f docker/docker-compose.yml build

# Run all services
docker-compose -f docker/docker-compose.yml up

# Run specific service
docker-compose -f docker/docker-compose.yml up selenium-chrome

# Run in background
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

---

## IDE Configuration

### PyCharm

1. **Configure Interpreter:**
   - File → Settings → Project → Python Interpreter
   - Add → Virtualenv Environment
   - Select `venv/bin/python`

2. **Configure Pytest:**
   - File → Settings → Tools → Python Integrated Tools
   - Default test runner: pytest

3. **Run Configuration:**
   - Right-click on test file → Create 'pytest in test_...'
   - Add environment variables: `BROWSER=chrome;HEADLESS=false`

### VS Code

1. **Install Extensions:**
   - Python
   - Pylance
   - Test Explorer UI
   - Python Test Explorer

2. **Configure settings.json:**
```json
{
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["-v"],
    "python.envFile": "${workspaceFolder}/.env"
}
```

3. **Create .env file:**
```
BROWSER=chrome
HEADLESS=false
ENV=dev
```

---

## Troubleshooting

### Common Issues

#### 1. WebDriver Not Found

**Solution:**
Selenium 4+ includes WebDriver Manager. If issues persist:
```bash
pip install --upgrade selenium
```

#### 2. Browser Not Opening

**Check:**
- Browser is installed
- Correct browser name in command
- Headless mode if running in CI

**Fix:**
```bash
# Try headless mode
pytest --browser=chrome --headless

# Check browser version
google-chrome --version
firefox --version
```

#### 3. Element Not Found

**Check:**
- Correct locator strategy
- Element is present on page
- Waiting strategy

**Fix:**
- Increase timeout in `config/environments.json`
- Add explicit waits in page objects

#### 4. Import Errors

**Solution:**
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 5. Permission Denied (Linux/Mac)

**Solution:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Getting Help

- Check logs in `logs/` directory
- Review screenshots in `screenshots/` directory
- Enable debug logging in pytest.ini
- Check [GitHub Issues](https://github.com/yourprofile/selenium-pytest-framework/issues)

---

## Next Steps

1. ✅ **Review Framework Architecture** - See [ARCHITECTURE.md](ARCHITECTURE.md)
2. ✅ **Learn Usage Patterns** - See [USAGE.md](USAGE.md)
3. ✅ **Write Your First Test** - Follow examples in `tests/`
4. ✅ **Explore Page Objects** - Review `pages/` directory
5. ✅ **Setup CI/CD** - Configure GitHub Actions workflow

---

**Need Help?** Open an issue on [GitHub](https://github.com/yourprofile/selenium-pytest-framework/issues)