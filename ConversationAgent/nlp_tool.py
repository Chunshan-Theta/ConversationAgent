def result_format(sentence,corpus,ans,score):
    return {
      "get parameter": {
        "sentence": [
          sentence
        ],
        "corpus": corpus
      },
      "worker response": {
        "ans": [
          [
            ans,
            score
          ]

        ]
      }
    }

def MED(sent_01, sent_02):
    n = len(sent_01)
    m = len(sent_02)

    matrix = [[i + j for j in range(m + 1)] for i in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if sent_01[i - 1] == sent_02[j - 1]:
                d = 0
            else:
                d = 1

            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    distance_score = matrix[n][m]

    return distance_score


def similar(sentence, corpus):
    ans = None
    min_distance = 999
    max_distance = 1
    for c in corpus:
        distance = MED(sentence, c)
        max_distance = distance if distance > max_distance else max_distance
        if distance < min_distance:
            min_distance = distance
            ans = c
    score = 1-(min_distance/max_distance)
    result = result_format(sentence, corpus, ans, score)
    return result
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