import fastapi
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException
from fastapi import File, UploadFile
from groq import Groq
import pyttsx3
from rich import print

from dotenv import load_dotenv
import os
import json

from prompts import question_classification, information_extraction

# Load the environment variables
load_dotenv()
api_key = os.getenv("API_KEY") # groq api key
llm_model = "llama3-70b-8192"

# AI model
client = Groq(
    # This is the default and can be omitted
    api_key=api_key,
)

# Create a FastAPI instance
app = fastapi.FastAPI()

@app.post("/speech_to_text")
async def speech_to_text(audio_data: UploadFile = File(...)):
    audio_content = await audio_data.read()
    try:
        transcription = client.audio.transcriptions.create(
            file=("output.wav", audio_content),
            model="whisper-large-v3",
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            language="zh",  # Optional
            temperature=0.0  # Optional
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return transcription

@app.post("/text_to_speech")
async def text_to_speech(text: str):
    """
    將給定的文字轉換為語音，並回傳結果
    """
    try:
        # 初始化 pyttsx3 引擎
        engine = pyttsx3.init()
        
        # 定義輸出文件名
        output_file = "output.wav"
        
        # 將文字轉換為語音並保存為文件
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        
        # 檢查文件是否生成
        if os.path.exists(output_file):
            print("ok")
            return FileResponse(output_file, media_type='audio/mpeg', filename=output_file)
        else:
            raise HTTPException(status_code=500, detail="生成音頻文件失敗")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/accounting")
async def accounting(text: str):
    """
    記帳服務，使用 LLM 判斷給定的文字是否為記帳相關的內容，如果是，判斷日期、金額、地點、類別等訊息
    """
    # 判斷是否為記帳相關的內容
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": question_classification(text)
                }
            ],
            model=llm_model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(chat_completion.choices[0].message.content)
    if chat_completion.choices[0].message.content == "No":
        return {"message": "Not accounting!"}
    
    # 判斷日期、金額、地點、類別等訊息
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": information_extraction(text)
                }
            ],
            model=llm_model,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    print(chat_completion.choices[0].message.content)
    result_json = json.loads(chat_completion.choices[0].message.content)
    return {"message": f"{result_json}"}