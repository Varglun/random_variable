from LinearOperators import DefIntegrator
from ContiniousFunctions import ExpFun, PowFun, ProdOp, SumOp, ConstFun, CompFun, SumFun, ProdDblFun, ProdTrplFun, LinFunIntegr


class Destribution:
    def __init__(self) -> None:
        pass
        
class RandomVariable:
    def __init__(self) -> None:
        pass


class ContiniousRandomVariable(RandomVariable):
    def __init__(self, pdf) -> None:
        super().__init__()
        self.pdf = pdf


class DescreteRandomVariable(RandomVariable):
    def __init__(self, pmf) -> None:
        super().__init__()
        self.pmf


class DC_RandomVariable(RandomVariable):
    def __init__(self, pmf) -> None:
        super().__init__()
        self.pmf


class RandomVariableSumOp:
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def sum(rv1, rv2):
        if isinstance(rv1, ContiniousRandomVariable) and isinstance(rv2, ContiniousRandomVariable):
            pdf1 = DefIntegrator.integrate(rv2.pdf, LinFunIntegr(k=0, b=0), LinFunIntegr(k=1, b=0))
            return ContiniousRandomVariable()