def channels_by_tp(df, j, ocurrencies, max_journey_size, separator = ' > '):
  """
  How many times did each channel appear at each stage of the journeys.

  Parameters: 
  df: pandas.Dataframe. Dataframe that will be counted.

  j: pandas.Series. Collumn representing the journey. Expected in the 
  format 'tp_0 > tp_1 > tp_2 ... tp_n'

  ocurrencies: dataframe's collumm. Collumn representing those times that 
  journey occured. 
  
  separator: str. Character, or sequence of characters, used to separate
  the touch points of the journey given in j. Default: ' > '
  
  Returns: pandas.Dataframe. Dataframe with the number of times each channel 
  appeared at each stage of the journeys.
  
  """  


  # Criando um df com uma coluna com os canais únicos do dataframe para dar merge lá em baixo
  df_result = pd.DataFrame({'channels':list(df[j].str.split(separator).explode().unique())})
  dataframe = df.copy()

  # Transformando o dataframe com explode para pode contar com o value counts
  dataframe['lista_vazia'] = dataframe[ocurrencies].apply(lambda j: list(range(j)))
  dataframe = dataframe.explode('lista_vazia')
  dataframe = dataframe[j].str.split(separator, expand=True)

  # Iterando pela quantidade de colunas (que é a quantidade de canais)
  for n in range (max_journey_size):
    if max_journey_size > len(dataframe.columns):

      result = f'out of range, max journey size is {len(dataframe.columns)}'
      return result

    else:
      # Criando um dataframe que tem uma coluna com os canais e outra com a quantidade de vezes que ele apareceu
      aux = dataframe[n].value_counts().reset_index()
      # Renomeando as colunas
      aux.columns = ['channels',f'tp_{n+1}']
      # Dando merge no df original
      df_result = df_result.merge(aux,how='outer',on='channels')

  # Substituindo os NaN por 0  
  df_result = df_result.fillna(0)

  # Transformando os valores em inteiro
  df_result.iloc[:, [1, -1]] = df_result.iloc[:, [1, -1]].astype(int)

  return df_result