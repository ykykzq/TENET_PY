import islpy as isl

class mapping:
    def __init__(self,context,space_map_str,time_map_str) -> None:
        """
        初始化mapping类。如果指定了时空映射字符串，则也初始化。
        """
        
        self._context = context
        if space_map_str and time_map_str:
            self._space_map = isl.UnionMap.read_from_str(context,space_map_str)
            self._time_map = isl.UnionMap.read_from_str(context,time_map_str)
        else:
            self._space_map = None
            self._time_map = None
            
    def load(self,filename):
        """
        从文件加载时空映射。文件的前两行是时空映射字符串
        """
        try:
            with open(filename,'r') as file:
                space_map_str = file.readline.strip()
                time_map_str = file.readline.strip()
                self._space_map = isl.UnionMap.read_from_str(self._context,space_map_str)
                self._time_map = isl.UnionMap.read_from_str(self._context,time_map_str)
                
                return True
        except IOError:
            return False
        
    def get_space_map(self):
        """
        获得空间映射的拷贝
        """
        if self._space_map is None:
            return None
        else:
            return self._space_map.copy()
        
    def get_time_map(self):
        """
        获得时间映射的拷贝
        """
        if self._time_map is None:
            return None
        else:
            return self._time_map.copy()
        
    def get_time_space_map(self):
        """
        获得时空映射，实际上为时间映射与空间映射的笛卡尔积
        """
        
        if self._time_map is not None and self._space_map is not None:
            return self._space_map.range_product(self._time_map)
        else:
            return None
        
    def print_info(self):
        """
        打印时空映射信息
        """
        
        if self._time_map is not None:
            print('Time Mapping:')
            print(self._time_map)
        else:
            print('Time Mapping: None')
            
        if self._space_map is not None:
            print('Space Mapping:')
            print(self._space_map)
        else:
            print('Space Mapping: None')
            
    def copy(self):
        """
        返回当前类的拷贝
        """
        
        newMapping = mapping(self._context,self.get_time_map,self.get_space_map)
        return newMapping