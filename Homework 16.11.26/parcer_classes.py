import json
import os
from collections import defaultdict
from dataclasses import dataclass
from abc import ABC, abstractmethod

# FAQ:
# JsonFinder - абстрактный класс для наследования. Находит Json
# JsonSelection - абстрактный класс для наследования. Выбирает Json
# Parcing - абстрактный класс для наследования. Парсит своим методом Parcing.get_method()
# HOW TO USE--------------------------------------------------------------------------------------
# Для работы создаём класс MyParced и передаём ему Parcing метод в него класс выбора и класс нахождения и нужные в них параметры

class NoJsonFiles(Exception):
    def __init__(self, message: str = "Никаких json файлов не найдено"):
        super().__init__(message)

# БЛОК КЛАССОВ ДЛЯ НАХОЖДЕНИЯ ФАЙЛОВ JSON -----------------------------------------------------------------------------
# Абстрактный класс, поиска

class JsonFinder(ABC):
    @abstractmethod
    def find_json(self) -> list[str]: 
        ...
    @abstractmethod
    def get_find_method(self) -> str:
        ...

# Реализация поиска json, можно подавать как от куда искать (относительный путь, как и полный путь) 
# Как и если ничего не передовать, то будет искать в рабочей директории

class WalkJsonFinder(JsonFinder):
    # black_list_files можно не передавать, тогда чёрного списка нет
    def __init__(self, black_list_files: set[str] | None = None, root: str = "."):
            self.root = root
            self.black_list_files = black_list_files if black_list_files is not None else set()
    
    def find_json(self) -> list[str]:
        list_of_json = list()
        
        for path, dir_name, file_names in os.walk(self.root):
            
            for file_name in file_names:
                
                if file_name.endswith(".json") and (file_name not in self.black_list_files):

                    list_of_json.append(os.path.join(path, file_name))
        
        if not list_of_json:
            raise NoJsonFiles()
            
        return list_of_json
    def get_find_method(self) -> str:
        return "OS.walk method"


# БЛОК КЛАССОВ ДЛЯ ОТБОРА ФАЙЛОВ JSON -----------------------------------------------------------------------------

# Абстрактный класс, для отбора json

class JsonSelection(ABC):
    @abstractmethod
    # Обязательно передаём список
    def selector(self, files: list[str]) -> list[str]:
        ...

class JsonSelectionByKeys(JsonSelection):
    def __init__(self, dict_of_set_of_dict_keys: set[str]):
        self.dict_of_set_of_dict_keys = dict_of_set_of_dict_keys
    
# files в данном случае должен содержать в себе указатель на возвращаемую JsonFinder
 
    def selector(self, files: list[str]) -> list[str]:
        selected_files = list()
        
        for file_name in files:
            try:
                with open(file_name, "r", encoding="UTF-8") as file:
                    temp_something_in_json = json.load(file)

# Если json пустой он валится, поэтому для пропуска пустых json нужно проверять
            
            except (json.JSONDecodeError, OSError):
                continue


# Можно так а можно через all() <- возвращает true если для всех интерируемых истина
# TODO: надо реализовать прогон под списочных элементов. 
# HOW: Просто добавить проверку каждого элемента на вложенный словарь через isinstance

            if isinstance(temp_something_in_json, list):
                amount_of_elemts = len(temp_something_in_json)
                temp_amount = 0
                    
                for dict_of_somthing in temp_something_in_json:
                        
                    if isinstance(dict_of_somthing, dict) and self.dict_of_set_of_dict_keys.issubset(dict_of_somthing.keys()):
                        temp_amount += 1

                if temp_amount == amount_of_elemts and temp_amount != 0:
                    selected_files.append(file_name)


        return selected_files
 

# БЛОК ЧТЕНИЯ ------------------------------------------------------------------------------------------
# Это нужно чтобы парсер получал готовые данные, с разделением работы
# Чтобы можно было передовать данный как из памяти так и из файла

# INFO: Нашёл интересную идею. Возвращать не целый кусок данного, а возращать функцию генератор
# Чтобы память не загрязналась и более гипкого использования. Объект становиться итерабильным

class Reading(ABC):
    @abstractmethod
    def reading(self) -> dict:
        ...

class ReadingFromMemory(Reading):
    def __init__(self, memory: dict):
        self.memory = memory
    
    def reading(self) -> dict:
        return {'memory': self.memory}

class ReadingFromJsonFiles(Reading):
    def __init__(self, paths_for_json):
        self.paths = paths_for_json
    
    def reading(self) -> dict:
        data_temp = dict()
        for file in self.paths:
            with open(file, 'r', encoding="UTF-8") as f:
                data_temp[file] = json.load(f)
        
        return data_temp


        


# БЛОК КЛАССОВ ПАРСЕРОВ --------------------------------------------------------------------------------

class Parcing(ABC):
    @abstractmethod
    def parcing(self) -> dict:
        ...
    @abstractmethod
    def get_parcing_method(self) -> str:
        ...

# INFO: Нормализация данных: одно правило -> одна таблица.
# Парсер возвращает словарь {имя_таблицы: [строки]}

@dataclass(frozen=True)
class TableRule:
    # Имя будущей таблицы
    table: str
    # Путь к сущности внутри записи JSON (пустой кортеж = запись целиком)
    entity_path: tuple[str, ...]
    # Путь к полю, по которому сущность считается уникальной (внутри сущности)
    key_path: tuple[str, ...]
    # Колонка таблицы -> путь к значению внутри сущности
    fields: dict[str, tuple[str, ...]]
    # Схлопывать повторы по ключу 
    deduplicate: bool = True


class ParcerNormalizedJSONData(Parcing):
    def __init__(self, data: Reading, rule: TableRule):
        self.data = data.reading()
        self.rule = rule

    def parcing(self) -> dict:
        rows: list[dict] = list()
        seen: set = set()

        for item_data in self.data.values():

            for record in item_data:
                if not isinstance(record, dict):
                    continue

                entity = self._get_by_path(record, self.rule.entity_path)
                if not isinstance(entity, dict):
                    continue

                key = self._get_by_path(entity, self.rule.key_path)
                if key is None:
                    continue

                if self.rule.deduplicate:
                    if key in seen:
                        continue
                    seen.add(key)

                rows.append(
                    {column: self._get_by_path(entity, path)
                     for column, path in self.rule.fields.items()}
                )

        return {self.rule.table: rows}

    @staticmethod
    def _get_by_path(data, path: tuple[str, ...]):
        for part in path:
            if not isinstance(data, dict) or part not in data:
                return None
            data = data[part]
        return data

    def get_parcing_method(self) -> str:
        return f"Нормализация данных в таблицу {self.rule.table}"

class MyParced:
    def __init__(self, parcing_class: Parcing):
        # Способ парсинга
        self.parcing_class = parcing_class
        # Полученные значения для состовления словоря парсинга
        self.parcered_dict: dict = parcing_class.parcing()

    def get_dict(self):
        return self.parcered_dict

    def __call__(self):
        print(self.parcing_class.get_parcing_method())

        for key, values in self.parcered_dict.items():
            print(f"Ключ: {key}, значение: {values}")
