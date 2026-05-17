import json
import os
from typing import List, Dict

import google.generativeai as genai
from dotenv import load_dotenv

from catalog import (
    search_catalog,
    load_catalog
)

# Load ENV
load_dotenv()

# Configure Gemini
genai.configure(
    api_key=os.environ.get("GEMINI_API_KEY")
)

# Load catalog
CATALOG = load_catalog("data/catalog.json")

SYSTEM_PROMPT = """
You are an SHL Assessment Recommender Agent.

ONLY discuss SHL assessments.
Ask clarification if query is vague.
Never hallucinate.
Respond ONLY in valid JSON.

Format:
{
  "reply": "text",
  "should_recommend": true,
  "end_of_conversation": false
}
"""


def extract_job_level(text: str):

    text = text.lower()

    if any(x in text for x in ["entry", "fresher", "junior"]):
        return "entry-level"

    if any(x in text for x in ["senior", "lead", "manager"]):
        return "senior"

    if any(x in text for x in ["mid", "experienced", "4 year"]):
        return "mid-professional"

    return ""


def get_test_type(keys):

    if not keys:
        return "K"

    key = keys[0].lower()

    if "personality" in key:
        return "P"

    elif "ability" in key:
        return "A"

    elif "simulation" in key:
        return "S"

    return "K"


def call_llm(messages, catalog_context):

    prompt = SYSTEM_PROMPT

    prompt += "\n\nCATALOG:\n"
    prompt += catalog_context

    prompt += "\n\nCONVERSATION:\n"

    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

    try:

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        raw_text = response.text.strip()

        if "```json" in raw_text:
            raw_text = raw_text.split("```json")[1].split("```")[0].strip()

        elif "```" in raw_text:
            raw_text = raw_text.split("```")[1].split("```")[0].strip()

        return json.loads(raw_text)

    except Exception as e:

        print("LLM ERROR:", e)

        return {
            "reply": "Here are some recommended SHL assessments for this role.",
            "should_recommend": True,
            "end_of_conversation": False
        }


def process_conversation(messages: List[Dict]):

    # FULL conversation use karo
    latest_message = " ".join(
        [m["content"] for m in messages if m["role"] == "user"]
    )

    latest_message_lower = latest_message.lower()

    # Vague query handling
    if len(latest_message.split()) <= 4:

        return {
            "reply": "Could you share the role, skills, and experience level you are hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    vague_phrases = [
        "i need an assessment",
        "need a test",
        "recommend something"
    ]

    if latest_message_lower in vague_phrases:

        return {
            "reply": "Could you share the role, skills, and experience level you are hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # Off-topic refusal
    off_topic = [
        "salary",
        "legal",
        "law",
        "politics",
        "medical"
    ]

    if any(word in latest_message_lower for word in off_topic):

        return {
            "reply": "I can only help with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # Extract job level
    job_level = extract_job_level(latest_message)

    # Search catalog
    results = search_catalog(
        CATALOG,
        query=latest_message,
        job_level=job_level,
        max_results=10
    )

    # Build catalog context
    catalog_context = ""

    for item in results:

        catalog_context += f"""
Name: {item.get('name', '')}
Description: {item.get('description', '')}
URL: {item.get('link', '')}
Keys: {item.get('keys', [])}

"""

    # Call LLM
    llm_response = call_llm(
        messages,
        catalog_context
    )

    recommendations = []

    if results:

        for item in results:

            recommendations.append({
                "name": item.get("name", ""),
                "url": item.get("link", ""),
                "test_type": get_test_type(
                    item.get("keys", [])
                )
            })

    return {
        "reply": llm_response.get(
            "reply",
            "Here are some recommended SHL assessments for this role."
        ),
        "recommendations": recommendations,
        "end_of_conversation": True if recommendations else False
        
    }