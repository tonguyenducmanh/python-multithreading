"""
File test việc có 1 consumer chuyên thực hiện handle nhiệm vụ đọc message gì đó
và có n thread sẽ xử lý song song theo threadpollexecutor
"""

from threading import current_thread
import asyncio
from concurrent.futures import ThreadPoolExecutor
from helper import TestSimulateHelper

thread_limit = 5
handler_name = "ThreadHandleMessage"
executor = ThreadPoolExecutor(max_workers= thread_limit, thread_name_prefix= handler_name)

print(f"Khởi tạo thread pool với {thread_limit} thread xử lý đồng thời")

async def receive_message_async(queue_message):
    """
    xử lý data bất đồng bộ trong 1 thread
    """
    await TestSimulateHelper.get_helper().slow_function_async(1)

def process_message_async(queue_message):
    """
    Hàm xử lý riêng của 1 thread
    """
    current_thread_name = current_thread().name
    print(f"{current_thread_name} bắt đầu xử lý message {queue_message}")
    try:
        loop = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop=loop)
            loop.run_until_complete(receive_message_async(queue_message=queue_message))
        finally:
            if loop is not None:
                loop.close()

    except:
        print(f"{current_thread_name} Có lỗi khi xử lý message {queue_message}")

    print(f"{current_thread_name} kết thúc xử lý message {queue_message}")


for i in range(100):
    data_put = f"Đã data put {i}"
    main_thread_name = current_thread().name
    print(f"{main_thread_name} + {data_put}")
    
    # Multithread, submit vào threadpoolexecutor
    # submit() sẽ chạy process_message_async vào 1 worker thread có sẵn
    # nếu tất cả worker đều bận, submit() sẽ block cho đến khi worker rảnh
    executor.submit(process_message_async, data_put)

    TestSimulateHelper.get_helper().slow_function(1)

# stop executor
# chờ tất cả worker hoàn thành
executor.shutdown(wait=True)