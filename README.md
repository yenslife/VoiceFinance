# 語音記帳系

摘要: 我想要做一個可以用說話的方式來計帳的系統

說明: 利用 groq 的 Speech to Text API 將文字轉成語音，透過 prompt engineering 判斷日期、時間、金額，使用 json 來紀錄。前端使用 flet，後端使用 FastAPI。