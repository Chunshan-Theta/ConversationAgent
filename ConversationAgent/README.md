## 說明
不需資料庫之對話腳本代理。

## agent
`agent`可以透過Json來產生對話核心，為此我們有一個接口可以使用
```
from ConversationAgent.LibStage import gen_agent
from ConversationAgent import to_bot
```
- 透過"ConversationAgent.LibStage.gen_agent"方法來建置機器人
- 透過"ConversationAgent.to_bot"方式與機器人溝通
    - 該方法需要三個參數
        - agent代理物件: gen_agent 產生
        - text: 使用者輸入內容，字串內容
        - data: 過場資訊，預設使用`{}`空字典，第二次與之後溝通應該戴上 `to_bot` 回傳的資料。
    - 該方法會回傳機器人回應與過場資訊，下次溝通保留該過場資訊在進行溝通。
    
### Quick start
```
from ConversationAgent.LibStage import gen_agent
import ConversationAgent
bot = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__QA_STAGE__",
            "qa_threshold": 1,
            "__STAGE_NAME__": "__開始階段__",
            "__SYS_QUESTION__": {
                "__SYS_WELCOME__": "歡迎句",
                "__SYS_REFUSE__": "拒絕句",
                "__SYS_COMPLETE__": "完成句"
            },
            "corpus": {
                "早安": "1",
                "午安": "2",
                "晚安": "3"
            },
            "__SAVED_NAME__": {
                QAStage.__QA_RESPOND__: "QA_r1",
                QAStage.__QA_RESPOND_THRESHOLD__: "QA_th",
                QAStage.__QA_RESPOND_QUESTION__: "QA_q1",
                QAStage.__QA_RESPOND_SCORE__: "QA_s1",
                QAStage.__RUNNING_CORPUS__: "QA_c1",
            },
            "__DISABLE_WELCOME__": False
        }
    ]
}
print(f"\n" * 5)

agent = gen_agent(bot)
data = {}
reply_text, data = ConversationAgent.to_bot(agent, "哈囉", data)
print(f"reply_text: {reply_text}， ")
reply_text, data = ConversationAgent.to_bot(agent, "哈囉", data)
print(f"reply_text: {reply_text}， ")
reply_text, data = ConversationAgent.to_bot(agent, "早安", data)
print(f"reply_text: {reply_text}， ")
```

## Stage 種類
### RE_STAGE

RE_STAGE 採用`stage_type`為`__RE_STAGE__`，是用於最基礎的對話階段，由兩個主要結構構成：
1. `__SYS_QUESTION__`: 用來設定該階段的回應句，回應句有三種類型
   * 歡迎句: 第一次到該階段時，機器人會回應該句子。(可依需求關閉功能，`DISSABLE_WELCOME`設為`True`就關閉，預設為`False`。)
   * 拒絕句: 當沒有滿足抓取到所有`is_fits`部分所要求的變數時，機器人會回應該句子。
   * 完成句: 以上都完成時，機器人會回應該句子。(可透過`%%`包裹變數名稱，並以`空格`前後相隔後，調用該變數。)

2. is_fits: 透過`正規表達式(regular expression)`從使用者的輸入句子來抓取變數，該變數會儲存起來提供給`完成句`和 `SWITCH_STAGE`使用。

選用設定:
1. `__STAGE_NAME__`: 這是選用設定。 可以設定每個stage的獨特名稱，名稱不可重複。
2. `__SYS_WELCOME__`、`__SYS_REFUSE__`、`__SYS_COMPLETE__`的回應句可以設定成文字陣列，若設為陣列則會隨機取用。
```
{
    "stage_type": "__RE_STAGE__",
    "__STAGE_NAME__": "__開始階段__",
    "__SYS_QUESTION__": {
        "__SYS_WELCOME__": "歡迎句",
        "__SYS_REFUSE__": "拒絕句",
        "__SYS_COMPLETE__": "完成句"
    },
    "is_fits": [
        [".*", "YOUSAYS"]
    ],
    "__DISABLE_WELCOME__": False,
    "__DISABLE_REFUSE__": False
}
```

### SWITCH_STAGE

SWITCH_STAGE 採用`stage_type`為`__LIB_SWITCH_STAGE__`，用於在`Agent`不同路線切換，主要結構是`stages_filter`。 stages_filter用來設定切換路線的條件，用`[]`可包含帶多種條件多路線，每一條件單位由`變數名稱`、`限定數值`和 `切換路線`三部分組成。

以下說明主要幾種設置方式:
* 無條件設定:
    ```
    [
        ["*",True,"_新路線1_"]
    ]
    ```
* 單一條件設定:
    ```
    [
        ["_VAR_","VALUE1","_新路線1_"],
        ["_VAR_","VALUE2","_新路線2_"]
    ]
    ```
* 多條件設定:
    ```
    [
        [["_VAR1_","_VAR2_"],["VALUE1","VALUE2"],"_新路線1_"],
        [["_VAR1_","_VAR2_"],["VALUE3","VALUE4"],"_新路線2_"],
    ]
    ```
* 混合條件設定:
    ```
    [
        ["_VAR1_","VALUE1","_新路線1_"],
        [["_VAR1_","_VAR2_"],["VALUE3","VALUE4"],"_新路線2_"],
        ["*",True,"_新路線3_"]
    ]
    ```
* 非`=`之條件設定:
    ```
    [
        ["_VAR1_",0.95,"_新路線1_",">="]
    ]
    ```
  
* 多重非`=`之條件設定:
    ```
    [
        [["_VAR1_","_VAR2_"],[0.1,0.56],"_新路線1_",[">=","<"]]
    ]
    ```
  
**儲存變數方式是透過`RE_STAGE`的 `is_fits`來執行。

範例：
```
{
    "stage_type": "__LIB_SWITCH_STAGE__",
    "stages_filter": [
        ["VAR","我想要的數值","_成功路線_"],,
        ["*",True,"_失敗路線_"]
    ]

}
```

### QA_STAGE
QA_STAGE 採用`stage_type`為`__QA_STAGE__`，是通過`相似度`來決定回應的一種階段，主要有三個部分的組成。
1. says: 用來設定該階段的回應句，回應句有三種類型
   * 歡迎句: 第一次到該階段時，機器人會回應該句子。(可依需求關閉功能，`DISSABLE_WELCOME`設為`True`就關閉，預設為`False`。)
   * 拒絕句: 當相似分數低於`qa_threshold`時，機器人會回應該句子。(可依需求關閉功能，`__DISABLE_REFUSE__`設為`True`就關閉，預設為`False`。)
   * 完成句: 以上都完成時，機器人會回應該句子。(可透過`%%`包裹變數名稱，並以`空格`前後相隔後，調用該變數。)

2. corpus: 使用者的輸入會與該字典的所有`key`進行比對，並儲存相關結果，相關結果包含：
    * `__QA_RESPOND_QUESTION__`: 相似值最高的 key
    * `__QA_RESPOND__`: 相似值最高的 key 對應之 value
    * `__QA_RESPOND_SCORE__`: 相似值最高的數值
    * `__RUNNING_CORPUS__`: 該次測試時使用的 corpus
    * `__QA_RESPOND_THRESHOLD__`: 該次測試使用的 threshold
    
3. `__SAVED_NAME__`: 設定儲存之變數的名稱，方便使用。


```
 {
    "stage_type": "__QA_STAGE__",
    "qa_threshold": 1,
    "says": {
        "sys_welcome": "歡迎句",
        "sys_refuse": "拒絕句",
        "sys_complete": "完成句"
    },
    "corpus": {
        "早安": "1",
        "午安": "2",
        "晚安": "3"
    },
    "__SAVED_NAME__": {
        "__QA_RESPOND__": "QA_r1",
        "__QA_RESPOND_THRESHOLD__": "QA_th",
        "__QA_RESPOND_QUESTION__": "QA_q1",
        "__QA_RESPOND_SCORE__": "QA_s1",
        "__RUNNING_CORPUS__": "QA_c1",
    },
    "__DISABLE_WELCOME__": False,
    "__DISABLE_REFUSE__": False,
}
```



## More Examples

# 飲料店
```
bot = {
    "__MAIN_STAGES__": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_welcome": "歡迎來到飲料店，請輸入您要的東西 紅茶/綠茶 少冰/去冰",
                "sys_refuse": "不完全輸入 %%drink_type%% %%ice_type%% ",
                "sys_complete": "你輸入的內容是 %%drink_type%% %%ice_type%% "
            },
            "is_fits": [
                ["(紅茶|綠茶)+", "drink_type"],
                ["(少冰|去冰)+", "ice_type"],

            ]
        },
        {
            "stage_type": "__LIB_SWITCH_STAGE__",
            "stages_filter": [
                [["drink_type", "ice_type"], ["綠茶", "去冰"], "_新路線1_"],
                ["*", True, "_新路線2_"]
            ]

        }
    ],
    "_新路線1_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "",
                "sys_complete": "切換分之成功1"
            },
            "__DISSABLE_Q1__": True
        },
    ],
    "_新路線2_": [
        {
            "stage_type": "__RE_STAGE__",
            "question": {
                "sys_welcome": "",
                "sys_refuse": "",
                "sys_complete": "切換分之成功2"
            },
            "__DISSABLE_Q1__": True
        },
    ]
}
print(f"\n" * 5)

agent = gen_agent(bot)
data = {}
reply_text, data = ConversationAgent.to_bot(agent, "哈囉", data)
print(f"reply_text: {reply_text}， ")
reply_text, data = ConversationAgent.to_bot(agent, "紅茶", data)
print(f"reply_text: {reply_text}， ")
reply_text, data = ConversationAgent.to_bot(agent, "少冰", data)
print(f"reply_text: {reply_text}， ")
```

## ToDo

~~* Switch除了等號以外的方法~~

~~* DISSABLE_WELCOME測試與勘誤名詞~~

~~* QAStage 停用拒絕句(無論分數都會通過)~~

~~* 多回應方式~~

~~* 設定階段名稱~~

* 修正QAstage為相似度模型階段
* 分類型模型階段
* 繼承的範例
* 說明agent刪除變數的規則


