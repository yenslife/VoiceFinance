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

    def handleClose(e):
        dlg_modal.open = False
        page.update()
        print("close")
    
    def handleDelete(e):
        print("delete")
        dlg_modal.open = False
        # delete
        try:
            response = requests.delete(API_URL + "/items/" + str(select_target_id))
        except Exception as e:
            print(e)
        if response.status_code == 200:
            print("delete success")
        else:
            print("delete failed")
        search(None)
        page.update
        
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Delete Item"),
        content=ft.Text("Are you sure to delete this item?"),
        actions=[
            ft.TextButton("Cancel", on_click=handleClose),
            ft.TextButton("Delete", on_click=handleDelete)
        ],
    )

    select_target_id = None
    def item_onclick(e):
        nonlocal select_target_id
        # show delete check
        item_id = e.control.content.id[0]
        page.dialog = dlg_modal
        dlg_modal.open = True
        select_target_id = item_id
        page.update()

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
            items.append(ft.Container(item_obj, 
                                      border=ft.border.all(1),
                                      border_radius=ft.border_radius.all(10),
                                      padding=ft.padding.all(1),
                                      margin=ft.margin.all(10),
                                      on_click=item_onclick,))
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
            ft.Text("Note", weight=ft.FontWeight.BOLD, width=80),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Create At", weight=ft.FontWeight.BOLD, width=100),
            col=screen_size_setting
        ),
        ft.Container(
            ft.Text("Action", weight=ft.FontWeight.BOLD, width=80),
            col=screen_size_setting
        )
    ])

    view_list = [ appbar,
                ft.Text("搜尋名字"),
                search_bar,
                header_row,
                item_list_view,
                ]

    page.views.append(
        ft.View(
            "/search",
            view_list,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
