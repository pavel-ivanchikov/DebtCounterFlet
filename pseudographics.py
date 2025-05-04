def row(name, main_start, main_finish, text, main_process, pm):
    n = 111
    ans = ['-' for _ in range(n + 2)]
    step = (main_finish - main_start) / n
    start = pm.main_dict[name].get_first_date()
    if start > main_start:
        for i in range(round((start - main_start) / step)):
            ans[i] = '_'
    for action in pm.main_dict[name].get_data():
        if action.text.split(' ')[0] in ('INFO', 'CROSS', 'NEW_DEAL', 'NEW_PERSON'):
            time_crossing = action.date
            if step == 0:
                step = 1
            position = round((time_crossing - main_start) / step)
            if name == main_process:
                pm.positions.append(time_crossing)
                ans[position] = 'x'
            else:
                if time_crossing in pm.positions:
                    ans[position] = 'x'
    return text + '\n' + ''.join(ans) + '>'


def row_home(name, main_start, main_finish, text, pm):
    n = 111
    ans = ['-' for _ in range(n + 2)]
    one = (main_finish - main_start) / n
    start = pm.main_dict[name].get_first_date()
    if start > main_start:
        for i in range(round((start - main_start) / one)):
            ans[i] = '_'
    for action in pm.main_dict[name].get_data():
        if action.text.split(' ')[0] in ('INFO', 'CROSS', 'NEW_DEAL', 'NEW_PERSON'):
            time_crossing = action.date
            if one == 0:
                one = 1
            position = round((time_crossing - main_start) / one)
            ans[position] = 'x'
    return text + '\n' + ''.join(ans) + '>'

