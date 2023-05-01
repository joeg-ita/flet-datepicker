import flet as ft
from date_picker import DatePicker
from datetime import datetime

class Example(ft.UserControl):

    def __init__(self):
        super().__init__()

        self.datepicker = None

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Date picker"),
            actions=[
                ft.TextButton("Cancel", on_click=self.cancel_dlg),
                ft.TextButton("Confirm", on_click=self.confirm_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.tf = ft.TextField(label="Select Date", dense=True, hint_text="yyyy-mm-ddThh:mm:ss", width=260, height=40)
        self.cal_ico = ft.TextButton(
            icon=ft.icons.CALENDAR_MONTH, 
            on_click=self.open_dlg_modal, 
            height=40,
            width=48,
            right=0,
            style=ft.ButtonStyle(
                padding=ft.Padding(4,0,0,0),
                shape={
                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=1),
                    },
            ))

        self.st = ft.Stack(
            [
                self.tf,
                self.cal_ico,
            ]
        )

        self.c1 = ft.Switch(label="With hours and minutes", value=False)
        self.tf1 = ft.TextField(label="Disable days until date", dense=True, hint_text="yyyy-mm-dd hh:mm:ss", width=260, height=40)
        self.tf2 = ft.TextField(label="Disable days from date", dense=True, hint_text="yyyy-mm-dd hh:mm:ss", width=260, height=40)
        self.c2 = ft.Switch(label="Hide previous and next month days from current", value=False)

    def build(self):
        return ft.Column(
            [
            ft.Text("Datepicker options", size=24),
            ft.Divider(),
            self.c1,
            self.c2,
            ft.Row([self.tf1, self.tf2,]),
            ft.Divider(),
            self.st
            ]
        )
    
    def confirm_dlg(self, e):
        self.tf.value = self.datepicker.selected_data
        self.dlg_modal.open = False
        self.update()
        self.page.update()
    
    def cancel_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def open_dlg_modal(self, e):
        self.datepicker = DatePicker(
            hour_minute=self.c1.value,
            selected_date=self.tf.value,
            disable_to=self._to_datetime(self.tf1.value),
            disable_from=self._to_datetime(self.tf2.value),
            hide_prev_next_month_days=self.c2.value
            )
        self.page.dialog = self.dlg_modal
        self.dlg_modal.content = self.datepicker
        self.dlg_modal.open = True
        self.page.update()

    def _to_datetime(self, date_str=None):
        if date_str:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        else:
            return None