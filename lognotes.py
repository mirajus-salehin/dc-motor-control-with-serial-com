class Process:

    class success:

        @staticmethod
        def camera_init() -> str:
            return "Camera initialized successfully"

        @staticmethod
        def camera_read() -> str:
            return "Camera read successfully"
            
        @staticmethod
        def camera_write() -> str:
            return "Camera write successfully"

        @staticmethod
        def serial_init() -> str:
            return "Serial initialized successfully"

        @staticmethod
        def serial_write() -> str:
            return "Serial write successfully"

    class failed:

        @staticmethod
        def camera_init() -> str:
            return "Camera initialization failed"

        @staticmethod
        def camera_read() -> str:
            return "Camera read failed"
        
        @staticmethod
        def camera_write() -> str:
            return "Camera write failed"
        
        @staticmethod
        def serial_init() -> str:
            return "Serial initialization failed"