from .__stage__ import Stage, __USER_TEXT__, StageType
from .__agent__ import Agent, MultiAgent
from .__tool__ import get_value_from_dict_by_multi_name, compute_by_string
from .jieba_zh import analyse
import re

__RE_STAGE__ = "__RE_STAGE__"
__QA_STAGE__ = "__QA_STAGE__"
__SWITCH_STAGE__ = StageType.SWITCH
__LIB_SWITCH_STAGE__ = "__LIB_SWITCH_STAGE__"

#
__QUESTIONS_LABEL__ = ["__SYS_QUESTION__", "question", "says"]
__WELCOME_SAYING_LABELS__ = ["__SYS_WELCOME__", "sys_reply_q1", "sys_welcome"]
__REFUSE_SAYING_LABELS__ = ["__SYS_REFUSE__", "sys_reply_q2", "sys_refuse"]
__COMPLETE_SAYING_LABELS__ = ["__SYS_COMPLETE__", "sys_reply_complete", "sys_complete"]
__DISABLE_WELCOME_LABEL__ = ["__DISABLE_WELCOME__", "__DISSABLE_Q1__", "DISSABLE_WELCOME"]
__DISABLE_REFUSE_LABEL__ = ["__DISABLE_REFUSE__"]

from .nlp_tool import similar


class QAStage(Stage):
    __QA_RESPOND__ = "__QA_RESPOND__"
    __QA_RESPOND_SCORE__ = "__QA_RESPOND_SCORE__"
    __QA_RESPOND_QUESTION__ = "__QA_RESPOND_QUESTION__"
    __QA_RESPOND_THRESHOLD__ = "__QA_RESPOND_THRESHOLD__"
    __QA_THRESHOLD__ = "qa_threshold"
    __IS_FITS__ = "is_fits"
    __SAVED_NAME__ = "__SAVED_NAME__"
    __CORPUS__ = "corpus"
    __QUESTIONS__ = "question"
    __SIMILAR_METHOD__ = "similar_method"
    __RUNNING_CORPUS__ = "__RUNNING_CORPUS__"
    __DISSABLE_Q1__ = "__DISSABLE_Q1__"
    __REFACTOR_QUESTION__ = "refactor_questions"

    def __init__(self, data):
        super(QAStage, self).__init__(**data)
        self.raw_data = data
        self.stage_type = data.get("stage_type")
        self.corpus = {}
        corpus = data.get(self.__CORPUS__)
        for k, v in corpus.items():
            self.corpus[k.replace(" ", "")] = v.replace(" ", "")

        #
        self.questions = get_value_from_dict_by_multi_name(d=data, names=__QUESTIONS_LABEL__)
        self.sys_reply_q1 = get_value_from_dict_by_multi_name(d=self.questions, names=__WELCOME_SAYING_LABELS__)
        self.sys_reply_q2 = get_value_from_dict_by_multi_name(d=self.questions, names=__REFUSE_SAYING_LABELS__)
        self.sys_reply_complete = get_value_from_dict_by_multi_name(d=self.questions,
                                                                    names=__COMPLETE_SAYING_LABELS__)
        self.saved_name: dict = data.get(self.__SAVED_NAME__, {})
        self.qa_threshold = data.get(self.__QA_THRESHOLD__, 0.1)

        # TODO: RENAME `refactor_questions` -> `refactor_corpus_questions`
        self.refactor_questions = data.get(self.__REFACTOR_QUESTION__, False)

        if get_value_from_dict_by_multi_name(d=data, names=__DISABLE_WELCOME_LABEL__, default=False):
            self.is_first_access = self.disabel_is_first_access

        self.disable_refuse_question = get_value_from_dict_by_multi_name(d=data, names=__DISABLE_REFUSE_LABEL__,
                                                                         default=False)

    def __request_similar_api__(self, text, corpus):
        return similar(text, corpus)

    def __encode_corpus__(self):
        source_corpus = list(self.corpus.keys())
        dict_corpus = {self.__keyword__(self.__stop_word__(s)): s for s in source_corpus}
        return list(self.corpus.keys() if not self.refactor_questions else dict_corpus.keys()), dict_corpus

    def __decode_corpus__(self, worker_response, new_dict_corpus):
        best_res_content = str(worker_response[0][0]).replace(" ", "")
        if self.refactor_questions:
            best_res_content = new_dict_corpus[best_res_content] if best_res_content in new_dict_corpus else '0'
        return best_res_content

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        user_text = kwargs.get(__USER_TEXT__, "")

        corpus, new_dict_corpus = self.__encode_corpus__()

        responds = self.__request_similar_api__(user_text, corpus)
        worker_response = responds["worker response"]["ans"]
        best_res_content = self.__decode_corpus__(worker_response, new_dict_corpus)

        ##
        best_res_score = worker_response[0][1]
        best_res_responds = self.corpus[best_res_content] if best_res_content in self.corpus else None

        ##
        __RUNNING_CORPUS__ = self.saved_name.get(self.__RUNNING_CORPUS__, self.__RUNNING_CORPUS__)
        __QA_RESPOND__ = self.saved_name.get(self.__QA_RESPOND__, self.__QA_RESPOND__)
        __QA_RESPOND_QUESTION__ = self.saved_name.get(self.__QA_RESPOND_QUESTION__, self.__QA_RESPOND_QUESTION__)
        __QA_RESPOND_SCORE__ = self.saved_name.get(self.__QA_RESPOND_SCORE__, self.__QA_RESPOND_SCORE__)
        __QA_RESPOND_THRESHOLD__ = self.saved_name.get(self.__QA_RESPOND_THRESHOLD__, self.__QA_RESPOND_THRESHOLD__)

        #
        kwargs = self.set_default_var(kwargs, __RUNNING_CORPUS__, corpus)
        kwargs = self.set_default_var(kwargs, __QA_RESPOND__, best_res_responds)
        kwargs = self.set_default_var(kwargs, __QA_RESPOND_QUESTION__, best_res_content)
        kwargs = self.set_default_var(kwargs, __QA_RESPOND_SCORE__, best_res_score)
        if best_res_score >= self.qa_threshold:
            pass_token = True
            kwargs = self.set_default_var(kwargs, __QA_RESPOND_THRESHOLD__, True)
        else:
            pass_token = False if self.disable_refuse_question is False else True

            kwargs = self.set_default_var(kwargs, __QA_RESPOND_THRESHOLD__, False)

        return pass_token, kwargs

    @staticmethod
    def disabel_is_first_access(kwargs, stage_id):
        return False

    @staticmethod
    def __stop_word__(text, pronouns=True, common_skip=True, road_name=True, symbol=True):
        text = text.replace(" ", "")
        filter_set = []
        if pronouns:
            filter_set += ["我", "你", "妳"]
        if common_skip:
            filter_set += ["請問", "不好意思", "這裡", "可以", "要", "怎麼", "如何"]
        if road_name:
            filter_set += ["路", "號"]
        if symbol:
            filter_set += ["-", "，", "？", "。"]
        for stopword in filter_set:
            text = text.replace(stopword, " ")
        return text

    @staticmethod
    def __keyword__(text, k=10):
        allowed_words = ""
        list_en = [i for i in "abcdefghijklmnopqrstuvwxyz"] + [i for i in "abcdefghijklmnopqrstuvwxyz".upper()]
        list_math = [str(i) for i in range(0, 10)]
        list_bus = ["紅", "棕", "綠", "橘", "藍", "黃", "區", "副"]
        new_text = analyse.tfidf(text, topK=k, withWeight=True)
        allowed_words += "".join([t for t, v in new_text] + list_bus + list_en + list_math)
        return_text = "".join([w for w in text if w in allowed_words])
        return return_text


class REStage(Stage):

    def __init__(self, data):
        super(REStage, self).__init__(**data)
        self.raw_data = data
        self.stage_type = data.get("stage_type")

        #
        self.questions = get_value_from_dict_by_multi_name(d=data, names=__QUESTIONS_LABEL__)
        self.sys_reply_q1 = get_value_from_dict_by_multi_name(d=self.questions, names=__WELCOME_SAYING_LABELS__)
        self.sys_reply_q2 = get_value_from_dict_by_multi_name(d=self.questions, names=__REFUSE_SAYING_LABELS__)
        self.sys_reply_complete = get_value_from_dict_by_multi_name(d=self.questions,
                                                                    names=__COMPLETE_SAYING_LABELS__)
        self.is_fits = data.get("is_fits", [])
        if get_value_from_dict_by_multi_name(d=data, names=__DISABLE_WELCOME_LABEL__, default=False):
            self.is_first_access = self.disabel_is_first_access

        self.disable_refuse_question = get_value_from_dict_by_multi_name(d=data, names=__DISABLE_REFUSE_LABEL__,
                                                                         default=False)

    @staticmethod
    def disabel_is_first_access(kwargs, stage_id):
        return False

    @staticmethod
    def __get_entity__(rule, text):
        entities = []
        results = re.findall(rule, text)
        for r in results:
            if isinstance(r, tuple):
                entities += list(r)
            else:
                entities.append(r)
        return entities

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        user_text = kwargs.get(__USER_TEXT__, "")
        pass_token = True

        missing_entities = []
        for (rule, entity_name) in self.is_fits:
            entities = self.__get_entity__(rule, user_text)
            if len(entities) > 0:
                kwargs = self.set_default_var(kwargs, entity_name, " ".join(entities))
            else:
                missing_entities.append(entity_name)

        for entity_name in missing_entities:
            if self.get_default_var(kwargs, entity_name) is None:
                pass_token = False

        if self.disable_refuse_question:
            pass_token = True

        return pass_token, kwargs


class LibSwitchStage(Stage):

    def __init__(self, data):
        super(LibSwitchStage, self).__init__(**data)
        self.raw_data = data
        self.stage_type = StageType.SWITCH
        self.stages_filter = data.get("stages_filter")

    @staticmethod
    def is_first_access(data, stage_id):
        return False

    def find_new_stages(self, kwargs):
        stages_searched = []
        for filter_tuple in self.stages_filter:

            if len(filter_tuple) == 3:
                label, text, stages_label = filter_tuple
                symbol = None
            elif len(filter_tuple) == 4:
                label, text, stages_label, symbol = filter_tuple
            else:
                raise SyntaxError("find_new_stages: filter_tuple format error")

            stages_searched.append(stages_label)
            #
            if label == "*" and text is True:
                return stages_label

            #
            assert not isinstance(label, list) or isinstance(label, type(
                text)), "切換路線之條件與限定結果的類型不一致，必須保持兩者都是`str` 或是兩者都是`list`"
            if not isinstance(label, list):
                label, text = [label], [text]

            assert len(label) == len(text), "切換路線之條件與限定結果的數量不一致"

            #
            if symbol is None:
                symbol = ["="] * int(len(text))
            elif not isinstance(symbol, list):
                symbol = [symbol]
            #
            assert len(symbol) == len(
                text), f"變數比較條件與限定結果的數量不一致len(symbol) == len(text): {symbol},{text}"

            #
            pass_token = True
            for l, s, t in zip(label, symbol, text):
                l_var = self.get_default_var(kwargs, l)
                pass_token = compute_by_string(l_var, s, t)

            if pass_token:
                return stages_label

        raise RuntimeError(f"Not Found Path: {stages_searched}")

    def is_fit_needs_n_gen_entity(self, kwargs) -> (bool, dict):
        raise RuntimeError


def gen_multi_agent(stage_dict: dict):
    stages = {}
    for stages_label, stage_jsons in stage_dict.items():
        stages[stages_label] = []
        for stage_json in stage_jsons:
            stage_class = __LIB_STAGES__[stage_json["stage_type"]]
            stages[stages_label].append(stage_class(stage_json))

    return MultiAgent(stages)


def gen_agent(stage_dict: dict):
    return gen_multi_agent(stage_dict)


#
__LIB_STAGES__ = {
    __RE_STAGE__: REStage,
    __QA_STAGE__: QAStage,
    __SWITCH_STAGE__: LibSwitchStage,
    __LIB_SWITCH_STAGE__: LibSwitchStage
}
