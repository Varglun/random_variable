from ContiniousFunctions import ExpFun, PowFun, ProdOp, SumOp, ConstFun, CompFun, SumFun, ProdDblFun, ProdTrplFun, LinFunIntegr
from DescrFunc import OneSideDescrete, DescreteSumOp, DescreteProdOp


class LinOp:
  def __init__(self):
    pass


class Integrator(LinOp):
  def __init__(self):
    super().__init__()


class IndIntegrator(Integrator):
  def __init__(self):
    super().__init__()

  @staticmethod
  def integrate(fun):
    methods = {"ExpFun": IndIntegrator.exp_int, "PowFun": IndIntegrator.pow_int, "ConstFun": IndIntegrator.const_int, "SumFun": IndIntegrator.sum_int, "ProdDblFun": IndIntegrator.prod_int, "ProdTrplFun": IndIntegrator.prod_int}
    return methods[fun.get_name()](fun)

  @staticmethod
  def exp_int(fun):
    if fun.lam == 0:
      return PowFun(1)
    else:
      return ProdOp.product(ConstFun(1 / fun.lam), fun)

  @staticmethod
  def pow_int(fun):
    if fun.n == -1:
      raise ZeroDivisionError("You need log function!!!")
    else:
      return ProdOp.product(ConstFun(1 / (fun.n +1)), PowFun(fun.n + 1))

  @staticmethod
  def const_int(fun):
    if fun.num == 0:
      raise "You need non-definite const function!!!"
    else:
      return ProdOp.product(fun, PowFun(1))

  @staticmethod
  def sum_int(fun):
    return SumOp.sum(IndIntegrator.integrate(fun.fun1), IndIntegrator.integrate(fun.fun2))

  @staticmethod
  def prod_int(fun):
    if isinstance(fun, ProdDblFun):
      return IndIntegrator.dbl_prod_int(fun)
    else:
      return IndIntegrator.trpl_prod_int(fun)
    

  @staticmethod
  def dbl_prod_int(fun):
    fun1_type = fun.fun1.get_name()
    fun2_type = fun.fun2.get_name()   
    funs_type = [fun1_type, fun2_type]
    funs = [fun.fun1, fun.fun2]
    if "ConstFun" in funs_type:
      const_ind = funs.index("ConstFun")
      return IndIntegrator.prod_int_const_some(funs[const_ind], funs[1 - const_ind])
    elif "PowFun" in funs_type and "ExpFun" in funs_type:
      pow_ind = funs_type.index("PowFun")
      exp_ind = funs_type.index("ExpFun")
      pow_fun = funs[pow_ind]
      exp_fun = funs[exp_ind]
      if pow_fun.n == 0:
        return IndIntegrator.exp_int(exp_fun)
      else:
        ans1 = ProdOp.product(ConstFun(1/exp_fun.lam), fun)
        new_fun = ProdDblFun(PowFun(pow_fun.n-1), exp_fun)
        ans2 = ProdOp.product(ConstFun(-1 * pow_fun.n/exp_fun.lam), IndIntegrator.prod_int(new_fun))
        return SumOp.sum(ans1, ans2)
    else:
      raise NameError("No such fun")

  @staticmethod
  def trpl_prod_int(fun):  
    fun1_type = fun.fun1.get_name()
    fun2_type = fun.fun2.get_name()   
    fun3_type = fun.fun3.get_name()   
    funs_type = [fun1_type, fun2_type, fun3_type]
    funs = [fun.fun1, fun.fun2, fun.fun3]
    if "ConstFun" in funs_type:
      const_ind = funs.index("ConstFun")
      indx_1 = [0, 1, 2].remove(const_ind)[0]
      indx_2 = [0, 1, 2].remove(const_ind)[1]
      return IndIntegrator.prod_int_const_some(funs[const_ind], ProdDblFun(funs[indx_1], funs[indx_2]))
    else:
      raise NameError("No such fun")

  @staticmethod
  def prod_int_const_some(fun_const, fun_some):
    return ProdOp.product(fun_const, IndIntegrator.integrate(fun_some))


class DefIntegrator(Integrator):
  def __init__(self):
    super().__init__()

  @staticmethod
  def integrate(fun, a, b):
    # a and b are LinFuns
    pass

  @staticmethod
  def fun_int(fun, a, b):
    # integrate non descrete function
    ans1 = CompFun.evaluate(IndIntegrator.integrate(fun), b)
    ans2 = ProdOp.product(ConstFun(-1), CompFun.evaluate(IndIntegrator.integrate(fun), a))
    return SumOp.sum(ans1, ans2)

  @staticmethod
  def descr_fun_int(fun, a, b):
    # integrate descrete function
    if a.k == 0:
      if a.b < fun.x0:
        func1 = ConstFun(0)
      else:
        func1 = DefIntegrator.integrate(ProdOp.product(fun.fun, Const(-1)), LinFunIntegr(k=0, b=fun.x0), a)
    else:
      func1 = OneSideDescrete(x0=fun.x0/a.k - a.b/a.k, fun=DefIntegrator.integrate(ProdOp.product(fun.fun, Const(-1)), LinFunIntegr(k=0, b=fun.x0), a))
    if b.k == 0:
      if b.b < fun.x0:
        func2 = ConstFun(0)
      else:
        func2 = DefIntegrator.integrate(fun.fun, LinFunIntegr(k=0, b=fun.x0), b)
    else:
      func2 = OneSideDescrete(x0=fun.x0/b.k - b.b/b.k, fun=DefIntegrator.integrate(fun.fun, LinFunIntegr(k=0, b=fun.x0), b))    
    return DescreteSumOp.sum(func1, func2)

    
    











