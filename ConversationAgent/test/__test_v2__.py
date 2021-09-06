from ..LibStage import gen_multi_agent, QAStage, gen_agent
from .. import mock_client_once

"""
# 預設腳本
"""
bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__RE_STAGE__",
            "__SYS_QUESTION__": {
                "__SYS_WELCOME__": "歡迎句",
                "__SYS_REFUSE__": "拒絕句",
                "__SYS_COMPLETE__": "完成句"
            },
            "is_fits": [
                [
                    "(通過條件)+",
                    "set_level"
                ]
            ]
        }
    ]
        
}
data = {}
agent = gen_agent(bot_json)

#
text = "hi"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['歡迎句'] == reply_text

text = "不要通過"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['拒絕句'] == reply_text

text = "通過條件"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['完成句'] == reply_text


"""
# 關閉Welcome問題
"""
bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "歡迎句",
                "sys_reply_q2": "拒絕句",
                "sys_reply_complete": "完成句"
            },
            "is_fits": [
                [
                    "(通過條件)+",
                    "set_level"
                ]
            ],
            "__DISABLE_WELCOME__": True
        }
    ]
        
}
data = {}
agent = gen_multi_agent(bot_json)

text = "不要通過"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['拒絕句'] == reply_text, f"['拒絕句'] == {reply_text}"

text = "通過條件"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['完成句'] == reply_text, f"['完成句'] == {reply_text}"

"""
# 關閉REFUSE問題
"""

bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "歡迎句",
                "sys_reply_q2": "拒絕句",
                "sys_reply_complete": "完成句"
            },
            "is_fits": [
                [
                    "(通過條件)+",
                    "set_level"
                ]
            ],
            "__DISABLE_REFUSE__": True
        }
    ]

}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['歡迎句'] == reply_text, f"['歡迎句'] == {reply_text}"


text = "測試"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['完成句'] == reply_text, f"['完成句'] == {reply_text}"
