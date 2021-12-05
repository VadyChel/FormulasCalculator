import math
import re
import matplotlib.pyplot as plt

from core.utilities import find_close_numbers
from core.formula import Formula


def function_from_formula(formula: str, xmin: int, xmax: int) -> Formula:
    expression = None
    if '?' in formula:
        splited_formula = formula.split('?')
        formula = splited_formula[0]
        expression = splited_formula[1]

    found_x_and_number = re.match('\d+x', formula)
    if found_x_and_number is None:
        output_formula = formula
    else:
        found_x_and_number = found_x_and_number.group(0)
        found_number = re.match('\d*', found_x_and_number).group(0)
        output_formula = f"{found_number if found_number else '1'} * x{formula.replace(found_x_and_number, '')}"

    func = eval(
        f"lambda x: {output_formula}{f'if {expression} else None' if expression is not None else ''}",
        {"sqrt": math.sqrt}
    )
    return Formula(
        function=func,
        formula=formula,
        expression=expression,
        xmin=xmin,
        xmax=xmax
    )


def create_graph_positions(formula: Formula) -> Formula:
    # Список координат по оси x
    xlist = []

    # Получаем функцию формулы
    function = formula.function

    # Заполняем выше указанный список
    for num in range(formula.xmin, formula.xmax+1):
        result = function(num)

        if result is None:
            continue

        # Проверяем только не целые числа
        if isinstance(result, float):
            # Получаем список чисел после запятой у числа которое возвратила функция графика
            numbers_after_comma = list(str(result).split('.')[1:][0]) if num != 0 else [0]

            # Суммируем числа после запятой
            sum_numbers_after_comma = sum(list(map(int, numbers_after_comma)))
        else:
            sum_numbers_after_comma = 0

        # Проверка на целое число
        if sum_numbers_after_comma == 0:
            xlist.append(num)

    # Вычислим значение функции в заданных точках
    ylist = [function(x) for x in xlist]

    # Устанавливаем точки x и y в экземпляр класса Formula
    formula.set_x_coordinates(xlist).set_y_coordinates(ylist)

    return formula


def draw_graph(text: str, x_coords_mode: str, y_coords_mode: str, xmin: int, xmax: int):
    xticks = []
    yticks = []

    for text_part in text.split(','):
        func = function_from_formula(formula=text_part.strip(), xmin=xmin, xmax=xmax)
        formula = create_graph_positions(func)

        xlist = formula.x_coordinates
        ylist = formula.y_coordinates

        # Нарисуем одномерный график
        plt.plot(xlist, ylist, marker='.', ls='-')

        xticks.extend(xlist)
        yticks.extend(ylist)

    # Нарисуем сетку графика
    plt.grid()

    xticks = list(set(xticks))
    yticks = list(set(yticks))

    # Сортируем списки тиков
    xticks.sort()
    yticks.sort()

    if not x_coords_mode == 'disable':
        if x_coords_mode == 'show':
            plt.yticks(yticks)
        else:
            if len(find_close_numbers(xticks)) < 4 and x_coords_mode == 'auto':
                plt.xticks(xticks)

    if not y_coords_mode == 'disable':
        if y_coords_mode == 'show':
            plt.yticks(yticks)
        else:
            if len(find_close_numbers(xticks)) < 4 and y_coords_mode == 'auto':
                plt.yticks(yticks)

    # Сохраняем созданный график
    plt.savefig('graph.png')

    # Покажем окно с нарисованным граф
    plt.show()
