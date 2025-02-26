import discord
import os 
import google.generativeai as genai 
import json
wsave= input("conversation_history file update\n 1=yes\n other=no\n")
# Google Gemini API 
genai.configure(api_key="API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

# 디스코드 봇 
intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

# 대화 히스토리 파일 경로
HISTORY_FILE = "conversation_history.json"
# 불러오기
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []
# 저장
def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)

# 기존 대화 기록 불러오기
conversation_history = load_history()

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # 가르치기
    if message.content.startswith("ㅠㅎㅅ"):
        user_text = message.content[4:].strip()
        if user_text:
            conversation_history.append(f"User: {user_text}")
            save_history(conversation_history)
            await message.channel.send("✅ 대화가 저장되었습니다!")
        else:
            await message.channel.send("⚠️ 저장할 텍스트를 입력해주세요!")
        return

    # 물음 ㅁㅇ
    if message.content.startswith("ㅠㅁㅇ"):
        user_input = message.content[4:].strip()
        
        if not user_input:
            await message.channel.send("질문을 입력해주세요! (예: ㅠㅁㅇ 날씨 어때?)")
            return
        
        thinking_message = await message.channel.send("sax12d가 답변생성중... 🤔")
        if wsave == 1:
	        conversation_history.append(f"User: {user_input}")
        
        try:
            prompt = "\n".join(conversation_history) + "\nBot:"
            response = model.generate_content(prompt)
            reply = response.text.strip()
            if wsave == 1:
    	        conversation_history.append(f"Bot: {reply}")
            save_history(conversation_history)
        except Exception as e:
            reply = f"Gemini API 호출 중 오류 발생: {e}"
        
        await thinking_message.edit(content=reply)

client.run("YOUT_BOT_TOKEN")
