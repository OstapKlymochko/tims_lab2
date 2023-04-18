# from math import inf, sqrt
# from scipy.stats import norm, chi2
# import matplotlib.pyplot as plt
# from tabulate import tabulate
#
#
# def calc_centers(_intervals: dict) -> dict:
#     result = {}
#     for key in _intervals:
#         result[key] = (key[0] + key[1]) * 0.5
#     return result
#
#
# def calc_avg(_intervals: dict) -> float:
#     _total = sum([_intervals[key] for key in _intervals])
#     return sum([(key[0] + key[1]) * 0.5 * _intervals[key] for key in _intervals]) / _total
#
#
# def calc_disp(_avg: float, _intervals: dict, _total: int) -> float:
#     s = sum([((key[0] + key[1]) * 0.5 - _avg) ** 2 * _intervals[key] for key in _intervals])
#     return s / _total
#
#
# def merge(_intervals: dict) -> dict:
#     result = {}
#     intervals_keys = list(_intervals.keys())
#     i = 0
#     while i < len(intervals_keys) - 1:
#
#         if _intervals[intervals_keys[i]] < 5:
#             tmp = (intervals_keys[i][0], intervals_keys[i + 1][1])
#             result[tmp] = _intervals[intervals_keys[i]] + _intervals[intervals_keys[i + 1]]
#             i += 1
#
#         else:
#             result[intervals_keys[i]] = _intervals[intervals_keys[i]]
#
#         if i == len(intervals_keys) - 2:
#             result[intervals_keys[i + 1]] = _intervals[intervals_keys[i + 1]]
#
#         i += 1
#
#     last_elem = list(result.keys())[-1]
#
#     if result[last_elem] < 5:
#         _last = result.popitem()
#         last_but_one = result.popitem()
#         interval = (last_but_one[0][0], _last[0][1])
#         result[interval] = _last[1] + last_but_one[1]
#
#     for key in result:
#         if result[key] < 5:
#             result = merge(result)
#             break
#
#     return result
#
#
# def calc_np_i(_intervals: dict, _sigma: float, _avg: float, _total: int) -> dict:
#     result = {}
#     intervals_keys = list(_intervals.keys())
#     i = 0
#     while i < len(intervals_keys):
#         f1 = (intervals_keys[i][1] - avg) / sigma
#         f2 = (intervals_keys[i][0] - avg) / sigma
#         np_i = _total * (norm.cdf(f1) - norm.cdf(f2))  # p_i
#         result[intervals_keys[i]] = np_i
#         i += 1
#     return result
#
#
# def calc_x_emp(_intervals: dict, _npi: dict) -> float:
#     res = 0
#     for key in _intervals:
#         tmp = (_intervals[key] - _npi[key]) ** 2 / _npi[key]
#         res += tmp
#     return res
#
#
# intervals = {
#     (28, 30): 1,
#     (30, 32): 2,
#     (32, 34): 10,
#     (34, 36): 54,
#     (36, 38): 88,
#     (38, 40): 79,
#     (40, 42): 45,
#     (42, 44): 17,
#     (44, 46): 3,
#     (46, 48): 1
# }
# # alpha = float(input('Введіть рівень значущості: '))
# alpha = 0.05
#
# if alpha > 1:
#     alpha /= 100
#
# total = sum([intervals[key] for key in intervals])
#
# centers = calc_centers(intervals)
#
# avg = calc_avg(intervals)
#
# disp = calc_disp(avg, intervals, total)
#
# sigma = sqrt(disp)
#
# print(tabulate({'Інтервали': list(intervals.keys()), 'm_i': list(intervals.values()), 'z_i': list(centers.values())},
#                headers='keys', tablefmt='grid'))
#
# fig, ax = plt.subplots()
# plt.grid()
# x, y = list(centers.values()), list(intervals.values())
# ax.set_title('Гістограма розподілу')
# ax.plot(x, y)
# ax.scatter(x, y)
# plt.xticks(x)
# plt.show()
#
# # Об'єднання інтервалів
# intervals = merge(intervals)
#
# ints = list(intervals.keys())
# first, last = [ints[0], intervals[ints[0]]], [ints[-1], intervals[ints[-1]]]
#
# del intervals[first[0]]
# del intervals[last[0]]
#
# intervals = {**{(-inf, first[0][1]): first[1]}, **intervals, **{(last[0][0], inf): last[1]}}
#
# npi = calc_np_i(intervals, sigma, avg, total)
#
# print(tabulate(
#     {"Об'єднані інтервали": list(intervals.keys()), 'm_i': list(intervals.values()), 'np_i': list(npi.values())},
#     headers='keys', tablefmt='grid'))
#
# x_emp = calc_x_emp(intervals, npi)
#
# df = len(list(intervals.keys())) - 3
#
# x_cr = chi2.ppf(1 - alpha, df=df)
#
# if x_emp < x_cr:
#     print(f'X^2_emp < X^2_cr(alpha = {alpha}, df = {df})')
#     print(f'{x_emp} < {x_cr}')
#     print('Гіпотеза правдива')
# else:
#     print(f'X^2_emp > X^2_cr({alpha}, {df})')
#     print(f'{x_emp} > {x_cr}')
#     print('Гіпотеза неправдива')

from math import inf, sqrt
from scipy.stats import norm, chi2
import matplotlib.pyplot as plt
from tabulate import tabulate


def calc_centers(_intervals: dict) -> dict:
    result = {}
    for key in _intervals:
        result[key] = (key[0] + key[1]) * 0.5
    return result


def calc_avg(_intervals: dict) -> float:
    _total = sum([_intervals[key] for key in _intervals])
    return sum([(key[0] + key[1]) * 0.5 * _intervals[key] for key in _intervals]) / _total


def calc_disp(_avg: float, _intervals: dict, _total: int) -> float:
    s = sum([((key[0] + key[1]) * 0.5 - _avg) ** 2 * _intervals[key] for key in _intervals])
    return s / _total


def merge(_intervals: dict, _npi: dict) -> dict:
    result = {}
    intervals_keys = list(_intervals.keys())
    i = 0
    while i < len(intervals_keys) - 1:

        if _intervals[intervals_keys[i]] < 5 or _npi[intervals_keys[i]] < 10:
            tmp = (intervals_keys[i][0], intervals_keys[i + 1][1])
            result[tmp] = _intervals[intervals_keys[i]] + _intervals[intervals_keys[i + 1]]
            i += 1

        else:
            result[intervals_keys[i]] = _intervals[intervals_keys[i]]

        if i == len(intervals_keys) - 2:
            result[intervals_keys[i + 1]] = _intervals[intervals_keys[i + 1]]

        i += 1

    last_elem = list(result.keys())[-1]

    if result[last_elem] < 5:
        _last = result.popitem()
        last_but_one = result.popitem()
        interval = (last_but_one[0][0], _last[0][1])
        result[interval] = _last[1] + last_but_one[1]

    for key in result:
        if result[key] < 5 or _npi[intervals_keys[i]] < 10:
            _npi = calc_np_i(result, sigma, avg, total)
            result = merge(result, _npi)
            break

    return result


def calc_np_i(_intervals: dict, _sigma: float, _avg: float, _total: int) -> dict:
    result = {}
    intervals_keys = list(_intervals.keys())
    i = 0
    while i < len(intervals_keys):
        f1 = (intervals_keys[i][1] - avg) / sigma
        f2 = (intervals_keys[i][0] - avg) / sigma
        _np_i = _total * (norm.cdf(f1) - norm.cdf(f2))  # p_i
        result[intervals_keys[i]] = _np_i
        i += 1
    return result


def calc_x_emp(_intervals: dict, _npi: dict) -> float:
    res = 0
    for key in _intervals:
        tmp = (_intervals[key] - _npi[key]) ** 2 / _npi[key]
        res += tmp
    return res


intervals = {
    (28, 30): 1,
    (30, 32): 2,
    (32, 34): 10,
    (34, 36): 54,
    (36, 38): 88,
    (38, 40): 79,
    (40, 42): 45,
    (42, 44): 17,
    (44, 46): 3,
    (46, 48): 1
}
# alpha = float(input('Введіть рівень значущості: '))
alpha = 0.05

if alpha > 1:
    alpha /= 100

total = sum([intervals[key] for key in intervals])
centers = calc_centers(intervals)
avg = calc_avg(intervals)
disp = calc_disp(avg, intervals, total)
sigma = sqrt(disp)
np_i = calc_np_i(intervals, sigma, avg, total)
x_emp = calc_x_emp(intervals, np_i)

print(tabulate({'Інтервали': list(intervals.keys()), 'm_i': list(intervals.values()), 'z_i': list(centers.values()),
                'np_i': list(np_i.values())},
               headers='keys', tablefmt='grid'))


fig, ax = plt.subplots()
plt.grid()
x, y = list(centers.values()), list(intervals.values())
ax.set_title('Гістограма розподілу')
ax.plot(x, y)
ax.scatter(x, y)
plt.xticks(x)
plt.show()

# Об'єднання інтервалів
intervals = merge(intervals, np_i)

ints = list(intervals.keys())
first, last = [ints[0], intervals[ints[0]]], [ints[-1], intervals[ints[-1]]]

del intervals[first[0]]
del intervals[last[0]]

intervals = {**{(-inf, first[0][1]): first[1]}, **intervals, **{(last[0][0], inf): last[1]}}

npi = calc_np_i(intervals, sigma, avg, total)

print(tabulate(
    {"Об'єднані інтервали": list(intervals.keys()), 'm_i': list(intervals.values()), 'np_i': list(npi.values())},
    headers='keys', tablefmt='grid'))

df = len(list(intervals.keys())) - 3

x_cr = chi2.ppf(1 - alpha, df=df)

if x_emp < x_cr:
    print(f'X^2_emp < X^2_cr(alpha = {alpha}, df = {df})')
    print(f'{x_emp} < {x_cr}')
    print('Гіпотеза правдива')
else:
    print(f'X^2_emp > X^2_cr({alpha}, {df})')
    print(f'{x_emp} > {x_cr}')
    print('Гіпотеза неправдива')
