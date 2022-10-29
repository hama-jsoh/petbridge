from tools import ParseQueue, RequestQueue
import shlex
import subprocess
from s3 import ReturnMsg


if __name__ == "__main__":

#     # 테스트용 대기열
#     TEST = [
#         {
#             "rp_idx": 23,
#             "ac_text": "happy",
#         },
#         {
#             "rp_idx": 24,
#             "ac_text": "happy",
#         }
#     ]
#     testQueue = ParseQueue(TEST)


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
    RESULT = dict(Result=result, flag='off')

    ChangeStatus(RESULT)
