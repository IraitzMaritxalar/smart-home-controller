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
- Use a global emergency-style action to reset the entire smart home
- Navigate through multiple screens using Flet’s view stack system
The UI is inspired by real home automation dashboards and provides separate pages for overview, statistics, and device-specific information.

✨ Features
✅ Overview Screen

Toggle ON/OFF devices:
- Living Room Light
- Front Door Lock
Live-adjust slider devices:
- Thermostat
- Ceiling Fan
Additional features:
- Buttons linking to device detail screens
- Fully persistent state using a global shared object
- NEW: “All OFF” Global Reset Button
  - A new button has been added at the top of the Overview screen
  - Pressing ALL OFF instantly resets all home devices to their default safe state:
    - Light → OFF
    - Door → LOCKED
    - Thermostat → 22°C
    - Fan → 0
  - Automatically updates the UI
  - Publishes a global event (“ALL DEVICES RESET”), visible in Statistics and device logs
  - Helps simulate an emergency shutdown or quick home reset action

📊 Statistics Screen
- Displays simulated energy consumption
- Dynamically updated bar graph using animated containers
- Logs every action (ON/OFF, slider changes, ALL OFF events)
- Automatic updates every X seconds using a background timer

🔍 Device Details Screen
Each device has its own detail view showing:
- Current status (ON/OFF, LOCKED/UNLOCKED, slider values)
- Device metadata (name, ID, type)
- A persistent “Recent actions” log
- Real-time updates via the event bus
- Dedicated back navigation

🔄 Event System (Publish/Subscribe)
- Every device interaction publishes an event
- All listening screens (statistics, details) update instantly
- Events are saved in the global log so switching screens never loses data
- The new ALL OFF action also generates a global log event

🗄 Global State Persistence
Stored globally:
- Device states
- Thermostat values
- Fan speed
- Device-specific logs
- Consumption history
Because all screens share the same state object, state persists naturally across all views.

⏲ Background Timer
A separate thread periodically simulates:
- Power consumption updates
- Automatic log entries
This creates the feeling of a live smart home system where devices continue running in the background.
