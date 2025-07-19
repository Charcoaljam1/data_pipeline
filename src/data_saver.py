from src.agents import BaseAgent, AgentStatus
from abc import abstractmethod
import json
from pathlib import Path

class BaseDataSaver(BaseAgent):
    def __init__(self, name: str):
        super().__init__(name=name, agent_type="Data Saver")
    @abstractmethod
    def save_data(self, data: dict, name: str):
        pass


class JSONFileSaver(BaseDataSaver):
    def __init__(self, output_directory: Path):
        super().__init__(name="JSON File")

        self.output_directory =  output_directory
        self.output_directory.mkdir(parents=True, exist_ok=True)

    def save_data(self, data: dict):
        self.set_status(AgentStatus.BUSY)
        for key, values in data.items():
            for symbol, info in values.items():
                filename = f'{symbol}_{key}.json'
                filepath = self.output_directory / filename
                try:
                    with open(filepath, 'w') as file:
                        json.dump(info, file, indent=4)
                    print(f"Data '{symbol}_{key}' saved successfully to {filepath}")
                except TypeError as e:
                    print(f"Error: Data for '{symbol}_{key}' is not JSON serializable: {e}")
                except Exception as e:
                    print(f"Error saving data '{symbol}_{key}' to {filepath}: {e}")

        self.set_status(AgentStatus.COMPLETED)