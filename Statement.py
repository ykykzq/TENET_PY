import islpy as isl
import Access
import stt

class Statement:
    def __init__(self,context, statement_domain_str=None) -> None:
        """
        初始化Statement类
        """
        self._context = context
        if statement_domain_str is not None:
            self._domain = isl.UnionSet.read_from_str(self._context,statement_domain_str)
        else:
            self._domain = None
        self._read = []
        self._write = []
    
    def add_access(self,access):
        """
        添加access，区分读写
        """
        if access._is_wirte:
            self._write.append(access)
        else:
            self._read.append(access)
    
    def load(self,filename):
        """
        从文件加载语句域和读写
        """
        try:
            with open(filename,'r') as file:
                read_num = int(file.readline().strip())
                write_num = int(file.readline().strip())
                domain_str = file.readline().strip()
                # 重写加载域并刷新读写
                self._domain = isl.UnionSet.read_from_str(self._context,domain_str)
                self._read.clear()
                self._write.clear()
                # 根据文件内容添加读写
                for _ in range(0,read_num):
                    access_str = file.readline().strip()
                    tensor_name = self.extract_tensor_name(access_str)
                    self.add_access(Access(self._context, tensor_name, access_str, is_write = False))
                for _ in range(0,write_num):
                    access_str = file.readline().strip()
                    tensor_name = self.extract_tensor_name(access_str)
                    self.add_access(Access(self._context, tensor_name, access_str, is_write = True))
                
        except IOError:
            return False
    
    def extract_tensor_name(self,access_str):
        """
        提取Access字符串中的张量名称
        """
        pos = access_str.rfind("->")+2
        len = access_str.find('[',pos) - pos
        return access_str[pos:pos+len]
    
    def get_cccess(self,tensor_name='',access_type=''):
        """
        获取指定张量的访问映射
        """
        result = None
        
        if access_type in ['read','read_or_write']:
            for access in self._read:
                if tensor_name == '' or tensor_name == access._tensor_name:
                    result = access.get_access() if result is None else result.union(access.get_access)
        
        if access_type in ['wirte','read_or_wirte']:
            for access in self._write:
                if tensor_name == '' or tensor_name == access._tensor_name:
                    result = access.get_access() if result is None else result.union(access.get_access)
        
        if result is not None:
            result = result.instersect_domain(self._domain)
    
    def print_info(self):
        """
        打印Statement的域和读写信息
        """
        print("Statement Domain: ",self._domain)
        print()
        print('Read Access: ')
        for access in self._read:
            access.print_info()
        print()
        print('Write Access: ')
        for access in self._write:
            access.print_info()
    
    def get_tensor_list(self):
        """
        返回Stetemnt中涉及的读和写的张量列表
        """
        
        input_tensors = sorted(set(access._tensor_name for access in self._read))
        output_tensors = sorted(set(access._tensor_name for access in self._write))
        return input_tensors, output_tensors
    
    def copy(self):
        """
        返回 Stetement 对象的拷贝
        """
        result = Statement(self._context)
        result._domain = self._domain.copy() if self._domain else None
        result._read = [access.copy() for access in self._read]
        result._write = [access.copy() for access in self._write]
        return result
    