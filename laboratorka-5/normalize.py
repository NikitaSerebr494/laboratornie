text = input("Введите строку: ")

original_length = len(text)
normalized_parts = filter(lambda x: x.strip() != "", text.split())
normalized = " ".join(normalized_parts)
new_length = len(normalized)
word_count = len(normalized.split())

print("Исходная длина:", original_length)
print("Новая длина:", new_length)
print("Нормализованный текст:", normalized)
print("Количество слов:", word_count)
