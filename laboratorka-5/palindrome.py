text = input("Введите текст: ")

lower = text.lower()
cleaned = lower.replace(" ", "")

if cleaned == "":
    print("Нет текста")
else:
    if cleaned == cleaned[::-1]:
        print("Палиндром")
    else:
        print("Не палиндром")

    # дополнительное решение циклом (обход половины длины очищенной строки)
    is_palindrome = True
    for i in range(len(cleaned) // 2):
        if cleaned[i] != cleaned[len(cleaned) - 1 - i]:
            is_palindrome = False
            break
