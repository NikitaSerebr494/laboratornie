text = input("Введите строку: ")

words = text.split()
result = []

for word in words:
    cleaned = word.strip(".,!?;:").lower()
    if cleaned == "":
        continue
    if len(cleaned) == 4:
        result.append(cleaned)

if not result:
    print("Нет совпадений")
    print("Количество: 0")
else:
    for w in result:
        print(w)
    print("Количество:", len(result))
