import flet as ft
import time
from event_bus import publish
from global_state import state
from view_device_details import DeviceDetailsView


def OverviewView(page: ft.Page):

    # -------------------------------------------------
    #   FUNCTION: SAFE BACK
    # -------------------------------------------------
    def safe_back():
        if len(page.views) > 1:
            page.views.pop()
        page.update()

    # -------------------------------------------------
    #   INITIAL STATUS TEXTS (from global_state)
    # -------------------------------------------------
    living_light_status = ft.Text(
        f"Status: {'ON' if state['light_on'] else 'OFF'}"
    )
    front_door_status = ft.Text(
        f"Door: {'LOCKED' if state['door_locked'] else 'UNLOCKED'}"
    )

    light_is_on = state["light_on"]
    door_is_locked = state["door_locked"]

    # -------------------------------------------------
    #   TOGGLE LIGHT
    # -------------------------------------------------
    def toggle_light(e):
        nonlocal light_is_on
        light_is_on = not light_is_on
        state["light_on"] = light_is_on

        if light_is_on:
            living_light_status.value = "Status: ON"
            light_button.text = "Turn OFF"
            action = "Turn ON"
        else:
            living_light_status.value = "Status: OFF"
            light_button.text = "Turn ON"
            action = "Turn OFF"

        # SEND EVENT
        publish({
            "time": time.strftime("%H:%M:%S"),
            "device": "living_room_light",
            "action": action,
            "user": "User"
        })

        page.update()

    # -------------------------------------------------
    #   TOGGLE DOOR
    # -------------------------------------------------
    def toggle_door(e):
        nonlocal door_is_locked
        door_is_locked = not door_is_locked
        state["door_locked"] = door_is_locked

        if door_is_locked:
            front_door_status.value = "Door: LOCKED"
            door_button.text = "Unlock"
            action = "Lock"
        else:
            front_door_status.value = "Door: UNLOCKED"
            door_button.text = "Lock"
            action = "Unlock"

        publish({
            "time": time.strftime("%H:%M:%S"),
            "device": "front_door",
            "action": action,
            "user": "User"
        })

        page.update()

    # -------------------------------------------------
    #   TOGGLE BUTTONS
    # -------------------------------------------------
    light_button = ft.ElevatedButton(
        "Turn OFF" if light_is_on else "Turn ON",
        on_click=toggle_light
    )

    door_button = ft.ElevatedButton(
        "Unlock" if door_is_locked else "Lock",
        on_click=toggle_door
    )

    # -------------------------------------------------
    #   OPEN DETAILS VIEWS
    # -------------------------------------------------
    def open_light_details(e):
        page.views.append(
            DeviceDetailsView(
                page,
                name="Living Room Light",
                device_id="living_room_light",
                device_type="light",
                go_back=safe_back
            )
        )
        page.update()

    def open_door_details(e):
        page.views.append(
            DeviceDetailsView(
                page,
                name="Front Door",
                device_id="front_door",
                device_type="door",
                go_back=safe_back
            )
        )
        page.update()

    # -------------------------------------------------
    #   BUTTON ROW
    # -------------------------------------------------
    def button_row(details_handler, button):
        return ft.Row(
            controls=[
                ft.TextButton("Details", on_click=details_handler),
                button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    # -------------------------------------------------
    #   DEVICE CARDS
    # -------------------------------------------------
    light_card = ft.Container(
        content=ft.Column([
            ft.Text("💡 Living Room Light", size=18, weight="bold"),
            living_light_status,
            ft.Text("Tap to switch the light."),
            button_row(open_light_details, light_button),
        ]),
        padding=20,
        border_radius=10,
        width=450,
        bgcolor="#FFF7D6",
    )

    door_card = ft.Container(
        content=ft.Column([
            ft.Text("🚪 Front Door", size=18, weight="bold"),
            front_door_status,
            ft.Text("Tap to lock / unlock the door."),
            button_row(open_door_details, door_button),
        ]),
        padding=20,
        border_radius=10,
        width=450,
        bgcolor="#F5EDE9",
    )

    # -------------------------------------------------
    #   SLIDERS
    # -------------------------------------------------
    thermostat_value = ft.Text(f"Set point: {state['thermostat']} °C")
    fan_value = ft.Text(f"Fan speed: {state['fan']}")

    def thermostat_changed(e):
        val = round(e.control.value, 1)
        thermostat_value.value = f"Set point: {val} °C"
        state["thermostat"] = val

        publish({
            "time": time.strftime("%H:%M:%S"),
            "device": "thermostat",
            "action": f"Set to {val} °C",
            "user": "User"
        })
        page.update()

    def fan_changed(e):
        val = int(e.control.value)
        fan_value.value = f"Fan speed: {val}"
        state["fan"] = val

        publish({
            "time": time.strftime("%H:%M:%S"),
            "device": "ceiling_fan",
            "action": f"Speed {val}",
            "user": "User"
        })
        page.update()

    thermostat_slider = ft.Slider(
        min=10, max=30, value=state["thermostat"], on_change=thermostat_changed
    )

    fan_slider = ft.Slider(
        min=0, max=3, divisions=3, value=state["fan"], on_change=fan_changed
    )

    thermostat_card = ft.Container(
        content=ft.Column([
            ft.Text("🌡 Thermostat", size=18, weight="bold"),
            thermostat_value,
            ft.Text("Use slider to change temperature."),
            thermostat_slider,
            ft.TextButton("Details"),   # Puedes enlazarlo más tarde
        ]),
        padding=20,
        border_radius=10,
        width=450,
        bgcolor="#FFE4E8",
    )

    fan_card = ft.Container(
        content=ft.Column([
            ft.Text("🌀 Ceiling Fan", size=18, weight="bold"),
            fan_value,
            ft.Text("0 = OFF, 3 = MAX."),
            fan_slider,
            ft.TextButton("Details"),
        ]),
        padding=20,
        border_radius=10,
        width=450,
        bgcolor="#E5FAFF",
    )

    # -------------------------------------------------
    #   ALL OFF FUNCTION
    # -------------------------------------------------
    def all_off(e):
        # Cambiar estados globales
        state["light_on"] = False
        state["door_locked"] = True
        state["thermostat"] = 22
        state["fan"] = 0

        # Actualizar textos de estado
        living_light_status.value = "Status: OFF"
        light_button.text = "Turn ON"

        front_door_status.value = "Door: LOCKED"
        door_button.text = "Unlock"

        thermostat_value.value = "Set point: 22 °C"
        fan_value.value = "Fan speed: 0"

        # Actualizar sliders
        thermostat_slider.value = 22
        fan_slider.value = 0

        # Publicar evento en logs
        publish({
            "time": time.strftime("%H:%M:%S"),
            "device": "system",
            "action": "ALL DEVICES RESET",
            "user": "User"
        })

        page.update()

    # Botón rojo
    all_off_button = ft.ElevatedButton(
        "ALL OFF",
        bgcolor=ft.Colors.RED,
        color=ft.Colors.WHITE,
        on_click=all_off
    )

    # -------------------------------------------------
    #   FINAL LAYOUT
    # -------------------------------------------------
    return ft.Column(
        [
            all_off_button,
            ft.Divider(),

            ft.Text("On/Off devices", size=22, weight="bold"),
            ft.Row([light_card, door_card], wrap=True),

            ft.Divider(),

            ft.Text("Slider controlled devices", size=22, weight="bold"),
            ft.Row([thermostat_card, fan_card], wrap=True)
        ],
        expand=True
    )
