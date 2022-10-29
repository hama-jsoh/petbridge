import requests


def RequestQueue():
    """
    Description:
        대기열 요청 함수
    """
    url = "http://devapi.petbridge.co.kr/api/remembrance/ai?done=0"
    response = requests.get(url).json()
    taskList = response['Data']['Result']['List']
    return taskList

def ParseQueue(tasklist):
    """
    Description:
        대기열 파싱하는 함수
    """
    hostTexts = []
    containerIds = []
    for task in tasklist:
        hostTexts.append(task['ac_text'])
        containerIds.append(task['rp_idx'])
    taskQueue = dict(zip(containerIds, hostTexts))
    return taskQueue

def LoadQueue():
    """
    Description:
        대기열 불러와서 파싱하는 함수
    """
    taskList = RequestQueue()
    taskQueue = ParseQueue(taskList)
    return taskQueue

def ChangeStatus(result):
    """
    Description:
        람다에 최종 결과 & 인스턴스 종료(상태) 메시지 전송하는 함수
    """
    lambdaUrl = "https://34ml67fwcb.execute-api.ap-northeast-2.amazonaws.com/aiStyleInstanceCon/instance"
    res = requests.post(lambdaUrl, json=result)
    print(res.text)
