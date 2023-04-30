from typing import List
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

    WEEKEND_DAYS = [5, 6]

    def __init__(self, 
            hour_minute: bool = False, 
            selected_date: datetime = None,
            disable_to: datetime = None, 
            disable_from: datetime = None,
            holidays: List[datetime] = None,
            hide_prev_next_month_days: bool = False,
            first_weekday: int = 0
        ):
        super().__init__()
        self.selected = None
        self.hour_minute = hour_minute
        self.now = datetime.now() if not selected_date else selected_date
        self.disable_to = disable_to
        self.disable_from  = disable_from
        self.holidays  = holidays
        self.hide_prev_next_month_days = hide_prev_next_month_days
        self.first_weekday = first_weekday

        self.yy = self.now.year
        self.mm = self.now.month
        self.dd = self.now.day
        self.hour = self.now.hour
        self.minute = self.now.minute
        self.cal = calendar.Calendar(first_weekday)
        self.days = self._get_current_month()
        self.month_name_text = ft.Text(calendar.month_name[self.mm], text_align='center')
        self.create_calendar()

    def _get_current_month(self):
        return self.cal.monthdatescalendar(self.yy, self.mm)

    def create_calendar(self):

        ym = self.year_month_selectors()
        
        labels = ft.Row(self.row_labels(), spacing=18)

        self.week_rows_controls = []
        self.week_rows_controls.append(ft.Column([ym], alignment=ft.MainAxisAlignment.START))
        self.week_rows_controls.append(ft.Column([labels], alignment=ft.MainAxisAlignment.START))
        self.week_rows_days_controls = []

        self.weeks_rows_num = len(self._get_current_month())
        today = datetime.now()

        for w in range(0, self.weeks_rows_num):
            row = []
            
            for d in self.days[w]:

                d = datetime(d.year, d.month, d.day, self.hour, self.minute) if self.hour_minute else datetime(d.year, d.month, d.day)
                dt_weekday = d.weekday()
                day = d.day
                month = d.month
                is_main_month = True if month == self.mm else False
                is_weekend = False
                
                is_day_disabled = False

                if self.disable_from and self._trunc_datetime(d) > self._trunc_datetime(self.disable_from):
                    is_day_disabled = True
                
                if self.disable_to and self._trunc_datetime(d) < self._trunc_datetime(self.disable_to):
                    is_day_disabled = True
                    
                # week end bg color
                if dt_weekday in self.WEEKEND_DAYS:
                    text_color = ft.colors.RED_500
                    is_weekend = True
                else:
                    text_color = None

                # current day bg
                if is_main_month and day == self.dd and self.dd == today.day and self.mm == today.month and self.yy == today.year:
                    bg = ft.colors.BLUE
                    text_color = ft.colors.WHITE
                elif is_weekend and (not is_main_month or is_day_disabled):
                    text_color = ft.colors.RED_200
                    bg = None
                elif not is_main_month and is_day_disabled:
                    text_color = ft.colors.BLACK38
                    bg = None
                elif not is_main_month:
                    text_color = ft.colors.BLUE_200
                    bg = None
                else:
                    bg = None

                # selected day 
                if  self.selected and self.selected == d:
                    bg = ft.colors.GREEN
                    text_color = ft.colors.WHITE             
                
                row.append(
                    ft.TextButton(
                        text=str(day), 
                        data=d, 
                        width=36,
                        height=36,
                        disabled=is_day_disabled,
                        style=ft.ButtonStyle(
                            color=text_color,
                            bgcolor=bg, 
                            padding=0, 
                            shape={
                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=20),
                            }
                        ), 
                    on_click=self.select_date) 
                )
            
            self.week_rows_days_controls.append(ft.Row(row, spacing=18))
        
        self.week_rows_controls.append(ft.Column(self.week_rows_days_controls, alignment=ft.MainAxisAlignment.START, spacing=0))

        if self.hour_minute:
            hm = self.hour_minute_selector()
            self.week_rows_controls.append(hm)
    
    def year_month_selectors(self):
        ym = ft.Row([
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_YEAR, on_click=self.adjust_calendar),
                        ft.Text(self.yy),
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_YEAR, on_click=self.adjust_calendar),
                    ], spacing=0),
                    ft.Row([
                        ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_MONTH, on_click=self.adjust_calendar),
                        self.month_name_text,
                        ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_MONTH, on_click=self.adjust_calendar),
                    ], spacing=0),
                ], spacing=0, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                
        return ym

    def row_labels(self):
        label_row = []
        days_label = calendar.weekheader(2).split(self.WHITE_SPACE)
        for i in range(0, self.first_weekday): days_label.append(days_label.pop(0))
        for l in days_label:
            label_row.append(
                ft.TextButton(
                    text=l, 
                    width=36, 
                    height=36,
                    disabled=True,
                    style=ft.ButtonStyle(
                        padding=0, 
                        color=ft.colors.BLACK,
                        bgcolor=ft.colors.GREY_300, 
                        shape={
                            ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=20),
                        }
                    )
                )
            )
                
        return label_row
    
    def hour_minute_selector(self):
        hm = ft.Row(
            [
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_HOUR, on_click=self.adjust_hh_min),
                    ft.Text(self.hour),
                    ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_HOUR, on_click=self.adjust_hh_min),
                ]),
                ft.Text(":"),
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_MINUTE, on_click=self.adjust_hh_min),
                    ft.Text(self.minute),
                    ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_MINUTE, on_click=self.adjust_hh_min),
                ]),
            ], spacing=48, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                
        return hm

    def build(self):  
        self.jcal=ft.Column(self.week_rows_controls, width=360, spacing=10) 
        self.cal_container = ft.Container(
            content=self.jcal,
            bgcolor=ft.colors.WHITE,
            padding=12,
            height=self._cal_height()
        )
        return self.cal_container
    
    def select_date(self, e: ft.ControlEvent):
        
        result: datetime = e.control.data
        print(result)
        print(self.selected)

        if self.selected and self.selected == result:
            self.selected = None
        else:
            if self.hour_minute:
                result = datetime(result.year, result.month, result.day, self.hour, self.minute)
            self.selected = result
        self._update_calendar()

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
        self.days = self._get_current_month()
        self._update_calendar()

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
        self.days = self._get_current_month()
        self._update_calendar()

    def _update_calendar(self):
        self.create_calendar()
        self.cal_container.height = self._cal_height()
        self.jcal.controls = self.week_rows_controls
        self.update()

    def _cal_height(self):
        if self.hour_minute:
            return 360 if self.weeks_rows_num == 5 else 400
        else:
            return 300 if self.weeks_rows_num == 5 else 340
        
    def _trunc_datetime(self, date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)