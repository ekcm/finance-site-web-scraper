import threading
import time

def t1_print_numbers():
    for i in range(100):
        print(f"Thread 1: {i}")

def t2_print_numbers():
    for i in range(100):
        print(f"Thread 2: {i}")

if __name__ == "__main__":
  start_time = time.time()
  t1 = threading.Thread(target=t1_print_numbers)
  t2 = threading.Thread(target=t2_print_numbers)

  t1.start()
  t2.start()

  t1.join()
  t2.join()
  end_time = time.time()
  elapsed_time = end_time - start_time
  print(f"Elapsed time: {elapsed_time}")
