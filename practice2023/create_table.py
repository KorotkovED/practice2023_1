
def func(to_str=None, to_int=None):
    """Функция перевода в строку или целочисленные занчения массива."""
    if to_str:
        value = []
        for i in to_str:
            value.append(str(i)[2:-3])
        return value
    else:
        value = []
        for i in to_int:
            value.append(*i)
        return value


def corresponding_fields_of_the_table(old_stack,
                                      new_id_run,
                                      int_list_id_runs):
    """Функция преобразования данных в соответсвии с id_run"""
    stack = []
    for i in new_id_run:
        value = int_list_id_runs.index(i)
        stack.append(old_stack[value])
    return stack


def create_table(cursor, connection):
    """Создание таблицы dop_results."""
    # название стенда из таблицы runs
    id_stand = "SELECT stand -> 'stand1' FROM runs;"

    # id теста из таблицы results
    id_test = "SELECT test_id FROM results;"

    # название версии стенда
    id_version = "SELECT stand -> 'version' -> 'version' FROM runs;"

    # id прогона из таблицы results, который связян с id_stand и id_version
    id_run = "SELECT run_id FROM results;"

    # количество входящих пакетов в секунду
    input_rate = "SELECT perfomance_stat -> 'input_rate' FROM results;"

    # ошибки в секунду
    ierrors = "SELECT perfomance_stat -> 'ierrors' FROM results;"

    # получение данных из таблиц и их преобразование в удобные типы

    cursor.execute(id_stand)
    id_stand = cursor.fetchall()
    new_id_stand = func(to_str=id_stand)

    cursor.execute(id_test)
    id_test = cursor.fetchall()
    new_id_test = func(to_int=id_test)

    cursor.execute(id_version)
    id_version = cursor.fetchall()
    new_id_version = func(to_str=id_version)

    cursor.execute(id_run)
    id_run = cursor.fetchall()
    new_id_run = func(to_int=id_run)

    cursor.execute(input_rate)
    input_rate = cursor.fetchall()
    new_input_rate = func(to_int=input_rate)

    cursor.execute(ierrors)
    ierrors = cursor.fetchall()
    new_ierrors = func(to_int=ierrors)

    # преобразование new_id_stand и new_id_version в соответсвии с данными из
    # таблицы results, а именно с полем id_run

    list_id_runs = "SELECT id FROM runs;"
    cursor.execute(list_id_runs)
    lists_id_runs = cursor.fetchall()
    int_list_id_runs = func(to_int=lists_id_runs)

    print(new_id_stand, new_id_run, int_list_id_runs)

    new_id_stand_lv = corresponding_fields_of_the_table(new_id_stand,
                                                        new_id_run,
                                                        int_list_id_runs)

    new_id_version_lv = corresponding_fields_of_the_table(new_id_version,
                                                          new_id_run,
                                                          int_list_id_runs)

    # создание таблицы

    cursor.execute(
        """CREATE TABLE dop_results(
        id serial PRIMARY KEY,
        id_stand varchar(50) NOT NULL,
        id_test integer NOT NULL,
        id_version varchar(50) NOT NULL,
        id_runs integer NOT NULL,
        input_rate integer NOT NULL,
        ierrors integer NOT NULL
        );"""
    )
    connection.commit()
    print('[INFO] Таблица создана!')

    # заполняем данными
    for i in range(326):
        insert_query = f""" INSERT INTO dop_results (id, id_stand, id_test,
                            id_version, id_runs, input_rate, ierrors)
                            VALUES ({i+1}, '{new_id_stand_lv[i]}',
                            {new_id_test[i]}, '{new_id_version_lv[i]}',
                            {new_id_run[i]},
                            {new_input_rate[i]}, {new_ierrors[i]})"""
        cursor.execute(insert_query)
        connection.commit()

    print('[INFO] Данные загружены!')
