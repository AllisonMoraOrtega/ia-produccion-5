
    # ---------------------------------------------
    # transformacion de nombre de proyecto basado en codigos unicos
    codigos = pd.read_excel('codigos_unicos.xlsx')
    # Asegurar que las columnas de cruce tengan formato string sin espacios extra
    df['código presupuestario'] = df['código presupuestario'].astype(str).str.strip()
    codigos['Codigo'] = codigos['Codigo'].astype(str).str.strip()

    # Realizar el Join entre df y codigos
    df_merged = df.merge(
        codigos[['Codigo', 'Nombre']], 
        left_on='código presupuestario', 
        right_on='Codigo', 
        how='left'
    )
    # Reemplazar los valores en 'Nombre Proyecto' con el nuevo 'Nombre' obtenido del join
    # Se mantiene el valor original en caso de que no haya coincidencia
    df['nombre proyecto'] = df_merged['Nombre'].fillna(df['nombre proyecto'])


