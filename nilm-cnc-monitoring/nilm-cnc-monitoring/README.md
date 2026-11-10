# NILM-Based CNC Machine Monitoring

Non-Intrusive Load Monitoring (NILM) system that monitors a CNC machine using ESP32
sensor nodes, MQTT, and a TimescaleDB database, and applies machine learning to
identify which machine subsystems (spindle, coolant, hydraulic, A-axis) are running.

Developed during my Research & Development internship at **CMTI, Bengaluru** (May-Jul 2026).

## System Architecture

```
Current sensors -> ESP32 -> WiFi/MQTT -> Python logger -> PostgreSQL/TimescaleDB -> ML (Random Forest)
```

## Features
- Real-time data acquisition from multiple analog channels using ESP32
- MQTT-based data transfer
- Time-series storage in TimescaleDB (`nilm` database, `machine_data` table)
- Automatic machine-state labeling (OFF, SPINDLE_RUNNING, MACHINING, ...)
- Multi-label Random Forest to predict each subsystem's ON/OFF state

## Project Structure

| Folder | Contents |
|---|---|
| `firmware/` | ESP32 Arduino code |
| `ingestion/` | `mqtt_subscriber.py` (debug), `mqtt_to_postgres.py` (logging) |
| `database/` | `schema.sql` for TimescaleDB |
| `ml/` | Label generation and Random Forest training |
| `data/` | Sample data only |

## Hardware
- ESP32 development board
- Current sensors (e.g. SCT-013 with burden resistor) on the machine's main supply and sub-circuits
- A PC/server running an MQTT broker (Mosquitto) and PostgreSQL with TimescaleDB

## Setup

1. **Clone and install**
   ```bash
   git clone https://github.com/<your-username>/nilm-cnc-monitoring.git
   cd nilm-cnc-monitoring
   pip install -r requirements.txt
   ```
2. **Database**: create a database named `nilm`, then run `database/schema.sql`.
3. **Config**: copy `ingestion/config.example.py` to `ingestion/config.py` and fill in your details.
4. **Firmware**: copy `firmware/esp32_nilm_node/secrets.h.example` to `secrets.h`, fill in WiFi/MQTT details, and upload the `.ino` to the ESP32 with Arduino IDE.
5. **Run**
   ```bash
   cd ingestion
   python mqtt_subscriber.py      # check data is arriving
   python mqtt_to_postgres.py     # store data in the database
   ```
6. **Machine learning**
   ```bash
   python ml/build_labels.py
   python ml/train_random_forest.py
   ```

## Results
Random Forest achieved high accuracy for the spindle, coolant and hydraulic subsystems.
The A-axis was harder to classify because of its low signal contrast.
*(Add your accuracy numbers / graphs here.)*

## Author
**Harsha Vardhan Parnapalli**, KSRMCE
