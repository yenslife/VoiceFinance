from datetime import datetime, timedelta
from rich import print

today = datetime.today()

def question_classification(question):
    """
    判斷該問題是否屬於記帳相關的問題，如果不是就回傳 "Other"，如果是，就回傳 "Yes"
    """    
    prompt = f"""請判斷以下文字是否屬於記帳相關內容，只要有提到花費、花了多少錢，就可以算是記帳內容，並**只回傳 "Yes" 或 "No"**：
'''{question}'''"""
    print(prompt)
    return prompt

def information_extraction(text):
    """
    提取給定的文字中的日期、金額、地點等訊息，並且使用 json 格式回傳，給 prompt 範例
    """
    dates = {
        "今天": today.strftime("%Y-%m-%d"),
        "剛剛": today.strftime("%Y-%m-%d"),
        "剛才": today.strftime("%Y-%m-%d"),
        "昨天": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "3天前": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
        "上禮拜": (today - timedelta(weeks=1)).strftime("%Y-%m-%d"),
        "一週前": (today - timedelta(weeks=1)).strftime("%Y-%m-%d"),
        "兩週前": (today - timedelta(weeks=2)).strftime("%Y-%m-%d"),
        "一個月前": (today - timedelta(weeks=4)).strftime("%Y-%m-%d"),
        "兩個月前": (today - timedelta(weeks=8)).strftime("%Y-%m-%d"),
    }
    weekday_names = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]    
    for i in range(0, 7):
        dates[weekday_names[i]] = (today - timedelta(days=today.weekday() - i)).strftime("%Y-%m-%d")    
    last_weekday_names_0 = ["上週一", "上週二", "上週三", "上週四", "上週五", "上週六", "上週日"]
    last_weekday_names_1 = ["上禮拜一", "上禮拜二", "上禮拜三", "上禮拜四", "上禮拜五", "上禮拜六", "上禮拜日"]
    for i in range(0, 7):
        dates[last_weekday_names_0[i]] = (today - timedelta(days=today.weekday() - i + 7)).strftime("%Y-%m-%d")
        dates[last_weekday_names_1[i]] = (today - timedelta(days=today.weekday() - i + 7)).strftime("%Y-%m-%d")
    print(dates)
    nl = "\n"
    prompt = f"""請提取以下文字中的物品、日期、金額、地點以及備註等訊息，並回傳結果：
'''{text}'''
使用 json 格式回傳提取的結果，例如：
範例一：
{{
    "date": "2022-10-01",
    "amount": 200,
    "location": "彰化",
    "item": "牛肉麵",
    "note": "和朋友一起吃"
}}
範例二：
{{
    "date": "2023-10-01",
    "amount": 150,
    "location": "台北",
    "item": "義大利麵",
    "note": "使用信用卡付款"
}}
如果沒有辦法判斷出日期、金額、地點、類別等訊息，請將該項目設為空字串 \"\"，例如：
{{
    "date": "2023-10-01",
    "amount": "119",
    "location": "",
    "item": "申請會員卡",
    "note": ""
}}

當出現以下日期時，請回傳對應的日期：
{str(dates).replace("'", "").replace(", ", nl).replace("{", "").replace("}", "")}

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

###備註的例子###
請將句子抽出除了日期、金額、地點、類別等訊息之外的其他訊息，例如：
- 我今天和妹妹去全聯買了些飲料，才花五十塊而已就這麼多飲料，不過可惜當天下雨 -> 和妹妹一起去，當天下雨
- 我今天去全家買了咖哩當作我的午餐總共花了60塊超便宜 -> 超便宜的午餐
- 我昨天去超市買菜的時候遇到認識的阿姨，我買了一些食材，總共花了三百元，因為我有和他殺價 -> 和認識的阿姨殺價，變便宜


請只回傳 json 格式的內容，不要有其他文字。
"""
    print(prompt)
    return prompt