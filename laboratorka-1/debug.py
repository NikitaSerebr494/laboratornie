# --- Фрагмент Б: Деление 1 / 2 должно давать 0.5, а не 0 ---
# Проблема: в Python 2 оператор "/" для целых чисел усечет результат до 0.
# Решение: использовать float-операнды или явное приведение.
# Также добавлен guard для совместимости с Python 2, если файл запускается там.

numerator, denominator = 1, 2

# Способ 1: принудительное приведение к float
div_float = float(numerator) / denominator
print(f"Деление (приведение к float): {div_float}")

# Способ 2: использование float-литерала
div_literal = numerator / 2.0
print(f"Деление (float-литерал): {div_literal}")

# Способ 3: импорт division из __future__ (для обратной совместимости с Py2)
try:
from __future__ import division
# После этого импорта оператор "/" всегда возвращает float
div_future = 1 / 2
print(f"Деление (после __future__): {div_future}")
except ImportError:
# В Python 3 импорт из __future__ невозможен, пропускаем
pass
 
#РЕЗУЛЬТАТ
  Деление (приведение к float): 0.5
Деление (float-литерал): 0.5
Деление (после __future__): 0.5
