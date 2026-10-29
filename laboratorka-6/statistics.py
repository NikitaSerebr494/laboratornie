line = input("Введите целые числа одной строкой: ")

if line.strip() == "":
    print("Нет данных")
else:
    numbers = list(map(int, line.split()))
    count = len(numbers)
    total = sum(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    average = total / count

    print("Количество:", count)
    print("Сумма:", total)
    print("Минимум:", minimum)
    print("Максимум:", maximum)
    print("Среднее:", f"{average:.2f}")
