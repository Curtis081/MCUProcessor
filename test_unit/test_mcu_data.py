import pytest

from src.mcu_data import mcu_data


class TestMCUData:
    def test_mcu_data_keys(self):
        required_keys = {"MCU型號", "生產公司", "核心架構", "時脈", "市場"}
        for entry in mcu_data:
            assert set(entry.keys()) == required_keys, "All entries must contain the required keys"

    def test_clock_speed_format(self):
        for entry in mcu_data:
            clock_speed = entry["時脈"]
            assert clock_speed.endswith("MHz"), f"Clock speed must be specified in MHz, found: {clock_speed}"
            numeric_part = clock_speed[:-3]  # Remove the "MHz" part
            assert numeric_part.isdigit(), f"Clock speed's numeric part must be a number, found: {numeric_part}"

    def test_unique_mcu_models(self):
        models = [entry["MCU型號"] for entry in mcu_data]
        assert len(models) == len(set(models)), "MCU models must be unique"

    def test_clock_speed_values(self):
        for entry in mcu_data:
            clock_speed = int(entry["時脈"][:-3])  # Convert "72MHz" to 72, for example
            assert 1 <= clock_speed <= 600, "Clock speed must be between 1MHz and 600MHz"

    def test_duplicate_mcu_models(self):
        model_counts = {}
        duplicates = []
        for mcu in mcu_data:
            model = mcu["MCU型號"]
            if model in model_counts:
                duplicates.append(model)
            else:
                model_counts[model] = 1
        assert not duplicates, f"重複的 MCU 型號: {', '.join(duplicates)}"


if __name__ == '__main__':
    pytest.main()
