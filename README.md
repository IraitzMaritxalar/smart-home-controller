Smart Home Controller – Flet Application

This project is a multi-screen Smart Home Controller built using Python and Flet, designed to simulate the control and monitoring of smart home devices such as lights, doors, thermostats, and ceiling fans.
It includes real-time UI updates, persistent device state, and a global event system that provides synchronized logs across different views.

📌 Project Description

The Smart Home Controller is a desktop/mobile-friendly interface that allows users to:
- Toggle power-controlled devices (lights, doors)
- Adjust slider-based devices (thermostat, ceiling fan)
- Track power consumption through an auto-updating statistics panel
- View device-specific details in separate screens
- Persist device status and logs across views using a global state system
- The UI is inspired by multi-screen home automation systems and uses Flet’s navigation stack (page.views) to simulate separate pages for the overview, statistics, and individual device details.

✨ Features
✅ Overview Screen

Toggle ON/OFF devices:
- Living Room Light
- Front Door Lock
Live-adjust slider devices:
- Thermostat
- Ceiling Fan
Buttons for navigating to device detail screens
States are fully persistent thanks to a global state object

📊 Statistics Screen

- Displays simulated energy consumption
- Dynamically updated bar graph using Flet containers
- Logs every action (ON/OFF, slider changes)
- Automatic updates every X seconds through a background timer

🔍 Device Details Screen

Each device has a dedicated detail view showing:
- Current status (ON/OFF, LOCKED/UNLOCKED, etc.)
- Device metadata (name, ID, type)
- A persistent “Recent actions” log
- Multi-screen navigation (Back button)
- Real-time updates through a publish/subscribe event bus

🔄 Event System (Publish/Subscribe)

- Any device action (toggle or slider change) publishes an event
- All listeners — Statistics screen, device details, etc. — receive updates instantly
- Events are stored in a global log system so nothing is lost when switching screens

🗄 Global State Persistence

Persistent state includes:
- Device statuses
- Thermostat values
- Fan speed
- Device-specific logs
- Energy consumption history
State is shared across all screens, so switching pages does not reset anything.

⏲ Background Timer

A separate thread periodically simulates:
- Power consumption readings
- New entries added automatically to Statistics screen and logs
This creates the effect of “real devices running in the background.”
