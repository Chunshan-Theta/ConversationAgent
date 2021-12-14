import json
import uuid
import re

from .__stage__ import Stage, __USER_TEXT__, __SYS_REPLY__, StageStatus, \
    __LOCAL_VAR_LABEL__, __LOCAL_VAR_VALUE__, StageType, __PASS_TOKEN__, __KEEP_VAR__, \
    __KEEP_DEFAULT_VAR__


class SingleThreadAgent:

    def __init__(self, stages: [Stage]):
        self.stages = stages

    @staticmethod
    def is_not_complete(data) -> bool:
        status = Stage.get_sys_stage_status(data)
        return True if status in [StageStatus.FIRST, StageStatus.REFUSE] else False

    @staticmethod
    def is_final_stage(stages, idx) -> bool:
        return True if len(stages) == (idx + 1) else False

    @staticmethod
    def clear_sys_reply(data):
        data.pop(__SYS_REPLY__, None)
        return data

    @classmethod
    def get_sys_reply(cls, data):
        reply: list = data.get(__SYS_REPLY__, [])
        reply = [line for line in reply if line != ""]
        return reply

    @staticmethod
    def set_sys_reply(data, texts: [str]):
        data[__SYS_REPLY__] = texts
        return data

    def run_all_stages(self, **kwargs) -> (list, dict):
        #
        kwargs = self.clear_sys_reply(kwargs)

        #
        for idx, stage in enumerate(self.stages):
            # print(f"kwargs in: {kwargs}")
            kwargs = stage.run(**kwargs)
            if self.is_not_complete(kwargs) is True:
                # print(f"\tkwargs out: {kwargs}")
                return self.get_sys_reply(kwargs), kwargs
            else:
                if self.is_final_stage(self.stages, idx) is True:
                    # print(f"\tkwargs out: {kwargs}")
                    return self.get_sys_reply(kwargs), kwargs

        raise RuntimeError


class MultiAgent(SingleThreadAgent):
    __MAIN_STAGES__ = "__MAIN_STAGES__"
    __MAX_LEVEL__ = 10

    def __init__(self, stages: dict):
        assert self.__MAIN_STAGES__ in stages, "__MAIN_STAGES__ need in stages"
        super().__init__(stages[self.__MAIN_STAGES__])
        self.multi_stages = stages
        self.__STAGES_IDS__ = []

    def to_dict(self):
        re_dict = {}
        for key, stages in self.multi_stages.items():
            re_dict[key] = [s.clear_user_text for s in stages]
        return re_dict

    @staticmethod
    def is_normal_reply(result):
        for r in result:
            if not isinstance(r, str):
                return False
        return True

    @staticmethod
    def is_switch_stage(stage: Stage):
        return True if stage.stage_type == StageType.SWITCH else False

    def run_one_stages(self, stages, kwargs):
        for idx, stage in enumerate(stages):

            # clear data for loop thread
            if stage.stage_id in self.__STAGES_IDS__:
                for rm_idx in self.__STAGES_IDS__[self.__STAGES_IDS__.index(stage.stage_id):]:

                    # clear pass-token
                    if rm_idx in kwargs[__PASS_TOKEN__]:
                        del kwargs[__PASS_TOKEN__][rm_idx]

                    # clear data of stage was deleted
                    if rm_idx in kwargs[__KEEP_VAR__]:
                        for var_name in kwargs[__KEEP_VAR__][rm_idx]:
                            if var_name in kwargs[__KEEP_VAR__][__KEEP_DEFAULT_VAR__]:
                                del kwargs[__KEEP_VAR__][__KEEP_DEFAULT_VAR__][var_name]
                        del kwargs[__KEEP_VAR__][rm_idx]

                # reset self.__STAGES_IDS__ because delete loop stage from user data
                self.__STAGES_IDS__ = self.__STAGES_IDS__[:self.__STAGES_IDS__.index(stage.stage_id)]

            #
            self.__STAGES_IDS__.append(stage.stage_id)

            ##
            if self.is_switch_stage(stage) is True:
                new_stages_label = stage.find_new_stages(kwargs)
                return self.multi_stages[new_stages_label], kwargs
            else:
                kwargs = stage.run(**kwargs)
                if self.is_not_complete(kwargs) is True:
                    return self.get_sys_reply(kwargs), kwargs
                else:
                    if self.is_final_stage(stages, idx) is True:
                        return self.get_sys_reply(kwargs), kwargs

    def run_all_stages(self, **kwargs) -> (list, dict):
        loop_level = 0
        self.__STAGES_IDS__ = []
        kwargs = self.clear_sys_reply(kwargs)
        result = self.stages
        while self.__MAX_LEVEL__ > loop_level:
            loop_level += 1
            #
            result, kwargs = self.run_one_stages(result, kwargs)
            #
            if self.is_normal_reply(result):
                return result, kwargs

        raise RuntimeError(f"""the agent NEVER close or over Max count of stage:{self.__MAX_LEVEL__}.""")

class Agent(SingleThreadAgent):
    pass
