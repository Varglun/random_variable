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