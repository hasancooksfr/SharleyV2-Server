import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Google GenAI Configuration
genai.configure(api_key=os.getenv("API_KEY2"))

generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 5,
}

# Instructions
INSTRUCTIONS = """
You will be given a conversation, a message from the human and a response sent by Robot (AI MODEL).

You have to return the expression, the expression should be one of these below:
Neutral,
Angry,
Sad,
Confused,
Happy

IMPORTANT: the expression should be ONE from the above and only return Expression, NO other words.
"""

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash-lite',
    generation_config=generation_config,
    system_instruction=INSTRUCTIONS
)

chat_sessions = {}

expressions = ['neutral', 'angry', 'sad', 'confused', 'happy']

def get_expression(prompt: str, response: str):
    if 'default' not in chat_sessions:
        chat_sessions['default'] = model.start_chat(history=[])
    
    chat = chat_sessions['default']

    msg = f"""
Return expression of the following conversation:
**Human**: {prompt}
**Bot**: {response}"""

    expression = chat.send_message(msg)

    lowered = expression.text.lower()
    for expr in expressions:
        if expr in lowered:
            return expr