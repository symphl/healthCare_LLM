from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv ()
class ChatOpenRouter(ChatOpenAI):
    openai_api_base: str
    openai_api_key: str
    model_name: str

    def __init__(self,
                 model_name: str,
                 openai_api_key: str = os.getenv('OPENROUTER_API_KEY'),
                 openai_api_base: str = "https://openrouter.ai/api/v1",
                 **kwargs):
        openai_api_key = openai_api_key or os.getenv('OPENROUTER_API_KEY')
        super().__init__(openai_api_base=openai_api_base,
                         openai_api_key=openai_api_key,
                         model_name=model_name, **kwargs)
        

llm = ChatOpenRouter(
    model_name="deepseek/deepseek-r1:free"
)
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")

template_medical = ChatPromptTemplate.from_template("""
**Medical Consultation Request**
Patient Profile:
- Age: {age}
- Gender: {gender}
- Medical Query: {query}

**Instructions for the AI Medical Consultant:**
1. Provide a professional yet compassionate response to the patient's concern
2. Offer a preliminary assessment based on the information provided
3. List possible common conditions that might relate to these symptoms (without diagnosing)
4. Suggest basic self-care recommendations when appropriate
5. Clearly state when professional medical attention is required
6. Maintain a structured, easy-to-understand format

**Response Structure:**
1.Preliminary Assessment
Provide your initial thoughts on the query based on the information given.

2.Possible Considerations
List 2-3 potential conditions that might relate (emphasize this is not a diagnosis).

3.Self-Care Suggestions
Offer 2-3 basic recommendations if the case appears mild (hydration, rest, OTC options etc).

4.When to Seek Help
Clearly state warning signs that warrant immediate medical attention.

5.Disclaimer
Remind that this is informational only and not a substitute for professional medical advice.

**Begin Response:**
""")

template_mental = ChatPromptTemplate.from_template("""
Therapy Session Request  
Client Profile:  
- Age: {age}  
- Gender: {gender}  
- Stress Level (1-10): {stress_level}  
- Sleep Quality: {sleep_quality}  
- Current Mood: {current_mood}  
- What’s on Your Mind?: {thoughts}  

Instructions for the AI Therapist:  
1. Respond with **empathy, warmth, and non-judgmental support**.  
2. **Validate emotions** before offering guidance.  
3. Use **open-ended questions** to encourage reflection.  
4. Provide **evidence-based coping strategies** (CBT, mindfulness, grounding techniques).  
5. **Avoid diagnosing**—focus on emotional support and self-awareness.  
6. Structure the response clearly under **bold headings**.  

**Response Structure:**  
**Emotional Validation**  
Acknowledge feelings (e.g., *"It sounds like you’re carrying a lot right now..."*).  

**Exploration**  
Ask 1-2 reflective questions (e.g., *"What feels heaviest about this?"*).  

**Coping Strategies**  
Suggest 2-3 tailored techniques based on stress/sleep/mood:  
- For stress: Deep breathing, journaling, or a short walk.  
- For poor sleep: Sleep hygiene tips or a calming routine.  
- For low mood: Positive activity scheduling or gratitude practice.  

**When to Seek Help**  
Gently recommend professional support if severity is high (e.g., *"If these feelings persist, a therapist could offer deeper tools..."*).  

**Closing Affirmation**  
End with encouragement (e.g., *"You’re not alone in this. Small steps matter."*).  

**Begin Response:**  
""")

medical_chain = template_medical | llm
mental_chain = template_mental | llm


def medical_consultation(age, gender, query):
    medical = medical_chain.invoke({
        "age": f'{age}',
        "gender": f'{gender}',
        "query": f'{query}'
    })
    return medical.content

def mental_consultation(age, gender, stress_level, sleep_quality, current_mood, thoughts):
    mental = mental_chain.invoke({
        "age": f'{age}',
        "gender": f'{gender}',
        "stress_level": f'{stress_level}',
        "sleep_quality": f'{sleep_quality}',
        "current_mood": f'{current_mood}',
        "thoughts": f'{thoughts}'
    })
    return mental.content

# age = "18"
# gender = "Female"
# stress_level = "high"
# sleep = "Good"
# mood = "Depressed"
# thoughts = "I am having bad thoughts i feel like I am an idiot idk what to do anymore"

# print(mental_consultation(age, gender, stress_level, sleep, mood, thoughts))