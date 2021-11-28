import matplotlib.pyplot as plt
from formulas_analyzer import create_graph_positions, function_from_formula
from utilities import find_close_numbers

text = """
(x + 1) * (x + 1),
x * x
"""


xticks = []
yticks = []

for text_part in text.split(','):
    func = function_from_formula(text_part.strip())
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

if len(find_close_numbers(xticks)) < 4 and len(find_close_numbers(yticks)) < 4:
    plt.xticks(xticks)
    plt.yticks(yticks)


# Сохраняем созданный график
plt.savefig('graph.png')

# Покажем окно с нарисованным граф                      
plt.show()