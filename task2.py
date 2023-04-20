# a, b = avg - sqrt(3) * sigma, avg + sqrt(3) * sigma
#
# p_i = {}
#
# for key in data:
#     if data[key] < a:
#         p_i[key] = 0
#     elif data[key] >= b:
#         p_i[key] = 1
#     else:
#         p_i[key] = (data[key] - a) / (b - a)
#
# print(p_i)
from math import e, factorial, sqrt

from matplotlib import pyplot as plt
from scipy.stats import chi2
from tabulate import tabulate


def calc_p_i(_data: dict, _avg: float) -> dict:
    result = {}
    for key in _data:
        result[key] = pow(_avg, key) * pow(e, -_avg) / factorial(key)
    return result


def calc_avg(_data: dict) -> float:
    res = 0
    for key in data:
        res += key * data[key]
    return res / total


def calc_disp(_data: dict, _avg: float) -> float:
    res = 0
    for key in data:
        res += (_data[key] - _avg) ** 2

    return res / total


def calc_x_emp(_data: dict, _npi: dict) -> float:
    res = 0
    for key in _data:
        tmp = pow(_data[key] - _npi[key], 2)
        res += tmp / _npi[key]
    return res


# alpha = input('Введіть рівень значущості: ')
alpha = 0.05

data = {
    1: 1438,
    2: 1380,
    3: 1393,
    4: 1421,
    5: 1430,
    6: 1389,
    7: 1390,
    8: 1433,
    9: 1444,
    10: 1407,
    11: 1395,
    12: 1376
}

fig, ax = plt.subplots()
plt.grid()
x, y = list(data.keys()), list(data.values())
ax.set_title('Гістограма розподілу')
ax.plot(x, y)
ax.scatter(x, y)
plt.xticks(x)
plt.show()

total = sum([data[key] for key in data])
avg = calc_avg(data)
sigma = sqrt(calc_disp(data, avg))
freqs = {key: 1 / len(data) for key in data}
np_i = {key: freqs[key] * total for key in freqs}
print(np_i)

x_emp = calc_x_emp(data, np_i)

print(tabulate(
    {'x_i': list(data.keys()), 'm_i': list(data.values()), 'p_i': list(freqs.values()), 'np_i': list(np_i.values())},
    headers='keys', tablefmt='grid'))
print('Сума m_i:', total)
print('Сума частот: ', sum(list(freqs.values())))
df = len(data) - 1

x_cr = chi2.ppf(1 - alpha, df=df)

if x_emp < x_cr:
    print(f'X^2_emp < X^2_cr(alpha = {alpha}, df = {df})')
    print(f'{x_emp} < {x_cr}')
    print('Гіпотеза правдива')
else:
    print(f'X^2_emp > X^2_cr({alpha}, {df})')
    print(f'{x_emp} > {x_cr}')
    print('Гіпотеза неправдива')
