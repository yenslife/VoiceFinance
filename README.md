# VoiceFinance

## 摘要

VoiceFinance 是一個語音記帳系統，可以通過說話的方式來記錄財務信息。

利用 Groq 的 Speech to Text API 將語音轉成文字，通過 prompt engineering 判斷日期、時間、金額，並使用 JSON 來記錄數據。前端使用 Flet 框架，後端基於 FastAPI。

## 功能

- 語音輸入記帳
- 自動識別日期、時間和金額
- 使用 JSON 格式來儲存資料

## 安裝

如果使用 MacOS 系統，你會需要先安裝 portaudio 才能使用 pyaudio。其他系統請參考 pyaudio 的安裝說明。

```bash
brew install portaudio
brew install ffmpeg
```

安裝需要的套件

```bash
pip install -r requirements.txt
```

### 注意事項
- pyttsx3 可能要換 py3-tts 才不會遇到[問題](https://stackoverflow.com/questions/77197398/error-running-pyttsx3-code-on-os-x-nameerror-name-objc-is-not-defined)
- 使用 `save_to_file` 函式時，需要將副檔名指定為 wav 才不會出錯

### API key

請自行到 Groq 上取得 API key，並參考 `backend/.env.example` 來設定 API_KEY，將資料寫入 `backend/.env` 中。

## Inspiration

[用文字生成打造下一代的使用者體驗 @ Let's visionOS 2024](https://youtu.be/obRTOtKp8OQ?si=3G4PEgkthYuYquRZ)