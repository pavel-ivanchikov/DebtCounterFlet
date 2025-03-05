import os
import datetime
import flet as ft
from MyLife import MyLife
from ProcessesManagerDC import ProcessesManagerDC


def main(page: ft.Page):
    path = r"C:/DebtCounter/fifth/"
    if len(os.listdir(path)) == 0:
        _ = MyLife.create_first_process()
    pm = ProcessesManagerDC(path)
    pm.deserialization()
    main_process_name = pm.first_process_name
    mode = 0

    page.title = "Flet Debt Counter"
    page.window_width = 700
    page.scroll = True
    process_tree = ft.Text()

    def handle_change(name):
        def fun(e):
            # Обновляем дату и время
            page.date = date_picker.value
            page.time = time_picker.value

            if page.date and page.time:
                # Объединяем дату и время в одну строку
                selected_datetime = f"{page.date.strftime('%d.%m.%Y')}-{page.time.strftime('%H:%M:%S')}"
                page.date_text = page.date.strftime('%d.%m.%Y')
                page.time_text = page.time.strftime('%H:%M:%S')
                # Обновляем атрибут страницы
                new_screen(name, mode)(None)
                item = page.controls.__getitem__(-5)  # Получаем текстовое поле
                item.value = selected_datetime  # Обновляем текстовое поле
                page.update()

        return fun

    def handle_dismissal(e):
        pass

    # Добавляем DatePicker и TimePicker
    date_picker = ft.DatePicker(
                            first_date=datetime.datetime.now(),
                            last_date=datetime.datetime.now() + datetime.timedelta(days=365),
                            on_change=handle_change(main_process_name),
                            on_dismiss=handle_dismissal)
    time_picker = ft.TimePicker(
                            on_change=handle_change(main_process_name),
                            on_dismiss=handle_dismissal)
    page.overlay.extend([date_picker, time_picker])  # Добавляем оба пикера в overlay
    page.date_text = 'Выберите дату'
    page.time_text = 'Выберите время'
    page.date = None
    page.time = None

    def row(name, main_start, main_finish, text, main_name=None):
        n = 100
        ans = ['-' for _ in range(n + 2)]
        one = (main_finish - main_start) / n
        start = pm.main_dict[name].get_identifier()[0]
        if start > main_start:
            for i in range(round((start - main_start) / one)):
                ans[i] = '_'
        for action in pm.main_dict[name].get_data():
            if action.official:
                time_crossing = action.date
                if one == 0:
                    one = 1
                position = round((time_crossing - main_start) / one)
                if main_name is None:
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
            item = page.controls.__getitem__(-5)
            if isinstance(item, ft.TextField):
                input_text = item.value
            else:
                raise ValueError("Пытаюсь достать текст из нетекстового поля")
            if input_text or official:
                if not input_text:
                    input_text = ''
                try:
                    rez = pm.main_dict[name].act((btn_name + ' ') * int(official) + input_text, official=official)
                    if rez:
                        pm.add_new_process(rez)
                    pm.controller()
                    pm.previous_action_result = 'Success!'
                    new_screen(name, mode)(None)
                except Exception as e:
                    pm.previous_action_result = str(e)
                    new_screen(name, mode)(None)

        return fun

    def new_screen(name, sorting_mode):
        def fun(e):
            page.clean()
            pm.positions.clear()
            if pm.main_dict[name].related_processes:
                main_start = min(pm.main_dict[name].get_first_date(),
                                 min(pm.main_dict[name].related_processes,
                                     key=lambda x: x.get_first_date()).get_first_date())
                main_finish = max(pm.main_dict[name].get_last_date(),
                                  max(pm.main_dict[name].related_processes,
                                      key=lambda x: x.get_last_date()).get_last_date())
            else:
                main_start = pm.main_dict[name].get_first_date()
                main_finish = pm.main_dict[name].get_last_date()
            page.controls.append(ft.Row([ft.TextButton(text='begin', on_click=new_screen(name, 0)),
                                         ft.TextButton(text='last_transaction', on_click=new_screen(name, 1)),
                                         ft.TextButton(text='reminder', on_click=new_screen(name, 2))],
                                        alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(process_tree)
            rows = [row(name, main_start, main_finish, pm.info_dict[name][1])]
            items = []
            if sorting_mode == 0:
                process_list = reversed(pm.main_dict[name].related_processes)
            elif sorting_mode == 1:
                process_list = sorted(pm.main_dict[name].related_processes, key=lambda p: -p.get_last_date())
            else:
                process_list = sorted(pm.main_dict[name].related_processes, key=lambda p: p.get_reminder_date_time())
            for process in process_list:
                text1 = pm.info_dict[process.get_process_name()][0]
                text2 = pm.info_dict[process.get_process_name()][1]
                items.append(ft.TextButton(text1, on_click=new_screen(process.get_process_name(), sorting_mode)))
                rows.append(row(process.get_process_name(), main_start, main_finish, text2, name))
            page.controls.append(ft.Row([ft.Column(items)], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(ft.Text(value=pm.previous_action_result))
            page.controls.append(
                ft.ElevatedButton(
                    page.date_text,
                    icon=ft.Icons.CALENDAR_MONTH,  # Используем ft.Icons вместо ft.icons
                    on_click=lambda e: page.open(date_picker),  # Открываем DatePicker через page.open
                )
            )
            page.controls.append(
                ft.ElevatedButton(
                    page.time_text,
                    icon=ft.Icons.ACCESS_TIME,  # Используем ft.Icons вместо ft.icons
                    on_click=lambda e: page.open(time_picker),  # Открываем TimePicker через page.open
                )
            )
            page.controls.append(ft.Dropdown(options=[ft.dropdown.Option(f"{process_id} ({process_info[1]})") for process_id, process_info in pm.info_dict.items()], label="Выберите процесс",))
            page.controls.append(ft.TextField())
            page.controls.append(ft.Row([ft.TextButton(text='Add Message', on_click=transaction(name, False, ''))] +
                                        [ft.TextButton(text=i, on_click=transaction(name, True, i)) for i in pm.main_dict[name].get_able_list()], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(ft.Text(value=pm.get_reminder(name)))
            page.controls.append(ft.Row([ft.Text(value=pm.get_transaction(name), text_align=ft.TextAlign.CENTER)], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(ft.Row([ft.TextButton(text='Close the program', on_click=exit_from_app())], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.__getitem__(1).value = '\n'.join(rows)
            page.update()
        return fun

    new_screen(main_process_name, mode)(None)


ft.app(main)
