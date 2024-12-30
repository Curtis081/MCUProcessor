import pytest
from src.mcu_processor import MCUProcessor
from src.customer_support_data import customer_supported_models


try:
    from test_unit.customer_support_data_for_test import customer_supported_models_for_test
    customer_supported_models.update(customer_supported_models_for_test)
except Exception as e:
    print(e)


class TestMCUProcessor:
    def test_init(self):
        mcu_processor = MCUProcessor('ASUS')
        assert mcu_processor is not None
        assert mcu_processor.get_mcu_list_len() == 4

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test is not None
        assert mcu_processor_test.get_mcu_list_len() == 3

    def test_find_mcu_by_company(self):
        mcu_processor = MCUProcessor('ASUS')
        found_mcu = mcu_processor.find_model_by_company("STMicroelectronics")
        assert len(found_mcu) == 4
        for mcu in found_mcu:
            assert mcu in ["STM32F103C8T6", "STM32F407VG", "STM8S207M8T3B", "STM8L152M8T6"]
        assert "GD32VF103CBT6" not in found_mcu
        assert (mcu_processor.find_model_by_company("STMicroelectronics")
                == ["STM32F103C8T6", "STM32F407VG", "STM8S207M8T3B", "STM8L152M8T6"])

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_model_by_company("GigaDevice") == ["GD32VF103CBT6"]
        assert mcu_processor_test.find_model_by_company("NXP") == ["i.MX RT1060"]
        assert mcu_processor_test.find_model_by_company("Texas Instruments") == ["MSP430G2553"]
        assert mcu_processor_test.find_model_by_company("Texas Instruments") != ["MSP430G2553", "GD32VF103CBT6"]

    def test_find_model_by_architecture(self):
        mcu_processor = MCUProcessor('ASUS')
        found_mcu = mcu_processor.find_model_by_architecture("32位元")
        assert len(found_mcu) == 2
        assert mcu_processor.find_model_by_architecture("32位元") == ["STM32F103C8T6", "STM32F407VG"]
        assert mcu_processor.find_model_by_architecture("8位元") == ["STM8S207M8T3B", "STM8L152M8T6"]

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_model_by_architecture("32位元") == ["i.MX RT1060", "GD32VF103CBT6"]
        assert mcu_processor_test.find_model_by_architecture("16位元") == ["MSP430G2553"]

    def test_find_model_by_clock(self):
        mcu_processor = MCUProcessor('ASUS')
        assert mcu_processor.find_model_by_clock("72MHz") == ['STM32F103C8T6']
        assert mcu_processor.find_model_by_clock("168MHz") == ['STM32F407VG']
        assert mcu_processor.find_model_by_clock("240MHz") == []

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_model_by_clock("108MHz") == ["GD32VF103CBT6"]
        assert mcu_processor_test.find_model_by_clock("600MHz") == ["i.MX RT1060"]
        assert mcu_processor_test.find_model_by_clock("16MHz") == ["MSP430G2553"]

    def test_find_model_by_market(self):
        mcu_processor = MCUProcessor('ASUS')
        assert mcu_processor.find_model_by_market("通用") == ['STM32F103C8T6', 'STM8S207M8T3B', 'STM8L152M8T6']
        assert mcu_processor.find_model_by_market("高性能") == ['STM32F407VG']

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_model_by_market("通用") == ["GD32VF103CBT6"]
        assert mcu_processor_test.find_model_by_market("跨界(crossover)") == ["i.MX RT1060"]
        assert mcu_processor_test.find_model_by_market("低功耗") == ["MSP430G2553"]
        assert mcu_processor_test.find_model_by_market("高性能") == []

    def test_get_unique_models(self):
        mcu_processor = MCUProcessor('ASUS')
        unique_models = mcu_processor.get_unique_models()
        assert len(unique_models) == 4
        assert "STM32F103C8T6" in unique_models
        assert "STM32F407VG" in unique_models

        mcu_processor_test = MCUProcessor('NJT')
        unique_models = mcu_processor_test.get_unique_models()
        assert len(unique_models) == 2
        assert "STM32F103C8T6" in unique_models
        assert "STM32F407VG" in unique_models

        mcu_processor_test = MCUProcessor('BTRT')
        unique_models = mcu_processor_test.get_unique_models()
        assert len(unique_models) == 3
        assert "GD32VF103CBT6" in unique_models
        assert "i.MX RT1060" in unique_models
        assert "MSP430G2553" in unique_models

    def test_find_company_by_model(self):
        mcu_processor = MCUProcessor('ASUS')
        assert mcu_processor.find_company_by_model("STM32F103C8T6") == 'STMicroelectronics'
        assert mcu_processor.find_company_by_model("STM32F407VG") == 'STMicroelectronics'
        assert mcu_processor.find_company_by_model("ATmega328P") is None
        assert mcu_processor.find_company_by_model("ESP32") is None

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_company_by_model("GD32VF103CBT6") == 'GigaDevice'
        assert mcu_processor_test.find_company_by_model("i.MX RT1060") == 'NXP'
        assert mcu_processor_test.find_company_by_model("MSP430G2553") == 'Texas Instruments'
        assert mcu_processor_test.find_company_by_model("STM32F103C8T6") is None

    def test_find_architecture_by_model(self):
        mcu_processor = MCUProcessor('ASUS')
        assert mcu_processor.find_architecture_by_model("STM32F103C8T6") == '32位元'
        assert mcu_processor.find_architecture_by_model("ATmega328P") is None
        assert mcu_processor.find_architecture_by_model("ESP32") is None

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_architecture_by_model("GD32VF103CBT6") == '32位元'
        assert mcu_processor_test.find_architecture_by_model("i.MX RT1060") == '32位元'
        assert mcu_processor_test.find_architecture_by_model("MSP430G2553") == '16位元'
        assert mcu_processor_test.find_architecture_by_model("STM32F103C8T6") is None

        mcu_processor_test = MCUProcessor('NJT')
        assert mcu_processor_test.find_architecture_by_model("i.MX RT1060") is None
        assert mcu_processor_test.find_architecture_by_model("STM32F103C8T6") == '32位元'
        assert mcu_processor_test.find_architecture_by_model("STM32F407VG") == '32位元'
        assert mcu_processor_test.find_architecture_by_model("STM32F103C8T6") == '32位元'
        assert mcu_processor_test.find_architecture_by_model("ATmega328P") is None

    def test_find_clock_by_model(self):
        mcu_processor = MCUProcessor('ASUS')
        assert mcu_processor.find_clock_by_model("STM32F103C8T6") == '72MHz'
        assert mcu_processor.find_clock_by_model("ATmega328P") is None
        assert mcu_processor.find_clock_by_model("ESP32") is None

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_clock_by_model("GD32VF103CBT6") == '108MHz'
        assert mcu_processor_test.find_clock_by_model("i.MX RT1060") == '600MHz'
        assert mcu_processor_test.find_clock_by_model("MSP430G2553") == '16MHz'
        assert mcu_processor_test.find_clock_by_model("STM32F103C8T6") is None

    def test_find_market_by_model(self):
        mcu_processor = MCUProcessor('ASUS')
        assert mcu_processor.find_market_by_model("STM32F103C8T6") == '通用'
        assert mcu_processor.find_market_by_model("ATmega328P") is None
        assert mcu_processor.find_market_by_model("ESP32") is None

        mcu_processor_test = MCUProcessor('BTRT')
        assert mcu_processor_test.find_market_by_model("GD32VF103CBT6") == '通用'
        assert mcu_processor_test.find_market_by_model("i.MX RT1060") == '跨界(crossover)'
        assert mcu_processor_test.find_market_by_model("MSP430G2553") == '低功耗'
        assert mcu_processor_test.find_market_by_model("STM32F103C8T6") is None

    if __name__ == "__main__":
        pytest.main()


if __name__ == '__main__':
    pytest.main()
