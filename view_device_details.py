import flet as ft
from event_bus import subscribe
from global_state import state


class DeviceDetailsView(ft.View):

    def __init__(self, page: ft.Page, name: str, device_id: str, device_type: str, go_back):
        super().__init__(route="/details")
        self.page = page
        self.name = name
        self.device_id = device_id
        self.device_type = device_type
        self.go_back = go_back

        # Estado actual
        self.state_text = ft.Text(self.get_state_string(), size=18)

        # Logs persistentes desde global_state
        self.log_entries = state["logs"][self.device_id]
        self.log_column = ft.Column()

        # Suscripción a eventos globales
        subscribe(self.on_event)

        # UI completa de la vista
        self.controls = [
            ft.Text(f"{self.name} details", size=30, weight="bold"),
            ft.Text(f"ID: {self.device_id}", size=18),
            ft.Text(f"Type: {self.device_type}", size=18),
            self.state_text,

            ft.Divider(),

            ft.Text("Recent actions", size=22, weight="bold"),
            self.log_column,

            ft.ElevatedButton("Back to overview", on_click=lambda _: self.go_back_safe())
        ]

        # Cargar log inicial en pantalla
        self.refresh_log()

    # -------------------------------------------------------
    # Obtener estado actual desde global_state
    # -------------------------------------------------------
    def get_state_string(self):
        if self.device_type == "light":
            return f"State: {'ON' if state['light_on'] else 'OFF'}"

        if self.device_type == "door":
            return f"State: {'LOCKED' if state['door_locked'] else 'UNLOCKED'}"

        if self.device_type == "thermostat":
            return f"State: {state['thermostat']}°C"

        if self.device_type == "fan":
            return f"State: speed {state['fan']}"

        return "State: Unknown"

    # -------------------------------------------------------
    # Evento recibido desde event_bus
    # -------------------------------------------------------
    def on_event(self, event):
        # Solo procesar eventos de este dispositivo
        if event["device"] != self.device_id:
            return

        # Crear entrada nueva
        entry = f"{event['time']} - {event['action']} ({event['user']})"

        # Guardar en global_state (PERSISTENTE)
        state["logs"][self.device_id].append(entry)

        # Limitar tamaño
        if len(state["logs"][self.device_id]) > 20:
            state["logs"][self.device_id].pop(0)

        # Actualizar referencia local
        self.log_entries = state["logs"][self.device_id]

        # Actualizar UI
        self.refresh_state()
        self.refresh_log()
        self.safe_update()

    # -------------------------------------------------------
    # Actualizar estado
    # -------------------------------------------------------
    def refresh_state(self):
        self.state_text.value = self.get_state_string()

    # -------------------------------------------------------
    # Actualizar lista de logs en pantalla
    # -------------------------------------------------------
    def refresh_log(self):
        self.log_column.controls = [
            ft.Text(e, size=16) for e in self.log_entries
        ]

    # -------------------------------------------------------
    # Update seguro
    # -------------------------------------------------------
    def safe_update(self):
        try:
            self.page.update()
        except:
            pass

    # -------------------------------------------------------
    # Volver atrás sin errores
    # -------------------------------------------------------
    def go_back_safe(self):
        if len(self.page.views) > 1:
            self.page.views.pop()
        self.page.update()
