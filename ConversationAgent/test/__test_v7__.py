import json

from ..LibStage import gen_multi_agent, QAStage, gen_agent
from .. import mock_client_once

"""
# 預設腳本 __classify_Stage__
"""
bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__Classify_STAGE__",
            "__STAGE_NAME__": "標籤抓取",
            "question": {
                "sys_welcome": "共抓取5種標籤： 生氣 開心 難過 愉快 悲傷 ",
                "sys_refuse": "拒絕： %%result%% ",
                "sys_complete": "完成： %%result%% "
            },
            "__Classify_THRESHOLD__": 1.0,
            "is_fits": [
                [".*生氣.*", "生氣"],
                [".*開心.*", "開心"],
                [".*難過.*", "難過"],
                [".*愉快.*", "愉快"],
                [".*悲傷.*", "悲傷"],
            ],
            "__SAVED_NAME__": {
                "__SAVE_Classify_THRESHOLD__": "__SAVE_Classify_THRESHOLD__",
                "__SAVE_Classify_PASS__": "__SAVE_Classify_PASS__",
                "__SAVE_Classify_Best__": "__SAVE_Classify_Best__",
                "__SAVE_Classify_result__": "result"
            }
        }
    ]
}
agent = gen_agent(bot_json)

#
text = "hi"
reply_text, data = mock_client_once(agent, text, {})
print(f"reply_text: {reply_text}")

#
text = "開心"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")


#
text = "hi"
reply_text, data = mock_client_once(agent, text, {})
print(f"reply_text: {reply_text}")
#
text = "請拒絕"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")