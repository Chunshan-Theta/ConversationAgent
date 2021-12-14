from ..LibStage import gen_multi_agent, QAStage
from .. import mock_client_once, to_bot

bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "請問是要做哪種票種呢？",
                "sys_reply_q2": "請說『月票』或是『單程票』",
                "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
            },
            "is_fits": [
                [
                    "(月票|1280|長期票|定期票)+",
                    "set_level"
                ],
                [
                    "(單程票|單程|一次)+",
                    "set_level"
                ]
            ]
        },
        {
            "stage_type": "Switch",
            "stages_filter": [
                [
                    "set_level",
                    "月票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "1280",
                    "_月票_"
                ],
                [
                    "set_level",
                    "長期票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "定期票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "單程票",
                    "_單程票_"
                ],
                [
                    "set_level",
                    "單程",
                    "_單程票_"
                ],
                [
                    "set_level",
                    "一次",
                    "_單程票_"
                ]
            ]
        }
    ],
    "_月票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "月票的價格為 1280元，是否確認？",
                "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
                "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
            },
            "is_fits": [
                [
                    "(是|好的|好|沒問題)+$",
                    "user_status"
                ],
                [
                    "(否|不|不行|不要|不好)+$",
                    "user_status"
                ]
            ]
        }
    ],
    "_單程票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "",
                "sys_reply_q2": "",
                "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
            },
            "is_fits": [],
            "__DISSABLE_Q1__": True
        }
    ]
}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")
assert reply_text == ['請問是要做哪種票種呢？'], f"ASSERT ERROR: {reply_text}. test_v1_02"

#
text = "月票"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "好"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

'''
#
#
#
#
#
#
#
#
#
#
#
#
#
#
'''

bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "哈囉請問要做什麼？ 目前提供『問答』和『訂票』服務",
                "sys_reply_q2": "目前只提供『問答』和『訂票』服務喔",
                "sys_reply_complete": "好的，將開始 『 %%selected_service%% 』 "
            },
            "is_fits": [
                [
                    "(問答|問題|詢問)+",
                    "selected_service"
                ],
                [
                    "(訂票|票價|買票)+",
                    "selected_service"
                ]
            ]
        },
        {
            "stage_type": "Switch",
            "stages_filter": [
                [
                    "selected_service",
                    "訂票",
                    "_訂票_"
                ],
                [
                    "selected_service",
                    "買票",
                    "_訂票_"
                ],
                [
                    "selected_service",
                    "票價",
                    "_訂票_"
                ],
                [
                    "selected_service",
                    "問答",
                    "_問答_"
                ],
                [
                    "selected_service",
                    "問題",
                    "_問答_"
                ],
                [
                    "selected_service",
                    "詢問",
                    "_問答_"
                ]
            ]
        }
    ],
    "_問答_": [
        {
            "stage_type": "__QA_STAGE__",
            "corpus": {
                "廁所在哪裡": "這裡沒有廁所",
                "詢問處在哪裡": "這裡沒有詢問處",
                "診所在哪裡": "這裡沒有診所",
            },
            "question": {
                "sys_reply_q1": "請問有什麼問題呢？",
                "sys_reply_q2": "",
                "sys_reply_complete": "我有 %%__QA_RESPOND_SCORE__%% 的信心覺得您要問：<br> \n        %%__QA_RESPOND_QUESTION__%% <br> \n        答案是 %%__QA_RESPOND__%% "
            },
            "is_fits": []
        }
    ],
    "_訂票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "請問是要做哪種票種呢？",
                "sys_reply_q2": "請說『月票』或是『單程票』",
                "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
            },
            "is_fits": [
                [
                    "(月票|1280|長期票|定期票)+",
                    "set_level"
                ],
                [
                    "(單程票|單程|一次)+",
                    "set_level"
                ]
            ]
        },
        {
            "stage_type": "Switch",
            "stages_filter": [
                [
                    "set_level",
                    "月票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "1280",
                    "_月票_"
                ],
                [
                    "set_level",
                    "長期票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "定期票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "單程票",
                    "_單程票_"
                ],
                [
                    "set_level",
                    "單程",
                    "_單程票_"
                ],
                [
                    "set_level",
                    "一次",
                    "_單程票_"
                ]
            ]
        }
    ],
    "_月票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "月票的價格為 1280元，是否確認？",
                "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
                "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
            },
            "is_fits": [
                [
                    "(是|好的|好|沒問題)+$",
                    "user_status"
                ],
                [
                    "(否|不|不行|不要|不好)+$",
                    "user_status"
                ]
            ]
        }
    ],
    "_單程票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "",
                "sys_reply_q2": "",
                "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
            },
            "is_fits": [],
            "__DISSABLE_Q1__": True
        }
    ]
}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "我要月票"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "好"
reply_text, data = mock_client_once(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

'''
#
#
#
#
#
#
#
#
#
#
#
#
#
#
'''

from ..LibStage import __LIB_STAGES__, QAStage
import requests

"""
##########
__NEW QAWorkerSTAGE__
##########
"""
__NEW_QUESTIONANSWER__ = "NEW_QUESTIONANSWER"


class QAWorkerSTAGE(QAStage):
    def __init__(self, data):
        super(QAWorkerSTAGE, self).__init__(data)
        self.similar_method = data.get(self.__SIMILAR_METHOD__, "worker_api")
        self.__NLPCORESERVER__ = "http://52.147.71.0:8000"

    def __request_similar_api__(self, text, corpus):
        res = requests.post(url=f"{self.__NLPCORESERVER__}/jobs/{self.similar_method}", json={
            "sentence": [
                text
            ],
            "corpus": corpus})
        return res.json()


# 增加自訂義的類別
__LIB_STAGES__[__NEW_QUESTIONANSWER__] = QAWorkerSTAGE

"""
##########
Bot
##########
"""
bot_json = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "哈囉請問要做什麼？ 目前提供『問答』和『訂票』服務",
                "sys_reply_q2": "目前只提供『問答』和『訂票』服務喔",
                "sys_reply_complete": "好的，將開始 『 %%selected_service%% 』 "
            },
            "is_fits": [
                [
                    "(問答|問題|詢問)+",
                    "selected_service"
                ],
                [
                    "(訂票|票價|買票)+",
                    "selected_service"
                ]
            ]
        },
        {
            "stage_type": "Switch",
            "stages_filter": [
                [
                    "selected_service",
                    "訂票",
                    "_訂票_",
                    "="
                ],
                [
                    "selected_service",
                    "買票",
                    "_訂票_",
                    "="
                ],
                [
                    "selected_service",
                    "票價",
                    "_訂票_",
                    "="
                ],
                [
                    "selected_service",
                    "問答",
                    "_問答_", "="

                ],
                [
                    "selected_service",
                    "問題",
                    "_問答_", "="
                ],
                [
                    "selected_service",
                    "詢問",
                    "_問答_", "="
                ]
            ]
        }
    ],
    "_死亡_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "",
                "sys_reply_q2": "",
                "sys_reply_complete": "死亡路線 "
            },
            "DISSABLE_WELCOME": True
        }

    ],
    "_存活_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "存活路線 1",
                "sys_reply_q2": "存活路線 2",
                "sys_reply_complete": "存活路線 "
            },
            "DISSABLE_WELCOME": True
        }

    ],
    "_問答_": [
        {
            "stage_type": "__QA_STAGE__",
            "corpus": {
                "廁所在哪裡": "這裡沒有廁所",
                "詢問處在哪裡": "這裡沒有詢問處",
                "診所在哪裡": "這裡沒有診所",
            },
            "question": {
                "sys_reply_q1": "請問有什麼問題呢？",
                "sys_reply_q2": "",
                "sys_reply_complete": "我有 %%__QA_RESPOND_SCORE__%% 的信心覺得您要問：<br> \n        %%__QA_RESPOND_QUESTION__%% <br> \n        答案是 %%__QA_RESPOND__%% "
            },
            "is_fits": []
        }, {
            "stage_type": "Switch",
            "stages_filter": [
                [
                    "__QA_RESPOND_SCORE__", 0.5, "_存活_", ">"
                ],
                [
                    "__QA_RESPOND_SCORE__", 0.5, "_死亡_", "<"
                ]
            ]
        }

    ],
    "_訂票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "請問是要做哪種票種呢？",
                "sys_reply_q2": "請說『月票』或是『單程票』",
                "sys_reply_complete": "好的，將開始訂購 %%set_level%% "
            },
            "is_fits": [
                [
                    "(月票|1280|長期票|定期票)+",
                    "set_level"
                ],
                [
                    "(單程票|單程|一次)+",
                    "set_level"
                ]
            ]
        },
        {
            "stage_type": "Switch",
            "stages_filter": [
                [
                    "set_level",
                    "月票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "1280",
                    "_月票_"
                ],
                [
                    "set_level",
                    "長期票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "定期票",
                    "_月票_"
                ],
                [
                    "set_level",
                    "單程票",
                    "_單程票_"
                ],
                [
                    "set_level",
                    "單程",
                    "_單程票_"
                ],
                [
                    "set_level",
                    "一次",
                    "_單程票_"
                ]
            ]
        }
    ],
    "_月票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "月票的價格為 1280元，是否確認？",
                "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』",
                "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        "
            },
            "is_fits": [
                [
                    "(是|好的|好|沒問題)+$",
                    "user_status"
                ],
                [
                    "(否|不|不行|不要|不好)+$",
                    "user_status"
                ]
            ]
        }
    ],
    "_單程票_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_reply_q1": "",
                "sys_reply_q2": "",
                "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        "
            },
            "is_fits": [],
            "__DISSABLE_Q1__": True
        }
    ]
}
data = {}
agent = gen_multi_agent(bot_json)

#
text = "hi"
reply_text, data = to_bot(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "我有點問題"
reply_text, data = to_bot(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")

#
text = "附近有廁所嗎"
reply_text, data = to_bot(agent, text, data)
print(f"data: {data}")
print(f"reply_text: {reply_text}")
