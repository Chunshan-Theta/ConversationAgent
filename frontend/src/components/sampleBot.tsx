
export let botSample = {
    "__MAIN_STAGES__": [
    {
        "__STAGE_NAME__": "開始詢問",
        "is_fits": [
        [
            "(月票|1280|長期票|定期票)+",
            "set_level"
        ],
        [
            "(單程票|單程|一次)+",
            "set_level"
        ]
        ],
        "question": {
        "sys_reply_complete": "好的，將開始訂購 %%set_level%% ",
        "sys_reply_q1": "請問是要做哪種票種呢？",
        "sys_reply_q2": "請說『月票』或是『單程票』"
        },
        "stage_type": "__RE_STAGE__"
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
    "_單程票_": [
    {
        "__DISSABLE_Q1__": true,
        "__STAGE_NAME__": "單程開始",
        "is_fits": [],
        "question": {
        "sys_reply_complete": "如果要訂購單程票，請使用票卷機，感謝您的使用。\n        ",
        "sys_reply_q1": "",
        "sys_reply_q2": ""
        },
        "stage_type": "__RE_STAGE__"
    }
    ],
    "_月票_": [
    {
        "__STAGE_NAME__": "月票開始",
        "is_fits": [
        [
            "(是|好的|好|沒問題)+$",
            "user_status"
        ],
        [
            "(否|不|不行|不要|不好)+$",
            "user_status"
        ]
        ],
        "question": {
        "sys_reply_complete": "好的，確認您使用 %%set_level%% 車廂的意願為 『 %%user_status%% 』，\n            感謝您的使用。\n        ",
        "sys_reply_q1": "月票的價格為 1280元，是否確認？",
        "sys_reply_q2": "月票的價格為 1280元，是否確認？請回答『是』或『否』"
        },
        "stage_type": "__RE_STAGE__"
    }
    ]
  }