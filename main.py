import flet as ft
from ProcessesManagerDC import ProcessesManagerDC


def main(page: ft.Page):
    path = r"C:/DebtCounter/third/"
    pm = ProcessesManagerDC(path)
    pm.deserialization()
    main_process_name = pm.first_process_name

    page.title = "Flet Debt Counter"
    page.window.width = 550
    page.scroll = True
    process_tree = ft.Text()

    def row(name, main_start, main_finish, text, main_name=None):
        n = 70
        ans = ['-' for _ in range(n + 2)]
        one = (main_finish - main_start) / n
        start = pm.main_dict[name].get_identifier()[0]
        if start > main_start:
            for i in range(round((start - main_start) / one)):
                ans[i] = '_'
        for transaction in pm.main_dict[name].get_data():
            if transaction.official:
                time_crossing = transaction.date
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
            input_text = page.controls.__getitem__(-5).value
            if input_text or official:
                try:
                    rez = pm.main_dict[name].act((btn_name + ' ') * int(official) + input_text, official=official)
                    if rez:
                        pm.add_new_process(rez)
                    pm.controller()
                    pm.previous_action_result = 'Success!'
                    new_screen(name)(None)
                except Exception as e:
                    pm.previous_action_result = str(e)
                    new_screen(name)(None)

        return fun

    def new_screen(name):
        def fun(e):
            page.clean()
            pm.positions.clear()
            main_start = min(pm.main_dict[name].get_first_date(),
                             min(pm.main_dict[name].related_processes,
                                 key=lambda x: x.get_first_date()).get_first_date())
            main_finish = max(pm.main_dict[name].get_last_date(),
                              max(pm.main_dict[name].related_processes,
                                  key=lambda x: x.get_last_date()).get_last_date())
            page.controls.append(process_tree)
            rows = [row(name, main_start, main_finish, pm.info_dict[name][1])]
            items = []
            for process in reversed(pm.main_dict[name].related_processes):
                text1 = pm.info_dict[process.get_process_name()][0]
                text2 = pm.info_dict[process.get_process_name()][1]
                items.append(ft.TextButton(text1, on_click=new_screen(process.get_process_name())))
                rows.append(row(process.get_process_name(), main_start, main_finish, text2, name))
            page.controls.append(ft.Row([ft.Column(items)], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(ft.Text(value=pm.previous_action_result))
            page.controls.append(ft.TextField())
            page.controls.append(ft.Row([ft.TextButton(text='Add Message', on_click=transaction(name, False, ''))], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(ft.Row([ft.TextButton(text=i, on_click=transaction(name, True, i)) for i in pm.main_dict[name].get_able_list()], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(ft.Row([ft.Text(value=pm.get_transactionDC(name), text_align=ft.TextAlign.CENTER)], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.append(ft.Row([ft.TextButton(text='Close the program', on_click=exit_from_app())], alignment=ft.MainAxisAlignment.CENTER))
            page.controls.__getitem__(0).value = '\n'.join(rows)
            page.update()
        return fun

    new_screen(main_process_name)(None)


ft.app(main)
