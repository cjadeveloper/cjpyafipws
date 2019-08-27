# -*- coding: utf8 -*-
# -*- encoding: utf-8 -*-
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

"Consulta Padron A5"

__author__ = "Cristian Javier Azulay <cjadesarrollador@gmail.com>"
__copyright__ = "Copyright (C) 2019 Cristian Javier Azulay, cjadeveloper"
__license__ = "GPL"
__version__ = "0.0.1"
__status__ = "Development"

from pyafipws.wsaa import WSAA
from pyafipws.ws_sr_padron import WSSrPadronA5
#import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Especificar la ubicacion de los archivos certificado y claves
CERTIFICADO = "FE/cjadeveloperPRO.crt"
CLAVEPRIVADA = "FE/cjadeveloperPRO.key"
# Servicios a acceder
SERVICIO = "ws_sr_padron_a5"
# Tiempo de vida en segundos
TTL = 2400
PADRON_CUIT = "20267268038"

#URL_homo = 'https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA4?WSDL'
URL = 'https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL'

wsaa = WSAA()

## Analizar certificado
# wsaa.AnalizarCertificado(CERTIFICADO)
# print wsaa.Identidad
# print wsaa.Caducidad
# print wsaa.Emisor
# print wsaa.CertX509

# --------------------------------------------------------------
# Generar TA (TRA, CMS y Luego TA): Ver abajo. Usar Autenticar()
# --------------------------------------------------------------
# # Generar un Ticket de Requerimiento de Acceso (TRA)
# tra = wsaa.CreateTRA(SERVICIO, TTL)
# # Generar el mensaje firmado (CMS)
# cms = wsaa.SignTRA(tra, CERTIFICADO, CLAVEPRIVADA)
# wsaa.LanzarExcepciones = False  # revisar Excepcion para controlar errores
# cache = "" # Directorio para archivos temporales (dejar en blanco para usar predeterminado)
# #wsdl =  "" # "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?wsdl" # homologación
# wsdl = "https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA4?wsdl"
# proxy = "" #' usar "usuario:clave@servidor:puerto"
# ok = wsaa.Conectar(cache, wsdl, proxy)
# ta = wsaa.LoginCMS(cms) # otener ticket de acceso

# ------------------------------------------------------------------------
# Desde la versión 2.07 de PyAfipWs se puede usar el método Autenticar()
#
# https://www.sistemasagiles.com.ar/trac/wiki/ManualPyAfipWs#M%C3%A9todos
# ------------------------------------------------------------------------
wsaa_url = 'https://wsaa.afip.gov.ar/ws/services/LoginCms'

# solo usar si hay servidor intermedio
proxy = ""
# httplib2 (default), pycurl (depende proxy)
wrapper = ""
# autoridades certificantes (servidores)
cacert = "pyafipws/conf/afip_ca_info.crt"
# Directorio para archivos temporales (dejar en blanco para usar predeterminado)
cache = "pyafipws/cache"

ta = wsaa.Autenticar(SERVICIO, CERTIFICADO, CLAVEPRIVADA, wsaa_url, proxy, wrapper, cacert, cache)

# utilizar las credenciales:
#print wsaa.Token
#print wsaa.Sign

#wsaa.SetTicketAcceso(ta)

# conectar al webservice de padrón:
padron = WSSrPadronA5()
padron.SetTicketAcceso(ta)
padron.Cuit = "20267268038"
padron.Conectar(
    wsdl="https://aws.afip.gov.ar/sr-padron/webservices/personaServiceA5?wsdl"
)

# if wsaa.Excepcion != '':
#     print "Excepcion!!: " + wsaa.Excepcion
# else:
#     Obtener Token y Sign de autorización
#     Token = wsaa.Token
#     Sign  = wsaa.Sign
#     print "Token: " + Token + "\n"
#     print "Sign: " + Sign

#conectar al webservice de padrón:
# padron = WSSrPadronA5()
# padron.Token = Token
# padron.Sign = Sign
# padron.HOMO = False
# padron.SetTicketAcceso(ta)
# padron.Cuit = "30"
# padron.Conectar("",wsdl)

print "Consultando PadronA5 AFIP online..."
ok = padron.Consultar("20267268038")

print "Denominacion:", padron.denominacion
print "CUIT:", padron.cuit
print "Tipo:", padron.tipo_persona, padron.tipo_doc, padron.dni
print "Estado:", padron.estado
print "Direccion:", padron.direccion
print "Localidad:", padron.localidad
print "Provincia:", padron.provincia
print "Codigo Postal:", padron.cod_postal
print "Impuestos:", padron.impuestos
print "Actividades:", padron.actividades
print "IVA:", padron.imp_iva
print "MT:", padron.monotributo
print "Categoria:", padron.actividad_monotributo
print "Empleador:", padron.empleador
