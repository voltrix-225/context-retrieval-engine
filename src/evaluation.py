class Evaluator:

    QUERIES = [
        "What should I focus on today?",
        "What commitments am I at risk of missing?",
        "What have I been procrastinating on?",
        "Summarize everything related to the UIE proposal."
    ]

    def run(
        self,
        engine
    ):

        results = []

        for query in self.QUERIES:
            results.append(
                engine.answer(query)
            )

        return results
