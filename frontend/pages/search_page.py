import flet as ft
import requests
from custom_controls import AppBar, Item
from api import API_URL

def keyword_search_request(query: str):
    response = requests.get(API_URL + "/search_items", params={"name": query})
    return response.json()

def search_page(page: ft.Page):
    appbar = AppBar(page=page)
    item_list_view = ft.ListView([], height=370)

    def search(e):
        nonlocal item_list_view
        query = search_bar.value
        response = keyword_search_request(query)
        items = []
        item_list_view.controls = []
        for item in response:
            print(item)
            item_obj = Item(name=item['name'], 
                            amount=item['amount'], 
                            location=item['location'], 
                            date=item['date_'], 
                            create_at=item['create_at'], 
                            id=item['id'],
                            note=item['note'])
            items.append(item_obj)
        item_list_view.controls.extend(items)
        page.update()

    search_bar = ft.TextField(
        label="Search",
        on_change=search,
        width=400
    )

    search(None)
    screen_size_setting = {"sm": 1.7, "md": 1.7}
    header_row = ft.ResponsiveRow([
        ft.Container(
            ft.Text("Name", weight=ft.FontWeight.BOLD, width=80),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Amount", weight=ft.FontWeight.BOLD, width=80),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Location", weight=ft.FontWeight.BOLD, width=80),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Date", weight=ft.FontWeight.BOLD, width=100),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Create At", weight=ft.FontWeight.BOLD, width=100),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Note", weight=ft.FontWeight.BOLD, width=80),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Action", weight=ft.FontWeight.BOLD, width=80),
            col=screen_size_setting
        )
        # ft.Text("Amount", weight=ft.FontWeight.BOLD, width=80),
        # ft.Text("Location", weight=ft.FontWeight.BOLD, width=80),
        # ft.Text("Date", weight=ft.FontWeight.BOLD, width=100),
        # ft.Text("Create At", weight=ft.FontWeight.BOLD, width=100),
        # ft.Text("Note", weight=ft.FontWeight.BOLD, width=80)
    ])

    view_list = [ appbar,
                ft.Text("搜尋名字"),
                search_bar,
                header_row,
                item_list_view
                ]

    page.views.append(
        ft.View(
            "/search",
            view_list,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
