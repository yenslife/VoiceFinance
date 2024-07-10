import flet as ft
import requests
from api import API_URL
class Item(ft.ResponsiveRow):
    def __init__(self, name, amount, location, date, create_at, id, note):
        super().__init__()
        self.screen_size_setting = {"sm": 1.7, "md": 1.7, "xl": 1.7}
        self.name_text = ft.Text(name, width=80)
        self.text_edit = ft.TextField(name, width=100)
        self.name_text_container = ft.Container(self.name_text, col=self.screen_size_setting)
        self.text_edit_container = ft.Container(self.text_edit, col=self.screen_size_setting)
        self.amount_text = ft.Text(amount, width=80)
        self.location_text = ft.Text(location, width=80)
        self.date_text = ft.Text(date.replace("T00:00:00", ""), width=100)
        self.create_at_text = ft.Text(create_at.replace("T", "\n"), width=100)
        self.note_text = ft.Text(note, width=80)
        self.id = id,
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(icon=ft.icons.SAVE, on_click=self.save)
        self.edit_button_container = ft.Container(self.edit_button, col=1.7)
        self.save_button_container = ft.Container(self.save_button, col=1.7)
        self.alignment = ft.MainAxisAlignment.CENTER
        self.controls = [
            # ft.Checkbox(),
            self.name_text_container,
            ft.Container(self.amount_text, col=self.screen_size_setting),
            ft.Container(self.location_text, col=self.screen_size_setting),
            ft.Container(self.date_text, col=self.screen_size_setting),
            ft.Container(self.create_at_text, col=self.screen_size_setting),
            ft.Container(self.note_text, col=self.screen_size_setting),
            self.edit_button_container,
        ]

    def edit(self, e):
        self.controls.insert(0, self.text_edit_container)
        self.controls.remove(self.name_text_container)
        self.controls.insert(-1, self.save_button_container)
        self.controls.remove(self.edit_button_container)
        self.update()

    def save(self, e):
        self.controls.insert(0, self.name_text_container)
        self.controls.remove(self.text_edit_container)
        self.controls.insert(-1, self.edit_button_container)
        self.controls.remove(self.save_button_container)
        self.name_text.value = self.text_edit.value
        response = requests.put(
            API_URL + "/items/" + str(self.id[0]), json={
                "name": self.text_edit.value, 
                "amount": self.amount_text.value, 
                "location": self.location_text.value, 
                "date": self.date_text.value, 
                "create_at": self.create_at_text.value.replace("\n", "T"),
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
        self.theme_mode_icon_button = ft.IconButton(ft.icons.LIGHT_MODE_ROUNDED if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE_ROUNDED,
                                                    on_click=self.change_theme_mode)
        self.actions = [
            self.theme_mode_icon_button,
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

    def change_theme_mode(self, e):
        # print(type(e))
        self.page.theme_mode = ft.ThemeMode.DARK if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        # change icon
        self.theme_mode_icon_button.icon = ft.icons.LIGHT_MODE_ROUNDED if self.page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE_ROUNDED
        self.page.update()