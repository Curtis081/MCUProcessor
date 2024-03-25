from copy import deepcopy
from mcu_data import mcu_data
from customer_support_data import customer_supported_models


class MCUProcessor:
    def __init__(self, customer):
        supported_models = customer_supported_models[customer]
        self.__mcu_list = [mcu for mcu in deepcopy(mcu_data) if mcu["MCU型號"] in supported_models]
        self.__mcu_data_dict_key = self.__calc_mcu_data_dict_key(self.__mcu_list)

        self.__tune_combo_box_text_function_dict = {
            'MCU型號': None,
            '生產公司': self.find_company_by_model,
            '核心架構': self.find_architecture_by_model,
            '時脈': self.find_clock_by_model,
            '市場': self.find_market_by_model
        }

    def get_mcu_list(self):
        return self.__mcu_list

    def get_mcu_list_len(self):
        return len(self.__mcu_list)

    def get_tune_combo_box_text_function(self, config_item_name):
        return self.__tune_combo_box_text_function_dict.get(config_item_name)

    @staticmethod
    def __calc_mcu_data_dict_key(mcu_list):
        return mcu_list[0].keys()

    def get_mcu_data_dict_key(self):
        return self.__mcu_data_dict_key

    def __get_unique(self, key):
        unique_values = set()
        for item in self.__mcu_list:
            unique_values.add(item[key])
        return unique_values

    def get_unique_models(self):
        return self.__get_unique("MCU型號")

    def find_company_by_model(self, model):
        for mcu in self.__mcu_list:
            if mcu['MCU型號'] == model:
                return mcu['生產公司']
        return None

    def find_architecture_by_model(self, model):
        for mcu in self.__mcu_list:
            if mcu['MCU型號'] == model:
                return mcu['核心架構']
        return None

    def find_clock_by_model(self, model):
        for mcu in self.__mcu_list:
            if mcu['MCU型號'] == model:
                return mcu['時脈']
        return None

    def find_market_by_model(self, model):
        for mcu in self.__mcu_list:
            if mcu['MCU型號'] == model:
                return mcu['市場']
        return None

    def find_model_by_company(self, company_name):
        found_mcu = []
        for mcu in self.__mcu_list:
            if mcu["生產公司"] == company_name:
                found_mcu.append(mcu.get('MCU型號'))
        return found_mcu

    def find_model_by_architecture(self, architecture_name):
        found_mcu = []
        for mcu in self.__mcu_list:
            if mcu["核心架構"] == architecture_name:
                found_mcu.append(mcu.get('MCU型號'))
        return found_mcu

    def find_model_by_clock(self, clock):
        found_mcu = []
        for mcu in self.__mcu_list:
            if mcu["時脈"] == clock:
                found_mcu.append(mcu.get('MCU型號'))
        return found_mcu

    def find_model_by_market(self, market):
        found_mcu = []
        for mcu in self.__mcu_list:
            if mcu["市場"] == market:
                found_mcu.append(mcu.get('MCU型號'))
        return found_mcu
