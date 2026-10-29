line = input("Введите целые числа одной строкой: ")

numbers = list(map(int, line.split())) if line.strip() != "" else []
values = [x for x in numbers if x % 3 == 0]
sorted_copy = sorted(values)

print("Выборка:", values)
print("Количество:", len(values))
print("Сумма:", sum(values))
print("Сортированная копия:", sorted_copy)
