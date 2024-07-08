import flet as ft
import requests
import pyaudio
import wave
import threading

API_URL = "http://127.0.0.1:8000"

# 錄音狀態
is_recording = False
audio_data = []

# 設定錄音參數
FORMAT = pyaudio.paInt16  # 錄音格式
CHANNELS = 1  # 錄音通道數，改為1
RATE = 44100  # 錄音取樣率
CHUNK = 1024  # 每次讀取的音頻塊大小
WAVE_OUTPUT_FILENAME = "output.wav"  # 輸出文件名

def start_recording_thread():
    global is_recording, audio_data, stream, p
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

# GUI part
def main(page: ft.Page):
    global is_recording

    # GUI的排版
    page.title = "Taiwan High Speed Rail Fare System"
    page.window_width = 750
    page.window_height = 600
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def start_recording(e):
        global is_recording
        if is_recording:
            return
        is_recording = True
        threading.Thread(target=start_recording_thread).start()
        page.update()
    
    def stop_recording(e):
        global is_recording
        is_recording = False
        page.update()


    # ------建立物件------
    # text veiw
    start_hint_text = ft.Text("請錄下你的花費以及時間", size=18)
    end_hint_text = ft.Text("當錄音結束，按下這個按鈕", size=18)
    start_text = ft.Text("")
    end_text = ft.Text("")
    result_text = ft.Text("")

    # calculate button
    start_recording_btn = ft.ElevatedButton(text=f"start recording", width=630, on_click=start_recording)
    stop_recording_btn = ft.ElevatedButton(text=f"stop recording", width=630, on_click=stop_recording)

    # ------將物件進行排版------
    page.add(start_hint_text,
             start_recording_btn,
             end_hint_text,
            stop_recording_btn,
            start_text,
            end_text,
            result_text
            )

ft.app(target=main)