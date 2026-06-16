from dataclasses import dataclass
from datetime import datetime


@dataclass
class Event:
    timestamp: datetime
    source: str
    content: str

    @classmethod
    def from_dict(cls, data):
        return cls(
            timestamp=datetime.fromisoformat(
                data["timestamp"].replace("Z", "+00:00")
            ),
            source=data["source"],
            content=data["content"]
        )