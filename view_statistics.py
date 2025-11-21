import flet as ft
from event_bus import subscribe


class StatisticsView(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__(scroll="auto")

        # Page se asigna después de crearse la vista
        self.page = None
        self.attach_page(page)

        # ---------------------------------
        #   TABLE LOG
        # ---------------------------------
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Time")),
                ft.DataColumn(ft.Text("Device")),
                ft.DataColumn(ft.Text("Action")),
                ft.DataColumn(ft.Text("User")),
            ],
            rows=[]
        )

        # ---------------------------------
        #   BAR CHART
        # ---------------------------------
        self.max_points = 30
        self.values = []

        self.bar_containers = [
            ft.Container(width=20, height=0, bgcolor=ft.Colors.CYAN)
            for _ in range(self.max_points)
        ]

        self.chart = ft.Container(
            content=ft.Row(self.bar_containers, spacing=2, vertical_alignment="end"),
            width=900,
            height=300,
            bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            border_radius=5,
        )

        # ---------------------------------
        #   LAYOUT
        # ---------------------------------
        self.controls = [
            ft.Text("Power consumption", size=26, weight="bold"),
            self.chart,
            ft.Divider(),
            ft.Text("Action log", size=22, weight="bold"),
            self.table,
        ]

        # ---------------------------------
        #   SUBSCRIBE ONLY ONCE
        # ---------------------------------
        subscribe(self.on_event)

    # ---------------------------------
    #  ATTACH PAGE SAFELY
    # ---------------------------------
    def attach_page(self, page):
        self.page = page

    # ---------------------------------
    #   EVENT HANDLER
    # ---------------------------------
    def on_event(self, event):

        # Agregar fila al log
        self.table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(event["time"])),
                    ft.DataCell(ft.Text(event["device"])),
                    ft.DataCell(ft.Text(event["action"])),
                    ft.DataCell(ft.Text(event["user"])),
                ]
            )
        )

        # Solo añadir valores del sistema (consumo)
        if event["device"] == "system":
            try:
                val = float(event["action"].split(": ")[1])
            except:
                val = 0

            self.values.append(val)
            if len(self.values) > self.max_points:
                self.values.pop(0)

            self.update_chart()

        self.safe_update()

    # ---------------------------------
    #   UPDATE BAR GRAPH
    # ---------------------------------
    def update_chart(self):
        if not self.values:
            return

        max_val = max(self.values) or 1

        for i in range(self.max_points):
            if i < len(self.values):
                value = self.values[i]
                h = int((value / max_val) * 280)
                self.bar_containers[i].height = h
                self.bar_containers[i].bgcolor = ft.Colors.CYAN
            else:
                self.bar_containers[i].height = 0

        self.safe_update()

    # ---------------------------------
    #   SAFE PAGE.UPDATE()
    # ---------------------------------
    def safe_update(self):
        if self.page and self.page.session:
            try:
                self.page.update()
            except:
                pass
