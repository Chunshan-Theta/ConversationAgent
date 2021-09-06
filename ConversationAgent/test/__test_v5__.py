from ..LibStage import gen_multi_agent, QAStage, gen_agent
from .. import mock_client_once

"""
# 預設腳本 非等號比較
"""
bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__QA_STAGE__",
            "__STAGE_NAME__": "__FAQ階段__",
            "question": {
                "sys_welcome": "FAQ歡迎",
                "sys_refuse": "FAQ拒絕",
                "sys_complete": ""
            },
            "qa_threshold": 0.0,
            "corpus": {
                "推薦商品": "1"
            },
            "__SAVED_NAME__": {
                "__QA_RESPOND__": "FAQ_r1",
                "__QA_RESPOND_THRESHOLD__": "FAQ_th",
                "__QA_RESPOND_QUESTION__": "FAQ_q1",
                "__QA_RESPOND_SCORE__": "FAQ_s1",
                "__RUNNING_CORPUS__": "FAQ_c1"
            }
        },
        {
            "stage_type": "__LIB_SWITCH_STAGE__",
            "__STAGE_NAME__": "__FAQ切換階段__",
            "stages_filter": [
                [
                    ["FAQ_r1", "FAQ_s1"],
                    ["1", 0.7],
                    "_商品推薦1_",
                    ["=", ">"]
                ],
                [
                    ["FAQ_r1", "FAQ_s1"],
                    ["1", 0.5],
                    "_商品推薦2_",
                    ["=", "<"]
                ]
            ]
        }
    ], "_商品推薦1_": [
        {
            "stage_type": "__RE_STAGE__",
            "__STAGE_NAME__": "__商品推薦階段1__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "",
                "sys_complete": "推薦完成1"
            },
            "__DISABLE_WELCOME__": True
        }
    ], "_商品推薦2_": [
        {
            "stage_type": "__RE_STAGE__",
            "__STAGE_NAME__": "__商品推薦階段2__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "",
                "sys_complete": "推薦完成2"
            },
            "__DISABLE_WELCOME__": True
        }
    ]

}
data = {}
agent = gen_agent(bot_json)

#
text = "hi"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")

text = "推薦商品"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")


text = "hi"
reply_text, data = mock_client_once(agent, text, {})
# print(f"reply_text: {reply_text}")

text = "走開"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")


