import json
import sys
import os
from collections import defaultdict
from abc import ABC, abstractmethod

# Константные переменные

USER_DICT_KEYS = {"id", "name", "username", "email", "address", "phone", "website", "company"}

# Ошибки

ERROR_NO_JSON_FILE = 1

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
            try:
                with open(file_name, "r", encoding="UTF-8") as file:
                    temp_something_in_json = json.load(file)

# Если json пустой он валится, поэтому для пропуска пустых json нужно проверять
            
            except (json.JSONDecodeError, OSError):
                continue


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
 
# Класс парсера

class Parcing(ABC):
    @abstractmethod
    def parcing(self) -> dict:
        ...
    @abstractmethod
    def get_parcing_method(self) -> str:
        ...

class ParcerByCityName(Parcing):
    def __init__(self, files: JsonFinder, files_selected: JsonSelection):
        self.files = files_selected.selector(files.find_json())

    def parcing(self) -> dict:
        parcered_dict = defaultdict(list)

        for file_name in self.files: 
            
            with open(file_name, "r", encoding="UTF-8") as file:
                list_in_json = json.load(file)
                
                for dict_list in list_in_json:
                    city = dict_list["address"]["city"]
                    name = dict_list["name"]
                    parcered_dict[city].append(name)

        return dict(parcered_dict)
    
    def get_parcing_method(self):
        return f"Сортировка ГОРОД-ИМЯ"

class MyParced:
    def __init__(self, parcing_class: Parcing):
        self.parcing_class = parcing_class
        self.parcered_dict: dict = parcing_class.parcing()

    def get_dict(self):
        return self.parcered_dict

    def __call__(self):
        print(self.parcing_class.get_parcing_method())

        for key, values in self.parcered_dict.items():
            print(f"Ключ: {key}, значение: {values}")

if __name__ == "__main__":
    
    try:
        parced_text = MyParced(ParcerByCityName(WalkJsonFinder(), JsonSelectionByKeys(USER_DICT_KEYS)))
    
    except NoJsonFiles as e:
        print(f"{e}, выход с кодом ошибки 1")
        sys.exit(ERROR_NO_JSON_FILE)
   

    file = open("cities.json", "w", encoding="UTF-8")
    
    try:
        json.dump(parced_text.get_dict(), file, ensure_ascii=False, indent=2)
    finally:
        file.close()
        

        

