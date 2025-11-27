"""
Test Simulate hepler
"""
import time
import asyncio

class TestSimulateHelper():
    """
    Class chứa các hàm chuyên xử lý việc giả lập test như test performace
    khi dev muốn tự tạo ra các hàm nặng đô thay vì sleep truyền thống bằng thư viện
    vì chưa rõ món asyncio.sleep có block all thread không
    """
    
    _instance = None

    def __init__(self):
        """
        Hàm khởi tạo
        """
        pass
    
    @classmethod
    def get_helper(cls):
        """
        Lấy instance của helper
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def slow_function(self, duration_seconds):
        """
        Hàm chạy chậm khoảng duration_seconds giây mà không dùng sleep.
        duration_seconds: thời gian chạy ước lượng (không chính xác tuyệt đối)
        """
        start_time = time.time()
        x = 0
        while time.time() - start_time < duration_seconds:
            # công việc tốn CPU
            for i in range(1, 10000):
                x += i**2
        return x
    
    async def slow_function_async(self, duration_seconds):
        """
        Hàm giả lập chạy chậm nhưng gọi async
        """
        # loop = asyncio.get_running_loop()
        # return await loop.run_in_executor(
        #     None,                     # dùng thread pool mặc định
        #     self.slow_function,       # gọi hàm gốc
        #     duration_seconds
        # )

        return self.slow_function(duration_seconds)