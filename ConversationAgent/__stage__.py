import json
import uuid
import re
import random

__USER_TEXT__ = "USER_TEXT"
__PASS_TOKEN__ = "PASS_TOKEN"
__SYS_REPLY__ = "SYS_REPLY"
__SYS_STAGE__ = "SYS_STAGE"
__KEEP_VAR__ = "KEEP_VAR"
__KEEP_DEFAULT_VAR__ = "KEEP_DEFAULT_VAR"
__PASSED_STAGES__ = "__PASSED_STAGES__"
__LOCAL_VAR_LABEL__ = "__LOCAL_VAR_LABEL__"
__LOCAL_VAR_VALUE__ = "__LOCAL_VAR_VALUE__"


class StageStatus:
    INIT = "INIT"
    FIRST = "FIRST"
    REFUSE = "REFUSE"
    COMPLETE = "COMPLETE"


class StageType:
    BASE = "BASE"
    SWITCH = "Switch"


class Stage:
    def __init__(self, **kwargs):
        self.stage_type = StageType.BASE
        self.stage_uuid_name = kwargs.get("__STAGE_NAME__", str(uuid.uuid4())[:15])
        self.stage_id = f"{self.stage_type}:{self.stage_uuid_name}"
        self.data = kwargs
        self.sys_reply_q1 = "init sys reply"  # init
        self.sys_reply_q2 = "refuse sys reply"  # refuse
        self.sys_reply_complete = "complete sys reply"  # complete
        self.keep_user_text = kwargs.get("__KEEP_USER_TEXT__", False)

    @staticmethod
    def set_sys_stage_status(data: dict, label: str) -> dict:
        data.update({__SYS_STAGE__: label})
        return data

    @staticmethod
    def get_sys_stage_status(data: dict) -> str:
        return data.get(__SYS_STAGE__, None)

    @staticmethod
    def is_first_access(data, stage_id):
        # First Access
        if __PASS_TOKEN__ not in data:
            return True
        if stage_id not in data[__PASS_TOKEN__]:
            return True
        return False

    @staticmethod
    def clear_user_text(data):
        # First Access
        _ = data.pop(__USER_TEXT__, None)
        return data

    @classmethod
    def save_user_text(cls, data, stage_id, label):
        user_text = cls.get_user_text(data)
        data = cls.set_var(data, __KEEP_DEFAULT_VAR__, label, user_text)
        return cls.set_var(data, stage_id, label, user_text)

    @staticmethod
    def get_user_text(data):
        return data.get(__USER_TEXT__, None)

    @staticmethod
    def had_the_token_was_pass(data: dict, stage_id) -> bool:
        token = data.get(__PASS_TOKEN__, None)
        if token is None:
            return False
        if isinstance(token, dict) and token.get(stage_id, None) is True:
            return True
        else:
            return False

    @staticmethod
    def set_none_token_pass(data, stage_id):
        if __PASS_TOKEN__ not in data:
            data[__PASS_TOKEN__] = {}
        data[__PASS_TOKEN__][stage_id] = None
        return data

    @staticmethod
    def set_true_token_pass(data, stage_id):
        if __PASS_TOKEN__ not in data:
            data[__PASS_TOKEN__] = {}
        data[__PASS_TOKEN__][stage_id] = True
        return data

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        kwargs = self.set_default_var(kwargs, __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__)
        # if want to reset data, return (True,None) to replace to (True,kwargs)
        return True, kwargs

    @staticmethod
    def is_var_label(label_string):
        return None if re.match("^var\t.*\t.*\tvar$", label_string) is None else label_string.split("\t")

    @staticmethod
    # def is_var_label_human(label_string):
    def get_var_name_from_string(label_string):
        return None if re.match("^%%.*%%$", label_string) is None else label_string[2:-2]

    @classmethod
    def get_default_var_ticket(cls, label: str) -> str:
        return cls.get_var_ticket(__KEEP_DEFAULT_VAR__, label)

    def set_default_var(self, data, label, save_text):
        data = self.set_var(data, self.stage_id, label, save_text)
        data = self.set_var(data, __KEEP_DEFAULT_VAR__, label, save_text)
        return data

    def get_default_var(self, data, label) -> any:
        return self.get_var(data, __KEEP_DEFAULT_VAR__, label)

    @staticmethod
    def get_var_ticket(stage_id: str, label: str):
        assert "\t" not in stage_id
        assert "\t" not in label
        return f"var\t{stage_id}\t{label}\tvar"

    @classmethod
    def set_var(cls, data, stage_id, label, save_text):
        if __KEEP_VAR__ not in data:
            data[__KEEP_VAR__] = {}
        if stage_id not in data[__KEEP_VAR__]:
            data[__KEEP_VAR__][stage_id] = {}

        data[__KEEP_VAR__][stage_id][label] = save_text
        return data

    @classmethod
    def get_var(cls, data, stage_id, label):
        try:
            return data[__KEEP_VAR__][stage_id][label]
        except KeyError:
            return None

    @staticmethod
    def set_sys_passed_stage(data, stage_name):
        if __PASSED_STAGES__ in data:
            data[__PASSED_STAGES__].append(stage_name)
        else:
            data[__PASSED_STAGES__] = [stage_name]
        return data

    @staticmethod
    def set_sys_reply(data, sys_reply_text):
        if __SYS_REPLY__ in data:
            data[__SYS_REPLY__].append(sys_reply_text)
        else:
            data[__SYS_REPLY__] = [sys_reply_text]
        return data

    @classmethod
    def replace_var_ticket_to_string(cls, kwargs, sys_reply):
        # print(f"kwargs: {kwargs}")
        # print(f"sys_reply: {sys_reply}")
        __NEXT_LINE__ = "||n||"
        # insert ENTITY
        sys_reply_complete_refactor = []
        ##
        sys_reply = sys_reply.replace("\n", __NEXT_LINE__)

        #
        var_ticket = None
        for var in sys_reply.split(" "):

            # check the var is var ticket or not.
            var_ticket_name = cls.get_var_name_from_string(var)
            if var_ticket_name is not None:
                # if it is a var ticket, then return:
                # ->: var \t KEEP_DEFAULT_VAR \t {var_ticket_human} \t var"
                var_ticket = cls.get_default_var_ticket(var_ticket_name).split("\t")

            # replace
            if var_ticket is not None:
                try:
                    var_value = kwargs[__KEEP_VAR__][var_ticket[1]][var_ticket[2]]
                    if isinstance(var_value, str):
                        sys_reply_complete_refactor.append(var_value)
                    elif isinstance(var_value, float):
                        sys_reply_complete_refactor.append(str(round(var_value, 4)))
                    else:
                        sys_reply_complete_refactor.append(str(var_value))

                except KeyError:
                    sys_reply_complete_refactor.append(f"{var}")
            else:
                var = var.replace(__NEXT_LINE__, "\n")
                sys_reply_complete_refactor.append(f"{var}")
        return " ".join(sys_reply_complete_refactor)

    def run(self, **kwargs):

        kwargs = self.set_sys_passed_stage(kwargs,self.stage_uuid_name)

        # the user had passed or not.
        if self.had_the_token_was_pass(data=kwargs, stage_id=self.stage_id) is True:
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.COMPLETE)
            return kwargs

        # the user had is first time to coming
        if self.is_first_access(kwargs, self.stage_id) is True:
            kwargs = self.set_none_token_pass(data=kwargs, stage_id=self.stage_id)
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.FIRST)

            # random reply from welcome corpus (q1)
            sys_reply = self.__choice_a_reply__(self.sys_reply_q1)

            #
            sys_reply = self.replace_var_ticket_to_string(kwargs, sys_reply)
            return self.set_sys_reply(kwargs, sys_reply)

        # computer core. the main flow in stage, base on static rule of stage to check rusult is pass or not.
        # return pass_token and data
        # pass_token: [True,  False]
        #     True -> complete
        #     False -> refuse
        is_fit_token, kwargs = self.is_fit_needs_n_gen_entity(kwargs)
        if is_fit_token is False:
            # REFUSE FLOW
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.REFUSE)
            sys_reply = self.__choice_a_reply__(self.sys_reply_q2)

            sys_reply = self.replace_var_ticket_to_string(kwargs, sys_reply)
            return self.set_sys_reply(kwargs, sys_reply)

        elif is_fit_token is True:
            # COMPLETE FLOW
            kwargs = kwargs if kwargs is not None else {}
            kwargs = self.save_user_text(kwargs, self.stage_id, __USER_TEXT__)
            if not self.keep_user_text:
                kwargs = self.clear_user_text(kwargs)
            kwargs = self.set_true_token_pass(kwargs, stage_id=self.stage_id)
            kwargs = self.set_sys_stage_status(kwargs, StageStatus.COMPLETE)

            # insert ENTITY
            sys_reply = self.replace_var_ticket_to_string(kwargs, self.__choice_a_reply__(self.sys_reply_complete))
            return self.set_sys_reply(kwargs, sys_reply)
        #
        # elif is_fit_token is True and kwargs is None:  # reset route
        #     sys_reply = self.replace_var_ticket_to_string(kwargs, self.__choice_a_reply__(self.sys_reply_complete))
        #     return self.set_sys_reply({}, sys_reply)

    @staticmethod
    def __choice_a_reply__(sys_reply):
        if isinstance(sys_reply, list):
            sys_reply = random.choice(sys_reply)
            return sys_reply
        return sys_reply


a = Stage()
res = a.run()
assert res.get(__SYS_STAGE__, None) == StageStatus.FIRST
res[__USER_TEXT__] = "hi"
res.pop(__SYS_REPLY__)
res = a.run(**res)
assert res.get(__SYS_STAGE__, None) == StageStatus.COMPLETE
res.pop(__SYS_REPLY__)
res = a.run(**res)
assert res.get(__SYS_STAGE__, None) == StageStatus.COMPLETE
