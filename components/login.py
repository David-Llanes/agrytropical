import flet as ft
from data import get_supabase_instance

data = get_supabase_instance()

class Login(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        # Usuario
        self.txtUsername = ft.TextField(label="Usuario", text_align=ft.TextAlign.LEFT, border_color="green10", border_radius=10, text_size=15, height=55, autofocus=True, icon=ft.icons.PEOPLE)
        # Contraseña
        self.txtPassword = ft.TextField(label="Contraseña",password=True, text_align=ft.TextAlign.LEFT, border_color="green10", border_radius=10, text_size=15, height=55, icon=ft.icons.LOCK)
        # Botón de inicio de sesión
        self.btnLogin = ft.ElevatedButton("Ingresar", width=320, height=45, elevation=2, disabled=True, bgcolor="#041838", color="white", style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
   


    def validate(self, e: ft.ControlEvent):
        if all([self.txtUsername.value, self.txtPassword.value]):
            self.btnLogin.disabled = False
            # self.page.go('/home')
        else:
            self.btnLogin.disabled = True

        self.update()

    def submit(self, e: ft.ControlEvent):
        print(f"Usuario: {self.txtUsername.value}")
        print(f"Contraseña: {self.txtPassword.value}")
        
        try:
            # Autenticar al usuario
            user = data.authenticate(self.txtUsername.value, self.txtPassword.value)
            if user:
                print(f"Usuario autenticado: {user}")
                self.page.go('/home') # Redireccionar a la página de inicio
                
                self.clean()
                
            else:
                print("No se encontró el usuario.")
        except Exception as e:
            print(f"Error: {e}")

    def build(self):
        self.txtUsername.on_change = self.validate
        self.txtPassword.on_change = self.validate
        self.btnLogin.on_click = self.submit

        return ft.Container(
            ft.Stack([
                ft.Image(src='assets/bg.jpg'),
                ft.Container(
                    ft.Container(
                        ft.Column(
                            [
                                ft.Column([
                                    ft.Row([ft.Image(src="assets/logo.webp", width=70, height=70),
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        ft.Text("AGRYTROPICAL SUPPY", color="black", weight="w700", size="24", text_align="center",)
                                    ], alignment=ft.MainAxisAlignment.CENTER),
                                ]),
                                self.txtUsername,
                                self.txtPassword,
                                ft.Row([
                                    ft.Checkbox(label="Recordar usuario", value=False, on_change=self.validate),
                                    ft.Text("¿Olvidaste tu contraseña?", color="black", size=12, weight="w500", text_align="right")
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                self.btnLogin,
                                ft.Row([
                                    ft.Text("¿No tienes una cuenta?", size=12, text_align="left"),
                                    ft.Text("Créala aquí", color="black", size=12, weight="w500", text_align="right")
                                ], alignment=ft.MainAxisAlignment.CENTER, spacing=5),
                            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20
                        ),
                        width=400,
                        height=510, 
                        blur=ft.Blur(12,12,ft.BlurTileMode.CLAMP), 
                        border_radius=10, 
                        border=ft.border.all(1, "#44f4f4f4"), 
                        bgcolor="#ddffffff", padding=40,
                    ), 
                    margin=ft.margin.only(top=80),
                    alignment=ft.alignment.center,
                )
            ])
        )