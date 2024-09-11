import islpy as isl
import stt

class PEArray:
    def __init__(self, context, pe_domain_str=None, interconnect_str=None, l1_size=1, l2_size=1, bandwidth= 1, avg_latency= 1) -> None:
        if isinstance(context,stt.ISL_Context):
            self._context = context.ctx()
        else:
            raise Exception('传入参数类型错误')
        
        if pe_domain_str is not None:
            self._domain = isl.UnionSet.read_from_str(self._context)
        else:
            self._domain = None
            
        if interconnect_str is not None:
            self._interconnect = isl.UnionMap.read_from_str(self._context, interconnect_str).interscet_domain(self._domain).intersect_range(self._domain)
        
        self._l1_size = l1_size
        self._l2_size = l2_size
        self._bandwidth = bandwidth
        self._avg_latency = avg_latency
        
    def load(self, filename):
        try:
            with open(filename,'r') as file:
                domain_str = file.readline().strip()
                interconnect_str = file.readline().strip()
                self._domain = isl.UnionSet.read_from_str(self._context, domain_str)
                self._interconnect = isl.UnionSet.read_from_str(self._context, interconnect_str)
                self._l1size = int(file.readline().strip())
                self._l2size = int(file.readline().strip())
                self._bandwidth = int(file.readline().strip())
                self._avg_latency = int(file.readline().strip())
                
        except IOError:
            return False
        
    
    def print_info(self):
        if self._domain is not None:
            print("PE Domain: ", self._domain)
        else:
            print("PE Domain: None")
        if self._interconnect is not None:
            print("interconnection: ", self._interconnect)
        print(f"L1-Size: {self._l1size}")
        print(f"L2-Size: {self._l2size}")
        print(f"Bandwidth: {self._bandwidth}")
        print(f"Average Latency: {self._avg_latency}")
        
        
    def copy(self):
        new_pe_array = PEArray(
            self._context,
            self._domain.copy() if self._domain is not None else None,
            self._interconnect.copy if self._interconnect is not None else None,
            self._l1_size,
            self._l2_size,
            self._bandwidth,
            self._avg_latency
        )
        
        return new_pe_array