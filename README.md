# VoiceFinance

## 摘要

VoiceFinance 是一個語音記帳系統，可以通過說話的方式來記錄財務信息。

利用 Groq 的 Speech to Text API 將語音轉成文字，通過 prompt engineering 判斷日期、時間、金額，並使用 JSON 來記錄數據。前端使用 Flet 框架，後端基於 FastAPI。

## 功能

- 語音輸入記帳
- 自動識別日期、時間和金額
- 使用 JSON 格式來儲存資料
