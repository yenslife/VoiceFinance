from datetime import datetime, timedelta

today = datetime.today()

def question_classification(question):
    """
    判斷該問題是否屬於記帳相關的問題，如果不是就回傳 "Other"，如果是，就回傳 "Yes"
    """    
    prompt = f"""請判斷以下文字是否屬於記帳相關內容，並只回傳 "Yes" 或 "No"：
'''{question}'''"""
    print(prompt)
    return prompt

def information_extraction(text):
    """
    提取給定的文字中的日期、金額、地點等訊息，並且使用 json 格式回傳，給 prompt 範例
    """
    prompt = f"""請提取以下文字中的日期、金額、地點等訊息，並回傳結果：
'''{text}'''
使用 json 格式回傳提取的結果，例如：
範例一：
{{
    "date": "2022-10-01",
    "amount": 200,
    "location": "彰化",
    "item": "牛肉麵",
}}
範例二：
{{
    "date": "2023-10-01",
    "amount": 150,
    "location": "台北",
    "item": "義大利麵",
}}
如果沒有辦法判斷出日期、金額、地點、類別等訊息，請將該項目設為空字串 \"\"，例如：
{{
    "date": "2023-10-01",
    "amount": "119",
    "location": "",
    "item": "申請會員卡",
}}

當出現以下日期時，請回傳對應的日期：
今天：{today.strftime("%Y-%m-%d")}
剛剛：{{today.strftime("%Y-%m-%d")}}
剛才：{{today.strftime("%Y-%m-%d")}}
昨天：{(today - timedelta(days=1)).strftime("%Y-%m-%d")}
3天前：{(today - timedelta(days=3)).strftime("%Y-%m-%d")}
上禮拜：{(today - timedelta(weeks=1)).strftime("%Y-%m-%d")}
一週前：{(today - timedelta(weeks=1)).strftime("%Y-%m-%d")}
兩週前：{(today - timedelta(weeks=2)).strftime("%Y-%m-%d")}
一個月前：{(today - timedelta(weeks=4)).strftime("%Y-%m-%d")}
兩個月前：{(today - timedelta(weeks=8)).strftime("%Y-%m-%d")}

###金額資訊###
一萬塊：10000
一萬元：10000
兩千塊：2000
十五元：15
三百六十五元：365

###地點資訊###
範例：
便利超商
超市
全家
台北
高雄
台南
學校

###其他常用語句###
花了：購買
買了：購買

請只回傳 json 格式的內容，不要有其他文字。
"""
    print(prompt)
    return prompt