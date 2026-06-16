 import json

from models import Event
from retrieval import HybridRetriever
from memory import MemoryBuilder
from query_engine import QueryEngine
from llm import LLMGenerator
from evaluation import Evaluator


def load_events(path):

    with open(
        path,
        "r",
        encoding="utf8"
    ) as f:

        data = json.load(f)

    return [
        Event.from_dict(x)
        for x in data
    ]


def main():

    events = load_events(
        "../data/memorae_mock_events.json"
    )

    retriever = HybridRetriever(
        events
    )

    memory = MemoryBuilder().build(
        events
    )

    llm = LLMGenerator()

    engine = QueryEngine(
        events,
        retriever,
        memory,
        llm
    )

    results = Evaluator().run(
        engine
    )

    print(
        json.dumps(
            results,
            indent=2
        )
    )


if __name__ == "__main__":
    main()
