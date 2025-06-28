import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from processor import DataProcessor
import config

class Visualizer:
    def __init__(self, processor: DataProcessor):
        self.processor = processor
        self.df = processor.get_dataframe()

    def create_top_keywords_chart(self, top_n: int = config.NUMBER_OF_GIGS) -> go.Figure:
        top_keywords = self.processor.get_top_keywords(top_n)
        
        if not top_keywords:
            return self._create_empty_chart("No keywords found")
        
        keywords, counts = zip(*top_keywords)
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(keywords),
                y=list(counts),
                marker_color=config.CHART_COLORS[:len(keywords)],
                text=list(counts),
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title=f'Top {top_n} Most Used Keywords',
            xaxis_title='Keywords',
            yaxis_title='Frequency',
            showlegend=False,
            height=500
        )
        
        return fig

    def create_keyword_distribution_pie(self) -> go.Figure:
        total_tags = len(self.processor.all_tags)
        unique_tags = len(self.processor.get_unique_tags())
        duplicate_tags = total_tags - unique_tags
        
        if total_tags == 0:
            return self._create_empty_chart("No tags found")
        
        fig = go.Figure(data=[
            go.Pie(
                labels=['Unique Keywords', 'Duplicate Keywords'],
                values=[unique_tags, duplicate_tags],
                hole=0.3,
                marker_colors=['#FF9999', '#66B2FF']
            )
        ])
        
        fig.update_layout(
            title='Distribution of Unique vs Duplicate Keywords',
            annotations=[dict(text=f'Total: {total_tags}', x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        
        return fig
    
    def create_keyword_correlation_chart(self, top_n: int = config.NUMBER_OF_GIGS) -> go.Figure:
        correlations = self.processor.get_keyword_correlations()
        
        if not correlations:
            return self._create_empty_chart("No keyword correlations found")
        
        top_correlations = correlations[:top_n]
        labels = [f"{corr[0]} + {corr[1]}" for corr in top_correlations]
        values = [corr[2] for corr in top_correlations]
        
        fig = go.Figure(data=[
            go.Bar(
                x=values,
                y=labels,
                orientation='h',
                marker_color=px.colors.sequential.Viridis[:len(values)],
                text=values,
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title=f'Top {top_n} Keyword Correlations',
            xaxis_title='Co-occurrence Count',
            yaxis_title='Keyword Pairs',
            height=600
        )
        
        return fig

    def _create_empty_chart(self, message: str) -> go.Figure:
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            height=400
        )
        return fig