import os
from dotenv import load_dotenv
from supabase import create_client, Client

_instance = None

def get_supabase_instance():
    global _instance
    if _instance is None:
        _instance = SupabaseDataLayer()
    return _instance

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
               
        # array = [[value for key, value in element.items()] for element in data.data]
        
        # print(array)
        # return array
        print(data.data)
        return data.data
        
    def get_variedades(self):
        data = self.client.table("VariedadMango").select("variedad").execute()
        
        # Assert we pulled real data.
        if len(data.data) < 1:
            return []
        
        array = [element['variedad'] for element in data.data]
        
        print(array)
        return array
    
    def get_info_manifiesto(self, id):
        infoManifiesto = self.client.table("ManifiestoCarga").select("*").eq("no_certificate", id).execute()
        infoCertificado = self.client.table("CertificadoDeEmbarque").select("*").eq("no_certificate", id).execute()


        if len(infoManifiesto.data) < 1:
            return {}
        
        if len(infoCertificado.data) < 1:
            return {}
        
        infoManifiesto = infoManifiesto.data[0] | infoCertificado.data[0]
        
        print(infoManifiesto)
        return infoManifiesto

    def get_manifiestos(self):
        data = self.client.table("ManifiestoCarga").select("no_certificate").execute()
        
        # Assert we pulled real data.
        if len(data.data) < 1:
            return []
        
        array = [element['no_certificate'] for element in data.data]
        
        print(array)
        return array

    def insert_manifiesto(self, data, embarque, temp=0):
        noCertificate = data['no_certificate']
        print(f"Embarque: {embarque}")
        
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
        print(f"Embarque: {embarque}")
        
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
    
    
        
        
if __name__ == "__main__":
    test = SupabaseDataLayer()
    test.get_resumen(4379065)



