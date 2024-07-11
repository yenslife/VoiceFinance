import flet as ft
import requests
from api import API_URL

class ItemCard(ft.Container):
    def __init__(self, name="", width=80, content=None):
        super().__init__()
        self.name = name
        if content is None:
            content = ft.Text(name, width=width)
        if name != "":
            content.value = self.name
        self.content = content
        self.col = {"sm": 1.7, "md": 1.7, "xl": 1.7}
        self.padding = ft.padding.all(5)

class Item(ft.ResponsiveRow):
    def __init__(self, name, amount, location, date, create_at, id, note, page: ft.Page = None, search_func=None):
        super().__init__()
        self.page = page
        self.screen_size_setting = {"sm": 0.85, "md": 0.85, "xl": 0.85}
        self.name_text_card = ItemCard(name)
        self.name_edit_card = ItemCard(content=ft.TextField(name, width=100))
        self.amount_text_card = ItemCard(amount)
        self.amount_edit_card = ItemCard(content=ft.TextField(amount, width=100))
        self.location_text_card = ItemCard(location)
        self.location_edit_card = ItemCard(content=ft.TextField(location, width=100))
        self.date_text_card = ItemCard(date.replace("T00:00:00", ""))
        self.date_edit_card = ItemCard(content=ft.TextField(date.replace("T00:00:00", ""), width=100))
        self.create_at_text_card = ItemCard(create_at.replace("T", "\n"))
        self.note_text_card = ItemCard(note)
        self.note_edit_card = ItemCard(content=ft.TextField(note, width=100))
        self.id = id,
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=self.save)
        self.edit_button_container = ft.Container(self.edit_button, col=self.screen_size_setting)
        self.save_button_container = ft.Container(self.save_button, col=self.screen_size_setting)
        self.delte_button = ft.IconButton(icon=ft.icons.DELETE, on_click=self.delete)
        self.delete_button_container = ft.Container(self.delte_button, col=self.screen_size_setting)
        self.alignment = ft.MainAxisAlignment.CENTER
        self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete Item"),
            content=ft.Text("Are you sure to delete this item?"),
            actions=[
                ft.TextButton("Cancel", on_click=self.handleClose),
                ft.TextButton("Delete", on_click=self.handleDelete)
            ],
        )
        self.search_func = search_func
        self.controls = [
            # ft.Checkbox(),
            self.name_text_card,
            self.amount_text_card,
            self.location_text_card,
            self.date_text_card,
            self.note_text_card,
            self.create_at_text_card,
            self.edit_button_container,
            self.delete_button_container,
        ]

    def edit(self, e):
        self.controls.insert(0, self.name_edit_card)
        self.controls.remove(self.name_text_card)
        self.controls.insert(1, self.amount_edit_card)
        self.controls.remove(self.amount_text_card)
        self.controls.insert(2, self.location_edit_card)
        self.controls.remove(self.location_text_card)
        self.controls.insert(3, self.date_edit_card)
        self.controls.remove(self.date_text_card)
        self.controls.insert(5, self.note_edit_card)
        self.controls.remove(self.note_text_card)
        self.controls.insert(-1, self.save_button_container)
        self.controls.remove(self.edit_button_container)
        self.update()

    def save(self, e):
        self.controls.insert(0, self.name_text_card)
        self.controls.remove(self.name_edit_card)
        self.controls.insert(1, self.amount_text_card)
        self.controls.remove(self.amount_edit_card)
        self.controls.insert(2, self.location_text_card)
        self.controls.remove(self.location_edit_card)
        self.controls.insert(3, self.date_text_card)
        self.controls.remove(self.date_edit_card)
        self.controls.insert(5, self.note_text_card)
        self.controls.remove(self.note_edit_card)
        self.controls.insert(-1, self.edit_button_container)
        self.controls.remove(self.save_button_container)
        self.name_text_card.content = ItemCard(self.name_edit_card.content.value)
        self.amount_text_card.content = ItemCard(self.amount_edit_card.content.value)
        self.location_text_card.content = ItemCard(self.location_edit_card.content.value)
        self.date_text_card.content = ItemCard(self.date_edit_card.content.value)
        self.note_text_card.content = ItemCard(self.note_edit_card.content.value)
        response = requests.put(
            API_URL + "/items/" + str(self.id[0]), json={
                "name": self.name_edit_card.content.value,
                "amount": self.amount_edit_card.content.value,
                "location": self.location_edit_card.content.value,
                "date": self.date_edit_card.content.value,
                "create_at": self.create_at_text_card.content.value.replace("\n", "T"),
                "note": self.note_edit_card.content.value
                }
        )
        print(response.json())
        self.update()
    
    def handleClose(self, e):
        self.dlg_modal.open = False
        self.page.update()
        print("close")
    
    def handleDelete(self, e):
        print("delete")
        self.dlg_modal.open = False
        # delete
        try:
            print(self.id)
            response = requests.delete(API_URL + "/items/" + str(self.id[0]))
        except Exception as e:
            print(e)
        if response.status_code == 200:
            print("delete success")
        else:
            print("delete failed")
        self.search_func(None)

    def delete(self, e):
        # show delete check
        print("delete")
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

class AppBar(ft.AppBar):
    def __init__(self, title="Voice Finance 你的語音記帳系統", page: ft.Page = None):
        super().__init__()
        self.title = ft.Text(title)
        self.leading_width = 40
        self.center_title = False
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.theme_mode_icon_button = ft.IconButton(ft.icons.LIGHT_MODE_ROUNDED if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE_ROUNDED,
                                                    on_click=self.change_theme_mode)
        self.actions = [
            self.theme_mode_icon_button,
        ]
        self.page = page        

    def change_theme_mode(self, e):
        self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        # change icon
        self.theme_mode_icon_button.icon = ft.icons.LIGHT_MODE_ROUNDED if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE_ROUNDED
        self.page.update()