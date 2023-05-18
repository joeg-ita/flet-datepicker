import flet as ft
from date_picker import DatePicker
from datetime import datetime

class Example(ft.UserControl):

    def __init__(self):
        super().__init__()

        self.datepicker = None
        self.holidays = [datetime(2023, 4, 25), datetime(2023, 5, 1), datetime(2023, 6, 2)]
        self.locales = ["en_US", "fr_FR", "it_IT", "es_ES"]
        self.selected_locale = None

        self.locales_opts = []
        for l in self.locales:
            self.locales_opts.append(ft.dropdown.Option(l))

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
            width=40,
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

        self.c0 = ft.Switch(label="Select From - To date", value=False)
        self.c1 = ft.Switch(label="With hours and minutes", value=False)
        self.tf1 = ft.TextField(label="Disable days until date", dense=True, hint_text="yyyy-mm-dd hh:mm:ss", width=260, height=40)
        self.tf2 = ft.TextField(label="Disable days from date", dense=True, hint_text="yyyy-mm-dd hh:mm:ss", width=260, height=40)
        self.c2 = ft.Switch(label="Hide previous and next month days from current", value=False)
        self.c3 = ft.Switch(label="Shows three months", value=False)

        self.dd = ft.Dropdown(
            label="Locale",
            width=200,
            options=self.locales_opts,
            dense=True,
            on_change=self.set_locale
        )

        self.from_to_text = ft.Text(visible=False)

    def build(self):
        return ft.Column(
            [
            ft.Text("Datepicker options", size=24),
            ft.Divider(),
            self.c0,
            self.c1,
            self.c2,
            self.c3,
            ft.Row([self.tf1, self.tf2,]),
            self.dd,
            ft.Divider(),
            self.st,
            self.from_to_text
            ]
        )
    
    def confirm_dlg(self, e):
        if type(self.datepicker.selected_data) == datetime:
            self.tf.value = self.datepicker.selected_data
        else:
            self.from_to_text.value = f"{self.datepicker.selected_data[0]} - {self.datepicker.selected_data[1]}"
            self.from_to_text.visible = True
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
            select_from_to=self.c0.value,
            disable_to=self._to_datetime(self.tf1.value),
            disable_from=self._to_datetime(self.tf2.value),
            hide_prev_next_month_days=self.c2.value,
            holidays=self.holidays,
            show_three_months=self.c3.value,
            locale=self.selected_locale
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
        
    def set_locale(self, e):
        self.selected_locale = self.dd.value if self.dd.value else None