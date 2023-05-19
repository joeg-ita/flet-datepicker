import locale as loc
import flet as ft 
import calendar
from datetime import datetime, timedelta

class DatePicker(ft.UserControl):

    @property
    def selected_data(self):
        if self.is_from_to:
            return self.selected, self.selected_to
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

    DELTA_MONTH_WEEK = 5
    DELTA_YEAR_WEEK = 52
    DELTA_HOUR = 1
    DELTA_MINUTE = 1

    WEEKEND_DAYS = [5, 6]

    CELL_SIZE = 32
    LAYOUT_WIDTH = 340
    LAYOUT_MIN_HEIGHT = 280
    LAYOUT_MAX_HEIGHT = 320
    LAYOUT_DT_MIN_HEIGHT = 320
    LAYOUT_DT_MAX_HEIGHT = 360

    def __init__(self, 
            hour_minute: bool = False, 
            selected_date: datetime | tuple[datetime, datetime | None] = None,
            select_from_to: bool=True,
            disable_to: datetime = None, 
            disable_from: datetime = None,
            holidays: list[datetime] = None,
            hide_prev_next_month_days: bool = False,
            first_weekday: int = 0,
            show_three_months: bool = False,
            locale: str = None
        ):
        super().__init__()
        self.selected = selected_date
        self.is_from_to = select_from_to and not hour_minute
        self.hour_minute = hour_minute
        self.disable_to = disable_to
        self.disable_from  = disable_from
        self.holidays  = holidays
        self.hide_prev_next_month_days = hide_prev_next_month_days
        self.first_weekday = first_weekday
        self.show_three_months = show_three_months
        if locale: loc.setlocale(loc.LC_ALL, locale)

        self.selected_to = None
        self.now = datetime.now()
        self.yy = self.now.year 
        self.mm = self.now.month 
        self.dd = self.now.day
        self.hour = self.now.hour if not selected_date else selected_date.hour
        self.minute = self.now.minute if not selected_date else selected_date.minute
        self.cal = calendar.Calendar(first_weekday)

    def _get_current_month(self, year, month):
        return self.cal.monthdatescalendar(year, month)

    def _create_calendar(self, year, month, hour, minute, hide_ymhm = False):
        
        week_rows_controls = []
        week_rows_days_controls = []
        today = datetime.now()

        days = self._get_current_month(year, month)

        ym = self._year_month_selectors(year, month, hide_ymhm)
        week_rows_controls.append(ft.Column([ym], alignment=ft.MainAxisAlignment.START))
        
        labels = ft.Row(self._row_labels(), spacing=18)
        week_rows_controls.append(ft.Column([labels], alignment=ft.MainAxisAlignment.START))

        weeks_rows_num = len(self._get_current_month(year, month))

        for w in range(0, weeks_rows_num):
            row = []
            
            for d in days[w]:

                d = datetime(d.year, d.month, d.day, self.hour, self.minute) if self.hour_minute else datetime(d.year, d.month, d.day)

                month = d.month
                is_main_month = True if month == self.mm else False
                
                if self.hide_prev_next_month_days and not is_main_month:
                    row.append(ft.Text("", width=self.CELL_SIZE, height=self.CELL_SIZE,))
                    continue

                dt_weekday = d.weekday()
                day = d.day
                is_weekend = False
                is_holiday = False

                is_day_disabled = False

                if self.disable_from and self._trunc_datetime(d) > self._trunc_datetime(self.disable_from):
                    is_day_disabled = True
                
                if self.disable_to and self._trunc_datetime(d) < self._trunc_datetime(self.disable_to):
                    is_day_disabled = True
                
                text_color = None   
                border_side = None 
                bg = None
                # week end bg color
                if dt_weekday in self.WEEKEND_DAYS:
                    text_color = ft.colors.RED_500
                    is_weekend = True
                # holidays
                if self.holidays and d in self.holidays:
                    text_color = ft.colors.RED_500
                    is_holiday = True                    

                # current day bg
                if is_main_month and day == self.dd and self.dd == today.day and self.mm == today.month and self.yy == today.year:
                    border_side = ft.BorderSide(2, ft.colors.BLUE)
                elif (is_weekend or is_holiday) and (not is_main_month or is_day_disabled):
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

                # selected days 
                if  (self.selected and self.selected == d) or (self.selected_to and self.selected_to == d):
                    bg = ft.colors.BLUE_400
                    text_color = ft.colors.WHITE 

                if self.is_from_to and self.selected and self.selected_to:
                    if d > self.selected and d < self.selected_to:
                        bg = ft.colors.BLUE_300
                        text_color = ft.colors.WHITE 
                
                row.append(
                    ft.TextButton(
                        text=str(day), 
                        data=d, 
                        width=self.CELL_SIZE,
                        height=self.CELL_SIZE,
                        disabled=is_day_disabled,
                        style=ft.ButtonStyle(
                            color=text_color,
                            bgcolor=bg, 
                            padding=0, 
                            shape={
                                ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=20),
                            },
                            side=border_side
                        ), 
                    on_click=self._select_date) 
                )
            
            week_rows_days_controls.append(ft.Row(row, spacing=18))
        
        week_rows_controls.append(ft.Column(week_rows_days_controls, alignment=ft.MainAxisAlignment.START, spacing=0))

        if self.hour_minute and not hide_ymhm:
            hm = self._hour_minute_selector(hour, minute)
            week_rows_controls.append(ft.Row([hm], alignment=ft.MainAxisAlignment.CENTER))

        return week_rows_controls
    
    def _year_month_selectors(self, year, month, hide_ymhm = False):
        prev_year = ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_YEAR, on_click=self._adjust_calendar) if not hide_ymhm else ft.Text(self.EMPTY, height=self.CELL_SIZE,)
        next_year = ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_YEAR, on_click=self._adjust_calendar) if not hide_ymhm else ft.Text(self.EMPTY)
        prev_month = ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_MONTH, on_click=self._adjust_calendar) if not hide_ymhm else ft.Text(self.EMPTY)
        next_month = ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_MONTH, on_click=self._adjust_calendar) if not hide_ymhm else ft.Text(self.EMPTY)
        ym = ft.Row([
                    ft.Row([
                        prev_year,
                        ft.Text(year),
                        next_year,
                    ], spacing=0),
                    ft.Row([
                        prev_month,
                        ft.Text(calendar.month_name[month], text_align=ft.alignment.center),
                        next_month,
                    ], spacing=0),
                ], spacing=0, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                
        return ym

    def _row_labels(self):
        label_row = []
        days_label = calendar.weekheader(2).split(self.WHITE_SPACE)
        for i in range(0, self.first_weekday): days_label.append(days_label.pop(0))
        for l in days_label:
            label_row.append(
                ft.TextButton(
                    text=l, 
                    width=self.CELL_SIZE, 
                    height=self.CELL_SIZE,
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
    
    def _hour_minute_selector(self, hour, minute):
        hm = ft.Row(
            [
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_HOUR, on_click=self._adjust_hh_min),
                    ft.Text(hour),
                    ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_HOUR, on_click=self._adjust_hh_min),
                ]),
                ft.Text(":"),
                ft.Row([
                    ft.IconButton(icon=ft.icons.ARROW_BACK, data=self.PREV_MINUTE, on_click=self._adjust_hh_min),
                    ft.Text(minute),
                    ft.IconButton(icon=ft.icons.ARROW_FORWARD, data=self.NEXT_MINUTE, on_click=self._adjust_hh_min),
                ]),
            ], spacing=48, alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                
        return hm

    def build(self):  
        
        rows = self._create_layout(self.yy, self.mm, self.hour, self.minute)

        cal_height = self._calculate_heigth(self.yy, self.mm)

        self.cal_container = ft.Container(
            content=ft.Row(rows),
            bgcolor=ft.colors.WHITE,
            padding=12,
            height=self._cal_height(cal_height)
        )
        return self.cal_container

    def _calculate_heigth(self, year, month):
        if self.show_three_months:
            prev, next = self._prev_next_month(year, month)
            cal_height = max(
                len(self._get_current_month(year, month)),
                len(self._get_current_month(prev.year, prev.month)),
                len(self._get_current_month(next.year, next.month))
            )
        else:
            cal_height = len(self._get_current_month(year, month))
        return cal_height

    def _create_layout(self, year, month, hour, minute):
        rows = []
        prev, next = self._prev_next_month(year, month)
        
        if self.show_three_months:
            week_rows_controls_prev = self._create_calendar(prev.year, prev.month, hour, minute, True)
            rows.append(ft.Column(week_rows_controls_prev, width=self.LAYOUT_WIDTH, spacing=10))
            rows.append(ft.VerticalDivider())

        week_rows_controls = self._create_calendar(year, month, hour, minute)
        rows.append(ft.Column(week_rows_controls, width=self.LAYOUT_WIDTH, spacing=10))
            
        if self.show_three_months:
            rows.append(ft.VerticalDivider())
            week_rows_controls_next= self._create_calendar(next.year, next.month, hour, minute, True)
            rows.append(ft.Column(week_rows_controls_next, width=self.LAYOUT_WIDTH, spacing=10))

        return rows

    def _prev_next_month(self, year, month):
        delta = timedelta(weeks=self.DELTA_MONTH_WEEK)
        current = datetime(year, month, 15)
        prev = current - delta
        next = current + delta
        return prev,next
    
    def _select_date(self, e: ft.ControlEvent):
        
        result: datetime = e.control.data
        print(result)
        print(self.selected)

        if self.is_from_to:
            if self.selected and self.selected_to:
                self.selected = self.selected_to = None

            if self.selected and self.selected is not None:
                if self.selected == result:
                    self.selected = None 
                else:
                    if result > self.selected:
                        if self.selected_to is None:
                            self.selected_to = result   
                        else:
                            return
                    else:
                        return
            else:
                self.selected = result        
        else:
            if self.selected and self.selected == result:
                self.selected = None
            else:
                if self.hour_minute:
                    result = datetime(result.year, result.month, result.day, self.hour, self.minute)
                self.selected = result

        self._update_calendar()

    def _adjust_calendar(self, e: ft.ControlEvent):

        print(self.yy, self.mm)

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
        self._update_calendar()

    def _adjust_hh_min(self, e: ft.ControlEvent):

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
        self._update_calendar()

    def _update_calendar(self):
        self.cal_container.content = ft.Row(self._create_layout(self.yy, self.mm, self.hour, self.minute))
        cal_height = self._calculate_heigth(self.yy, self.mm)
        self.cal_container.height = self._cal_height(cal_height)
        self.update()

    def _cal_height(self, weeks_number):
        if self.hour_minute:
            return self.LAYOUT_DT_MIN_HEIGHT if weeks_number == 5 else self.LAYOUT_DT_MAX_HEIGHT
        else:
            return self.LAYOUT_MIN_HEIGHT if weeks_number == 5 else self.LAYOUT_MAX_HEIGHT
        
    def _trunc_datetime(self, date):
        return date.replace(hour=0, minute=0, second=0, microsecond=0)