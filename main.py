import flet as ft
from components.login import Login
from components.navbar import Navbar
from components.home import Home
from components.form import Form
from components.formRegistrar import FormRegistro
from data import get_supabase_instance

# Obtiene la instancia de Supabase
data = get_supabase_instance()

def main(page: ft.Page) -> None:
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.theme = ft.theme.Theme(color_scheme_seed="green")
    page.theme_mode = ft.ThemeMode.LIGHT
    page.title = "Agrytropical Supply"
    page.window_resizable = False
    page.padding = 0
    
    
    t = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        
        tabs=[
            ft.Tab(
                tab_content=ft.Row([ft.Image(src="assets/logo.webp", width=30, height=30), ft.Text("Agrytropical Supply", weight="w700", size="12")], spacing=10),
                adaptive=True,
                icon=ft.icons.HOME,
                content=Home(),
            ),
            ft.Tab(
                text="Consultar",
                icon=ft.icons.SEARCH,
                content=Form(),
            ),
            ft.Tab(
                text="Registrar",
                icon=ft.icons.ADD,
                content=FormRegistro(page),
            ),
        ],
        expand=1,        
    )
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [Login(page)],
                padding=0
            )
        )
        if page.route == "/home":
            page.views.append(
                ft.View(
                    "/home",
                    [t], padding=0 #[Navbar(page), t]
                )
            )
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    

if __name__ == "__main__":
    ft.app(main)