from threading import Lock, Thread, Event, current_thread
from queue import Queue, Empty
import time
import atexit
from helper import TestSimulateHelper

log_queue = Queue(maxsize=10)
batch_size = 20
batch_timeout = 10

worker_stop_event = Event()

def send_batch(arr):
    current_thread_name = current_thread().name
    print(f"{current_thread_name} Đã nhận được batch gửi đi là {len(arr)} bản ghi {arr}")

def batch_worker_loop():
    batch = []
    last_send_time = time.time()
    while not worker_stop_event.is_set():
        try:
            try:
                log_data = log_queue.get(timeout=0.5)
                batch.append(log_data)
            except:
                pass

            current_time = time.time()
            time_sine_last_send = current_time - last_send_time

            # Gửi batch nếu
            # 1. Đủ số lượng batch size
            # 2. Hoặc quá timeout và có ít nhất 1 log

            shoud_send = (
                len(batch) >= batch_size or
                (len(batch)> 0 and time_sine_last_send >= batch_timeout)
            )

            if shoud_send:
                send_batch(batch)
                batch = []
                last_send_time = current_time

        except:
            pass
    # gửi nốt số còn lại
    if batch:
        send_batch(batch)

batch_worker_thread = Thread(
    target= batch_worker_loop,
    daemon= True,
    name= "SingleWorkerLog"
)

batch_worker_thread.start()

# đăng ký clean up khi shutdown
def shutdown_batch_worker():
    if worker_stop_event and batch_worker_thread:
        worker_stop_event.set()
        batch_worker_thread.join(timeout=5)

atexit.register(shutdown_batch_worker)


for i in range(100):
    data_put = f"Đã data put {i}"
    log_queue.put(data_put)
    main_thread_name = current_thread().name
    print(f"{main_thread_name} + {data_put}")
    TestSimulateHelper.get_helper().slow_function(1)