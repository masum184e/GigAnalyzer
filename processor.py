import pandas as pd
import numpy as np
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
import config

class DataProcessor:
    def __init__(self, gigs_data: List[Dict[str, Any]]):
        self.gigs_data = gigs_data
        self.df = self._create_dataframe()
        self.all_tags = self._extract_all_tags()
        self.tag_counter = Counter(self.all_tags)

    def _create_dataframe(self) -> pd.DataFrame:
        df = []
        for gig in self.gigs_data:
            df.append({
                'title': gig['title'],
                'description': gig['description'],
                'completed_orders': gig['completed_orders'],
                'price': gig['price'],
                'tags': ', '.join(gig['tags']),
                'tag_count': len(gig['tags']),
            })
        
        return pd.DataFrame(df) 

    def _extract_all_tags(self) -> List[str]:
        all_tags = []
        for gig in self.gigs_data:
            all_tags.extend(gig['tags'])
        return all_tags
    
    def get_dataframe(self) -> pd.DataFrame:
        return self.df

    def get_summary_statistics(self) -> Dict[str, Any]:
        return {
            'total_gigs': len(self.gigs_data),
            'total_tags': len(self.all_tags),
            'unique_tags': len(set(self.all_tags)),
            'duplicate_tags': len(self.all_tags) - len(set(self.all_tags)),
            'average_price': self.df['price'].mean(),
            'median_price': self.df['price'].median(),
            'total_orders': self.df['completed_orders'].sum(),
            'average_orders': self.df['completed_orders'].mean(),
        }

    def get_average_price(self) -> float:
        return self.df['price'].mean()
    
    def get_total_orders(self) -> int:
        return self.df['completed_orders'].sum()
        
    def get_keyword_frequency(self) -> Dict[str, int]:
        return dict(self.tag_counter.most_common())
    
    def get_top_keywords(self, n: int = config.number_of_gigs) -> List[Tuple[str, int]]:
        return self.tag_counter.most_common(n)
    
    def get_unique_tags(self) -> List[str]:
        return list(set(self.all_tags))
    
    def get_price_statistics(self) -> Dict[str, float]:
        prices = self.df['price']
        return {
            'mean': prices.mean(),
            'median': prices.median(),
            'std': prices.std(),
            'min': prices.min(),
            'max': prices.max(),
            'q1': prices.quantile(0.25),
            'q3': prices.quantile(0.75)
        }
    
    def get_order_statistics(self) -> Dict[str, float]:
        orders = self.df['completed_orders']
        return {
            'mean': orders.mean(),
            'median': orders.median(),
            'std': orders.std(),
            'min': orders.min(),
            'max': orders.max(),
            'total': orders.sum()
        }

    def get_keyword_correlations(self, min_cooccurrence: int = 2) -> List[Tuple[str, str, int]]:
        co_occurrence = defaultdict(lambda: defaultdict(int))
        
        for gig in self.gigs_data:
            gig_tags = gig['tags']
            for i, tag1 in enumerate(gig_tags):
                for j, tag2 in enumerate(gig_tags):
                    if i != j:
                        co_occurrence[tag1][tag2] += 1
        
        correlations = []
        for tag1, related_tags in co_occurrence.items():
            for tag2, count in related_tags.items():
                if tag1 < tag2 and count >= min_cooccurrence:
                    correlations.append((tag1, tag2, count))
        
        correlations.sort(key=lambda x: x[2], reverse=True)
        return correlations