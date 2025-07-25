
# API Development Hub

![API Development](https://img.shields.io/badge/API-Development-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-green)

A centralized repository for API-related projects, including current implementations and future API development initiatives.

## 📌 Current Projects

### 1. QuizMaster API Client

- **Description**: Trivia quiz game with OpenTDB API integration
- **Tech Stack**: Python, Requests, Tkinter
- **Features**:

  - API data fetching with offline fallback
  - Modern GUI interface
  - Score tracking system
- **File**: `quizmaster/`

### 2. ISS Tracker API (Coming Soon)

- **Description**: Tracks International Space Station position and sends notifications
- **Tech Stack**: Python, Requests, SMTP
- **Features**:

  - Real-time ISS position tracking
  - Location-based visibility calculations
  - Email notification system
- **File**: `iss_tracker/`

### 3. Weather API Wrapper (Coming Soon)

- **Description**: Unified interface for multiple weather APIs
- **Planned Features**:
  - Multiple provider support (OpenWeather, WeatherAPI)
  - Caching system
  - Location autocomplete

### 4. RESTful Microservice Template (Coming Soon)

- **Description**: Boilerplate for FastAPI microservices
- **Planned Features**:
  - JWT authentication
  - Database integration
  - Automated documentation

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/API.git
cd API

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```
