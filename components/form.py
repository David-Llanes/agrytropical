import flet as ft
from data import get_supabase_instance

data = get_supabase_instance()


class CustomTextField(ft.TextField):
    def __init__(self, label: str, value: str):
      super().__init__(label=label, value=value, text_align=ft.TextAlign.LEFT, border_color="#00f4f4f4", border_radius=10, text_size=16, height=50, read_only=True, col=6, text_style=ft.TextStyle(weight="w500"))
        
    def build(self):
      return self

class Form(ft.UserControl):
    def __init__(self):
      super().__init__(expand=True)
    
      def close_anchor(e):
        selected = f"{e.control.data}"
        print(f"Se selecciono: {selected}")
        self.buscar.close_view(selected)
        

      def handle_change(e):
        print(f"handle_change e.data: {e.data}")
        # Filtrado de la lista


      def handle_submit(e):
        print(f"handle_submit e.data: {e.data}")
        if self.buscar.value:
          load_data()

      def handle_tap(e):
        print(f"handle_tap")
        
      
      # Campos del formulario
      self.buscar = ft.SearchBar(
        col=8,
        view_elevation=5,
        height=50,
        divider_color=ft.colors.GREEN_200,
        bar_hint_text="Buscar ...",
        view_hint_text="Selecciona un No. de Certificado ...",
        on_change=handle_change,
        on_submit=handle_submit,
        on_tap=handle_tap,
        autofocus=True,
        controls=[
            ft.ListTile(title=ft.Text(i), on_click=close_anchor, data=i)
            for i in data.get_manifiestos()
        ],
      )
      
      self.noCertificate = CustomTextField(label="No. Certificado", value="")
      self.NoEmbarque = CustomTextField(label="No. Embarque", value="")
      self.empaque = CustomTextField(label="Empaque", value="")
      self.fechaCarga = CustomTextField(label="Fecha de carga", value="")
      self.paisOrigen = CustomTextField(label="País de origen", value="")
      self.puertoSalida = CustomTextField(label="Puerto de salida", value="")
      self.puertoLlegada = CustomTextField(label="Puerto de llegada", value="")
      self.totalPallets = CustomTextField(label="Total de pallets", value="")
      
      self.searchBar = ft.TextField(
        label="Buscar",
        text_size=16,
        border_color="#44f4f4f4",
        border="none",
        suffix_icon=ft.icons.SEARCH,
      )
      
      # Función para cargar los datos
      def load_data():
        # Obtener la información del manifiesto
        info = data.get_info_manifiesto(self.buscar.value)
        
        if not info:
          self.update()
          return
        
        self.noCertificate.value = info['no_certificate']
        self.NoEmbarque.value = info['no_embarque']
        self.empaque.value = info['empaque']
        self.fechaCarga.value = info['fecha_carga']
        self.puertoSalida.value = info['export_port']
        self.puertoLlegada.value = info['entry_port']
        self.totalPallets.value = info['total_pallets']
        self.paisOrigen.value = "México"
        
        resumenData = data.get_resumen(self.buscar.value)
        if not resumenData:
          self.update()
          return
        # Obtener el resumen de la carga
        registros = []
        for i in resumenData:
          registros.append(ft.DataRow(
            cells=[
              ft.DataCell(ft.Text(i["id"])),
              ft.DataCell(ft.Text(i["no_certificate"])),
              ft.DataCell(ft.Text(i["marca_caja"])),
              ft.DataCell(ft.Text(i["calibre"])),
              ft.DataCell(ft.Text(i["variedad"])),
              ft.DataCell(ft.Text(i["cajas"])),
              ft.DataCell(ft.Text(i["calidad"])),
            ]
          ))
          
        self.dataTable.rows = registros
        self.update()
      
      # Tabla de datos
      self.dataTable = ft.DataTable(
        expand=True,
        columns= [
          ft.DataColumn(ft.Text('ID')),
          ft.DataColumn(ft.Text('No.Certificado')),
          ft.DataColumn(ft.Text('Marca de caja')),
          ft.DataColumn(ft.Text('Calibre')),
          ft.DataColumn(ft.Text('Variedad')),
          ft.DataColumn(ft.Text('Cajas')),
          ft.DataColumn(ft.Text('Calidad')),
        ],
      )
    
      
      # Formulario
      self.form = ft.Container(
        col=4,
        padding=20,
        bgcolor=ft.colors.GREEN_100,
        content=ft.Column(
          controls=[
              ft.ResponsiveRow(
                [self.buscar, ft.ElevatedButton("Cargar", col=4, height=50, elevation=5, on_click=handle_submit)]
              ), 
              ft.Column([
                ft.ResponsiveRow(
                [self.noCertificate, self.NoEmbarque]
              ), self.empaque, self.fechaCarga, self.paisOrigen, self.puertoSalida, self.puertoLlegada, self.totalPallets
              ])
            ], spacing=50
        )
      )
      # Tabla
      self.table = ft.Container(
        bgcolor=ft.colors.GREEN_50,
        col=8,
        padding=20,
        content=ft.Column([
          ft.Container(
            content=ft.Row(
              spacing=10,
              controls=[
                self.searchBar,
                ft.Container(
                  ft.Row([
                    ft.IconButton(
                      tooltip="Exportar a Excel",
                      icon=ft.icons.FILE_DOWNLOAD,
                      icon_color=ft.colors.GREEN_900
                    ),
                  ])
                )
              ]
            )
          ),
          # Tabla
          ft.Column(
            expand=True, 
            scroll="auto",
            controls=[self.dataTable],
          )
        ], scroll="auto", spacing=16) # Puedo quitar estas props
      )
      
      self.content = ft.ResponsiveRow(controls=[self.form, self.table], spacing=0)
      
    def build(self):
      return self.content
