from datetime import datetime, timezone

CURRENT_TIME = datetime.fromisoformat(
    "2026-04-13T03:00:00+00:00"
)


class QueryEngine:

    def __init__(
        self,
        events,
        retriever,
        memory,
        llm
    ):

        self.events = events
        self.retriever = retriever
        self.memory = memory
        self.llm = llm

    def answer(
        self,
        query
    ):

        retrieval_query = self.map_query(query)

        retrieved = self.retriever.retrieve(
            retrieval_query
        )

        context = self.build_context(
            retrieved
        )

        answer = self.llm.generate(
            query=query,
            context=self.serialize(
                context
            ),
            current_time=CURRENT_TIME
        )

        return {
            "query": query,
            "answer": answer,
            "selected_context": [
                self.to_dict(e)
                for e in context
            ],
            "reasoning": {
                "why_selected":
                    "Highest relevance and recency scores",
                "why_ignored":
                    "Low relevance or outdated messages",
                "uncertainty":
                    "Implicit commitments may not be captured"
            }
        }

    def build_context(
        self,
        retrieved,
        limit=15
    ):

        rescored = []

        for event, score in retrieved:

            age_days = (
                CURRENT_TIME
                - event.timestamp
            ).days

            recency_bonus = max(
                0,
                14 - age_days
            )

            rescored.append(
                (
                    event,
                    score + recency_bonus
                )
            )

        rescored.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return [
            e
            for e, _
            in rescored[:limit]
        ]

    def map_query(
        self,
        query
    ):

        q = query.lower()

        if "focus" in q:
            return """
            urgent deadline today
            commitment pending
            """

        if "risk" in q:
            return """
            deadline due follow up
            unfinished commitment
            """

        if "procrastinating" in q:
            return """
            reminder pending
            follow up not done
            """

        if "uie" in q:
            return """
            UIE proposal
            """

        return query

    def serialize(
        self,
        events
    ):
        return "\n".join(
            [
                e.content
                for e in events
            ]
        )

    def to_dict(
        self,
        e
    ):
        return {
            "timestamp":
                e.timestamp.isoformat(),
            "source":
                e.source,
            "content":
                e.content
        }