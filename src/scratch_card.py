from enum import Enum

class AgentStatus(Enum):
    IDLE = "Idle"
    BUSY = "Busy"
    COMPLETED = "Completed Successfully"
    FAILED = "Failed"


print(AgentStatus)