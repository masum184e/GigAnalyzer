import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from typing import List, Dict, Any
from decouple import config
import streamlit as st

# GOOGLE_API_KEY = config('GOOGLE_API_KEY')
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

class Intelligence:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=GOOGLE_API_KEY)

    def generate_optimized_metadata(self, gig_data: List[Dict[str, any]]) -> Dict[str, str]:
        if hasattr(gig_data, "to_dict"):
            gig_data = gig_data.to_dict(orient="records")
        messages  = self._build_prompt(gig_data)

        try:
            response = self.model.invoke(messages)
            return response.content if hasattr(response, "content") else str(response)
        except Exception as exception:
            print(f"Error generating content: {exception}")
            return "Error generating content"

    def _build_prompt(self, gigs: List[Dict[str, any]]) -> str:
        example_input = "\n\n".join([
            f"Title: {gig['title']}\n"
            f"Description: {gig['description']}\n"
            f"Tags: {gig['tags']}"
            for gig in gigs
        ])

        chat_prompt_template = ChatPromptTemplate.from_messages([
            SystemMessage(content=(
                "You're an expert SEO content strategist. Based on the following gig dataset, "
                "generate the most SEO-optimized metadata. "
                "Only respond with the formatted output. Do not include any explanation or intro text."
            )),
            HumanMessage(content=(
                "Generate the most SEO-optimized:\n"
                "1. Title (under 60 characters, catchy and keyword-focused)\n"
                "2. A detailed, SEO-rich description (300-350 words) highlighting value, services, and unique selling points\n"
                "3. 5 unique and high-traffic SEO keywords\n\n"
                "### Input Dataset:\n"
                f"{example_input}\n\n"
                "### Output Format:\n"
                "Title: ...\n"
                "Description: ...\n"
                "Keywords: keyword1, keyword2, keyword3, keyword4, keyword5"
                ))
        ])

        formatted_messages = chat_prompt_template.format_messages(input=example_input)
        return formatted_messages
