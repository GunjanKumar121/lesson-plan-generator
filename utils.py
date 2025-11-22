import google.generativeai as genai
import json
import streamlit as st

def generate_lesson_plan(grade, subject, topic, duration, api_key):
    """
    Generates a lesson plan using Google's Gemini API.
    """
    if not api_key:
        return {"error": "API Key is missing."}
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        
        prompt = f"""
        Create a detailed lesson plan for a {duration} class.
        Class/Grade: {grade}
        Subject: {subject}
        Topic: {topic}
        
        Return the response strictly as a valid JSON object with the following structure:
        {{
            "topic": "{topic}",
            "subject": "{subject}",
            "grade": "{grade}",
            "duration": "{duration}",
            "objectives": ["List of learning objectives"],
            "introduction": "A short story or hook to introduce the topic",
            "explanation_steps": ["Step 1: ...", "Step 2: ..."],
            "activities": [
                {{
                    "title": "Activity Title",
                    "time": "Duration",
                    "description": "Brief description"
                }}
            ],
            "real_life_examples": ["Example 1", "Example 2"],
            "blackboard_summary": ["Key point 1", "Key point 2"],
            "homework": ["Homework item 1", "Homework item 2"],
            "homework": ["Homework item 1", "Homework item 2"],
            "assessment": ["Question 1", "Question 2"],
            "image_keywords": ["keyword1", "keyword2", "keyword3", "keyword4"]
        }}
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Clean up potential markdown formatting in response
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
            
        return json.loads(text)
        
    except Exception as e:
        return {"error": str(e)}

