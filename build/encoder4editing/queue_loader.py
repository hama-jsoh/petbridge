from tools import ParseQueue, RequestQueue, ChangeStatus
import shlex
import subprocess
import argparse
from logger import Logger
from s3 import ReturnMsg


def set_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="service", help="test or service")
    args = parser.parse_args()
    return args

ARGS = set_argument()
MODE = ARGS.mode


if __name__ == "__main__":

    if MODE == "test":
        # 테스트용 대기열
        TEST = [
            {
                "rp_idx": 23,
                "ac_text": "happy",
            },
            {
                "rp_idx": 24,
                "ac_text": "happy",
            }
        ]
        taskQueue = ParseQueue(TEST)
    else:
        taskList = RequestQueue()
        taskQueue = ParseQueue(taskList)
        
    total = len(taskQueue)

    fail = []
    success = []
    for cid, htext in taskQueue.items():
        command = shlex.split(f"python3 app.py --cid {cid} --htext {htext}")
        proc = subprocess.run(command, stdout=subprocess.PIPE)

        out = proc.stdout.decode('utf-8')
        response = eval(out[out.find('{'):])
        resultData = response['Result']['Data']

        data_f = resultData['fail']
        data_s = resultData['success']
        if data_f:
            try:
                fail.append(data_f[0])
            except:
                fail.append(data_f)
        elif data_s:
            try:
                success.append(data_s[0])
            except:
                success.append(data_s)

    data = dict(total=total, fail=fail, success=success)
    result = ReturnMsg(1, "Success", 1, data)
    result['Status'] = True
    RESULT = dict(Result=result, flag='off')
    
    # 로그 저장
    Logger.info(RESULT)
    
    if MODE is not "test":
        ChangeStatus(RESULT)
