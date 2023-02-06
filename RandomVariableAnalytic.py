сlass Destribution:
  def __init__(self):
    pass


class ContinDestr(Destribution):
  def __init__(destr_funct, df_type='pdf'):
    if df_type == 'pdf':
      self.pdf = destr_funct