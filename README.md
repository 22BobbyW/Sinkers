# Sinkers – MIT BWSI AUV Challenge

## Project Overview  
The *Sinkers* project was developed for the MIT Lincoln Labs Beaver Works Summer Institute (BWSI) Autonomous Underwater Vehicle Challenge — a rigorous underwater robotics competition where teams design, build, and program a BlueFin Sandshark autonomous underwater vehicle  (AUV) to navigate a buoy field course.
This repository contains the flight-software, sensor drivers, control logic, mission automation and test protocols for the team’s AUV using the Bluefin Sandshark hull. 

See this project page for more information: [https://www.aidanrc.com/mit-bwsi-auv-challenge](https://www.aidanrc.com/mit-bwsi-auv-challenge)
This team consisted of Aidan Carrier, Bobby Wang, Naomi Naranjo, and Matthew Weng 


## Demonstration  
Test Run #3
[![Sinkers AUV Test Run](https://img.youtube.com/vi/z71xyqpF_E0/0.jpg)](https://www.youtube.com/watch?v=z71xyqpF_E0)

## Key Capabilities  
- Autonomous mission execution: waypoint navigation, object detection, buoy manipulation, return to base.  
- Sensor integration: IMU, depth sensor, cameras, sonar/range sensors.  
- Modular software architecture: separate layers for hardware interface, control logic, mission automation.  
- Build replicability: hardware pin-map, software dependencies, build/run instructions included.  
- Logging & telemetry: onboard and surface logs for debugging, test-campaign summaries.

## Hardware Overview  
The AUV is built on the following primary subsystems:  
- **Hull / Buoyancy:** Pressure‐rated cylinder, sealed through-hull wiring, main battery pack.  
- **Propulsion & Steering:** Thrusters (forward/reverse), vertical control, rudder/sides for yaw.  
- **Sensors:** IMU (orientation), depth/pressure sensor, forward-looking sonar or pinger, cameras for visual feedback.  
- **Compute:** Embedded board (e.g., Raspberry Pi or equivalent) running Python/C++ control software.  
- **Power & Interfaces:** 12 V battery, 5 V logic regulator, common ground, waterproof connectors for sensors/thrusters.

## Software Architecture  
### Language & Dependencies  
- Core control logic in **Python 3.x** (with optional C++ modules for performance-critical tasks).  
- Key libraries: `numpy`, `opencv-python`, sensor drivers (I²C, SPI, UART), ROS or custom message framework (if used).  
- Versioning of dependencies and environment scripts included in `/env` (or requirements file).

### Module Structure  
```bash
/src
├─ hardware_interface/
│ ├ motors.py
│ ├ sensors.py
│ ├ imu.py
│ └ thrusters.py
├─ control/
│ ├ state_machine.py
│ ├ autonomy.py
│ └ manual_control.py
├─ mission/
│ ├ mission_planner.py
│ └ waypoints.py
└─ main.py
```

### Runtime Control Loop (Simplified Pseudocode)  
```python
initialize all modules (hardware, sensors, control)
select mode (manual or autonomous)
while mission_not_done:
    sensor_data = sensors.read_all()
    if mode == "autonomous":
        command = autonomy.decide(sensor_data)
    else:
        command = manual_control.get_input()
    thrusters.set_command(command)
    log.write(sensor_data, command)
shutdown safe
```


## Setup & Duplication Guide

### Prepare System

Use a Linux-based embedded board (e.g., Raspberry Pi, Nvidia Jetson). We used a Raspberry Pi 4B+ in our modified AUV BlueFin Sandshark.

Install OS, enable network/SSH, update packages.

Clone this repo:

```bash
git clone https://github.com/ArcKnight01/Sinkers.git
cd Sinkers
```

### Install Dependencies
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-gpiozero python3-opencv
pip3 install numpy opencv-python pyserial
```

### Hardware Wiring / Pin-Mapping

Key summary:

Thruster PWM → GPIO pins 12, 13, 18, 19

IMU I²C → SDA (GPIO 2), SCL (GPIO 3)

Depth sensor → SPI / I²C as configured

Cameras → CSI (Raspberry Pi camera interface) or USB

Battery cutoff, safety switch, kill-switch wiring must be confirmed.

### Calibrate Sensors
Run:

``` bash
python3 scripts/calibrate_imu.py
python3 scripts/check_depth_sensor.py
```
Verify thruster direction and motor command response before launch (on a test stand).

### Run Mission
```bash
python3 main.py --mode autonomous --config configs/mission1.yaml
```
Use --mode manual for teleop.

Logs are stored in logs/YYYY_MM_DD_HHMMSS/ and include sensor dump, command trace, state transitions.

### Post-Test Procedures

Download logs for analysis.

Review visual camera feed recordings under videos/.

For multiple runs, compare mission performance metrics in analysis/.

## License

This project is released under the MIT License.

## Acknowledgements

Thanks to the MIT BWSI program, including instructors/mentors Madeleine Miller and Jospeph Edwards, our awesome TA Joseph Ntaimo, and the BWSI director Joel Grimm, as well as the broader open-source robotics community for resources and support.
