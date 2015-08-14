#!/usr/bin/env
# -*- coding:utf-8 -*-


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
