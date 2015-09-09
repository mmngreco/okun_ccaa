

def decimal_to_point(x):
    '''
    Solo en cadenas de texto, si no es una cadena omite la operación.
    Elimina los puntos (.) de miles.
    Reemplaza la coma decimal (",") por el punto decimal (".")
    en una cadena de texto y lo convierte a punto flotante.
    ----------
    ej:
    decimal_to_point('123.456.789,43') == 123456789.43
    '''
    try:
        return float(x.replace('.', '').replace(',', '.'))
    except:
        return float(x)


def romans_to_num(x): # modificar para que no dependa de T
    '''
    Reemplaza los numeros romanos del 1 al 4 por el caracter númerico.
    ----------
    ej:
    romans_to_num('II') == 2
    '''
    roman = x[x.index('T') + 1:]
    translate = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}

    if any(map(lambda y: roman == y, translate.keys())):
        return x[:x.index('T')+1] + str(translate[roman])
    else:
        return x


def extrae_trimestre(x):
    '''
    Para tendencia temporal con el formato 2015T1, 2015T2...
    Extrae el trimestre y desprecia el resto.
    Coge los caracteres 'T' hasta el final.
    ----------
    ej:
    year('2015T4') == T4
    '''
    return x[x.index('T'):]


def extrae_year(x):
    '''
    Para tendencia temporal con el formato 2015T1, 2015T2...
    Extrae el año y desprecia el resto. Coge los 4 números anteriores a 'T'
    ----------
    ej:
    year('2015T4') == 2015
    '''
    return x[x.index('T')-4:x.index('T')]



def estimar_mco(df, endogena, exogena, regiones):
    '''
        Estima el modelo mco, para cada columna del dataframe,
        que contiene dos variables.
        
        df: dataframe
        endogena: nombre de la variable del df.
        exogena: nombre de la variable del df.
        regiones: nombres de las regiones.
        
        return (sumr, betas, modelos)
        '''
    import statsmodels.api as sm
    from numpy import divide

    sumr = dict()
    betas = dict()
    modelos = dict()
    
    for i, ca in enumerate(regiones):
        x = sm.add_constant(df[exogena][ca])
        mod = sm.OLS(endog=df[endogena][ca], exog=x, missing='drop')
        res = mod.fit()
        # guardar datos:
        modelos[ca] = res
        sumr[ca] = res.summary(xname=['const', endogena],
                               yname=exogena,
                               title=ca)
        betas[ca] = [res.params[0],
                     res.pvalues[0],
                     res.params[1],
                     res.pvalues[1],
                     res.rsquared]

    return (sumr, betas, modelos)


def crear_df(df_list, keys=['empleo', 'paro', 'pib']):
    '''
        Crea un dataframe con los dataframes pasados mediante pd.concat.
        
        df_list: lista de df, [df_empleo, df_paro, df_pib]
        keys: lista con los nombres de las variables representadas en cada df.
        
        return df
        '''
    import pandas as pd

    df = pd.concat(df_list,
                   axis= 1,
                   keys=keys,
                   names=['Variables', 'Regiones'])
                   
    return df


def resumen_mco(dicc, nombres_latex, ):
    '''
        dicc = Diccionario donde keys = Regiones, values = lista de Valores del mco.
        nombres_parametros = Nombres de los parámetros que contiene la lista.
        
        return: df ordenado por R² descendente.
        '''
    from pandas import DataFrame
    global nombres_parametros

    if nombres_latex == 0:
        nombres_parametros = ['b0', 'pv_b0', 'b1', 'pv_b1', 'R2',]
    else:
        nombres_parametros = ['$β_0$', '$pv_{β_0}$', '$β_1$',  '$pv_{β_1}$', '$R^2$']
    
    mco_paro = DataFrame(dicc, index=nombres_parametros).T.sort(nombres_parametros[3], ascending=False)
    
    return mco_paro


def guardar_mco(resumen, etiqueta):
    '''
        Guarda los modelos MCO pasados como diccionario en
        formato HTML y TXT, en la carpeta data_work/MCO/.
        
        Argumentos:
        - resumen: Diccionario creado en statsmodels con
        la salida sumary, tabla resúmen de cada model mco.
        - etiqueta: Etiqueta del modelo 'modelos_u'= paro ; 'modelos_l'= empleo; 'modelos_y': PIB.
        
        e.j.:
        guardar_mco(diccionario_mco, 'modelos_gls_outliers') -> Guarda data_work/MCO/modelos_gls_outliers.html y
        data_work/MCO/modelos_gls_outliers.txt
        
        return: None.
        '''
    with open(u'data_work/MCO/%s.html' % etiqueta, "w") as fweb:
        for k, v in resumen.items():
            print('<h1>{}</h1>'.format(k), file=fweb)
            print(resumen[k].as_html(), file=fweb)
            print(u'</br></br></br>', file=fweb)
        
        fweb.close()
    print('%s.html guardado.' % etiqueta)

    n = 0
    with open('data_work/MCO/%s.txt' % etiqueta, "w") as f:
        for k, v in resumen.items():
            n += 1
            print(str(n), file=f)
            print(k, file=f)
            print(v.as_text(), file=f)
            print('\n\n\n', file=f)
        
        f.close()
    print('%s.txt guardado.' % etiqueta)
    print('Archivos Guardados Correctamente.')
    return None

def pvalue_sig_5(x):
    '''
    Ver si es significativo un p-value para 
    un nivel de significación del 5%.
    '''
    if x < 0.05:
        return '***'
    else:
        return ' '