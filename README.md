
# Sinkers – MIT BWSI AUV Challenge

## Project Overview
The **Sinkers** project was developed for the MIT Lincoln Labs **Beaver Works Summer Institute** (BWSI) Autonomous Underwater Vehicle Challenge.  In this competition teams design, build and program a BlueFin Sandshark AUV to navigate a buoy field course.  This repository contains the flight‑software, sensor drivers, control logic, mission automation and test protocols used by the team’s AUV. For additional context and media, see this project page [https://www.aidanrc.com/mit-bwsi-auv-challenge
](https://www.aidanrc.com/mit-bwsi-auv-challenge)

## Hardware Architecture
This AUV uses a modular architecture with the following major subsystems:
| Subsystem        | Description                                                                 | Interface/Notes         |
|------------------|-----------------------------------------------------------------------------|-------------------------|
| **Hull/Buoyancy**| Pressure‑rated cylinder with sealed through‑hull wiring and a main battery pack | Physical structure      |
| **Propulsion & Steering** | Thrusters for forward/reverse and vertical motion; rudders for yaw control | PWM thruster drivers    |
| **Sensors**      | IMU for orientation, depth/pressure sensor, optional sonar/pinger, and cameras for vision | I²C/SPI/CSI/USB         |
| **Compute**      | Embedded computer (e.g., Raspberry Pi 4B+) running Python and C++ control software | GPIO, I²C, SPI          |
| **Power**        | 12 V battery with 5 V logic regulator; common ground and waterproof connectors | Power distribution      |

### Pinout Summary
The original BlueFin Sandshark hardware uses the following pin mappings.  If you modify the wiring or use a different board, update these accordingly.

| Device/Signal      | Pin(s)                        | Notes                                     |
|--------------------|-------------------------------|-------------------------------------------|
| **Thrusters**      | GPIO 12, GPIO 13, GPIO 18, GPIO 19 | PWM channels for left, right and vertical thrusters |
| **IMU (I²C)**      | SDA → GPIO 2; SCL → GPIO 3     | 9‑DOF orientation sensor |
| **Depth sensor**   | SPI/I²C bus (config‑dependent) | Pressure sensor for depth |
| **Cameras**        | CSI or USB ports              | Pi camera module |
| **Safety switches**| Additional GPIO lines         | Battery cutoff and kill‑switch (verify wiring) |


## Software Architecture
The code is written primarily in Python 3.x and depends on `numpy`, `opencv‑python` and various sensor libraries.  The repository currently contains camera processing utilities and a network interface for the BlueFin Sandshark front‑ and back‑seat computers.  Key modules include:

- **Image_Processor.py** – captures images from the Pi camera or simulation and detects buoys.
- **MissionReconstruction.py** – reconstructs mission logs for analysis.
- **Sandshark_Interface.py** – TCP server/client providing command and telemetry exchange between the ‘front seat’ (payload computer) and ‘back seat’ (navigation computer).  It handles socket communications and message queuing.
- **cam_util.py**, **camera_util.py**, **pool_cam_util.py** – helper functions for pixel‑to‑angle conversions and buoy detection.

## Control Loop
The overall control loop for an autonomous mission follows this logic:
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

Although the core loop remains, this repository only implements the camera and communication utilities.  The full autonomy and control algorithms reside in the main Sinkers repository.

## Setup & Duplication Guide
1. **Clone this repo:**

   ```bash
   git clone https://github.com/ArcKnight01/Sinkers.git
   cd Sinkers
   ```

2. **Install dependencies:**

   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3-pip python3-gpiozero python3-opencv
   pip3 install numpy opencv-python pyserial
   ```

3. **Calibrate sensors:**

   Run the calibration scripts (if available) to zero your IMU and depth sensor:

   ```bash
   python3 scripts/calibrate_imu.py
   python3 scripts/check_depth_sensor.py
   ```

4. **Run a mission:**

   Execute the main program with a configuration filehttps://github.com/ArcKnight01/Sinkers/blob/HEAD/README.md#L115-L120:

   ```bash
   python3 main.py --mode autonomous --config configs/mission1.yaml
   ```

   Use `--mode manual` for tele‑operation.  Logs are saved under `logs/YYYY_MM_DD_HHMMSS/` for post‑run analysis.

5. **Analyze results:**

   Use `MissionReconstruction.py` and Jupyter notebooks to reconstruct missions, plot trajectories and evaluate performance.  See the `analysis/` folder for examples.

## Demonstration Videos
Below are test runs from our AUV challenge playlist.  Each thumbnail links to the corresponding YouTube video:

| Run | Embedded Video | Summary |
|----|---|---|
| **Test Run #2** | [![Run 2](https://img.youtube.com/vi/rft1sYsLbGc/0.jpg)](https://www.youtube.com/watch?v=rft1sYsLbGc) | Early trial navigating buoys  |
| **Test Run #3** | [![Run 3](https://img.youtube.com/vi/z71xyqpF_E0/0.jpg)](https://www.youtube.com/watch?v=z71xyqpF_E0) | Improved run with slower speedview |
| **Test Run Fail** | [![Fail](https://img.youtube.com/vi/G_wWVP8iRcc/0.jpg)](https://www.youtube.com/watch?v=G_wWVP8iRcc) | Failure mode demonstration |

## License
This project is released under the **MIT License**

## Acknowledgements
Thanks to the MIT BWSI instructors and mentors (especially Madeleine Miller and Joseph Edwards), BWSI director Joel Grimm, and our awesome TA Joseph Ntaimo, and to our teammates Aidan Carrier, Bobby Wang, Naomi Naranjo, and Matthew Weng for their contributions.

---
