import os
from dotenv import load_dotenv
from supabase import create_client, Client
import random
from datetime import datetime

_instance = None

def get_supabase_instance():
    global _instance
    if _instance is None:
        _instance = SupabaseDataLayer()
    return _instance

def desenpaquetar_set(data):
    setxd = set(data)
    return setxd.pop()

def calcular_total_usd(dato):
    precio = dato['VariedadMango']['precio']
    cajas = dato['cajas']
    return round(precio * cajas, 2)

def calcular_total_mxn(dato, tipo_cambio):
    precio = dato['VariedadMango']['precio']
    cajas = dato['cajas']
    return round(precio * cajas * tipo_cambio, 2)


class SupabaseDataLayer:
    def __init__(self):
        load_dotenv()
        # Configura las credenciales de tu aplicación Supabase
        supabase_url = os.environ.get("SUPABASE_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        
        # Crea un cliente Supabase
        self.client: Client = create_client(supabase_url, supabase_key)

    def authenticate(self, email, password):
        # Método para autenticar un usuario
        user = self.client.auth.sign_in_with_password({ "email": email, "password": password })
        if user:
            return user
        else:
            raise Exception(f"Error en la autenticación.")
        
    def get_resumen(self, id):
        # Método para obtener
        data = self.client.table("ResumenCarga").select("*").eq("no_certificate", id).execute()
        
        # Assert we pulled real data.
        if len(data.data) < 1:
            return []
        
        print (data.data)
        return data.data
        
    def get_variedades(self):
        data = self.client.table("VariedadMango").select("variedad").execute()
        
        # Assert we pulled real data.
        if len(data.data) < 1:
            return []
        
        array = [element['variedad'] for element in data.data]
        
        # print(array)
        return array
    
    def get_info_manifiesto(self, id):
        infoManifiesto = self.client.table("ManifiestoCarga").select("*").eq("no_certificate", id).execute()
        infoCertificado = self.client.table("CertificadoDeEmbarque").select("*").eq("no_certificate", id).execute()


        if len(infoManifiesto.data) < 1:
            return {}
        
        if len(infoCertificado.data) < 1:
            return {}
        
        infoManifiesto = infoManifiesto.data[0] | infoCertificado.data[0]
        
        # print(infoManifiesto)
        return infoManifiesto

    def get_manifiestos(self):
        data = self.client.table("ManifiestoCarga").select("no_certificate").execute()
        
        # Assert we pulled real data.
        if len(data.data) < 1:
            return []
        
        array = [element['no_certificate'] for element in data.data]
        
        # print(array)
        return array

    def insert_manifiesto(self, data, embarque, temp=0):
        noCertificate = data['no_certificate']
        
        try:
            # Inserta un manifiesto
            result = self.client.table("CertificadoDeEmbarque").insert(data).execute()
            
            if result.data and len(result.data) > 0:
                result2 = self.client.table("ManifiestoCarga").insert({ "no_certificate": noCertificate, "no_embarque": embarque, "temp": temp }).execute()
            if result2.data and len(result2.data) < 1:
                raise Exception ("Error al insertar el manifiesto.")
            
            allInfo = self.get_info_manifiesto(noCertificate)
                  
        except Exception as e:
            print(f"Error: {e}")
            return []
        

        return allInfo
    
    def modify_manifiesto(self, data, embarque, temp=0):
        noCertificate = data['no_certificate']
        
        try:
            # Modifica un manifiesto
            result = self.client.table("CertificadoDeEmbarque").update(data).eq("no_certificate", noCertificate).execute()
            
            if result.data and len(result.data) > 0:
                result2 = self.client.table("ManifiestoCarga").update({ "no_certificate": noCertificate, "no_embarque": embarque, "temp": temp }).eq("no_certificate", noCertificate).execute()
            if result2.data and len(result2.data) < 1:
                raise Exception ("Error al modificar el manifiesto.")
        except Exception as e:
            print(f"Error: {e}")
            return []
        
        allInfo = self.get_info_manifiesto(noCertificate)
        
        return allInfo
    
    def insert_resumen(self, data):
        try:
            # Inserta un resumen de carga
            result = self.client.table("ResumenCarga").insert(data).execute()
            
            if result.data and len(result.data) < 1:
                raise Exception ("Error al insertar el resumen.")
            
            info = self.get_resumen(data['no_certificate'])
            return info
        except Exception as e:
            print(f"Error: {e}")
            return []
    
    def obtener_tipoDeCambio(self, fechaCarga):
        fecha = datetime.strptime(fechaCarga, '%Y-%m-%d')
        seed = int(fecha.strftime('%Y%m%d'))
        random.seed(seed)
        
        tipoCambio = round(random.uniform(16.50, 17.20), 2)
        print (f"Tipo de cambio: {tipoCambio}")
        return tipoCambio
    
    def get_costos(self, id):
        # Método para obtener
        data = self.client.table("ResumenCarga").select("variedad, calibre,cajas, VariedadMango(precio), CertificadoDeEmbarque(fecha_carga)").eq("no_certificate", id).execute()
        
        # Assert we pulled real data.
        if len(data.data) < 1:
            return []
        
        print(data.data)
        
        fecha = data.data[0]['CertificadoDeEmbarque']['fecha_carga']
        tipoCambio = self.obtener_tipoDeCambio(fecha)
        
        # Sacar la cantidad de cajas por variedad
        cajasPorVariedad = { dato['variedad']: {'cajas': sum([elem['cajas'] for elem in data.data if elem['variedad'] == dato['variedad']]), 'precio': desenpaquetar_set([dato['VariedadMango']['precio'] for elem in data.data if elem['variedad'] == dato['variedad']])} for dato in data.data }
        
        # Sacar costos por variedad
        costosPorVariedad = {variedad: {'cajas': cajasPorVariedad[variedad]['cajas'], 'precio': cajasPorVariedad[variedad]['precio'], 'total_usd': round(cajasPorVariedad[variedad]['cajas'] * cajasPorVariedad[variedad]['precio'],2), 'total_mxn': round(cajasPorVariedad[variedad]['cajas'] * cajasPorVariedad[variedad]['precio'] * tipoCambio, 2)} for variedad in cajasPorVariedad}
        
        
        for dato in data.data:
            del(dato['CertificadoDeEmbarque'])
            dato['total_usd'] = calcular_total_usd(dato)
            dato['total_mxn'] = calcular_total_mxn(dato, tipoCambio)
        
        resultado = {
            "no_certificate": id,
            "fecha_carga": fecha,
            "tipo_cambio": tipoCambio,
            "costos": data.data,
            "costo_total_usd": sum([dato['total_usd'] for dato in data.data]),
            "costo_total_mxn": sum([dato['total_mxn'] for dato in data.data]),
            "costosPorVariedad": costosPorVariedad,
        }
        
        # print(resultado)
        return resultado
    
    
    
        
        
if __name__ == "__main__":
    test = SupabaseDataLayer()
    test.get_costos(4379065)
    # test.obtener_tipoDeCambio('2024-05-02')



