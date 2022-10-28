from tools import ParseQueue
import shlex
import subprocess


if __name__ == "__main__":

  taskList = RequestQueue()
  taskQueue = ParseQueue(taskList)
  total = len(taskQueue)

  for cid, htext in taskQueue.items():
      command = shlex.split(f"python3 app.py --cid {cid} --htext {htext} --total {total}")
      result = subprocess.run(command, stdout=subprocess.PIPE)
