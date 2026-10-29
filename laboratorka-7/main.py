from functions import sum_digits, average, normalize_text, select_numbers

number = int(input("Введите целое число: "))
print("Сумма цифр:", sum_digits(number))

num_line = input("Введите строку чисел: ")
numbers = list(map(int, num_line.split())) if num_line.strip() != "" else []
avg = average(numbers)
if avg is None:
    print("Среднее: Нет данных")
else:
    print("Среднее:", avg)

text = input("Введите произвольный текст: ")
print("Нормализованный текст:", normalize_text(text))

threshold = int(input("Введите порог: "))
result = select_numbers(numbers, threshold)
print("Выборка:", result)
