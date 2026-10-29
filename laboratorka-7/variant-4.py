def select_numbers(numbers, threshold):
    return [x for x in numbers if x >= threshold]


line = input("Введите целые числа одной строкой: ")
numbers = list(map(int, line.split())) if line.strip() != "" else []
threshold = int(input("Введите порог: "))

result = select_numbers(numbers, threshold)
print("Выборка:", result)
