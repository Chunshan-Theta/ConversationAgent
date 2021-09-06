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
                "__SYS_WELCOME__": ["歡迎句1","歡迎句2","歡迎句3"],
                "__SYS_REFUSE__": ["拒絕句1","拒絕句2","拒絕句3"],
                "__SYS_COMPLETE__": ["完成句1","完成句2","完成句3"]
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
assert ['歡迎句1'] == reply_text or ['歡迎句2'] == reply_text or ['歡迎句3'] == reply_text

text = "不要通過"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['拒絕句1'] == reply_text or ['拒絕句2'] == reply_text or ['拒絕句3'] == reply_text

text = "通過條件"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
assert ['完成句1'] == reply_text or ['完成句2'] == reply_text or ['完成句3'] == reply_text
