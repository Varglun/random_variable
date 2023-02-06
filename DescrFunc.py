from ContiniousFunctions import Fun, SumOp, ProdOp


class DescreteFuntion:
    def __init__(self) -> None:
        pass


class OneSideDescrete(DescreteFuntion):
    def __init__(self, x0, fun) -> None:
        super().__init__()
        self.x0 = x0
        self.fun = fun


class DescreteSumFun:
    def __init__(self, fun1, fun2) -> None:
        self.fun1 = fun1
        self.fun2 = fun2


class DescreteSumOp:
    def __init__(self):
        super().__init__()

    @staticmethod
    def sum(fun1, fun2):
        return DescreteSumFun(fun1, fun2)


class DescreteProdOp:
    def __init__(self):
        super().__init__()

    @staticmethod
    def product(fun1, fun2):
        if isinstance(fun1, OneSideDescrete) and isinstance(fun2, OneSideDescrete):
            return OneSideDescrete(x0=max(fun1.x0, fun2.x0), fun=ProdOp.product(fun1.fun, fun2.fun))
        elif isinstance(fun2, DescreteSumFun):
            return DescreteSumOp.sum(DescreteProdOp.product(fun1, fun2.fun1), DescreteProdOp.product(fun1, fun2.fun2))
        elif isinstance(fun1, DescreteSumFun):
            return DescreteSumOp.sum(DescreteProdOp.product(fun2, fun1.fun1), DescreteProdOp.product(fun2, fun1.fun2))  
        elif isinstance(fun1, Fun) and isinstance(fun2, OneSideDescrete):
            return OneSideDescrete(x0=fun2.x0, fun=ProdOp.product(fun1, fun2.fun))
        elif isinstance(fun2, Fun) and isinstance(fun1, OneSideDescrete):
            return OneSideDescrete(x0=fun1.x0, fun=ProdOp.product(fun2, fun1.fun))            
                   
