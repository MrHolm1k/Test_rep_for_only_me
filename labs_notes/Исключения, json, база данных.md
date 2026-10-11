#PYTHON #LABS #CS
## Исключения

Для обработки ошибок в python существует специальные метод связки команд `try` - `except`:

```python
try:
	# Код, в котором может подняться exception
except NameOfExsepstion as e:
	# Обработки ошибки
```

`as e` - выполния функцию так сказать алиасса

С помощью `raise` - можно поднимать объект exception. В python существует ряд встроенных классов ошибок:

Интересный способ для реализации ошибки:

```python
class MyClass():

	def someFunction(self, *args, **kwargs):
		raise SomeException(f"some error message")

```

В этом примере мы используем класс. Если метод нем был _переопрделён_, то мы _поднимает_ исключение.

### Наследование исключений

[Офф документация](https://docs.python.org/3/builtins/exceptions.html#BaseException)

В python _все_ исключения - это экземпляры классов, которые наследуются от `BaseException`. Схема наследования встроенных исключений:

```
BaseException
 ├── BaseExceptionGroup
 ├── GeneratorExit
 ├── KeyboardInterrupt
 ├── SystemExit
 └── Exception
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ExceptionGroup [BaseExceptionGroup]
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    ├── NotImplementedError
      │    ├── PythonFinalizationError
      │    └── RecursionError
      ├── StopAsyncIteration
      ├── StopIteration
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning
           ├── BytesWarning
           ├── DeprecationWarning
           ├── EncodingWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── PendingDeprecationWarning
           ├── ResourceWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UnicodeWarning
           └── UserWarning
```

Правила наследования:

1. В `except` указывается класс - ловятся _он сам и все его подклассы_, но не его суперклассы. То есть `except Exception` поймает `KeyError`, но не поймает `KeyboardInterrupt`;
2. Два класса исключений, которые не связаны наследованием, никогда не эквивалентны, даже если у них одинаковое имя;
3. `BaseException` - корень всего дерева, но он _не предназначен_ для прямого наследования пользовательскими классами (для этого есть `Exception`);
4. Все пользовательские исключения должны наследоваться от `Exception` или одного из его подклассов;
5. Наследоваться лучше от _одного_ типа исключения за раз: встроенные классы реализованы на C и имеют свою memory layout, поэтому множественное наследование может конфликтовать из-за обработки `args` и раскладки в памяти.

__Базовый пример своего исключения__:

```python
class MyError(Exception):

	def __init__(self, message, code):
		super().__init__(message, code)
		self.message = message
		self.code = code
```

__Важно__: `SystemExit`, `KeyboardInterrupt` и `GeneratorExit` наследуются напрямую от `BaseException`, а не от `Exception` - это сделано специально, чтобы их не ловил случайный `except Exception` и программа могла корректно завершиться (Ctrl+C, `sys.exit()`, закрытие генератора).

### BaseException - базовый класс

Атрибуты и методы, которые есть у _каждого_ исключения:

- `args` - tuple аргументов, с которыми исключение создавалось; некоторые встроенные исключения (например `OSError`) ожидают определённое количество аргументов и дают элементам этого tuple особый смысл, остальные обычно вызываются с одной строкой - сообщением об ошибке;
- `with_traceback(tb)` - устанавливает _tb_ как новый traceback исключения и возвращает объект исключения; полезно, чтобы перевести одно исключение в другое, сохранив traceback;
- `__traceback__` - изменяемое поле с traceback-объектом, привязанным к исключению;
- `add_note(note)` / `__notes__` (с python 3.11) - добавляет строку к заметкам исключения, они выводятся в traceback после сообщения об ошибке; `note` обязан быть строкой;
- `__context__` - неявная цепочка: какое исключение _уже обрабатывалось_ в момент поднятия нового (заполняется автоматически);
- `__cause__` - явная причина исключения, задаётся через `raise new_exc from original_exc`;
- `__suppress_context__` - если `True`, `__context__` не показывается в traceback; выставляется автоматически при установке `__cause__`.

```python
try:
	...
except SomeException as e:
	raise OtherException('описание') from e
```

### Базовые exceptions

__Базовые классы__ - сами по себе почти не поднимаются, используются как родители для других:

- `Exception` - родитель всех обычных (не системных) исключений, от него и нужно наследовать свои;
- `ArithmeticError` - родитель арифметических ошибок: `OverflowError`, `ZeroDivisionError`, `FloatingPointError`;
- `LookupError` - родитель ошибок невалидного ключа или индекса: `IndexError`, `KeyError`;
- `BufferError` - операция с buffer не может быть выполнена;
- `Warning` - родитель всех категорий предупреждений (подкласс `Exception`).

__Чаще всего встречающиеся__: 

|Исключение|Когда поднимается|
|---|---|
|`TypeError`|Операция применена к объекту _неправильного типа_ (например `1 + 'a'`)|
|`ValueError`|Тип правильный, но значение _неподходящее_ (например `int('abc')`)|
|`NameError`|Локальное или глобальное имя не найдено|
|`UnboundLocalError`|Локальная переменная используется до присваивания (подкласс `NameError`)|
|`AttributeError`|Не найден атрибут или метод у объекта|
|`IndexError`|Индекс последовательности вне диапазона|
|`KeyError`|Нет ключа в словаре|
|`ZeroDivisionError`|Деление или взятие остатка на ноль|
|`OverflowError`|Результат арифметической операции слишком велик для представления|
|`AssertionError`|Не прошёл `assert`|
|`ImportError`|Проблема с загрузкой модуля (в т.ч. нет имени в `from ... import`)|
|`ModuleNotFoundError`|Модуль не найден (подкласс `ImportError`)|
|`OSError`|Системная ошибка: файл не найден, нет прав доступа, диск полон и т.п.|
|`FileNotFoundError`|Файл или директория запрошены, но не существуют (подкласс `OSError`)|
|`PermissionError`|Нет прав доступа к операции (подкласс `OSError`)|
|`MemoryError`|Не хватило памяти|
|`RuntimeError`|Ошибка, не попавшая ни в одну другую категорию|
|`RecursionError`|Превышена максимальная глубина рекурсии (подкласс `RuntimeError`)|
|`NotImplementedError`|Абстрактный метод не реализован (подкласс `RuntimeError`)|
|`StopIteration`|Итератор закончился, `next()` больше не даёт элементов|
|`StopAsyncIteration`|Асинхронный итератор закончился|
|`SyntaxError`|Ошибка синтаксиса при парсинге кода|
|`IndentationError`|Неправильные отступы (подкласс `SyntaxError`)|
|`TabError`|Смешаны табы и пробелы в отступах (подкласс `IndentationError`)|
|`EOFError`|`input()` встретил конец файла, ничего не прочитав|
|`SystemError`|Внутренняя ошибка интерпретатора|
|`ReferenceError`|Обращение к weak reference после сборки мусора|
|`UnicodeDecodeError` / `UnicodeEncodeError`|Ошибка декодирования / кодирования Unicode (подклассы `UnicodeError`, он сам - подкласс `ValueError`)|

__Системные__ (напрямую от `BaseException`, `except Exception` их не ловит):

- `SystemExit` - поднимается `sys.exit()`, завершает интерпретатор; атрибут `code` - код выхода;
- `KeyboardInterrupt` - пользователь нажал прерывание (Ctrl+C);
- `GeneratorExit` - закрытие генератора или корутины, технически _не ошибка_;

__Группы исключений__ (с python 3.11):

- `ExceptionGroup(msg, excs)` - оборачивает набор _несвязанных_ исключений в одно; наследуется от `Exception`, поэтому оборачивает только подклассы `Exception`;
- `BaseExceptionGroup(msg, excs)` - то же самое, но наследуется от `BaseException` и может оборачивать любые исключения; ловится через `except*`.

__Предупреждения__: `Warning` и его подклассы (`UserWarning`, `DeprecationWarning`, `RuntimeWarning`, `ResourceWarning` и др.) - поднимаются не ошибками, а через `warnings.warn()`; они подклассы `Exception`, но по умолчанию многие отфильтровываются.

## Module LOGGING

Помогает логировать происходящее в программе. Можно выбрать тот же syslog. [Офф документация](https://docs.python.org/3/builtins/exceptions.html). Также на [geeksforgeeks](https://www.geeksforgeeks.org/python/logging-in-python/)


## JSON

__JSON__ - один из основных удобных способов хранения данных в python. Модуль для работы с этим типов уже есть в _python_. 

### Структура json

1. Файл всегда начинается с `{}` - это корневой элемент;
2. По сути json - это большой словарь;
3. `{}` - словарь, `[]` - список;
4. "Ключ": значение;
5. При переходе на новую строку ставится запятая;
6. Всегда только один корневой элемент в json;

__Например__:

```json
{
"firstVar": [
{
"VarOfArray": 1,
"SomeOtherVar": null
},
10,
true, 
"Meow"
],
}
```

Типы данных в __JSON__:

- Object (аналог dict в python);
- Array;
- String;
- Number (int);
- Number (real);
- true;
- false;
- null;


### Работа в python

[Офф документация](https://docs.python.org/3/library/json.html)

__Преорбразование типов данных__: json -> python:

| JSON          | Python |
| ------------- | ------ |
| object        | dict   |
| array         | list   |
| string        | str    |
| number (int)  | int    |
| number (real) | float  |
| true          | True   |
| false         | False  |
| null          | None   |

### Базовые методы

В модуле __json__ всего 4 базовые функции. Разница внутри пары только в том, куда уходит результат: буква **s** в названии - _string_ (`dumps` - _dump string_, `loads` - _load string_). Без - уходить сразу в файл

|Метод|Работает с|Что делает|Возвращает|
|---|---|---|---|
|`dumps`|строка|Кодирует объект python -> JSON строку|`str`|
|`dump`|файл|Кодирует объект python -> JSON в файл|`None`|
|`loads`|строка|Декодирует JSON строку -> объект python|объект python|
|`load`|файл|Декодирует JSON из файла -> объект python|объект python|

[Офф документация](https://docs.python.org/3/library/json.html#basic-usage)

#### json.dumps(obj, \*, skipkeys=False, ensure_ascii=True, ...)

Преобразует _obj_ в JSON строку:

```python
json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])
# '["foo", {"bar": ["baz", null, 1.0, 2]}]'
```

__Параметры__:

- `obj` - сам объект python, который кодируем;
- `skipkeys` (bool, default `False`) - если `True`, ключи не базовых типов (`str`, `int`, `float`, `bool`, `None`) просто пропускаются вместо `TypeError`;
- `ensure_ascii` (bool, default `True`) - если `True`, все не-ASCII и непечатаемые символы экранируются; если `False`, выводятся как есть. необходим для коректной работы с кирилицей;
- `check_circular` (bool, default `True`) - проверка циклических ссылок у контейнеров, иначе будет `RecursionError`;
- `allow_nan` (bool, default `True`) - если `True`, `nan`, `inf`, `-inf` пишутся как `NaN`, `Infinity`, `-Infinity` (не строгий JSON); если `False` - `ValueError`;
- `cls` (подкласс `JSONEncoder`) - свой кодировщик; если `None`, используется стандартный `JSONEncoder`;
- `indent` (int | str | None, default `None`) - отступы для красивого вывода: число - столько пробелов на уровень, строка (например `"\t"`) - используется как отступ, `None` - компактный вывод без переносов строк;
- `separators` (tuple | None, default `None`) - кортеж `(разделитель элементов, разделитель ключей)`; по умолчанию `(', ', ': ')`, для самого компактного JSON - `(',', ':')`;
- `default` (callable | None, default `None`) - функция, которая вызывается для объектов, которые нельзя сериализовать, и должна вернуть JSON-совместимый тип; если `None` - `TypeError`;
- `sort_keys` (bool, default `False`) - если `True`, ключи словарей выводятся по возрастанию;
- `**kw` - остальные ключевые аргументы передаются в конструктор `JSONEncoder`.

Примеры:

```python
# компактный вывод
json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
# '[1,2,3,{"4":5,"6":7}]'

# красивый вывод
print(json.dumps({'6': 7, '4': 5}, sort_keys=True, indent=4))
# {
#     "4": 5,
#     "6": 7
# }
```

__Raises__: `TypeError` (нельзя сериализовать), `ValueError` (например, `nan` при `allow_nan=False`).

#### json.dump(obj, fp, \*, skipkeys=False, ensure_ascii=True, ...)

Сериализует _obj_ как JSON поток в _fp_ (объект с методом `.write()`). Параметры __те же самые__, что и у `dumps()`, только добавляется:

- `fp` (file-like object) - файл или поток, куда пишем JSON; модуль всегда пишет `str`, а не `bytes`, поэтому `fp.write()` должен принимать строки.

```python
with open('data.json', 'w', encoding='utf-8') as f:
	json.dump({'name': 'Python', 'version': 3}, f, indent=4)
# возвращает None, результат уже в файле
```

Важно: JSON - _не фреймовый протокол_ (в отличие от `pickle`), поэтому несколько вызовов `dump()` в один файл дадут невалидный JSON. например:

```python
with open('data.json', 'w') as f:
	json.dump({"a": 1}, f)
	json.dump({"b": 2}, f)

# В файле получится: {"a": 1}{"b": 2}
```

__Raises__: `TypeError`, `ValueError`.

#### json.loads(s, \*, cls=None, object_hook=None, ...)

Десериализует _s_ (строку, `bytes` или `bytearray` с JSON документом) в объект python:

```python
json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
# ['foo', {'bar': ['baz', None, 1.0, 2]}]
```

__Параметры__:

- `s` (str | bytes | bytearray) - строка с JSON документом (кодировка UTF-8, UTF-16 или UTF-32);
- `cls` (подкласс `JSONDecoder`) - свой декодер; если `None`, используется стандартный `JSONDecoder`;
- `object_hook` (callable | None, default `None`) - функция, которая вызывается с результатом каждого декодированного JSON объекта (т.е. с `dict`), её возвращаемое значение подставляется вместо словаря; удобно для кастомной десериализации;
- `object_pairs_hook` (callable | None, default `None`) - то же самое, но на упорядоченном списке пар ключ-значение (сохраняет порядок); если заданы оба - приоритет у `object_pairs_hook`;
- `parse_float` (callable | None, default `None`) - функция, вызываемая на каждую строку float; если `None` - эквивалент `float(num_str)`, можно передать например `decimal.Decimal`;
- `parse_int` (callable | None, default `None`) - то же самое для int, по умолчанию эквивалент `int(num_str)`;
- `parse_constant` (callable | None, default `None`) - функция, вызываемая на `'-Infinity'`, `'Infinity'`, `'NaN'`; можно использовать, чтобы ругаться на невалидный JSON;
- `**kw` - остальные ключевые аргументы передаются в конструктор `JSONDecoder`.

Примеры:

```python
json.loads('{"__complex__": true, "real": 1, "imag": 2}', object_hook=as_complex)
# (1+2j)

json.loads('1.1', parse_float=decimal.Decimal)
# Decimal('1.1')
```

__Raises__: `json.JSONDecodeError` (подкласс `ValueError`) - данные не являются валидным JSON, `UnicodeDecodeError` - не UTF-8/16/32.

#### json.load(fp, \*, cls=None, object_hook=None, ...)

Десериализует _fp_ (файл) в объект python. Параметры __те же самые__, что и у `loads()`:

- `fp` (file-like object) - текстовый или бинарный файл с `.read()`, из него читается JSON документ.

```python
with open('data.json', 'r', encoding='utf-8') as f:
	data = json.load(f)
```

__Raises__: `json.JSONDecodeError`, `UnicodeDecodeError`.

__Важно__: `loads(dumps(x)) != x`, если у словаря были не строковые ключи - при сериализации все ключи конвертируются в `str`.



