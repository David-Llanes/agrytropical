import datetime
import flet as ft
from data import get_supabase_instance

data = get_supabase_instance()


class CustomTextField(ft.TextField):
    def __init__(self, label: str, value: str, read_only=False, disabled=True):
      super().__init__(label=label, value=value, read_only=read_only,text_align=ft.TextAlign.LEFT, border_color=ft.colors.GREEN_200, border_radius=10, text_size=16, height=50, col=6, text_style=ft.TextStyle(weight="w500"), disabled=disabled)
        
    def build(self):
      return self

class FormRegistro(ft.UserControl):
    def __init__(self, page: ft.Page):
      super().__init__(expand=True)
    
      # Buscar manifiesto
      def close_anchor(e):
        selected = f"{e.control.data}"
        print(f"Se selecciono: {selected}")
        self.buscar.close_view(selected)
      
      # Agregar nuevo registro a la tabla resumen 
      def agregarNuevoRegistro(e):
        if all([self.noCertificate.value, self.calidad.value, self.calibre.value, self.variedad.value, self.noCajas.value]):
          noCertificate = int(self.noCertificate.value)
          calidad = str(self.calidad.value).upper()
          calibre = int(self.calibre.value)
          variedad = str(self.variedad.value).upper()
          cajas = int(self.noCajas.value)
          marcaCaja = str(self.marcaCaja.value).upper()
        
          newRegistro = {
            "no_certificate": noCertificate,
            "calidad": calidad,
            "calibre": calibre,
            "variedad": variedad,
            "cajas": cajas,
            "marca_caja": marcaCaja
          } 

          try:
            result = data.insert_resumen(newRegistro)
            print(f"Data: {result}")
            
            self.load_table(noCertificate)  
          except Exception as e:
            print("Error al insertar el resumen de la carga")
            print(e)
          
          self.addDialog.open = False
        else:
          print("Faltan campos por llenar")
          
        #Limpia los campos del formulario       
        self.limpiarFormularioRegistro()
        
        
        page.update()
        
      def seleccionarCertificado(e):
        self.selectDialog.open = False
        
        editData = data.get_info_manifiesto(self.buscar.value)
        
        if not editData:
          return
        
        # Si hay datos, llenar los campos para editarse
        # Limpiar la tabla
        self.dataTable.rows = []
        self.addRow.disabled = False
        self.noCertificate.read_only = True
        self.editarRegistroExistente(editData)
        page.update()
        
        
      def close_modal(e):
        self.selectDialog.open = False
        self.addDialog.open = False
        self.limpiarFormularioRegistro()
        page.update()
        
      def open_dlg_modal_edit(e):
        page.dialog = self.selectDialog
        self.selectDialog.open = True
        page.update()
        
      def open_dlg_modal_add(e):
        if self.noCertificate.value == "":
          return
        if self.state == None:
          return
        
        page.dialog = self.addDialog
        self.addDialog.open = True
        page.update()

      # Campos del formulario
      self.buscar = ft.SearchBar(
        col=8,
        view_elevation=5,
        height=50,
        divider_color=ft.colors.GREEN_200,
        bar_hint_text="Buscar ...",
        view_hint_text="Selecciona un No. de Certificado ...",
        on_submit=seleccionarCertificado,
        autofocus=True,
        controls=[
            ft.ListTile(title=ft.Text(i), on_click=close_anchor, data=i)
            for i in data.get_manifiestos()
        ],
      )
      
      # Campos para cargar los registros en el modal
      self.variedad = ft.Dropdown(
        label="Variedad",
        options=[
          ft.dropdown.Option(text=i, data=i) for i in data.get_variedades()],
      )
      self.calibre = ft.Dropdown(
        label="Calibre",
        options=[ft.dropdown.Option(text=i, data=i) for i in [6,7,8,9,10,12,14,16,18]],
      )
      self.marcaCaja = ft.Dropdown(
        label="Marca de caja",
        options=[ft.dropdown.Option(text=i, data=i) for i in ["ARTESANAL", "WORLD DIRECT", "OTRA"]],
      )
      self.noCajas = CustomTextField(label="No. de cajas", value="", disabled=False)
      self.calidad = ft.Dropdown(
        label="Calidad",
        options=[ft.dropdown.Option(text=i, data=i) for i in ["ORGANICO", "ORGANICO-FT-USA", "PRIMERA"]],
      )
      
      self.addDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar un registro"),
        content=ft.Container(
          ft.Column([
          self.marcaCaja,
          self.calidad,
          self.variedad,
          self.calibre,
          self.noCajas,
        ]), width=400
        ),
        actions=[
          ft.TextButton("Cancelar", on_click=close_modal),
          ft.TextButton("Guardar", on_click=agregarNuevoRegistro)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
      )
      
      self.selectDialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Selecciona un No. de Certificado..."),
        content=ft.Column([
          self.buscar
        ]),
        actions=[
          ft.TextButton("Cancelar", on_click=close_modal),
          ft.TextButton("Seleccionar", on_click=seleccionarCertificado)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
      )
      
      # ESTADO 
      self.state = None
      
      # BOTONES SUPERIORES
      self.editarRegistro = ft.ElevatedButton("Editar existente", col=6, height=50, elevation=1, on_click=open_dlg_modal_edit, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
      self.nuevoRegistro = ft.ElevatedButton("Nuevo", col=6, height=50, elevation=1, on_click=self.agregarNuevoRegistro, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
      
      self.noCertificate = CustomTextField(label="No. Certificado", value="")
      # Y, M, D
      self.datePicker = ft.DatePicker(
        on_change=self.change_date,
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime(2040, 12, 31),
      )
      self.fechaCarga = ft.ElevatedButton(
        "Fecha de carga",
        icon=ft.icons.CALENDAR_MONTH,
        on_click=lambda _: self.datePicker.pick_date(),
        disabled=True,
      )
      self.txtFechaCarga = ft.Text()
      page.overlay.append(self.datePicker)
      
      self.puertoSalida = CustomTextField(label="Puerto de salida", value="")
      self.puertoLlegada = CustomTextField(label="Puerto de llegada", value="")
      self.temp = CustomTextField(label="Temperatura en °C", value="")
      self.totalPallets = CustomTextField(label="Total de pallets", value="")
      
      self.btnGuardar = ft.ElevatedButton("Guardar", height=50, disabled=True, col=12, elevation=1, on_click=self.guardarManifiesto, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
      
      self.searchBar = ft.TextField(
        label="Buscar",
        text_size=16,
        border_color="#44f4f4f4",
        border="none",
        suffix_icon=ft.icons.SEARCH,
      )
      
      # BOTON Q ABRE DIALOG PARA AGREGAR REGISTROS
      self.addRow = ft.ElevatedButton("Agregar registro", disabled=True, height=50, elevation=1, on_click=open_dlg_modal_add, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
      
      
      # Tabla de datos
      self.dataTable = ft.DataTable(
        expand=True,
        columns= [
          ft.DataColumn(ft.Text('ID')),
          ft.DataColumn(ft.Text('No.Certificado')),
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
                [self.editarRegistro, self.nuevoRegistro]
              ), 
              ft.Column([
                ft.ResponsiveRow(
                  [self.noCertificate]
                ), 
                ft.Row([self.fechaCarga, self.txtFechaCarga]),
                self.puertoSalida,
                self.puertoLlegada,
                self.temp,
                self.totalPallets,
                ft.Text(". . .",text_align="center", color=ft.colors.GREEN_100),
                ft.ResponsiveRow([self.btnGuardar]),
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
                    self.addRow,
                    ft.IconButton(
                      tooltip="Refrescar",
                      icon=ft.icons.REFRESH,
                      icon_color=ft.colors.GREEN_900
                    )
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
    
    def guardarManifiesto(self, e):
      
      if self.state == None:
        return
      
      # GUARDAR EN LA BASE DE DATOS EL MANIFIESTO
      embarque =  str(self.noCertificate.value)[-3:]
      empaque = str(self.noCertificate.value)[1:-3]
      temp = float(self.temp.value) if self.temp.value else 0
      
      newCertificado = {
        "no_certificate": int(self.noCertificate.value),
        "export_port": self.puertoSalida.value,
        "entry_port": self.puertoLlegada.value,
        "empaque": empaque,
        "fecha_carga": self.datePicker.value.date().isoformat(),
        "total_pallets": int(self.totalPallets.value),
      } 
      
      # Insertar el manifiesto como NUEVO
      if self.state == 0:
        try:
          result = data.insert_manifiesto(newCertificado, embarque, temp)
          print(f"Data: {result}")
          self.state = 1
          self.addRow.disabled = False
            
        except Exception as e:
          print("Error al insertar el manifiesto")
          print(e)
        
      # Editar un manifiesto existente
      if self.state == 1:
        try:
          result = data.modify_manifiesto(newCertificado, embarque, temp)
          print(f"Data: {result}")
          self.state = 1
          self.addRow.disabled = False
            
        except Exception as e:
          print("Error al insertar el manifiesto")
          print(e)
        
      
      self.update()
        
    
    def clearForm(self):
      self.noCertificate.value = ""
      self.txtFechaCarga.value = ""
      self.puertoSalida.value = ""
      self.puertoLlegada.value = ""
      self.totalPallets.value = ""
      self.noCertificate.disabled = True
      self.datePicker.value = datetime.datetime.now()
      self.fechaCarga.disabled = True
      self.puertoSalida.disabled = True
      self.puertoLlegada.disabled = True
      self.temp.value = ""
      self.temp.disabled = True
      self.totalPallets.disabled = True
      self.btnGuardar.disabled = True
      
      self.dataTable.rows = []
      self.limpiaFormularioRegistro()
      
      # Reiniciar el estado
      self.state = None
      self.update()
      
      
    def agregarNuevoRegistro(self, e):
      print("Agregar nuevo registro")
      self.noCertificate.value = ""
      self.noCertificate.disabled = False
      self.noCertificate.read_only = False
      self.fechaCarga.disabled = False
      self.datePicker.value = datetime.datetime.now()
      self.txtFechaCarga.value = ""
      self.puertoSalida.value = ""
      self.puertoSalida.disabled = False
      self.puertoLlegada.value = ""
      self.puertoLlegada.disabled = False
      self.temp.value = ""
      self.temp.disabled = False
      self.totalPallets.value = ""
      self.totalPallets.disabled = False
      self.btnGuardar.disabled = True
      
      self.dataTable.rows = []
      
      # 0 si se guarda un nuevo registro
      self.state = 0
      self.addRow.disabled = True
      self.update()
      
      
    def editarRegistroExistente(self, data):
      print("Editar registro existente")
      self.noCertificate.value = data['no_certificate']
      self.noCertificate.disabled = False
      self.noCertificate.read_only = True
      self.datePicker.value = data['fecha_carga']
      self.fechaCarga.disabled = False
      self.txtFechaCarga.value = f"A/M/D: {data['fecha_carga']}"
      self.puertoSalida.value = data['export_port']
      self.puertoSalida.disabled = False
      self.puertoLlegada.value = data['entry_port']
      self.puertoLlegada.disabled = False
      self.temp.value = data['temp']
      self.temp.disabled = False
      self.totalPallets.value = data['total_pallets']
      self.totalPallets.disabled = False
      self.btnGuardar.disabled = False
      
      # self.table.rows = []
      self.load_table(data['no_certificate'])
      
      # 1 si se edita un registro existente
      self.state = 1
      self.update()
      
    def limpiarFormularioRegistro(self):
      self.variedad.value = ""
      self.calibre.value = ""
      self.marcaCaja.value = ""
      self.noCajas.value = ""
      self.calidad.value = ""
      self.update()
      
    # DATE PICKER
    def change_date(self, e):
      print(f"Date picker changed, value is {self.datePicker.value}")
      self.txtFechaCarga.value = f"A/M/D: {self.datePicker.value.date()}"
      self.update()
      
    def validate(self, e: ft.ControlEvent):
      if all([self.noCertificate.value, self.datePicker.value, self.puertoSalida.value, self.puertoLlegada.value, self.totalPallets.value, self.temp.value]):
          self.btnGuardar.disabled = False
      else:
          self.btnGuardar.disabled = True
      self.update()
      

    # Función para cargar los datos
    def load_table(self, noCertificate):
      # Obtener la información del manifiesto
      resumenData = data.get_resumen(noCertificate)
      
      if not resumenData:
        return
      
      # Obtener el resumen de la carga
      registros = []
      for i in resumenData:
        registros.append(ft.DataRow(
          cells=[
            ft.DataCell(ft.Text(i["id"])),
            ft.DataCell(ft.Text(i["no_certificate"])),
            ft.DataCell(ft.Text(i["calibre"])),
            ft.DataCell(ft.Text(i["variedad"])),
            ft.DataCell(ft.Text(i["cajas"])),
            ft.DataCell(ft.Text(i["calidad"])),
          ]
        ))
      
      self.dataTable.rows = None
      self.dataTable.rows = registros
      self.dataTable.update()
      self.update()
    
    def build(self):
      self.noCertificate.on_change = self.validate
      self.datePicker.on_change = self.validate
      self.puertoSalida.on_change = self.validate
      self.puertoLlegada.on_change = self.validate
      self.totalPallets.on_change = self.validate
      self.temp.on_change = self.validate
      return self.content
