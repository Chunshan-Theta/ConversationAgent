from . import Stage, Agent, mock_client, mock_client_human, __USER_TEXT__
import re


__HELLO_STAGE__ = "HELLO_STAGE"
__CLEAR_STAGE__ = "CLEAR_STAGE"
__ORDER_HELLO_STAGE__ = "ORDER_HELLO_STAGE"
__ORDER_START_STAGE__ = "__ORDER_START_STAGE__"
__ORDER_OUT_STAGE__ = "__ORDER_OUT_STAGE__"
__ORDER_CONFIRM_STAGE__ = "__ORDER_CONFIRM_STAGE__"


def fit_re(rule, text) -> bool:
    return False if re.match(rule, text) is None else True      # 不在起始位置匹配


class CleanStage(Stage):

    def __init__(self):
        super(CleanStage, self).__init__()
        self.stage_type = __CLEAR_STAGE__
        self.sys_reply_q1 = "您好目前您已經完成訂票了，如果想重新體驗，請輸入『我要重置』"
        self.sys_reply_q1 = f"""
            好的，您已經完成訂票了
            您預計將在
            %%{OrderStartStage.ON_BOARD}%% 上車
            在
             {self.get_default_var_label(OrderEndStage.OUT_BOARD)} 下車
            如果想重新體驗，請輸入『我要重置』
        """
        self.sys_reply_q2 = "如果想重新體驗，請輸入『我要重置』，想結束請輸入exit"
        self.sys_reply_complete = "已經重置"

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        if fit_re(".*重置.*", kwargs.get(__USER_TEXT__, "")):
            return True, None
        else:
            return False, kwargs


class HelloStage(Stage):

    def __init__(self):
        super(HelloStage, self).__init__()
        self.stage_type = __HELLO_STAGE__
        self.sys_reply_q1 = "歡迎光臨～"
        self.sys_reply_q2 = "歡迎跟我說一聲hi喔"
        self.sys_reply_complete = "哈囉您好，請問是來訂票的嗎？"

    @staticmethod
    def is_fit_needs_n_gen_entity(kwargs) -> (bool,dict):
        if fit_re(".*hi.*", kwargs[__USER_TEXT__]):
            return True, kwargs
        else:
            return False, kwargs


class OrderHelloStage(Stage):

    def __init__(self):
        super(OrderHelloStage, self).__init__()
        self.stage_type = __ORDER_HELLO_STAGE__
        self.sys_reply_q2 = "如果想訂票，請說 「線上訂票」，或是「我要訂票」"
        self.sys_reply_complete = "接下來進行訂票流程"

    @staticmethod
    def is_first_access(data, stage_id):
        return False

    @staticmethod
    def is_fit_needs_n_gen_entity(kwargs) -> (bool, dict):
        if fit_re(".*訂票.*", kwargs.get(__USER_TEXT__, "")):
            return True, kwargs
        else:
            return False, kwargs


class OrderStartStage(Stage):
    ON_BOARD = "on_board_station"

    def __init__(self):
        super(OrderStartStage, self).__init__()
        self.stage_type = __ORDER_START_STAGE__
        self.sys_reply_q1 = "請問是哪一站上車呢？"
        self.sys_reply_q2 = "請說站名，例如『板橋火車站』"
        self.sys_reply_complete = f"好的，您將從 {self.get_default_var_label(self.ON_BOARD)} 出發"

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        user_text = kwargs.get(__USER_TEXT__, "")
        if fit_re(".*車站.*", user_text):
            kwargs = self.set_default_var(kwargs, self.ON_BOARD, user_text)
            return True, kwargs
        else:
            return False, kwargs


class OrderEndStage(Stage):
    OUT_BOARD = "out_station"

    def __init__(self):
        super(OrderEndStage, self).__init__()
        self.stage_type = __ORDER_OUT_STAGE__
        self.sys_reply_q1 = "請問是哪一站下車呢？"
        self.sys_reply_q2 = "請說站名，例如『板橋火車站』"
        self.sys_reply_complete = f"好的，您將從 {self.get_default_var_label(self.OUT_BOARD)} 下車"

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        user_text = kwargs.get(__USER_TEXT__, "")
        if fit_re(".*車站.*", user_text):
            kwargs = self.set_default_var(kwargs, self.OUT_BOARD, user_text)
            return True, kwargs
        else:
            return False, kwargs


class OrderConfirmStage(Stage):

    def __init__(self):
        super(OrderConfirmStage, self).__init__()
        self.stage_type = __ORDER_CONFIRM_STAGE__
        self.sys_reply_complete = f"好的，您完成訂票了\n {self.get_default_var_label(OrderStartStage.ON_BOARD)} 上車\n {self.get_default_var_label(OrderEndStage.OUT_BOARD)} 下車"

    @staticmethod
    def is_first_access(data, stage_id):
        return False

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        return True, kwargs



