import os
import datetime
import flet as ft
from MyLife import MyLife
from Process import Process
from ProcessesManagerDC import ProcessesManagerDC


def main(page: ft.Page):
    path = Process.path
    if len(os.listdir(path)) == 0:
        _ = MyLife.create_first_process()
    pm = ProcessesManagerDC(path)
    pm.deserialization()
    page.process_name = pm.first_process_name
    page.sorting_mode = 0

    page.title = "Flet Debt Counter"
    page.window.width = 777
    page.scroll = True
    page.process_tree = ft.Text()

    def change_process_name(name):
        def fun(e):
            page.process_name = name
            page.date_text = 'select a date for reminder'
            page.time_text = 'select a time for reminder'
            page.date = None
            page.time = None
            page.text_field.value = ''
            new_screen()
        return fun

    def go_home():
        def fun(e):
            home_screen()
        return fun

    def change_sorting_mode_home(mode):
        def fun(e):
            page.sorting_mode = mode
            home_screen()
        return fun

    def change_sorting_mode(mode):
        def fun(e):
            page.sorting_mode = mode
            new_screen()
        return fun

    def handle_change_date():
        def fun(e):
            page.date = date_picker.value

            if page.date:
                page.date_text = page.date.strftime('%d.%m.%Y')
                new_screen()
                handle_date_time_changes()
        return fun

    def handle_change_time():
        def fun(e):
            page.time = time_picker.value

            if page.time:
                page.time_text = page.time.strftime('%H:%M:%S')
                new_screen()
                handle_date_time_changes()
        return fun

    def handle_date_time_changes():
        if page.date and page.time:
            # Объединяем дату и время в одну строку
            selected_datetime = f"{page.date_text}-{page.time_text}"
            # Обновляем атрибут страницы
            new_screen()
            page.text_field.value = selected_datetime
            page.update()

    def handle_process_choose(e):
        # Получаем выбранное значение из выпадающего списка
        selected_process = page.dropdown.value  # Используем page.dropdown
        # Обновляем текстовое поле
        page.text_field.value = str(float(selected_process.split()[0])/(10**6))  # Используем page.text_field
        # Сбрасываем значение выпадающего списка
        page.dropdown.value = None
        # Явно обновляем состояние виджета с помощью атрибута кей, это нормпрактика для флэт
        page.dropdown.key = str(datetime.datetime.now())
        # Обновляем страницу
        page.update()

    def handle_dismissal():
        pass

    # Добавляем DatePicker и TimePicker
    date_picker = ft.DatePicker(
                            first_date=datetime.datetime.now(),
                            last_date=datetime.datetime.now() + datetime.timedelta(days=365),
                            on_change=handle_change_date(),
                            on_dismiss=handle_dismissal)
    time_picker = ft.TimePicker(
                            on_change=handle_change_time(),
                            on_dismiss=handle_dismissal)
    page.overlay.extend([date_picker, time_picker])  # Добавляем оба пикера в overlay
    page.date_text = 'select a date for reminder'
    page.time_text = 'select a time for reminder'
    page.date = None
    page.time = None
    page.text_field = ft.TextField()

    def row(name, main_start, main_finish, text):
        n = 111
        ans = ['-' for _ in range(n + 2)]
        one = (main_finish - main_start) / n
        start = pm.main_dict[name].get_first_date()
        if start > main_start:
            for i in range(round((start - main_start) / one)):
                ans[i] = '_'
        for action in pm.main_dict[name].get_data():
            if action.text.split(' ')[0] in ('INFO', 'CROSS', 'NEW_DEBT', 'NEW_PERSON'):
                time_crossing = action.date
                if one == 0:
                    one = 1
                position = round((time_crossing - main_start) / one)
                if name == page.process_name:
                    pm.positions.append(position)
                    ans[position] = 'x'
                else:
                    if position in pm.positions:
                        ans[position] = 'x'
        return text + '\n' + ''.join(ans) + '>'

    def exit_from_app():
        def fun(e):
            page.window.destroy()
        return fun

    def transaction(name, official, btn_name):
        def fun(e):
            input_text = page.text_field.value
            if input_text or official:
                if not input_text:
                    input_text = ''
                try:
                    rez = pm.main_dict[name].act((btn_name + ' ') * int(official) + input_text, official=official)
                    if rez:
                        pm.add_new_process(rez)
                    pm.controller()
                    pm.previous_action_result = 'Success!'
                    new_screen()
                except Exception as e:
                    pm.previous_action_result = str(e)
                    new_screen()

        return fun

    def home_screen():
        page.process_name = pm.first_process_name

        page.clean()
        pm.positions.clear()
        main_start = min(Process.all_processes.values(), key=lambda x: x.get_first_date()).get_first_date()
        main_finish = max(Process.all_processes.values(), key=lambda x: x.get_last_date()).get_last_date()
        page.controls.append(ft.Row([ft.TextButton(text='begin', on_click=change_sorting_mode_home(0)),
                                     ft.TextButton(text='last_transaction', on_click=change_sorting_mode_home(1)),
                                     ft.TextButton(text='reminder', on_click=change_sorting_mode_home(2))],
                                    alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(page.process_tree)
        rows = []
        items = []
        if page.sorting_mode == 0:
            process_list = sorted(Process.all_processes.values(), key=lambda x: x.get_first_date())
        elif page.sorting_mode == 1:
            process_list = sorted(Process.all_processes.values(), key=lambda x: -x.get_last_date())
        else:
            process_list = sorted(Process.all_processes.values(), key=lambda x: x.get_reminder_date_time())
        for process in process_list:
            text1 = pm.info_dict[process.get_process_name()][0]
            text2 = pm.info_dict[process.get_process_name()][1]
            items.append(ft.TextButton(text1, on_click=change_process_name(process.get_process_name())))
            rows.append(row(process.get_process_name(), main_start, main_finish, text2))
        page.controls.append(ft.Row([ft.Column(items)], alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(ft.Row([ft.TextButton(text='Close the program', on_click=exit_from_app())],
                                    alignment=ft.MainAxisAlignment.CENTER))
        page.process_tree.value = '\n'.join(rows)
        page.update()

    def new_screen():
        page.clean()
        pm.positions.clear()

        # Создаем выпадающий список
        page.dropdown = ft.Dropdown(
            options=[ft.dropdown.Option(f"{process_id} ({process_info[1]})") for process_id, process_info in
                     pm.info_dict.items()],
            label="select process to intersect",
            on_change=handle_process_choose  # Привязываем обработчик события
        )

        if pm.main_dict[page.process_name].related_processes:
            main_start = min(pm.main_dict[page.process_name].get_first_date(),
                             min(pm.main_dict[page.process_name].related_processes,
                                 key=lambda x: x.get_first_date()).get_first_date())
            main_finish = max(pm.main_dict[page.process_name].get_last_date(),
                              max(pm.main_dict[page.process_name].related_processes,
                                  key=lambda x: x.get_last_date()).get_last_date())
        else:
            main_start = pm.main_dict[page.process_name].get_first_date()
            main_finish = pm.main_dict[page.process_name].get_last_date()
        page.controls.append(ft.TextButton(text='Home', on_click=go_home()))
        page.controls.append(ft.Row([ft.TextButton(text='begin', on_click=change_sorting_mode(0)),
                                     ft.TextButton(text='last_transaction', on_click=change_sorting_mode(1)),
                                     ft.TextButton(text='reminder', on_click=change_sorting_mode(2))],
                                    alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(page.process_tree)
        rows = [row(page.process_name, main_start, main_finish, pm.info_dict[page.process_name][1])]
        items = []
        if page.sorting_mode == 0:
            process_list = reversed(pm.main_dict[page.process_name].related_processes)
        elif page.sorting_mode == 1:
            process_list = sorted(pm.main_dict[page.process_name].related_processes,
                                  key=lambda p: -p.get_last_date())
        else:
            process_list = sorted(pm.main_dict[page.process_name].related_processes,
                                  key=lambda p: p.get_reminder_date_time())
        for process in process_list:
            text1 = pm.info_dict[process.get_process_name()][0]
            text2 = pm.info_dict[process.get_process_name()][1]
            items.append(ft.TextButton(text1, on_click=change_process_name(process.get_process_name())))
            rows.append(row(process.get_process_name(), main_start, main_finish, text2))
        page.controls.append(ft.Row([ft.Column(items)], alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(ft.Text(value=pm.previous_action_result))
        # Добавляю выпадающий календарь и часы для выбора напоминания.
        page.controls.append(
            ft.ElevatedButton(
                page.date_text,
                icon=ft.icons.CALENDAR_MONTH,  # Используем ft.Icons вместо ft.icons
                on_click=lambda e: page.open(date_picker),  # Открываем DatePicker через page.open
            )
        )
        page.controls.append(
            ft.ElevatedButton(
                page.time_text,
                icon=ft.icons.ACCESS_TIME,  # Используем ft.Icons вместо ft.icons
                on_click=lambda e: page.open(time_picker),  # Открываем TimePicker через page.open
            )
        )
        # Добавляем выпадающий список и текстовое поле на страницу
        page.controls.append(page.dropdown)
        page.controls.append(page.text_field)
        page.controls.append(ft.Row([ft.TextButton(text='Add Message', on_click=transaction(page.process_name, False, ''))] +
                                    [ft.TextButton(text=i, on_click=transaction(page.process_name, True, i)) for i in pm.main_dict[page.process_name].get_able_list()], alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(ft.Row([ft.Text(value=pm.get_reminder(page.process_name))], alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(ft.Row([ft.Text(value=pm.get_transaction(page.process_name), text_align=ft.TextAlign.CENTER)], alignment=ft.MainAxisAlignment.CENTER))
        page.controls.append(ft.Row([ft.TextButton(text='Close the program', on_click=exit_from_app())], alignment=ft.MainAxisAlignment.CENTER))
        page.process_tree.value = '\n'.join(rows)
        page.update()

    home_screen()

ft.app(main)
