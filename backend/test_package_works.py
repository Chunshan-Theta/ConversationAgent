from ConversationAgent import mock_client, mock_client_once
from ConversationAgent.types.static import __USER_TEXT__
from ConversationAgent.types.memory import Memory
from ConversationAgent.__stage__ import Stage
from ConversationAgent.__agent__ import Agent, MultiAgent
from ConversationAgent.LibStage import gen_multi_agent
from typing import Dict, Any
bot_json: Dict[str, Any] = {
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
agent: MultiAgent = gen_multi_agent(bot_json)
#
text = "hi"
reply_text, data = mock_client_once(agent, text, data)
# print(f"data: {data}")
# print(f"reply_text: {reply_text}")
assert reply_text == ['請問是要做哪種票種呢？'], f"ASSERT ERROR: {reply_text}. test_v1_02"

#
text = "月票"
reply_text, data = mock_client_once(agent, text, data)
# print(f"data: {data}")
# print(f"reply_text: {reply_text}")
assert reply_text == ['好的，將開始訂購 月票', '月票的價格為 1280元，是否確認？'], f"ASSERT ERROR: {reply_text}. test_v1_02"

#
text = "好"
reply_text, data = mock_client_once(agent, text, data)
# print(f"data: {data}")
# print(f"reply_text: {reply_text}")
assert reply_text == ['好的，確認您使用 月票 車廂的意願為 『 好 』，\n            感謝您的使用。\n'], f"ASSERT ERROR: {reply_text}. test_v1_02"
