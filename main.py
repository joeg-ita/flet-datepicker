import flet as ft
from date_picker import DatePicker
from example import Example

def main(page: ft.Page):

    examples = Example()

    page.add(examples)
    page.update()

ft.app(target=main)
