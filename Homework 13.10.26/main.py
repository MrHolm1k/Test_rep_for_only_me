import json
import sys
import os
from collections import defaultdict
from abc import ABC, abstractmethod

USER_DICT_KEYS = {"id", "name", "username", "email", "address", "phone", "website", "company"}



class NoJsonFiles(Exception):
    def __init__(self, message: str = "Никаких json файлов не найдено"):
        super().__init__(message)

# Абстрактный класс, поиска

class JsonFinder(ABC):
    @abstractmethod
    def find_json(self) -> list[str]: 
        ...

# Реализация поиска json, можно подавать как от куда искать (относительный путь, как и полный путь) 
# Как и если ничего не передовать, то будет искать в рабочей директории

class WalkJsonFinder(JsonFinder):
    def __init__(self, root: str = "."):
            self.root = root
    
    def find_json(self) -> list[str]:
        list_of_json = list()
        
        for path, dir_name, file_names in os.walk(self.root):
            
            for file_name in file_names:
                
                if file_name.endswith(".json"):
                    list_of_json.append(os.path.join(path, file_name))
        
        if not list_of_json:
            raise NoJsonFiles()
            
        return list_of_json

# Абстрактный класс, для отбора json


class JsonSelection(ABC):
    @abstractmethod
    # Обязательно передаём список
    def selector(self, files: list[str]) -> list[str]:
        ...

class JsonSelectionByKeys(JsonSelection):
    def __init__(self, dict_keys: set[str]):
        self.dict_keys = dict_keys
    
# files в данном случае должен содержать в себе указатель на возвращаемую JsonFinder
 
    def selector(self, files: list[str]) -> list[str]:
        selected_files = list()
        
        for file_name in files:
            
            with open(file_name, "r", encoding="UTF-8") as file:
                temp_something_in_json = json.load(file)

# Можно так а можно через all() <- возвращает true если для всех интерируемых истина

                if isinstance(temp_something_in_json, list):
                    amount_of_elemts = len(temp_something_in_json)
                    temp_amount = 0
                    
                    for dict_of_somthing in temp_something_in_json:
                        
                        if isinstance(dict_of_somthing, dict) and self.dict_keys.issubset(dict_of_somthing.keys()):
                            temp_amount += 1

                    if temp_amount == amount_of_elemts and temp_amount != 0:
                        selected_files.append(file_name)


        return selected_files
        

# Лучше запихнуть в класс. 
# 1) лучше передовать функцию с обёрткой для быстрого изменения.
# 2) Передовать список с файлами, неправильность заполнения будет узнаваться на этапе парсинга


if __name__ == "__main__":
    pass   

