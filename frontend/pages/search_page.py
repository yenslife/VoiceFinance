import flet as ft
from custom_controls import AppBar

def search_page(page: ft.Page):
    appbar = AppBar(page=page)
    page.views.append(
        ft.View(
            "/search",
            [
                appbar,
                ft.Text("search page")
            ]
        )
    )
    print("search page")