import json
from typing import List, Dict
import config

class Fetcher:

    def match_score(self, gig: Dict, keywords: List[str]) -> int:
        text = (
            gig.get("title", "") + " " +
            gig.get("description", "") + " " +
            " ".join(gig.get("tags", []))
        ).lower()
        return sum(1 for kw in keywords if kw.lower() in text)

    def fetch_mock_data(self, keywords: List[str]) -> List[Dict[str, any]]:
        with open('sample-gigs-data.json', 'r', encoding='utf-8') as file:
            gigs = json.load(file)

        # Sort with keyword-aware score
        sorted_gigs = sorted(gigs, key=lambda gig: self.match_score(gig, keywords), reverse=True)

        return sorted_gigs[:config.number_of_gigs]
