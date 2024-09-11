import islpy as isl


class ISL_Context:
    
    def __init__(self, file_path):
        """
        初始化类，初始化ISL上下文与文件句柄
        """
        
        self._file = open(file_path,'w')
        self._ctx = isl.Context()

        
    def __del__(self):
        """
        析构函数，关闭文件，释放资源
        """
        self._file.close()
    
    def ctx(self):
        """
        返回类的上下文
        """
        return self._ctx
    
    def file(self):
        """
        返回类的文件句柄
        """
        return self._file
    
    def printf(self,*args):
        """
        把格式化的输出写入文件
        """
        print(*args,file=self._file)