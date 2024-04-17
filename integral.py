class Integral:
    
    def __init__(self, start_point, end_point, number_of_points):
        self.start_point = start_point
        self.end_point = end_point
        self.number_of_points = number_of_points
        self.result = 0
        
    def integral_function(self, x):
        y = x*x
        return y
        
    def calculate_trapezoid(self, s_point, e_point):
        ys = self.integral_function(s_point)
        ye = self.integral_function(e_point)
        p = (ye+ys)*(e_point-s_point)/2
        return p
        
    def calculate_result(self):
        step = (self.end_point-self.start_point)/self.number_of_points
        # for s_point in range (self.start_point, self.end_point, step):
        s_point = self.start_point
        while s_point < self.end_point:    
            e_point = s_point + step
            p = self.calculate_trapezoid(s_point, e_point)
            self.result += p
            s_point = e_point
            
    
    def add_partial_result(self, partial_result):
        self.result += partial_result