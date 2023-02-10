from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

def plot_funct(fun, a, b, n=1000):
  l_real = []
  l_compl = []
  val = a
  vals = []
  for _ in range(n):
    vals.append(val)
    try:
      l_real.append(np.real(fun(val)))
      l_compl.append(np.imag(fun(val)))
    except:
      print("was mistake")
    val += (b - a)/n

  plt.plot(vals, l_real)
  #plt.plot(l_compl)
  plt.show()



def char_fun_unit(l_s, t_s):
  def fun(t):
    return (l_s - 1j*t * np.exp(-l_s * t_s + 1j * t_s * t)) / (l_s - 1j * t)
  return fun


def cdf_from_char(char_fun, b, T, a=0):
  # finds F(b) - F(a)
  # choose greate T for more precise answer
  if a == 0:
    def int_fun(t):
      return np.real((1 - np.exp(-1j * t * b)) / (1j * t) * char_fun(t))
  else:
    def int_fun(t):
      return np.real((np.exp(-1j * t * a) - np.exp(-1j * t * b)) / (1j * t) * char_fun(t))
  return 1 / (2 * np.pi) * quad(int_fun, 0, T, limit=100000, points=[0])[0] * 2

def char_fun_unit_product(l_s, t_s):
  def fun(t):
    ans = 1
    for i in range(len(l_s)):
      ans *= char_fun_unit(l_s[i], t_s[i])(t)
    return ans
  return fun

t0 = 3*8760
b = 0.85*17*t0
myfun = char_fun_unit_product(l_s=[-np.log(0.95)/t0, -np.log(0.98995) / t0, -np.log(0.98995) / t0, -np.log(0.971) / t0, -np.log(0.9935) / t0, -np.log(0.9935) / t0, -np.log(0.9975) / t0, -np.log(0.9975) / t0, -np.log(0.95182) / t0, -np.log(0.962) / t0, -np.log(0.965) / t0, -np.log(0.965) / t0, -np.log(0.965) / t0, -np.log(0.975) / t0, -np.log(0.97572) / t0, -np.log(0.97572) / t0, -np.log(0.95) / t0], t_s = [t0] * 17)

myfun_int = lambda val: np.real((1 - np.exp(-1j * val * b)) / (1j * val) * myfun(val))


"""
l_real = []
l_compl = []

n = 1000
T = 10
val = -T
for _ in range(n):
  val += (2*T)/n
  if val != 0:
    l_real.append(np.real((1 - np.exp(-1j * val * 10)) / (1j * val) * myfun(val)))
    l_compl.append(np.imag((1 - np.exp(-1j * val * 10)) / (1j * val) * myfun(val)))


plt.plot(l_real)
plt.plot(l_compl)
plt.show()
"""


#plot_funct(myfun_int, -0.01, 0.01)

#mycdf = [cdf_from_char(myfun, 150, T/100) for T in range(10, 30)]

plot_funct(lambda T: cdf_from_char(myfun, b, T), 10, 10.1, n=10)

"""
f = open("integr_results.csv", "w")
dT = 0.001
T = 0
int_tot = 0
T_end = 1000
while T < T_end:
  val = 1 / (2 * np.pi) * quad(myfun_int, T, T + dT, limit=100000, points=[0])[0] * 2
  T += dT
  int_tot += val
  f.write(str(T) + ", " + str(val) + ", " + str(int_tot) + ",\n")
  print(f"{round(T / T_end*100)} %", end="\r")

f.close()
"""

#plt.plot(mycdf)
#plt.show()


