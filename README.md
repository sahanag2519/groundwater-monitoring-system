# AI-Based Groundwater Monitoring and Smart Water Distribution System

An IoT-enabled groundwater monitoring prototype designed to provide real-time
information about **groundwater level and water quality**, generate local
alerts, and support data-driven water resource monitoring.

The system integrates an **ESP32-based sensor node**, ultrasonic water-level
measurement, TDS-based water-quality monitoring, Wi-Fi communication,
threshold-based alerts, Flask backend processing, data storage, and a
real-time monitoring dashboard.

---

## Problem Statement

### Problem Statement 6 – AI-Based Groundwater Monitoring and Smart Water Distribution System for Rural India

Groundwater is a major source of drinking and irrigation water across rural
India. However, groundwater resources face challenges such as over-extraction,
irregular recharge, contamination, and unequal distribution.

In many rural areas, groundwater monitoring depends on periodic manual
measurements. This can lead to delayed identification of declining water
levels, water-quality degradation, and other critical conditions.

The objective of this project is to develop an affordable and localized
monitoring system capable of continuously collecting groundwater parameters
and presenting useful information through a digital monitoring platform.

---

# Project Overview

Our system monitors two key groundwater parameters:

- **Water Level**
- **Total Dissolved Solids (TDS)**

An ESP32 collects the sensor measurements and evaluates local alert
conditions. The readings are transmitted over Wi-Fi to a Flask-based backend,
where they can be processed, stored, and displayed on a real-time dashboard.

The system also provides immediate local alerts through LEDs and a buzzer.

```text
Groundwater Source
       │
       ├───────────────┐
       │               │
       ▼               ▼
Ultrasonic Sensor   TDS Sensor
       │               │
       └───────┬───────┘
               ▼
             ESP32
               │
             Wi-Fi
               │
               ▼
         Flask Backend
               │
       ┌───────┴────────┐
       ▼                ▼
 Data Processing    Dashboard
       │
       ▼
 Data Storage

Local Alerts
     │
     ├── White LED → Normal
     ├── Blue LED  → Warning
     ├── Red LED   → Critical
     └── Buzzer    → High TDS Alert
```

---
# System Architecture

```text
        ┌──────────────────────────────┐
        │       Groundwater Source     │
        │                              │
        │  Water Level + Water Quality │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │            ESP32             │
        │                              │
        │  Ultrasonic Sensor           │
        │  TDS Sensor                  │
        └──────────────┬───────────────┘
                       │
                  Wi-Fi / HTTP
                       │
                       ▼
        ┌──────────────────────────────┐
        │        Flask Server          │
        │                              │
        │  Data Reception              │
        │  Alert Evaluation            │
        │  Data Analysis               │
        │  AI Prediction               │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │       SQLite Database        │
        │                              │
        │ Village / Well / Level / TDS │
        └──────────────┬───────────────┘
                       │
                       ▼
        ┌──────────────────────────────┐
        │       Web Dashboard          │
        │                              │
        │ Current Values               │
        │ Status                       │
        │ Historical Graphs            │
        │ AI Prediction / Trend        │
        └──────────────────────────────┘

        Local Hardware Alerts
             │          │
             ▼          ▼
          LEDs        Buzzer
```
---
# Key Features

## 1. Real-Time Water-Level Monitoring

An ultrasonic sensor measures the distance between the sensor and the water
surface.

The measured distance is converted into water level using the known depth of
the prototype.

```text
Water Level = Total Well Depth − Measured Distance
```

The calculated water level is then transmitted to the monitoring dashboard.

---

## 2. TDS-Based Water-Quality Monitoring

A TDS sensor is used to estimate the concentration of dissolved substances in
water.

The ESP32 reads the sensor's analog output and converts it into an estimated
TDS value in **ppm**.

The prototype uses the following alert threshold:

```text
TDS > 500 ppm
```

When the measured TDS exceeds the configured threshold, the local buzzer is
activated.

> TDS is an indicator of the concentration of dissolved solids. It does not
> identify individual contaminants or specific chemical substances.

---

## 3. Water-Level LED Alert System

Three LEDs provide an immediate visual indication of the water level.

| LED | Condition | Status |
|-----|-----------|--------|
| White | ≥ 3.5 cm | Normal |
| Blue | > 2.0 cm and < 3.5 cm | Warning / Medium |
| Red | ≤ 2.0 cm | Critical / Low |

These threshold values are configured for the current prototype and can be
modified for real-world deployment.

---

## 4. TDS Alert Buzzer

The buzzer provides a local audible warning when the measured TDS exceeds the
configured threshold.

```text
TDS ≤ 500 ppm
      ↓
 Buzzer OFF

TDS > 500 ppm
      ↓
 Buzzer ON
```

This allows a local user to recognize a potential water-quality warning
without relying entirely on the dashboard.

---

## 5. Wi-Fi-Based Data Transmission

The ESP32 connects to a Wi-Fi network and sends sensor readings to the Flask
server using an HTTP POST request.

Example data transmitted by the ESP32:

```json
{
  "village": "Village A",
  "well": "Well 1",
  "water_level": 6.98,
  "tds": 121
}
```

The backend receives the data and makes it available for monitoring and
further processing.

---

## 6. Real-Time Monitoring Dashboard

The Flask-based backend receives the measurements from the ESP32 and provides
data to the monitoring dashboard.

The dashboard displays information including:

- Village
- Well identification
- Water level
- TDS value
- Recorded measurements
- Monitoring status

This provides a centralized interface for observing groundwater conditions.

---

### 7. AI-Based Prediction

The system analyzes previously recorded groundwater-level data to identify
trends and estimate future groundwater-level conditions.

The prediction module uses the collected historical measurements to support
early identification of possible changes in groundwater availability.

This provides an additional decision-support feature alongside real-time
sensor monitoring.

## 8. Data Storage and Analysis

The project includes Python modules for data handling, analysis, database
updates, prediction, and viewing stored measurements.

The repository contains modules supporting:

- Database operations
- Data analysis
- Prediction
- Alert handling
- Database updates
- Data viewing
- Sample/random data generation

These modules provide a foundation for extending the prototype toward
historical trend analysis and predictive groundwater monitoring.

---

# Hardware Components

| Component | Purpose |
|-----------|---------|
| ESP32 | Main controller and Wi-Fi communication |
| Ultrasonic Sensor | Water-level measurement |
| TDS Sensor | Dissolved-solids measurement |
| Active Buzzer | Water-quality warning |
| White LED | Normal water-level indication |
| Blue LED | Medium/warning indication |
| Red LED | Critical/low water-level indication |
| 220 Ω Resistors | LED current limiting |
| 5.6 kΩ Resistor | Ultrasonic ECHO voltage divider |
| 10 kΩ Resistor | Ultrasonic ECHO voltage divider |
| Breadboard | Prototype circuit assembly |
| Jumper Wires | Component interconnection |

---

# ESP32 Pin Connections

| Component | ESP32 GPIO | Purpose |
|-----------|-----------:|---------|
| TDS Sensor Analog Output | GPIO 34 | TDS measurement |
| Ultrasonic TRIG | GPIO 23 | Trigger pulse |
| Ultrasonic ECHO | GPIO 18 | Echo measurement |
| Buzzer | GPIO 25 | TDS warning |
| White LED | GPIO 26 | Normal water level |
| Blue LED | GPIO 27 | Medium/warning level |
| Red LED | GPIO 32 | Critical/low level |

---

# Ultrasonic ECHO Voltage Divider

The ultrasonic sensor's ECHO signal is connected to the ESP32 through a
resistor voltage-divider network.

The prototype uses:

- **5.6 kΩ resistor**
- **10 kΩ resistor**

The voltage divider reduces the ECHO signal voltage before it reaches the
ESP32 input.

### Connection

```text
Ultrasonic ECHO
      │
     5.6 kΩ
      │
      ├──────────────→ ESP32 GPIO 18
      │
     10 kΩ
      │
     GND
```

This provides a safer voltage interface between the ultrasonic sensor's ECHO
output and the ESP32 GPIO.

---

# LED Connections

Each LED is connected through a **220 Ω series resistor**.

```text
ESP32 GPIO
    │
  220 Ω
    │
   LED
    │
   GND
```

The LEDs are used to provide simple local status information without requiring
access to the monitoring dashboard.

---

# Software Architecture

### Embedded System

- ESP32
- Arduino framework
- C/C++

### Backend

- Python
- Flask
- HTTP communication

### Data Processing

- Python
- Data analysis
- Database handling
- Prediction module

### Dashboard

- HTML
- CSS
- JavaScript
- Flask templates

---
### AI / Data Analysis

- Historical groundwater-level data analysis
- AI-based groundwater-level prediction
- Trend identification
- Prediction visualization on the dashboard

---  
# System Data Flow

```text
       ┌─────────────────────┐
       │ Groundwater Source  │
       └──────────┬──────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
 ┌──────────────┐    ┌──────────────┐
 │ Ultrasonic   │    │ TDS Sensor   │
 │ Water Level  │    │ Water Quality│
 └──────┬───────┘    └──────┬───────┘
        │                   │
        └─────────┬─────────┘
                  ▼
            ┌───────────┐
            │   ESP32   │
            └─────┬─────┘
                  │
               Wi-Fi
                  │
                  ▼
          ┌──────────────┐
          │ Flask Server │
          └──────┬───────┘
                 │
        ┌────────┴─────────┐
        │                  │
        ▼                  ▼
 ┌──────────────┐   ┌──────────────┐
 │ Data Storage │   │  Dashboard   │
 │ & Analysis   │   │              │
 └──────────────┘   └──────────────┘
```

---

# Local Alert Flow

The ESP32 evaluates alert conditions locally.

### Water-Level Monitoring

```text
Measured Distance
       ↓
Calculate Water Level
       ↓
┌───────────────┐
│ Water Level?  │
└───────┬───────┘
        │
        ├── ≥ 3.5 cm ─────→ WHITE LED
        │                     NORMAL
        │
        ├── 2–3.5 cm ─────→ BLUE LED
        │                    WARNING
        │
        └── ≤ 2 cm ───────→ RED LED
                             CRITICAL
```

### TDS Monitoring

```text
TDS Sensor
    ↓
Calculate TDS
    ↓
TDS > 500 ppm?
    │
   YES
    ↓
Buzzer ON
```

---

# Repository Structure

```text
groundwater-monitoring-system/
│
├── media/
│   ├── README.md
│   ├── circuit.jpeg
│   ├── buzzer-tds-alert.mp4
│   ├── dashboard-real-time-monitoring.mp4
│   └── water-level-led-indicators.mp4
│
├── static/
│   └── dashboard assets
│
├── templates/
│   └── dashboard templates
│
├── alert.py
├── analysis.py
├── app.py
├── database.py
├── hardware_setup_ground_water_monitoring.ino
├── prediction.py
├── requirements.txt
├── send_random_data.py
├── update_database.py
├── view_data.py
├── .gitignore
└── README.md
```

---
# AI-Based Groundwater Prediction

The system uses historical groundwater-level measurements collected from the
monitoring setup to identify groundwater-level trends and estimate future
groundwater conditions.

The prediction module works with the recorded sensor data and provides an
additional decision-support layer beyond real-time monitoring.

### Prediction Workflow

```text
Historical Groundwater Data
          ↓
Data Processing
          ↓
Trend Analysis
          ↓
AI Prediction Model
          ↓
Predicted Groundwater Level
          ↓
Dashboard Visualization
```
---
# Demonstration

The working prototype demonstrates:

- Groundwater-level measurement
- TDS-based water-quality monitoring
- Local water-level LED alerts
- TDS buzzer alert
- ESP32 Wi-Fi communication
- Flask backend
- Real-time monitoring dashboard
- Data handling and analysis
- AI prediction

All hardware images and demonstration videos are available in the
[`media`](./media/) folder.

---

# Demo Videos

## TDS Alert Buzzer

Demonstrates the audible warning generated when the measured TDS exceeds the
configured threshold of **500 ppm**.

[▶ Watch TDS Buzzer Alert](https://youtu.be/CHl_UEb8vh4)

---

## Water-Level LED Indicators

Demonstrates the three water-level status indicators:

- **White LED** – Normal water level
- **Blue LED** – Warning / Medium water level
- **Red LED** – Critical / Low water level

[▶ Watch Water-Level LED Demonstration](https://youtu.be/RgPJi_KCC2A)

---

## Real-Time Dashboard

Demonstrates real-time sensor data being transmitted from the ESP32 through
Wi-Fi to the Flask backend and displayed on the monitoring dashboard.

[▶ Watch Real-Time Dashboard Demonstration](https://youtu.be/41BdZGNdYzY)

---

# Hardware Demonstration

The `media` folder contains:

- Complete circuit image
- TDS buzzer demonstration
- Water-level LED demonstration
- Real-time dashboard demonstration

Visit the [`media`](./media/) folder to view the complete demonstration
materials.

---
## Project Presentation

The complete project presentation covering the problem statement, proposed
system, hardware implementation, software architecture, results, and future
scope is available below.

[📑 View Project Presentation](media/Presentation.pptx)

# Running the Project

## 1. Clone the Repository

```bash
git clone https://github.com/sahanag2519/groundwater-monitoring-system.git
cd groundwater-monitoring-system
```

## 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure ESP32 Wi-Fi

Open:

```text
hardware_setup_ground_water_monitoring.ino
```

Configure the Wi-Fi credentials:

```cpp
const char* WIFI_SSID = "YOUR_WIFI_SSID";
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";
```

Also configure the Flask server IP address according to the computer running
the backend.

> Do not upload real Wi-Fi passwords or other private credentials to a public
> repository.

## 4. Upload the ESP32 Firmware

Connect the ESP32 to the computer, select the appropriate ESP32 board and COM
port in Arduino IDE, and upload the firmware.

## 5. Start the Flask Backend

Install the required Python packages and run:

```bash
python app.py
```

The dashboard can then be opened using the local server address provided by
the Flask application.

---

# Prototype Testing

The prototype was tested under controlled conditions to demonstrate different
groundwater monitoring states.

### Test Conditions

**Normal water condition**

A normal water sample is used to demonstrate regular operation.

**Higher dissolved-solids condition**

A separate sample with increased dissolved solids is used to demonstrate the
TDS alert and buzzer operation.

**Low water-level condition**

A reduced water quantity is used to demonstrate the critical water-level
condition and red LED indication.

**Real-time communication**

Sensor measurements are transmitted from the ESP32 to the Flask backend over
Wi-Fi and displayed on the dashboard.

---

# Example Monitoring States

The prototype uses separate sample containers to demonstrate different
conditions.

```text
┌─────────────────┐
│ Normal Water    │
│                 │
│ White LED       │
│ Normal Status   │
└─────────────────┘

┌─────────────────┐
│ Higher TDS      │
│                 │
│ Buzzer Alert    │
│ Quality Warning │
└─────────────────┘

┌─────────────────┐
│ Low Water Level │
│                 │
│ Red LED         │
│ Critical Status │
└─────────────────┘
```

---

# Limitations

This project is a functional prototype developed for academic and hackathon
demonstration purposes.

Current limitations include:

- TDS provides an estimate of dissolved-solids concentration and does not
  identify individual contaminants.
- The prototype uses a small-scale **10 cm water-depth model**.
- Wi-Fi is currently used for communication.
- Threshold values are configured for the prototype and require calibration
  for actual groundwater wells.
- Long-term field deployment would require weatherproof enclosures.
- Field deployment would require appropriate sensor calibration and
  maintenance.
- Reliable remote deployment would require a suitable power and communication
  system.

---

# Future Scope

The system can be further enhanced to support larger-scale groundwater
monitoring and smart water-resource management.

Potential enhancements include:

- Multi-well monitoring
- Multiple rural monitoring locations
- GSM or LoRa communication
- Solar-powered sensor nodes
- SD-card-based local data logging
- Long-term groundwater trend analysis
- Machine-learning-based groundwater-level prediction
- Water-quality trend analysis
- Automated mobile/web notifications
- Panchayat-level monitoring
- Spatial and temporal groundwater analysis
- Smart water-distribution recommendations
- Decision-support tools for equitable water allocation

These enhancements can help extend the prototype toward a scalable groundwater
monitoring and decision-support platform for rural communities.

---

# Project Status

**Functional Prototype**

The current prototype successfully demonstrates:

- The ultrasonic sensor measures the water level.
- The TDS sensor measures the dissolved-solids level of the water.
- The ESP32 processes the sensor readings.
- Water level scaling is applied to convert the prototype measurement into the required monitoring scale.
- The ESP32 sends the readings to the Flask server using Wi-Fi and HTTP.
- Flask receives and stores the data in an SQLite database.
- The dashboard displays the latest groundwater readings.
- Stored readings are used for graphical analysis and trend estimation.
- Local LEDs indicate the groundwater-level condition.
- A buzzer provides an alert when the TDS value crosses the configured threshold.
- Data handling and analysis modules.
- Historical measurements are analyzed to identify groundwater trends.
- The prediction module estimates future groundwater-level trends from the available historical data.

The system provides a foundation for future predictive analytics and smart
water-distribution capabilities.

---

# Team

This project was developed collaboratively by:

| Team Member | Role |
|-------------|------|
| **Sanjana N** | Team Leader |
| **Sahana G** | Team Member |
| **Venkata Sai Deekshitha Darsi** | Team Member |
---

### Team Contribution

The team collaboratively worked on:

- Problem analysis
- Hardware design and prototyping
- ESP32 programming
- Sensor integration
- Alert-system implementation
- Wi-Fi communication
- Flask backend
- Dashboard development
- Data handling and analysis
- Testing and validation
- Documentation and project presentation
- AI prediction

---

## Project Highlights

- Real-time groundwater-level monitoring using ESP32 and ultrasonic sensing
- TDS-based water-quality monitoring
- **AI-based groundwater-level prediction using historical sensor data**
- Real-time Wi-Fi communication with Flask
- Web-based monitoring dashboard
- SQLite database for storing groundwater measurements
- Local water-level alerts using White, Blue and Red LEDs
- Audible TDS warning using an active buzzer
- Data analysis and groundwater trend visualization
  

**ESP32 • IoT • Groundwater Monitoring • TDS • Ultrasonic Sensing • Flask •
Python • Real-Time Dashboard • Data Analysis •AI Prediction**
