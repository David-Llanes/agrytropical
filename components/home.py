import flet as ft
from data import get_supabase_instance

data = get_supabase_instance()


class CustomTextField(ft.TextField):
    def __init__(self, label: str, value: str, read_only=False, disabled=True):
      super().__init__(label=label, value=value, read_only=read_only,text_align=ft.TextAlign.LEFT, border_color=ft.colors.GREEN_200, border_radius=10, text_size=16, height=50, col=6, text_style=ft.TextStyle(weight="w500"), disabled=disabled)
        
    def build(self):
      return self

class Home(ft.UserControl):
    def __init__(self):
      super().__init__(expand=True)
      
      def close_anchor(e):
        selected = f"{e.control.data}"
        print(f"Se selecciono: {selected}")
        self.buscar.close_view(selected)
        
      def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")
        if self.buscar.value:
          self.btnLimpiar.disabled = False
          self.load_data()


      def handle_tap(e):
        print(f"handle_tap")
      
      
      self.resumenCostos = {}
      
      # Campos del formulario
      self.buscar = ft.SearchBar(
        col=8,
        view_elevation=5,
        height=50,
        divider_color=ft.colors.GREEN_200,
        bar_hint_text="Buscar ...",
        view_hint_text="Selecciona un No. de Certificado ...",
        on_submit=handle_submit,
        on_tap=handle_tap,
        autofocus=True,
        controls=[
            ft.ListTile(title=ft.Text(i), on_click=close_anchor, data=i)
            for i in data.get_manifiestos()
        ],
      )
      
      self.btnCargar = ft.ElevatedButton("Cargar", col=4, height=50, elevation=5, on_click=handle_submit)
      
      self.noCertificate = CustomTextField(label="No. Certificado", read_only=True, value="")
      self.fechaCarga = CustomTextField(label="Fecha de carga a/m/d", read_only=True, value="")
      self.tipoCambio = CustomTextField(label="Tipo de cambio", read_only=True, value="")
      
      self.btnLimpiar = ft.ElevatedButton("Limpiar campos", col=12, height=50, elevation=1, disabled=True, on_click=self.handle_reset, icon=ft.icons.CLEAR, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
      
      self.exportExcel = ft.IconButton(
        tooltip="Exportar a Excel",
        on_click=self.handle_export_excel,
        icon=ft.icons.FILE_DOWNLOAD,
        icon_color=ft.colors.GREEN_900
      )
    
      # Tabla de datos
      self.dataTable = ft.DataTable(
        height=250,
        columns= [
          ft.DataColumn(ft.Text('Variedad')),
          ft.DataColumn(ft.Text('Calibre')),
          ft.DataColumn(ft.Text('Cajas')),
          ft.DataColumn(ft.Text('Precio/caja')),
          ft.DataColumn(ft.Text('Total USD')),
          ft.DataColumn(ft.Text('Total MXN')),
        ],
        data_text_style=ft.TextStyle(size=11, weight="w500"),
        heading_text_style=ft.TextStyle(size=12, weight="w500", color=ft.colors.GREEN_900),
      )
      
      self.costosVariedadTable = ft.DataTable(
        columns= [
          ft.DataColumn(ft.Text('Variedad')),
          ft.DataColumn(ft.Text('Cajas')),
          ft.DataColumn(ft.Text('Precio/caja')),
          ft.DataColumn(ft.Text('Total USD')),
          ft.DataColumn(ft.Text('Total MXN')),
        ],
        data_text_style=ft.TextStyle(size=11, weight="w500"),
        heading_text_style=ft.TextStyle(size=12, weight="w500", color=ft.colors.GREEN_900),
      )
    
      
      self.costoTotalUSD = CustomTextField(label="Costo total en USD", read_only=True, value="")
      self.costoTotalMXN = CustomTextField(label="Costo total en MXN", read_only=True, value="")
      
      # Formulario
      self.form = ft.Container(
        col=4,
        padding=20,
        bgcolor=ft.colors.GREEN_100,
        content=ft.Column(
          controls=[
            ft.Column([
              ft.ResponsiveRow(
                [self.buscar, self.btnCargar]
              ), 
              ft.Column([self.noCertificate, self.fechaCarga, self.tipoCambio], spacing=15
              ),
              ft.ResponsiveRow(
                [self.btnLimpiar]
              )
            ], spacing=50)
          ]
        )
      )
      # Lado derecho
      self.table = ft.Container(
        bgcolor=ft.colors.GREEN_50,
        col=8,
        padding=20,
        content=ft.Column([
          ft.Container(
            height=300,
            content=ft.Column([
              ft.Row([ft.Text("Costos por variedad/calibre", weight="w500", size="10")]),
              ft.Row([self.dataTable])
            ], spacing=0),
          ),
          ft.Container(
            expand=True,
            content=ft.Column([
              ft.Row([ft.Text("Costos por variedad", weight="w500", size="10")]),
              ft.Row([self.costosVariedadTable])
            ], spacing=0),
          ),
          ft.Container(
            height=60,
            content=ft.Row([self.costoTotalUSD, self.costoTotalMXN, self.exportExcel], spacing=10),
          )
        ])
      )
      
      self.content = ft.ResponsiveRow(controls=[self.form, self.table], spacing=0)
    
    def handle_export_excel(self, e):
      print("Exportar a Excel")
      result = data.download_costos(int(self.noCertificate.value))
      
      if result:
        print(result)
    
    def handle_reset(self, e):
      self.resumenCostos = {}
      
      self.noCertificate.value = ""
      self.fechaCarga.value = ""
      self.tipoCambio.value = ""
      self.costoTotalUSD.value = ""
      self.costoTotalMXN.value = ""
      
      self.btnLimpiar.disabled = True
      self.noCertificate.disabled = True
      self.fechaCarga.disabled = True
      self.tipoCambio.disabled = True
      self.costoTotalUSD.disabled = True
      self.costoTotalMXN.disabled = True

      self.exportExcel.disabled = True
      self.dataTable.rows = []
      self.costosVariedadTable.rows = []
      self.update()
    
    def activar_campos(self):
      self.noCertificate.disabled = False
      self.fechaCarga.disabled = False
      self.tipoCambio.disabled = False
      self.costoTotalUSD.disabled = False
      self.costoTotalMXN.disabled = False
      self.exportExcel.disabled = False
      
    def load_data(self):
      self.activar_campos()
      # Obtener el resumen de la carga y costos
      self.resumenCostos = data.get_costos(self.buscar.value)
      
      if not self.resumenCostos:
        self.update()
        return
      
      self.noCertificate.value = self.resumenCostos['no_certificate']
      self.fechaCarga.value = self.resumenCostos['fecha_carga']
      self.tipoCambio.value = self.resumenCostos['tipo_cambio']
      self.costoTotalUSD.value = self.resumenCostos['costo_total_usd']
      self.costoTotalMXN.value = self.resumenCostos['costo_total_mxn']
      
      # Llenar la primera tabla
      registros = []
      for i in self.resumenCostos["costos"]:
        registros.append(ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(i["variedad"])),
            ft.DataCell(ft.Text(i["calibre"])),
            ft.DataCell(ft.Text(i["cajas"])),
            ft.DataCell(ft.Text(i["VariedadMango"]["precio"])),
            ft.DataCell(ft.Text(i["total_usd"])),
            ft.DataCell(ft.Text(i["total_mxn"])),
          ]
        ))
        
      # Llenar la segunda tabla
      registrosVariedad = []
      for i in self.resumenCostos["costosPorVariedad"]:
        registrosVariedad.append(ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(i)),
            ft.DataCell(ft.Text(self.resumenCostos["costosPorVariedad"][i]["cajas"])),
            ft.DataCell(ft.Text(self.resumenCostos["costosPorVariedad"][i]["precio"])),
            ft.DataCell(ft.Text(self.resumenCostos["costosPorVariedad"][i]["total_usd"])),
            ft.DataCell(ft.Text(self.resumenCostos["costosPorVariedad"][i]["total_mxn"])),
          ]
        ))
        
      self.dataTable.rows = registros
      self.costosVariedadTable.rows = registrosVariedad
      self.update()
      
      
    def build(self):
      return self.content
