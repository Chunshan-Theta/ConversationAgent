from typing import NamedTuple, List

class SimilarResult(NamedTuple):
    sentence: str
    corpus: List[str]
    ans: str
    score: float


def result_format(sentence: str,corpus: List[str], ans:str, score:float) -> SimilarResult:
    return SimilarResult(
      sentence=sentence,
      corpus=corpus,
      ans=ans,
      score=score
    )

def MED(s1: str, s2: str) -> float:
    # Create a matrix of size (len(s1) + 1) x (len(s2) + 1)
    s1 = [w for w in s1]
    s2 = [w for w in s2]
    if len(s1) <= len(s2):
      s1,s2 = s2,s1

    for w in s2:
      if w in s1:
        del s1[s1.index(w)]

    # Return the Levenshtein distance
    score= len(s1)
    if score == 0:
      return 1
    return (1 / score)-0.0000001



def similar_text_distance(sentence: str, corpus: List[str]) -> SimilarResult:
    socres: List[Tuple(str, float)] = []
    for c in corpus:
        distance = MED(sentence, c)
        socres.append((c, distance))
    sorted_data = sorted(socres, key=lambda x: x[1])
    # print(sorted_data)
    return result_format(sentence, corpus, sorted_data[-1][0], sorted_data[-1][1])
#
# corpus= [
#     "我想去醫院",
#     "我想去大學",
#     "我想去台北",
#     "我想去跑步",
#     "我想去公園"
# ]
# sentence="我想去大公園"
# print(similar(sentence,corpus))
# print("socre", MED('廁所在哪裡', '附近有廁所嗎'))
# print("socre", MED('廁所在哪裡', '詢問處在哪裡'))
