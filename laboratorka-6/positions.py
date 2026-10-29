line = input("Введите целые числа одной строкой: ")

if line.strip() == "":
    print("Нет данных")
else:
    numbers = list(map(int, line.split()))
    maximum = max(numbers)
    positions = [i for i, x in enumerate(numbers) if x == maximum]

    print("Позиции максимума:", positions)
