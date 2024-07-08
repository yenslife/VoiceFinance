import flet as ft
import requests
import pyaudio
import wave
import threading
import opencc

# components
from custom_controls import AppBar

API_URL = "http://127.0.0.1:8000"

# 錄音狀態
is_recording = False
audio_data = []
result_text = ""

# 設定錄音參數
FORMAT = pyaudio.paInt16  # 錄音格式
CHANNELS = 1  # 錄音通道數，改為1
RATE = 44100  # 錄音取樣率
CHUNK = 1024  # 每次讀取的音頻塊大小
WAVE_OUTPUT_FILENAME = "output.wav"  # 輸出文件名

def start_recording_thread():
    global is_recording, audio_data, stream, p, result_text
    audio_data = []
    p = pyaudio.PyAudio()
    print("開始錄音...")
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while is_recording:
        data = stream.read(CHUNK)
        audio_data.append(data)
    print("錄音結束")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    # 儲存音頻數據
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_data))
    wf.close()

    # request
    with open(WAVE_OUTPUT_FILENAME, 'rb') as f:
        audio_data = f.read()
    file = {'audio_data': audio_data}
    response = requests.post(API_URL + "/speech_to_text", files=file)
    result_text = response.json()['text']
    print(f"辨識結果: {result_text}")

def update_result_text(query_text_field: ft.Text, page: ft.Page):
    global result_text
    while result_text == "":
        query_text_field.value = result_text
    # 簡體字轉繁體字
    cc = opencc.OpenCC('s2twp')
    result_text = cc.convert(result_text)
    query_text_field.value = result_text
    result_text = ""
    page.update()
    print("update result text done")


def recording_page(page: ft.Page):
    # functions
    def accounting(e):
        url = API_URL + "/accounting"
        params = {'text': query_text_field.value}
        response = requests.get(url, params=params)
        result_text.value = response.json()["message"]
        print(response.json()["message"])
        page.update()

    def start_recording(e):
        global is_recording
        if is_recording:
            return
        is_recording = True
        threading.Thread(target=start_recording_thread).start()
    
    def stop_recording(e):
        global is_recording, result_text
        is_recording = False
        threading.Thread(target=update_result_text, args=(query_text_field, page)).start()

    # text veiw
    appbar = AppBar(page=page)
    start_hint_text = ft.Text("請錄下你的花費以及時間", size=18)
    end_hint_text = ft.Text("當錄音結束，按下這個按鈕", size=18)
    query_text_field = ft.TextField("")
    result_text = ft.Text("result")

    # calculate button
    start_recording_btn = ft.ElevatedButton(text=f"start recording", width=630, on_click=start_recording)
    stop_recording_btn = ft.ElevatedButton(text=f"stop recording", width=630, on_click=stop_recording)
    test_btn = ft.ElevatedButton(text=f"確定記帳", width=630, on_click=accounting)
    
    page.views.append(
        ft.View(
            "/recording",
            [
                appbar,
                start_hint_text,
                start_recording_btn,
                end_hint_text,
                stop_recording_btn,
                ft.Row(
                    [
                        ft.Text("輸入文字："),
                        query_text_field
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                test_btn,
                result_text
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    )