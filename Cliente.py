from dataclasses import dataclass

@dataclass
class Clientes:
    dni: str
    nombre: str
    fecha_nacimiento: str
    telefono: str
    #deportes: list

    def __datos__(self):
        print(f"""
        Nombre: {self.nombre}
        DNI: {self.dni}
        Fecha de nacimiento: {self.fecha_nacimiento}
        Teléfono: {self.telefono}
        """)

    def __deportes__(self):
        print(f"""
        Deportes: {self.deportes}
        """)