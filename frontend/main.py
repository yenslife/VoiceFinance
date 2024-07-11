import flet as ft

# pages
from pages.main_page import main_page
from pages.record_page import recording_page
from pages.search_page import search_page

# GUI part
def main(page: ft.Page):
    # GUI的排版
    page.title = "Voice Finance 你的語音記帳系統"
    page.window_width = 850
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(route):
        page.views.clear()
        main_page(page)
        if page.route == "/recording":
            recording_page(page)
        elif page.route == "/search":
            search_page(page)
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.YELLOW,
    )
    page.theme_mode = ft.ThemeMode.LIGHT
    page.go(page.route)

ft.app(target=main)