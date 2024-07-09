import flet as ft
import requests
from api import API_URL
class Item(ft.Row):
    def __init__(self, name, amount, location, date, create_at, id, note):
        super().__init__()
        self.name_text = ft.Text(name)
        self.amount_text = ft.Text(amount)
        self.location_text = ft.Text(location)
        self.date_text = ft.Text(date)
        self.create_at_text = ft.Text(create_at)
        self.note_text = ft.Text(note)
        self.id = id,
        self.text_edit = ft.TextField(name, visible=False, width=100)
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(
            visible=False, icon=ft.icons.SAVE, on_click=self.save
        )
        self.controls = [
            ft.Row(
                [
                    ft.Checkbox(),
                    self.name_text,
                    self.text_edit,
                    self.amount_text,
                    self.location_text,
                    self.date_text,
                    self.create_at_text,
                    self.note_text,
                    self.edit_button,
                    self.save_button
                ]
            )
        ]

    def edit(self, e):
        self.edit_button.visible = False
        self.save_button.visible = True
        self.name_text.visible = False
        self.text_edit.visible = True
        self.update()

    def save(self, e):
        self.edit_button.visible = True
        self.save_button.visible = False
        self.name_text.visible = True
        self.text_edit.visible = False
        self.name_text.value = self.text_edit.value
        response = requests.put(
            API_URL + "/items/" + str(self.id[0]), json={
                "name": self.text_edit.value, 
                "amount": self.amount_text.value, 
                "location": self.location_text.value, 
                "date": self.date_text.value, 
                "create_at": self.create_at_text.value,
                "note": self.note_text.value
                }
        )
        print(response.json())
        self.update()
class AppBar(ft.AppBar):
    def __init__(self, title="Voice Finance 你的語音記帳系統", page: ft.Page = None):
        super().__init__()
        self.title = ft.Text(title)
        # self.leading = ft.Icon(ft.icons.PALETTE)
        self.leading_width = 40
        self.center_title = False
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.actions = [
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    # ft.PopupMenuItem(
                    #     text="Checked item", checked=False, on_click=check_item_clicked
                    # ),
                ]
            ),
        ]
        self.page = page        