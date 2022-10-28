from tools import ParseQueue
import shlex
import subprocess


if __name__ == "__main__":
#   taskList = [
#       {
#           "rp_idx": 23,
#           "ac_text": "happy",
#       },
#       {
#           "rp_idx": 24,
#           "ac_text": "happy",
#       }
#   ]
  
  taskList = RequestQueue()
  taskQueue = ParseQueue(taskList)
  total = len(taskQueue)

  output = []
  for cid, htext in taskQueue.items():
      command = shlex.split(f"python3 app.py --cid {cid} --htext {htext} --total {total}")
      proc = subprocess.run(command, stdout=subprocess.PIPE)
      stdout = proc.stdout.decode('utf-8')
      parsedStdout = eval(out[out.find('{'):])
      output.append(parsedStdout)
      
  #result = dict(Status=1, Msg="Success", Type=1, Data=data)
  #response = dict(Result=result, flag="off")
