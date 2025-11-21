# global_state.py

state = {
    "light_on": False,
    "door_locked": True,
    "thermostat": 22.0,
    "fan": 0,

    # LOG STORAGE PERSISTENT
    "logs": {
        "living_room_light": [],
        "front_door": [],
        "thermostat": [],
        "ceiling_fan": []
    }
}
