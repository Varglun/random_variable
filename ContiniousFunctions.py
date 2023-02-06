from dataclasses import dataclass
import numpy as np
# 62a1#uj_m&$rld$uYAP7

class Fun:
  def __init__(self):
    pass
  def get_name(self):
    return self.__class__.__name__


class ElFun(Fun):
  def __init__(self):
    super().__init__()


class ExpFun(ElFun):
  # imitates exp(lam * x)
  def __init__(self, lam):
    super().__init__()
    self.lam = lam

  def print_fun(self, var="x"):
    if self.lam == 0:
      return "1"
    else:
      return f"exp({self.lam} * {var})"
  

class PowFun(ElFun):
  # imitates x^n
  def __init__(self, n):
    super().__init__()
    self.n = n

  def print_fun(self, var="x"):
    if self.n == 0:
      return "1"
    else:
      return f"{var}^({self.n})"


class ConstFun(ElFun):
  def __init__(self, num):
    super().__init__()
    self.num = num

  def print_fun(self, var="x"):
    return f"{self.num}"


class SumFun(Fun):
  def __init__(self, fun1, fun2):
    super().__init__()
    self.fun1 = fun1
    self.fun2 = fun2

  def print_fun(self, var="x"):
    return f"{self.fun1.print_fun(var)} + {self.fun2.print_fun(var)}"


class ProdFun(Fun):
  # product of two elementary functions
  def __init__(self):
    super().__init__()


class ProdDblFun(ProdFun):
  # product of two elementary functions
  def __init__(self, fun1, fun2):
    if not (isinstance(fun1, ElFun) and isinstance(fun2, ElFun)):
      raise TypeError("fun1 and fun2 should be elementary functions.")
    super().__init__()
    self.fun1 = fun1
    self.fun2 = fun2

  def print_fun(self, var="x"):
    if (self.fun1.get_name() == "ConstFun" and self.fun1.num == 0) or (self.fun2.get_name() == "ConstFun" and self.fun2.num == 0):
      return "0"
    else:
      return f"{self.fun1.print_fun(var)} *  {self.fun2.print_fun(var)}"


class ProdTrplFun(ProdFun):
  # product of three elementary functions
  def __init__(self, fun1, fun2, fun3):
    if not (isinstance(fun1, ElFun) and isinstance(fun2, ElFun) and isinstance(fun3, ElFun)):
      raise TypeError("fun1, fun2 and fun3 should be elementary functions.")
    super().__init__()
    self.fun1 = fun1
    self.fun2 = fun2
    self.fun3 = fun3

  def print_fun(self, var="x"):
    if (self.fun1.get_name() == "ConstFun" and self.fun1.num == 0) or (self.fun2.get_name() == "ConstFun" and self.fun2.num == 0) or (self.fun3.get_name() == "ConstFun" and self.fun3.num == 0):
      return "0"
    else:
      return f"{self.fun1.print_fun(var)} *  {self.fun2.print_fun(var)} *  {self.fun3.print_fun(var)}"


class BinOp:
  def __init__(self):
    pass
  

class SumOp(BinOp):
  def __init__(self):
    super().__init__()

  @staticmethod
  def sum(fun1, fun2):
    # add additional operation for elementary functions, such as constant
    if fun1.get_name() == fun2.get_name() and (fun1.get_name() in ["ExpFun", "PowFun", "ConstFun"]):
      if fun1.get_name() == "ConstFun":
        return ConstFun(fun1.num + fun2.num)
      elif fun1.get_name() == "ExpFun" and (fun1.lam == fun2.lam):
        return ProdOp.product(ConstFun(2), ExpFun(fun1.lam))
      elif fun1.get_name() == "PowFun" and (fun1.n == fun2.n):
        return ProdOp.product(ConstFun(2), PowFun(fun1.n))
    else:
      return SumFun(fun1, fun2)


class ProdOp(BinOp):
  dict_funs = {"ExpFun": 0, "PowFun": 1, "ConstFun": 2, "SumFun": 3, "ProdDblFun": 4, "ProdTrplFun": 4}
  methods_funs_order = [[(0, 1), (1, 0), (1, 0), (0, 1), (0, 1)], 
                        [(0, 1), (0, 1), (1, 0), (0, 1), (0, 1)],
                        [(0, 1), (0, 1), (0, 1), (0, 1), (0, 1)],
                        [(1, 0), (1, 0), (1, 0), (0, 1), (1, 0)],
                        [(1, 0), (1, 0), (1, 0), (0, 1), (0, 1)],]


  def __init__(self):
    super().__init__()

  @staticmethod
  def product(fun1, fun2):
    methods_matrix = [[ProdOp.prodExp, ProdOp.prodExpPow, ProdOp.prodConstExp, ProdOp.prodSum, ProdOp.prodElPr],
                      [ProdOp.prodExpPow, ProdOp.prodPow, ProdOp.prodConstPow, ProdOp.prodSum, ProdOp.prodElPr],
                      [ProdOp.prodConstExp, ProdOp.prodConstPow, ProdOp.prodConst, ProdOp.prodSum, ProdOp.prodElPr],
                      [ProdOp.prodSum, ProdOp.prodSum, ProdOp.prodSum, ProdOp.prodSum, ProdOp.prodSum],
                      [ProdOp.prodElPr, ProdOp.prodElPr, ProdOp.prodElPr, ProdOp.prodSum, ProdOp.prodPr]]
    funs = (fun1, fun2)
    fun1_ind = ProdOp.dict_funs[fun1.get_name()]
    fun2_ind = ProdOp.dict_funs[fun2.get_name()]
    order = ProdOp.methods_funs_order[fun1_ind][fun2_ind]
    return methods_matrix[fun1_ind][fun2_ind](funs[order[0]], funs[order[1]])

  @staticmethod
  def prodExp(fun1, fun2):
    return ExpFun(fun1.lam + fun2.lam)

  @staticmethod
  def prodPow(fun1, fun2):
    return PowFun(fun1.n + fun2.n)

  @staticmethod
  def prodConst(fun1, fun2):
    return ConstFun(fun1.num * fun2.num)

  @staticmethod
  def prodExpPow(fun1, fun2):
    # fun1 - Pow
    # fun2 - Exp
    return ProdDblFun(fun1, fun2)

  @staticmethod
  def prodConstExp(fun1, fun2):
    # fun1 - Const
    # fun2 - Exp
    return ProdDblFun(fun1, fun2)

  @staticmethod
  def prodConstPow(fun1, fun2):
    # fun1 - Const
    # fun2 - Pow
    return ProdDblFun(fun1, fun2)

  @staticmethod
  def prodSum(fun1, fun2):
    # fun2 - sum
    return SumOp.sum(ProdOp.product(fun1, fun2.fun1), ProdOp.product(fun1, fun2.fun2))

  @staticmethod
  def prodElPr(fun_el, fun_pr):
    fun_el_type = fun_el.get_name()

    if isinstance(fun_pr, ProdDblFun):
      funs_pr = [fun_pr.fun1, fun_pr.fun2]
      fun_pr1_type = fun_pr.fun1.get_name()
      fun_pr2_type = fun_pr.fun2.get_name()
      fun_pr_types = [fun_pr1_type, fun_pr2_type]
      if fun_el_type in fun_pr_types:
        return ProdDblFun(funs_pr[1 - fun_pr_types.index(fun_el_type)], ProdOp.product(fun_el, funs_pr[fun_pr_types.index(fun_el_type)])) 
      else:
        return ProdTrplFun(fun_el, fun_pr.fun1, fun_pr.fun2)
    elif isinstance(fun_pr, ProdTrplFun):
      funs_pr = [fun_pr.fun1, fun_pr.fun2, fun_pr.fun3]
      fun_pr1_type = fun_pr.fun1.get_name()
      fun_pr2_type = fun_pr.fun2.get_name()
      fun_pr3_type = fun_pr.fun3.get_name()
      fun_pr_types = [fun_pr1_type, fun_pr2_type, fun_pr3_type]
      if fun_el_type in fun_pr_types:
        l1 = [0, 1, 2]
        l1.remove(fun_pr_types.index(fun_el_type))
        indx_1 = l1[0]
        indx_2 = l1[1]
        return ProdTrplFun(funs_pr[indx_1], funs_pr[indx_2], ProdOp.product(fun_el, funs_pr[fun_pr_types.index(fun_el_type)])) 
      else:
        raise TypeError("No such fun")
    else:
      raise NameError("No such product type")

  @staticmethod
  def prodPr(fun1, fun2):
    if isinstance(fun1, ProdDblFun):
      return ProdOp.product(fun1.fun2, ProdOp.product(fun1.fun1, fun2))
    elif isinstance(fun1, ProdTrplFun):
      if isinstance(fun2, ProdDblFun):
        return ProdOp.product(fun2.fun2, ProdOp.product(fun2.fun1, fun2))
      elif isinstance(fun2, ProdTrplFun):
        return ProdOp.product(ProdDblFun(fun1.fun2, fun1.fun3), ProdOb.product(fun1.fun1, fun2))
    else:
      raise NameError("No such product type")


@dataclass
class LinFunIntegr:
  k: float
  b: float


class CompFun:
  def __init__(self):
    pass

  @staticmethod
  def evaluate(fun_main, fun_inner):
    if fun_main.get_name() == "ConstFun":
      return fun_main
    elif fun_main.get_name() == "ExpFun":
      return ProdOp.product(ConstFun(np.exp(fun_main.lam * fun_inner.b)), ExpFun(fun_main.lam * fun_inner.k))
    elif fun_main.get_name() == "PowFun":
      if fun_main.n == 0:
        return ConstFun(1)
      else:
        return ProdOp.product(SumOp.sum(ProdOp.product(ConstFun(fun_inner.k), PowFun(1)), ConstFun(fun_inner.b)), CompFun.evaluate(PowFun(fun_main.n - 1), fun_inner))
    elif fun_main.get_name() == "ProdDblFun":
      return ProdOp.product(CompFun.evaluate(fun_main.fun1, fun_inner), CompFun.evaluate(fun_main.fun2, fun_inner))
    elif fun_main.get_name() == "ProdTrplFun":
      return ProdOp.product(CompFun.evaluate(fun_main.fun1, fun_inner), ProdOp.product(CompFun.evaluate(fun_main.fun2, fun_inner), CompFun.evaluate(fun_main.fun3, fun_inner)))
    elif fun_main.get_name() == "SumFun":
      return SumOp.sum(CompFun.evaluate(fun_main.fun1, fun_inner), CompFun.evaluate(fun_main.fun2, fun_inner))
    else:
      raise NameError(f"No such fun {fun_main.get_name()}")



















