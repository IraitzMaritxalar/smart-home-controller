import flet as ft
from view_overview import OverviewView
from view_statistics import StatisticsView
from timer_service import start_timer


def main(page: ft.Page):
    page.title = "Smart Home Controller"
    page.window_width = 1100
    page.window_height = 700
    page.padding = 20
    page.scroll = "auto"

    # -----------------------------------------
    #   CREAR VISTAS UNA SOLA VEZ (PERSISTENTES)
    # -----------------------------------------
    overview_view = OverviewView(page)
    statistics_view = StatisticsView(page)

    # Contenedor donde se muestran las vistas
    content = ft.Container(expand=True, content=overview_view)

    # Estado pestaña seleccionada
    selected_tab = "Overview"

    # -----------------------------
    #   Cambiar vista
    # -----------------------------
    def change_view(view_name: str):
        nonlocal selected_tab
        selected_tab = view_name

        if view_name == "Overview":
            content.content = overview_view
        elif view_name == "Statistics":
            content.content = statistics_view

        update_nav_buttons()
        page.update()

    # -----------------------------
    #   Botones de navegación
    # -----------------------------
    btn_overview = ft.TextButton(
        "Overview",
        on_click=lambda _: change_view("Overview"),
    )

    btn_statistics = ft.TextButton(
        "Statistics",
        on_click=lambda _: change_view("Statistics"),
    )

    # -----------------------------
    #   Actualizar estilos (color)
    # -----------------------------
    def update_nav_buttons():
        btn_overview.style = ft.ButtonStyle(
            color=ft.Colors.BLUE if selected_tab == "Overview" else ft.Colors.BLACK54
        )
        btn_statistics.style = ft.ButtonStyle(
            color=ft.Colors.BLUE if selected_tab == "Statistics" else ft.Colors.BLACK54
        )

    update_nav_buttons()

    # -----------------------------
    #   Barra superior (título + nav)
    # -----------------------------
    top_bar = ft.Row(
        [
            ft.Text("Smart Home Controller", size=28, weight="bold"),
            ft.Container(expand=True),
            btn_overview,
            btn_statistics,
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    start_timer(10)

    page.add(top_bar, content)


ft.app(target=main)
