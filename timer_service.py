# timer_service.py

import threading
import time
from event_bus import publish
from global_state import state   # <-- Importar estado global

running = False


# -------------------------------------------
#  CALCULAR CONSUMO REAL SEGÚN EL ESTADO
# -------------------------------------------
def calculate_consumption():
    # Luz
    light = 70 if state["light_on"] else 10

    # Termostato (una fórmula simple)
    # 22º = 20 consumo, cada grado suma 3
    thermostat = 20 + (state["thermostat"] - 22) * 3

    # Ventilador
    # 0 = 0, 1 = 10, 2 = 20, 3 = 30
    fan = state["fan"] * 10

    # Suma total
    total = light + thermostat + fan

    # Evitar negativos
    return max(0, round(total, 2))


# -------------------------------------------
#  INICIAR TIMER
# -------------------------------------------
def start_timer(interval=10):
    global running
    if running:
        return
    running = True

    def loop():
        while running:
            value = calculate_consumption()

            publish({
                "time": time.strftime("%H:%M:%S"),
                "device": "system",
                "action": f"Consumption: {value}",
                "user": "Auto"
            })

            time.sleep(interval)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()


def stop_timer():
    global running
    running = False
