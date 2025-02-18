import discord
import os
import google.generativeai as genai

# 환경 변수에서 API 키 가져오기
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Google Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 디스코드 봇 설정
intents = discord.Intents.all()
intents.messages = True
client = discord.Client(intents=intents)

# 대화 히스토리 저장 (예시: "너 누구야?" 질문과 답변)
conversation_history = [
    "User: 너가 누구냐고 물으면 저는 sax12d입니다 라고 말해",
    "Bot: 만약 누군가가 '너 누구야?'라고 묻는다면 저는 '저는 sax12d입니다'라고 대답할 것입니다."
]

@client.event
async def on_ready():
    print(f'✅ Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("ㅠㅁㅇ"):
        user_input = message.content[4:].strip()

        if not user_input:
            await message.channel.send("질문을 입력해주세요! (예: ㅠㅁㅇ 날씨 어때?)")
            return

        # "생각중..." 메시지 먼저 전송
        thinking_message = await message.channel.send("saaaaaaaaaaaad가 생각중... 🤔")

        # 대화 히스토리에 질문 추가
        conversation_history.append(f"User: {user_input}")

        try:
            # 대화 히스토리 기반으로 응답 생성
            prompt = "\n".join(conversation_history) + "\nBot:"
            response = model.generate_content(prompt)
            reply = response.text.strip()  # response.text로 답변을 추출합니다.

            # 대화 히스토리에 봇의 답변도 저장
            conversation_history.append(f"Bot: {reply}")

        except Exception as e:
            reply = f"Gemini API 호출 중 오류 발생: {e}"

        # 기존 "생각중..." 메시지를 수정하여 답변 출력
        await thinking_message.edit(content=reply)

client.run(DISCORD_BOT_TOKEN)