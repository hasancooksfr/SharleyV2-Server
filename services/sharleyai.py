import os
from dotenv import load_dotenv
import google.generativeai as genai
from services.expressions import get_expression

load_dotenv()

apikey = os.getenv("API_KEY")
# Google GenAI Configuration
genai.configure(api_key=os.getenv("API_KEY"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 400
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
]

# Knowledge Base
knowledge_base = """
SYSTEM INSTRUCTIONS: You are an AI assistant for a serving robot that is made in Sacred Heart Convent School, Sri Ganganagar. Always use this knowledge to answer questions:

=== ABOUT YOU ===
- Name: Sharley
- Full form: Sacred Heart Assistant Robotic Linguist and Expressionist.
- Developed in: 2026
- Also known as: Charlie, Charley (Real Name will be Sharley always, even if asked so!)

=== ABOUT OUR SCHOOL ===
- Name: Sacred Heart Convent School
- Type: Convent School
- Location: Sri Ganganagar, Rajasthan (INDIA)
- Phone: 8233924488
- Email: sacredheartschoolsgnr@gmail.com

=== SERVICES ===
- Robotics Lab (where this bot is made.)
- AC Classrooms
- Trained Teachers
- Unique Teaching Methods
- Affiliated to CBSE(Central Board of Secondary Education)

=== FAQ RESPONSES ===
- AC: "Our school's classrooms are fully air-conditioned."
- Parking: "You can always park your vehicle outside the school"
- Dress Code: "Please visit our website for more detailed dress code"
- Book List: "Please visit our website to get the book list for session 2025-26"
- Developer: "I am developed by a team of Robotics in Sacred Heart Convent School, Sri Ganganagar"

=== IMPORTANT GUIDELINES ===
1. ONLY use the above business info when asked specifically about THIS business/cafe
2. For all OTHER questions (math, weather, general knowledge, creative tasks, etc.), respond normally as a helpful AI assistant
3. You can generate random numbers, help with coding, explain concepts, be creative, etc.
4. Don't force business information into unrelated conversations
5. Be friendly and helpful for all types of questions
6. 

EXAMPLES:
- "What are your hours?" → Use business info
- "Generate a random number" → Generate normally (don't mention business)
- "What's the weather?" → Respond normally (explain you can't check real-time weather)
- "Help me write code" → Help with coding normally
- "Tell me about your coffee" → Use menu information
"""

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash-lite',
    generation_config=generation_config,
    safety_settings=safety_settings,
    system_instruction=knowledge_base
)

chat_sessions = {}

# Functions

def send_message(prompt, sessionid = "default"):
    try:
        if sessionid not in chat_sessions:
            chat_sessions[sessionid] = model.start_chat(history=[])

        chat = chat_sessions[sessionid]

        response = chat.send_message(prompt)

        expression = get_expression(prompt, response.text)

        return {
            "success": True,
            "prompt": prompt,
            "expression": expression,
            "response": response.text,
            "sessionId": sessionid
        }

    except Exception as e:
        return {
            "success": False,
            "detail": "Unexpected error occured",
            "error": str(e)
        }
        print(e)

def history(sessionid = "default"):
    try:
        if sessionid not in chat_sessions:
            return {"success": False, "detail": "Session not found"}

        history = []
        chat = chat_sessions[sessionid]

        for msg in chat.history:
            history.append({
                'role': msg.role,
                'content': msg.parts[0].text if msg.parts else ''
            })

        return {
            "success": True,
            "sessionId": sessionid,
            "history": history,
            "totalMessages": len(history)
        }

    except Exception as e:
        return {
            "success": False,
            "detail": "Unexpected error occured.",
            "error": str(e)
        }
        print(e)

def health_check():
    try:
        if "health" not in chat_sessions:
            chat_sessions['health'] = model.start_chat(history=[])

        chat = chat_sessions['health']
        response = chat.send_message('Health check: reply with OK')

        return {
            "success": True,
            "model": 'gemini-2.5-flash-lite',
            "response": response.text,
            "activeSessions": len(chat_sessions)
        }
    except Exception as e:
        return {
            "success": False,
            "model": 'gemini-2.5-flash-lite',
            "detail": "Unexpected error occured",
            "error": str(e)
        }
        print(e)

