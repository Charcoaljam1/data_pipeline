from enum import Enum
from abc import ABC, abstractmethod
from typing import Optional

class AgentStatus(Enum):
    IDLE = "Idle"
    BUSY = "Busy"
    COMPLETED = "Completed Successfully"
    FAILED = "Failed"

class BaseAgent(ABC):
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.status = AgentStatus.IDLE
        self.error_message: Optional[str] = None

    def set_status(self, new_status: AgentStatus, error_message: Optional[str] = None):
        self.status = new_status
        self.error_message = error_message
        print(f"{self.agent_type}_{self.name} agent status has changed to {self.status.value}")
        if self.error_message:
            print(f"  Error details: {self.error_message}")