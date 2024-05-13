import flet as ft
from data import get_supabase_instance

data = get_supabase_instance()


class CustomTextField(ft.TextField):
    def __init__(self, label: str, value: str):
      super().__init__(label=label, value=value, text_align=ft.TextAlign.LEFT, border_color="#00f4f4f4", border_radius=10, text_size=16, height=50, read_only=True, col=6, text_style=ft.TextStyle(weight="w500"))
        
    def build(self):
      return self

class Home(ft.UserControl):
    def __init__(self):
      super().__init__(expand=True)
      
      self.exportExcel = ft.IconButton(
                      tooltip="Exportar a Excel",
                      icon=ft.icons.FILE_DOWNLOAD,
                      icon_color=ft.colors.GREEN_900
                    )
    
      # Tabla de datos
      self.dataTable = ft.DataTable(
        expand=True,
        columns= [
          ft.DataColumn(ft.Text('Variedad')),
          ft.DataColumn(ft.Text('Total de cajas')),
          ft.DataColumn(ft.Text('Precio por caja')),
          ft.DataColumn(ft.Text('Tipo de cambio')),
          ft.DataColumn(ft.Text('Total USD')),
          ft.DataColumn(ft.Text('Total MXN')),
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
                [ft.ElevatedButton("Cargar", col=4, height=50, elevation=5)]
              ), 
              ft.Column([
                ft.ResponsiveRow(),
              ], spacing=50)]
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
                ft.Container(
                  ft.Row([
                    self.exportExcel,
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
        ], scroll="auto") # Puedo quitar estas props
      )
      
      self.content = ft.ResponsiveRow(controls=[self.form, self.table], spacing=0)
      
    def build(self):
      return self.content
