import sys
from PyQt6.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QComboBox
from copy import deepcopy

from mcu_processor import MCUProcessor
from mcu_data import mcu_data


class Window(QWidget):
    def __init__(self, customer):
        super().__init__()
        self.combo_box_num_dict = {}
        self.mcu_config_item_list = []
        self.combo_box_event_dict = {
            0: self.on_model_combobox_selected,
            1: self.on_company_combobox_selected,
            2: self.on_architecture_combobox_selected,
            3: self.on_clock_combobox_selected,
            4: self.on_market_combobox_selected,
        }
        self.mcu_processor = MCUProcessor(customer)
        self.init_ui()

    @staticmethod
    def get_item_content_by_dict_key_in_list(data_list, dict_key):
        item_content_set = set([data[dict_key] for data in data_list])
        item_content_list = sorted(list(item_content_set))
        return item_content_list

    def create_label_and_combox(self, layout):
        mcu_config_item = mcu_data[0].keys()
        self.mcu_config_item_list = list(mcu_config_item)

        for item_index, item in enumerate(self.mcu_config_item_list):
            label = QLabel(item)

            combo_box = QComboBox()
            combo_box_item_content_list = self.get_item_content_by_dict_key_in_list(mcu_data, item)
            support_item_content_list = self.get_item_content_by_dict_key_in_list(
                self.mcu_processor.get_mcu_list(), item)
            already_set_current_index = False
            for item_content_index, item_content in enumerate(combo_box_item_content_list):
                combo_box.addItem(item_content)
                if item_content in support_item_content_list:
                    if not already_set_current_index:
                        combo_box.setCurrentIndex(item_content_index)
                        already_set_current_index = True
                    combo_box.model().item(item_content_index).setEnabled(True)
                else:
                    combo_box.model().item(item_content_index).setEnabled(False)

            func = self.combo_box_event_dict.get(item_index)
            combo_box.currentIndexChanged.connect(func)
            self.combo_box_num_dict.update({item: (item_index, combo_box)})

            layout.addWidget(label)
            layout.addWidget(combo_box)

        return layout

    def get_config_item_tune_list(self, combobox_item_name):
        mcu_config_item_tune_list = deepcopy(self.mcu_config_item_list)
        mcu_config_item_tune_list.remove(combobox_item_name)
        return mcu_config_item_tune_list

    def get_combo_box_selected_text(self, combobox_item_name):
        model_combo_box_index, model_combo_box = self.combo_box_num_dict.get(combobox_item_name)
        selected_text = model_combo_box.currentText()
        return selected_text

    def tune_combo_box_text(self, config_item_tune_name, config_item_name, selected_text):
        tune_combo_box_text_function = self.mcu_processor.get_tune_combo_box_text_function(config_item_name)
        if config_item_tune_name == config_item_name:
            item_name = tune_combo_box_text_function(selected_text)
            _, item_combo_box = self.combo_box_num_dict.get(config_item_name)
            item_combo_box.setCurrentText(item_name)

    def tune_model_combo_box_text(self, config_item_tune_name, config_item_name, selected_text):
        tune_combo_box_text_function = self.mcu_processor.get_tune_combo_box_text_function(config_item_name)

        item_name = tune_combo_box_text_function(selected_text)
        _, item_combo_box = self.combo_box_num_dict.get(config_item_name)
        item_combo_box.setCurrentText(item_name)

    def tune_item_combo_box_text(self, selected_text, config_item_tune_name):
        # model_config_item_name = "MCU型號"
        # self.tune_combo_box_text(config_item_tune_name, model_config_item_name, selected_text)

        company_config_item_name = "生產公司"
        self.tune_combo_box_text(config_item_tune_name, company_config_item_name, selected_text)

        architecture_config_item_name = "核心架構"
        self.tune_combo_box_text(config_item_tune_name, architecture_config_item_name, selected_text)

        clock_config_item_name = "時脈"
        self.tune_combo_box_text(config_item_tune_name, clock_config_item_name, selected_text)

        market_config_item_name = "市場"
        self.tune_combo_box_text(config_item_tune_name, market_config_item_name, selected_text)

    def set_model_item_combo_box_current_text(self, selected_models):
        selected_model = selected_models[0]
        model_item_name = "MCU型號"
        _, item_combo_box = self.combo_box_num_dict.get(model_item_name)
        item_combo_box.setCurrentText(selected_model)
        return selected_model

    def on_model_combobox_selected(self):
        combobox_item_name = "MCU型號"
        config_item_tune_list = self.get_config_item_tune_list(combobox_item_name)
        selected_text = self.get_combo_box_selected_text(combobox_item_name)
        print("on_model_combobox_selected = %s" % selected_text)
        for mcu_config_item_tune in config_item_tune_list:
            self.tune_item_combo_box_text(selected_text, mcu_config_item_tune)

    def on_company_combobox_selected(self):
        combobox_item_name = "生產公司"
        config_item_tune_list = self.get_config_item_tune_list(combobox_item_name)
        selected_text = self.get_combo_box_selected_text(combobox_item_name)
        selected_models = self.mcu_processor.find_model_by_company(selected_text)
        selected_model = self.set_model_item_combo_box_current_text(selected_models)
        print("on_company_combobox_selected = %s" % selected_text)
        for mcu_config_item_tune in config_item_tune_list:
            self.tune_item_combo_box_text(selected_model, mcu_config_item_tune)

    def on_architecture_combobox_selected(self):
        combobox_item_name = "核心架構"
        config_item_tune_list = self.get_config_item_tune_list(combobox_item_name)
        selected_text = self.get_combo_box_selected_text(combobox_item_name)
        selected_models = self.mcu_processor.find_model_by_architecture(selected_text)
        selected_model = self.set_model_item_combo_box_current_text(selected_models)
        print("on_architecture_combobox_selected = %s" % selected_text)
        for mcu_config_item_tune in config_item_tune_list:
            self.tune_item_combo_box_text(selected_model, mcu_config_item_tune)

    def on_clock_combobox_selected(self):
        combobox_item_name = "時脈"
        config_item_tune_list = self.get_config_item_tune_list(combobox_item_name)
        selected_text = self.get_combo_box_selected_text(combobox_item_name)
        selected_models = self.mcu_processor.find_model_by_clock(selected_text)
        selected_model = self.set_model_item_combo_box_current_text(selected_models)
        print("on_clock_combobox_selected = %s" % selected_text)
        for mcu_config_item_tune in config_item_tune_list:
            self.tune_item_combo_box_text(selected_model, mcu_config_item_tune)

    def on_market_combobox_selected(self):
        combobox_item_name = "市場"
        config_item_tune_list = self.get_config_item_tune_list(combobox_item_name)
        selected_text = self.get_combo_box_selected_text(combobox_item_name)
        selected_models = self.mcu_processor.find_model_by_market(selected_text)
        selected_model = self.set_model_item_combo_box_current_text(selected_models)
        print("on_market_combobox_selected = %s" % selected_text)
        for mcu_config_item_tune in config_item_tune_list:
            self.tune_item_combo_box_text(selected_model, mcu_config_item_tune)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout = self.create_label_and_combox(layout)
        self.setLayout(layout)


def configure_ui(customer):
    app = QApplication(sys.argv)

    window = Window(customer)
    window.show()

    sys.exit(app.exec())
