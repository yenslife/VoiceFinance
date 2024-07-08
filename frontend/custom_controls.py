import flet as ft
class Task(ft.Row):
    def __init__(self, text):
        super().__init__()
        self.text_view = ft.Text(text)
        self.text_edit = ft.TextField(text, visible=False)
        self.edit_button = ft.IconButton(icon=ft.icons.EDIT, on_click=self.edit)
        self.save_button = ft.IconButton(
            visible=False, icon=ft.icons.SAVE, on_click=self.save
        )
        self.controls = [
            ft.Checkbox(),
            self.text_view,
            self.text_edit,
            self.edit_button,
            self.save_button,
        ]

    def edit(self, e):
        self.edit_button.visible = False
        self.save_button.visible = True
        self.text_view.visible = False
        self.text_edit.visible = True
        self.update()

    def save(self, e):
        self.edit_button.visible = True
        self.save_button.visible = False
        self.text_view.visible = True
        self.text_edit.visible = False
        self.text_view.value = self.text_edit.value
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