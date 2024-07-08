import flet as ft
from custom_controls import AppBar

def main_page(page: ft.Page):
    # view
    appbar = AppBar(page=page)
    welcome_text = ft.Text("歡迎使用 VoiceFinance", size=24)
    to_recording_btn = ft.ElevatedButton(text="記帳", on_click=lambda _: page.go("/recording"))
    to_search_btn = ft.ElevatedButton(text="查詢", on_click=lambda _: page.go("/search"))

    page.views.append(
        ft.View(
            "/",
            [
                appbar,
                welcome_text,
                to_recording_btn,
                to_search_btn
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    )