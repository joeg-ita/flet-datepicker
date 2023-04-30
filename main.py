import flet as ft
from date_picker import DatePicker
from datetime import datetime

def main(page: ft.Page):

    picker = DatePicker(disable_to=datetime.now())
    picker_hm = DatePicker(hour_minute=True)
    selected = ft.Text(value=picker.selected_data)

    def confirm_dlg(e):
        selected.value = picker_hm.selected_data if c1.value else picker.selected_data
        dlg_modal.open = False
        page.update()
    
    def cancel_dlg(e):
        dlg_modal.open = False
        page.update()

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.content = picker_hm if c1.value else picker
        dlg_modal.open = True
        page.update()

    def with_hm(e):
        c1.label = "Datetime" if e.control.value else "Date"
        page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Date picker"),
        content=picker,
        actions=[
            ft.TextButton("Cancel", on_click=cancel_dlg),
            ft.TextButton("Confirm", on_click=confirm_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    c1 = ft.Checkbox(label="Date", value=False, on_change=with_hm)

    page.add(c1, ft.ElevatedButton("Select Date", on_click=open_dlg_modal), selected)
    page.update()

ft.app(target=main)