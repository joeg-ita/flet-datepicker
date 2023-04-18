import flet as ft 
import calendar
from datetime import datetime
from datetime import timedelta

class DatePicker(ft.UserControl):

    @property
    def selected_data(self):
        return self.selected
    
    PREV_MONTH = "PM"
    NEXT_MONTH = "NM"
    PREV_YEAR = "PY"
    NEXT_YEAR = "NY"

    PREV_HOUR = "PH"
    NEXT_HOUR = "NH"
    PREV_MINUTE = "PMIN"
    NEXT_MINUTE  = "NMIN"

    EMPTY = ""
    WHITE_SPACE = " "

    DELTA_MONTH_WEEK = 4
    DELTA_YEAR_WEEK = 52
    DELTA_HOUR = 1
    DELTA_MINUTE = 1

    def __init__(self, hour_minute: bool = False):
        super().__init__()
        self.selected = None
        self.hour_minute = hour_minute
        self.now = datetime.now()

        self.yy = self.now.year
        self.mm = self.now.month
        self.dd = self.now.day
        self.hour = self.now.hour
        self.minute = self.now.minute
        self.cal = calendar.Calendar()
        self.days = self.cal.monthdays2calendar(self.yy, self.mm)
        self.month_name_text = ft.Text(calendar.month_name[self.mm], text_align='center')
        self.create_calendar()

    def create_calendar(self):

        ym = self.year_month_selectors()
        
        labels = ft.Row(self.row_labels(), spacing=10, expand=True)

        self.week_rows_controls = []
        self.week_rows_controls.append(ym)
        self.week_rows_controls.append(labels)

        self.weeks_rows_num = len(self.cal.monthdayscalendar(self.yy, self.mm))
        today = datetime.now()

        for w in range(0, self.weeks_rows_num):
            row = []
            for d in self.days[w]:
                day = d[0] if d[0] > 0 else self.EMPTY

                # week end bg color
                if d[1] == 5 or d[1] == 6:
                    text_color = ft.colors.RED_50
                else:
                    text_color = None

                # current day bg
                if day == self.dd and self.dd == today.day and self.mm == today.month and self.yy == today.year:
                    bg = ft.colors.BLUE
                    text_color = ft.colors.WHITE
                else:
                    bg = None

                # selected day 
                if self.selected and day == self.selected[2] and self.mm == self.selected[1] and self.yy == self.selected[0]:
                    bg = ft.colors.GREEN
                    text_color = ft.colors.WHITE             
                
                row.append(
                    ft.Container(
                        ft.OutlinedButton(
                                text=str(day), 
                                data=(self.yy, self.mm, day), 
                                style=ft.ButtonStyle(
                                    color=text_color,
                                    bgcolor=bg, 
                                    padding=0, 
                                    shape={
                                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                                    }
                                ), 
                                on_click=self.select_date), 
                                width=48,
                        ))
            
            self.week_rows_controls.append(ft.Row(row, spacing=10, expand=True))
    
        if self.hour_minute:
            hm = self.hour_minute_selector()
            self.week_rows_controls.append(hm)
    
    def year_month_selectors(self):
        ym = ft.Row([
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_YEAR, on_click=self.adjust_calendar),
                        ft.Container(ft.Text(self.yy), padding=ft.Padding(5,1,5,1),
                                     border=ft.Border(
                                            top=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            left=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            bottom=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            right=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100))
                                    ),
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_YEAR, on_click=self.adjust_calendar),
                    ]),
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_MONTH, on_click=self.adjust_calendar),
                        ft.Container(self.month_name_text, padding=ft.Padding(5,1,5,1), width=100,
                                     border=ft.Border(
                                            top=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            left=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            bottom=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            right=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100))),
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_MONTH, on_click=self.adjust_calendar),
                    ]),
                ], spacing=48, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                
        return ym

    def row_labels(self):
        label_row = []
        days_label = calendar.weekheader(2).split(self.WHITE_SPACE)
        for l in days_label:
            label_row.append(
                ft.OutlinedButton(
                    text=l, 
                    width=48, 
                    style=ft.ButtonStyle(
                        padding=0, 
                        bgcolor=ft.colors.AMBER_50, 
                        shape={
                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=2),
                        }
                        )
                    )
                )
                
        return label_row
    
    def hour_minute_selector(self):
        hm = ft.Row([
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_HOUR, on_click=self.adjust_hh_min),
                        ft.Container(content=ft.Text(self.hour), padding=ft.Padding(5,1,5,1),
                                     border=ft.Border(
                                            top=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            left=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            bottom=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            right=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100))
                                    ),
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_HOUR, on_click=self.adjust_hh_min),
                    ]),
                    ft.Text(":"),
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_MINUTE, on_click=self.adjust_hh_min),
                        ft.Container(content=ft.Text(self.minute), padding=ft.Padding(5,1,5,1), 
                                     border=ft.Border(
                                            top=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            left=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            bottom=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100), 
                                            right=ft.BorderSide(width=1, color=ft.colors.BLUE_GREY_100))
                                    ),
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_MINUTE, on_click=self.adjust_hh_min),
                    ]),
                ], spacing=48, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                
        return hm
    
    
    def build(self):  
        self.jcal=ft.Column(self.week_rows_controls, height=300, width=400) 
        return self.jcal
    
    def select_date(self, e: ft.ControlEvent):
        
        result = list(e.control.data)

        if self.selected and self.selected[0] == result[0] and self.selected[1] == result[1] and self.selected[2] == result[2]:
            self.selected = None
        else:
            if self.hour_minute:
                result.append(self.hour)
                result.append(self.minute)
            self.selected = result
        self.update_calendar()

    def adjust_calendar(self, e: ft.ControlEvent):

        if(e.control.data == self.PREV_MONTH or e.control.data == self.NEXT_MONTH):
            delta = timedelta(weeks=self.DELTA_MONTH_WEEK)
        if(e.control.data == self.PREV_YEAR or e.control.data == self.NEXT_YEAR):
            delta = timedelta(weeks=self.DELTA_YEAR_WEEK)

        if(e.control.data == self.PREV_MONTH or e.control.data == self.PREV_YEAR):
            self.now = self.now - delta
        if(e.control.data == self.NEXT_MONTH or e.control.data == self.NEXT_YEAR):
            self.now = self.now + delta

        self.mm = self.now.month
        self.yy = self.now.year
        self.month_name_text.value=calendar.month_name[self.mm]
        self.days = self.cal.monthdays2calendar(self.yy,self.mm)
        self.update_calendar()

    def adjust_hh_min(self, e: ft.ControlEvent):

        if(e.control.data == self.PREV_HOUR or e.control.data == self.NEXT_HOUR):
            delta = timedelta(hours=self.DELTA_HOUR)
        if(e.control.data == self.PREV_MINUTE or e.control.data == self.NEXT_MINUTE):
            delta = timedelta(minutes=self.DELTA_MINUTE)

        if(e.control.data == self.PREV_HOUR or e.control.data == self.PREV_MINUTE):
            self.now = self.now - delta
        if(e.control.data == self.NEXT_HOUR or e.control.data == self.NEXT_MINUTE):
            self.now = self.now + delta

        self.hour = self.now.hour
        self.minute = self.now.minute
        self.month_name_text.value=calendar.month_name[self.mm]
        self.days = self.cal.monthdays2calendar(self.yy,self.mm)
        self.update_calendar()

    def update_calendar(self):
        self.create_calendar()
        self.jcal.controls= self.week_rows_controls
        self.update()