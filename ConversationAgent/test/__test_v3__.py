from ..LibStage import gen_multi_agent, QAStage, gen_agent
from .. import mock_client_once
import json

"""
# 預設腳本 迴圈式腳本
"""
bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__QA_STAGE__",
            "__STAGE_NAME__": "__開始階段__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "初始句拒絕",
                "sys_complete": ""
            },
            "qa_threshold": 0.8,
            "corpus": {
                "問答服務": "問答服務",
                "商品推薦": "商品推薦",
                "哈囉": "打招呼",
            },
            "__SAVED_NAME__": {
                "__QA_RESPOND__": "hello_r1",
                "__QA_RESPOND_THRESHOLD__": "hello_th",
                "__QA_RESPOND_QUESTION__": "hello_q1",
                "__QA_RESPOND_SCORE__": "hello_s1",
                "__RUNNING_CORPUS__": "hello_c1"
            },
            "__DISABLE_WELCOME__": True
        },
        {
            "stage_type": "__LIB_SWITCH_STAGE__",
            "__STAGE_NAME__": "__開始 切換階段__",
            "stages_filter": [
                [
                    "hello_r1",
                    "問答服務",
                    "_FAQ_"
                ],
                [
                    "hello_r1",
                    "商品推薦",
                    "_商品推薦_"
                ],
                [
                    "hello_r1",
                    "打招呼",
                    "_打招呼_"
                ]
            ]
        }
    ],
    "_打招呼_": [
        {
            "stage_type": "__RE_STAGE__",
            "__STAGE_NAME__": "__打招呼階段__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "",
                "sys_complete": "打招呼完成"
            },
            "__DISABLE_WELCOME__": True,
            "__DISABLE_REFUSE__": True
        }
    ],
    "_商品推薦_": [
        {
            "stage_type": "__RE_STAGE__",
            "__STAGE_NAME__": "__商品推薦階段__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "",
                "sys_complete": "推薦完成"
            },
            "__DISABLE_WELCOME__": True
        }
    ],
    "_FAQ_": [
        {
            "stage_type": "__QA_STAGE__",
            "__STAGE_NAME__": "__FAQ階段__",
            "question": {
                "sys_welcome": "FAQ歡迎",
                "sys_refuse": "FAQ拒絕",
                "sys_complete": ""
            },
            "qa_threshold": 0.7,
            "corpus": {
                "餐飲問題": "1",
                "營業時間": "2",
                "推薦商品": "3"
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
                    "FAQ_r1",
                    "1",
                    "_餐飲問題_"
                ],
                [
                    "FAQ_r1",
                    "2",
                    "_店舖問題_"
                ],
                [
                    "FAQ_r1",
                    "3",
                    "_商品推薦_"
                ]
            ]
        }
    ],
    "_循環FAQ_": [
        {
            "stage_type": "__QA_STAGE__",
            "__STAGE_NAME__": "__循環問答階段__",
            "question": {
                "sys_welcome": "循環FAQ歡迎",
                "sys_refuse": "循環FAQ拒絕",
                "sys_complete": ""
            },
            "qa_threshold": 0.7,
            "corpus": {
                "餐飲問題": "1",
                "營業時間": "2",
                "推薦商品": "3",
                "謝謝": "4"
            },
            "__SAVED_NAME__": {
                "__QA_RESPOND__": "FAQ2_r1",
                "__QA_RESPOND_THRESHOLD__": "FAQ2_th",
                "__QA_RESPOND_QUESTION__": "FAQ2_q1",
                "__QA_RESPOND_SCORE__": "FAQ2_s1",
                "__RUNNING_CORPUS__": "FAQ2_c1"
            }
        },
        {
            "stage_type": "__LIB_SWITCH_STAGE__",
            "__STAGE_NAME__": "__循環問答切換階段__",
            "stages_filter": [
                [
                    "FAQ2_r1",
                    "1",
                    "_餐飲問題_"
                ],
                [
                    "FAQ2_r1",
                    "2",
                    "_店舖問題_"
                ],
                [
                    "FAQ2_r1",
                    "3",
                    "_商品推薦_"
                ],
                [
                    "FAQ2_r1",
                    "4",
                    "_結束_"
                ]
            ]
        }
    ],
    "_店舖問題_": [
        {
            "stage_type": "__RE_STAGE__",
            "__STAGE_NAME__": "__店舖問題階段__",
            "question": {
                "sys_complete": "店舖問題 完成",
                "sys_refuse": "",
                "sys_welcome": ""
            },
            "__DISABLE_WELCOME__": True
        },
        {
            "stage_type": "__LIB_SWITCH_STAGE__",
            "stages_filter": [
                [
                    "*",
                    True,
                    "_循環FAQ_"
                ]
            ]
        }
    ],
    "_餐飲問題_": [
        {
            "stage_type": "__RE_STAGE__",
            "__STAGE_NAME__": "__餐飲問題階段__",
            "question": {
                "sys_complete": "飲品問題 完成",
                "sys_refuse": "",
                "sys_welcome": ""
            },
            "__DISABLE_WELCOME__": True
        },
        {
            "stage_type": "__LIB_SWITCH_STAGE__",
            "__STAGE_NAME__": "__餐飲問題切換階段__",
            "stages_filter": [
                [
                    "*",
                    True,
                    "_循環FAQ_"
                ]
            ]
        }

    ],
    "_結束_": [
        {
            "stage_type": "__RE_STAGE__",
            "__STAGE_NAME__": "__結束階段__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "",
                "sys_complete": "_結束_ 結束"
            },
            "__DISABLE_WELCOME__": True
        }
    ]
}


def output2file(data, filename="sample.json"):
    with open(f"./{filename}", "w") as f:
        json.dump(data, f, ensure_ascii=False)


data = {}
agent = gen_agent(bot_json)

#
text = "hi"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")
# print(f"data: {data}")
assert ['初始句拒絕'] == reply_text

#
text = "問答服務"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")
# print(f"data: {data}")
assert ['FAQ歡迎'] == reply_text

#
text = "餐飲問題"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")
# print(f"data: {data}")
# output2file(data, "0.json")

assert ['飲品問題完成', '循環FAQ歡迎'] == reply_text

#
text = "餐飲問題"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")
# print(f"data: {data}")
# output2file(data, "1.json")

assert ['飲品問題完成', '循環FAQ歡迎'] == reply_text

#
text = "餐飲問題"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")
# print(f"data: {json.dumps(data,ensure_ascii=False)}")
# output2file(data, "2.json")
assert ['飲品問題完成', '循環FAQ歡迎'] == reply_text


#
text = "餐飲問題"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")
# print(f"data: {data}")
# output2file(data, "3.json")
assert ['飲品問題完成', '循環FAQ歡迎'] == reply_text

#
text = "餐飲問題"
reply_text, data = mock_client_once(agent, text, data)
print(f"reply_text: {reply_text}")
# print(f"data: {data}")
# output2file(data, "4.json")
assert ['飲品問題完成', '循環FAQ歡迎'] == reply_text
