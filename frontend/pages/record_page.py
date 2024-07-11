import flet as ft
import requests
import pyaudio
import wave
import threading
import opencc
from datetime import datetime

# components
from custom_controls import AppBar

# api
from api import API_URL

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

def start_recording_thread(query_text_field, page: ft.Page):
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
    cc = opencc.OpenCC('s2twp')
    result_text = cc.convert(result_text)
    print(f"繁體轉換結果: {result_text}")
    query_text_field.value = result_text
    page.update()

def recording_page(page: ft.Page):
    # functions
    def analysis(e):
        url = API_URL + "/accounting"
        params = {
            "text": query_text_field.value
        }
        response = requests.post(url, params=params)
        print(response.json())
        if query_text_field.value != "" and response.json()["message"] != "Not accounting!":
            result_table.controls.pop(1)
            result_table.controls.insert(1, ft.ResponsiveRow(
                [
                    ft.Container(ft.Text(response.json()["message"]['item']), col=2.4),
                    ft.Container(ft.Text(response.json()["message"]['date']), col=2.4),
                    ft.Container(ft.Text(response.json()["message"]['amount']), col=2.4),
                    ft.Container(ft.Text(response.json()["message"]['location']), col=2.4),
                    ft.Container(ft.Text(response.json()["message"]['note']), col=2.4)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ))
        elif query_text_field.value != "" and response.json()["message"] == "Not accounting!":
            result_table.controls.pop(1)
            result_table.controls.insert(1, ft.Text("無法解析"))
            hint_snackbar.content = ft.Text("無法解析")
            hint_snackbar.open = True
        else:
            hint_snackbar.content = ft.Text("請先進行錄音!!!")
            hint_snackbar.open = True
        page.update()

    def add_to_db(e):
        url = API_URL + "/items"
        try:
            json_data = {
                "name": result_table.controls[1].controls[0].content.value,
                "date": result_table.controls[1].controls[1].content.value,
                "amount": result_table.controls[1].controls[2].content.value,
                "location": result_table.controls[1].controls[3].content.value,
                "note": result_table.controls[1].controls[4].content.value,
                "create_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except IndexError:
            print("no data")
            hint_snackbar.content = ft.Text("請先進行解析!!!")
            hint_snackbar.open = True
            page.update()
            return
        response = requests.post(url, json=json_data)
        if response.status_code == 200:
            print(f"add to db: {json_data}")
            hint_snackbar.content = ft.Text("加入資料庫成功")
            hint_snackbar.open = True
        else:
            hint_snackbar.content = ft.Text("加入資料庫失敗")
            hint_snackbar.open = True
        page.update()

    def start_recording(e):
        global is_recording
        if not is_recording:
            start_recording_btn.text = "停止"
            start_hint_text.value = "錄音中..."
            page.update()
            if is_recording:
                return
            is_recording = True
            threading.Thread(target=start_recording_thread, args=(query_text_field, page)).start()
        else:
            is_recording = False
            start_recording_btn.text = "開始錄音"
            start_hint_text.value = "請錄下你的花費以及時間"

    # text veiw
    appbar = AppBar(page=page)
    start_hint_text = ft.Text("請錄下你的花費以及時間", size=18)
    query_text_field = ft.TextField("我昨天買了五隻筆，花了九十塊")
    result_table = ft.Column(
        [
            ft.ResponsiveRow(
                [
                    ft.Container(ft.Text("Item"), col=2.4),
                    ft.Container(ft.Text("Date"), col=2.4),
                    ft.Container(ft.Text("Amount"), col=2.4),
                    ft.Container(ft.Text("Location"), col=2.4),
                    ft.Container(ft.Text("Note"), col=2.4)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.ResponsiveRow(alignment=ft.MainAxisAlignment.CENTER)
        ],
        width=630
    )

    # calculate button
    start_recording_btn = ft.ElevatedButton(text=f"start recording", width=630, on_click=start_recording)
    # stop_recording_btn = ft.ElevatedButton(text=f"stop recording", width=630, on_click=stop_recording)
    analysis_btn = ft.ElevatedButton(text=f"解析", width=630, on_click=analysis)
    add_to_db_btn = ft.ElevatedButton(text=f"加入資料庫", width=630, on_click=add_to_db)

    # snackbar
    hint_snackbar = ft.SnackBar(ft.Text("加入資料庫成功"), action="關閉")
    
    page.views.append(
        ft.View(
            "/recording",
            [
                appbar,
                start_hint_text,
                start_recording_btn,
                ft.ResponsiveRow(
                    [
                        ft.Text("輸入文字："),
                        query_text_field
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    width=630
                ),
                analysis_btn,
                result_table,
                add_to_db_btn,
                hint_snackbar
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )
    )