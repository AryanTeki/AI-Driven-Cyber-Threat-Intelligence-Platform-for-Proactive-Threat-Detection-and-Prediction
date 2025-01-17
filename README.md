# Real-Time Threat Intelligence System

A comprehensive AI-driven cybersecurity platform for real-time threat detection, analysis, and visualization.

## Overview

This platform provides Security Operation Center (SOC) analysts with real-time threat intelligence, interactive visualizations, and automated reporting capabilities. It combines modern web technologies with artificial intelligence to deliver actionable security insights.

## Features

- **Real-Time Threat Detection & Monitoring**
  - Interactive global threat map
  - Real-time alert notifications
  - Threat trend analysis
  - Severity-based categorization

- **Interactive Dashboard**
  - Customizable visualization components
  - Threat distribution analytics
  - Attack vector analysis
  - Geographic threat mapping

- **Automated Reporting**
  - PDF report generation
  - CSV data export
  - Customizable report templates
  - Executive summaries

- **Advanced Analytics**
  - Threat pattern recognition
  - Risk assessment metrics
  - Historical trend analysis
  - Predictive analytics

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Redis server (for background tasks)
- Git

## Installation Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AryanTeki/AI-Driven-Cyber-Threat-Intelligence-Platform-for-Proactive-Threat-Detection-and-Prediction.git
   cd real-time-threat-intelligence-system
   ```

2. **Create a Virtual Environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/MacOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Redis** (Required for background tasks)
   - Windows: Download and install from [Redis Windows](https://github.com/microsoftarchive/redis/releases)
   - Linux: `sudo apt-get install redis-server`
   - MacOS: `brew install redis`

5. **Environment Setup**
   Create a `.env` file in the root directory with the following variables:
   ```env
   SECRET_KEY=your-secret-key-here
   OTX_API_KEY=your-otx-api-key
   VT_API_KEY=your-virustotal-api-key
   ```

## Running the Application

1. **Start Redis Server**
   ```bash
   # Windows
   redis-server

   # Linux/MacOS
   sudo service redis-server start
   ```

2. **Start the Application**
   ```bash
   python app/main.py
   ```

3. **Access the Dashboard**
   - Open your web browser and navigate to `http://localhost:8050`
   - Default login credentials:
     - Username: admin
     - Password: admin


## Configuration

The application can be configured through the following files:
- `app/config.py`: Main configuration file
- `.env`: Environment variables
- `requirements.txt`: Python dependencies

