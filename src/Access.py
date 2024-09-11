import islpy as isl
import src.stt as stt

class Access:
    def __init__(self,context,tensor_name='',access_str=None,is_write=False) -> None:
        """
        初始化Access类
        """
        if isinstance(context,stt.ISL_Context):
            self._context = context.ctx()
        else: 
            raise Exception('传入参数类型错误')
        self._tensor_name = tensor_name
        
        if access_str is not None:
            self._access = isl.UnionMap.read_from_str(self._context,access_str)
        else:
            self._access = None
        
        self._is_wirte = is_write
        
    def get_access(self):
        """
        获取当前类的拷贝
        """
        if self._access is not None:
            return self._access.copy()
        else:
            return None
        
    def print_info(self):
        """
        打印访问信息
        """
        print(f'Tensor Name:{self._tensor_name}')
        access_type = 'write' if self._is_wirte else 'read'
        print('Access Type:'+access_type)
        
        if self._access is not None:
            print('Access:'+self._access)
        else:
            print('Access: None')
        
        print()
        
    def copy(self):
        """
        获取Access类的拷贝
        """
        new_Access = Access(self._context)
        new_Access._tensor_name = self._tensor_name
        new_Access._access = self.get_access()
        new_Access._is_wirte = self._is_wirte
        
        return new_Access