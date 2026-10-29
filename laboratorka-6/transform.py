line = input("Введите целые числа одной строкой: ")

numbers = list(map(int, line.split())) if line.strip() != "" else []
new_list = [abs(x) for x in numbers]

print("Исходный список:", numbers)
print("Новый список:", new_list)
