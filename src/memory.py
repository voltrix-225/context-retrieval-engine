import re
from collections import defaultdict


class MemoryBuilder:

    COMMITMENT_PATTERNS = [
        r"\bneed to\b",
        r"\bmust\b",
        r"\bdue\b",
        r"\bdeadline\b",
        r"\bsubmit\b",
        r"\bfinish\b",
        r"\bcomplete\b",
        r"\bfollow up\b",
    ]

    PROJECT_KEYWORDS = [
        "uie",
        "proposal",
        "roadmap",
        "budget",
        "launch",
    ]

    def build(self, events):

        commitments = []
        projects = defaultdict(list)

        for event in events:

            text = event.content.lower()

            if any(
                re.search(pattern, text)
                for pattern in self.COMMITMENT_PATTERNS
            ):
                commitments.append(event)

            for keyword in self.PROJECT_KEYWORDS:

                if keyword in text:
                    projects[keyword].append(event)

        return {
            "commitments": commitments,
            "projects": projects
        }