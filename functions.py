import os
import json
import arrow


def make_directory(path):
    if not directoryExists(path):
        os.mkdir(path)


def directoryExists(path):
    return os.path.isdir(path)


def create_timetable_as_matrix(days, blocks, modules):
    timetable = []
    header = ['Block', 'Zeit']
    for day in days:
        header.append(days[day])

    timetable.append(header)

    for block in blocks:
        timetable.append([block, blocks[block], '', '', '', '', ''])

    for modul in modules:
        add_event_to_matrix(modul, timetable, 'vorlesung')
        add_event_to_matrix(modul, timetable, 'übung')

    return timetable


def add_event_to_matrix(modul, timetable, event):
    if event in modul:
        abbreviation = modul['abkuerzung']
        block = modul[event]['block']
        day = modul[event]['tag']
        timetable[block][day + 1] = abbreviation


def open_file(path):
    with open(path, 'r', encoding='utf8') as template:
        return template.read()


def make_markdown_table(matrix):
    widths = get_column_widths(matrix)
    header = '|'
    divider = '|'
    content = ''

    for i, entry in enumerate(matrix[0]):
        header += ' ' + str(entry).ljust(widths[i]) + ' |'

    for i, entry in enumerate(matrix[0]):
        divider += ' ' + '-' * widths[i] + ' |'

    for row in matrix[1:]:
        content += '|'
        for i, entry in enumerate(row):
            content += ' ' + str(entry).ljust(widths[i]) + ' |'
        content += '\n'

    return header + '\n' + divider + '\n' + content


def get_column_widths(matrix):
    widths = [0] * get_column_amount(matrix)
    for row in matrix:
        for i, column in enumerate(row):
            if widths[i] < len(str(column)):
                widths[i] = len(str(column))
    return widths


def get_column_amount(matrix):
    columns = 0
    for row in matrix:
        if columns < len(row):
            columns = len(row)
    return columns


def create_semester_readme_file(semester_data):
    template = open_file('templates/semester_readme.md')

    title = semester_data['semester_titel']
    timetable_matrix = create_timetable_as_matrix(semester_data['days'], semester_data['block_times'], semester_data['modules'])
    timetable = make_markdown_table(timetable_matrix)
    modulelist = ''

    for modul in semester_data['modules']:
        modulelist += '- [' + modul['modul'] + '](' + modul['modul'] + '/)\n'

    return eval(f'f"""{template}"""') # hacky as fuck, not very safe: https://stackoverflow.com/questions/47339121/how-do-i-convert-a-string-into-an-f-string


def create_note_file(title, date):
    template = open_file('templates/note.md')
    return eval(f'f"""{template}"""') # hacky as fuck, not very safe: https://stackoverflow.com/questions/47339121/how-do-i-convert-a-string-into-an-f-string


def create_module_readme(semester_data, modul):
    template = open_file('templates/module_readme.md')
    title = modul['modul']
    moduletimetable = make_markdown_table(create_module_timetable_as_matrix(semester_data, modul))
    examtable = make_markdown_table(create_module_examtable_as_matrix())
    return eval(f'f"""{template}"""') # hacky as fuck, not very safe: https://stackoverflow.com/questions/47339121/how-do-i-convert-a-string-into-an-f-string


def create_module_timetable_as_matrix(semester_data, modul):
    timetable = [['Veranstaltung', 'Dozent', 'Raum', 'Tag', 'Uhrzeit']]

    if 'vorlesung' in modul:
        timetable.append(['Vorlesung', modul['dozent'], modul['vorlesung']['raum'], semester_data['days'][str(modul['vorlesung']['tag'])], semester_data['block_times'][str(modul['vorlesung']['block'])]])

    if 'übung' in modul:
        timetable.append(['Übung', modul['dozent'], modul['übung']['raum'], semester_data['days'][str(modul['übung']['tag'])], semester_data['block_times'][str(modul['übung']['block'])]])

    return timetable


def create_module_examtable_as_matrix():
    examtable = [
        ['Element', 'Entry'],
        ['Raum', ''],
        ['Datum', ''],
        ['Zeit', '']
    ]
    return examtable


def day_of_event(modul, event, week):
    return arrow.get(week, "YYYY-MM-DD").shift(days=+modul[event]['tag']-1).format('YYYY-MM-DD')


def write_file(file, content):
    with open(file, 'w', encoding='utf8') as file:
        file.write(content)


def semester_weeks(semester_data):
    begin = arrow.get(semester_data['vorlesungsbegin'])
    end = arrow.get(semester_data['vorlesungsende'])
    weeks = arrow.Arrow.range('week', begin, end)

    week_strings = []
    for week in weeks:
        week_strings.append(week.format('YYYY-MM-DD'))

    return week_strings


def create_note_files(week_directory, week, modul):
    if 'vorlesung' in modul:
        note = create_note_file('vorlesung', day_of_event(modul, 'vorlesung', week))
        write_file(week_directory + 'vorlesung.md', note)

    if 'übung' in modul:
        note = create_note_file('übung', day_of_event(modul, 'übung', week))
        write_file(week_directory + 'übung.md', note)

    note = create_note_file('zusammenfassung', week)
    write_file(week_directory + 'zusammenfassung.md', note)
