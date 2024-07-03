from litellm import completion
import os 
from dotenv import load_dotenv
load_dotenv()

system = """
คุณคือ AI ผู้ช่วยสนทนาที่เชี่ยวชาญด้านฟุตบอล มีความสามารถในการใช้เครื่องมือในการตอบคำถาม 
ภารกิจของคุณคือการให้คำตอบที่เกี่ยวข้องกับฟุตบอลเท่านั้น
คุณจะต้องตอบกลับในรูปแบบดังต่อไปนี้:
1.การตอบกลับโดยข้อมูลทั่วไป : 
```json 
{ 
"method" : "direct",
"response_msg" : [message for answer],
}
```
2.ตอบกลับแบบใช้ RAG: ค้นหาข้อมูลจากฐานข้อมูลความรู้ (Knowledge Base) ก่อนตอบ : 

```json
{
"method" : "rag",
"query" : [message for query in knowledge],
"knowledge_base_name" : "Special Rules for Football Match",
}
```

**ตัวอย่าง:**
**คำถาม:** "กฏ offside คืออะไร?"
**คำตอบ:**
```json
{
"method" : "direct",
"response_msg" : "กฏ offside เกิดขึ้นเมื่อผู้เล่นฝ่ายรุกอยู่ใกล้ประตูฝ่ายตรงข้ามมากกว่าผู้เล่นฝ่ายรับ 2 คน ยกเว้นผู้รักษาประตูของฝ่ายตรงข้าม",
}
```

**คำถาม:** "มีกฏพิเศษใดบ้างสำหรับการเตะลูกโทษ?"
**คำตอบ:**
```json
{
"method" : "rag",
"query" : "กฎพิเศษสำหรับการเตะลูกโทษ",
"knowledge_base_name" : "กฎพิเศษสำหรับการแข่งขันฟุตบอล",
}
```
Make Sure your response is in JSON format.

"""
chat_session = [
    {"role": "system", "content": system}
]

def get_response(user_input):
    global chat_session
    chat_session.append({"role": "user", "content": user_input})
    response = completion(
        model="claude-3-haiku-20240307",
        messages=chat_session,
        api_key=os.getenv("MODEL_API_KEY")
    )
    chat_session.append({"role": "assistant", "content": response.choices[0].message.content
})
    
    return response.choices[0].message.content
        
    


if __name__ == "__main__":
    while True:
        user_input = input("คุณ: ")
        response = get_response(user_input)
        print(response)
