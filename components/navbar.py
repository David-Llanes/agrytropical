import flet as ft

class Navbar(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.btnLogout = ft.IconButton(
          icon=ft.icons.LOGOUT,
          icon_color="red500",
          icon_size=20,
          tooltip="Cerrar sesión",
        )
    
    def logout(self, e: ft.ControlEvent):
      self.page.go('/')
      # lo de abajo no se si funciona xd lo hizo copiot
      self.page.views.clear()
      self.page.update()
    
    def build(self):
        self.btnLogout.on_click = self.logout
        
        return ft.Container(
            ft.Row([
              ft.Container(
                ft.Row([
                  ft.Row([ft.Image(src="assets/logo.webp", width=30, height=30),
                  ft.Text("Agrytropical Supply", weight="w700", size="12")], spacing=10),
                ])
              ),
              self.btnLogout
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
          padding=10,
        )