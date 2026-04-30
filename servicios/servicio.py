from datetime import datetime, timedelta #sirve para importar las clases necesarias para gestionar fechas, horas y realizar cálculos temporales.

#La clase Servicio actúa como un molde
#Sirve para que todas las clases hijas tengan estos métodos
class Servicio:
    def describir(self):
        pass

    def calcular_costo(self, *args):
        pass



class ServicioReservaSalas(Servicio): #ServicioReservaSalas es una subclase que hereda todas las propiedades y métodos de la clase Servicio
                                      # # Esta clase maneja las reservas de salas
    def __init__(self, salas): # Guarda la lista de las salas 
        self.salas = salas
        self.ocupadas = set()   # Guarda qué salas ya están ocupadas (id, fecha)

    def describir(self): # Inicializa una cadena de texto con el encabezado
        texto = "Salas:\n" # Recorre la lista de salas almacenadas en el objeto
        for s in self.salas:# junta  el ID, nombre y precio por hora de cada sala al texto
            texto += f"{s['id']} - {s['nombre']} - ${s['precio_hora']}/hora\n" #devuelve el resumen completo 
        return texto

    def calcular_costo(self, id_sala, fecha, horas): # calcula los costos de la reserva de una sala 
        for s in self.salas:
            if s["id"] == id_sala: # realiza una busqueda de la sala por su id

                if (id_sala, fecha) in self.ocupadas: # verifica si la sala esta disponible para esas fechas 
                    raise ValueError("Sala ocupada")

                costo = s["precio_hora"] * horas  # Calcula el costo (precio por hora * horas)
                self.ocupadas.add((id_sala, fecha))  # Guarda la reserva como ocupada
                return costo  # Devuelve el costo total

        raise ValueError("Sala no existe")




class ServicioAlquilerEquipos(Servicio): #sub calse de servicios que maneja el alquiler de los equipos

    def __init__(self, equipos): # guarda el listado de equipos
        self.equipos = equipos
        self.alquileres = {} #guarda los alquileres realizados (id_equipo, fecha) 

    def describir(self):#muestra el listado de equipos disponibles para alquilar, con su ID, nombre y precio por día
        texto = "Equipos:\n"
        for e in self.equipos:
            texto += f"{e['id']} - {e['nombre']} - ${e['precio_dia']}/día\n"
        return texto

    def calcular_costo(self, id_equipo, cantidad, fecha_inicio, dias):# calcula el costo del alquiler de un equipo, verificando su disponibilidad para las fechas solicitadas
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")#convierte la fecha de texto a un objeto datetime para facilitar los cálculos de fechas

        for e in self.equipos:#busca el equipo por su ID en la lista de equipos disponibles
            if e["id"] == id_equipo:

                for i in range(dias):# recorre  los dias de alquiler para verificar la disponibilidad del equipo
                    dia = (inicio + timedelta(days=i)).strftime("%Y-%m-%d")#calcula la fecha de cada día del alquiler sumando i días a la fecha de inicio 
                    usadas = self.alquileres.get((id_equipo, dia), 0)#consulta cuantos equipos ya están alquilados para ese día

                    if usadas + cantidad > e["unidades"]:#verifica si hay unidades disponibles 
                        raise ValueError("No disponible")#si la cantidad solicitada más las unidades ya alquiladas excede el total de unidades disponibles, se lanza un error indicando que no hay disponibilidad

                for i in range(dias):#guarda el alquiler dia por dia
                    dia = (inicio + timedelta(days=i)).strftime("%Y-%m-%d")
                    self.alquileres[(id_equipo, dia)] = self.alquileres.get((id_equipo, dia), 0) + cantidad

                return e["precio_dia"] * dias * cantidad#calcula el costo total del alquiler multiplicando el precio por día del equipo, por la cantidad de días y por la cantidad de unidades alquiladas

        raise ValueError("Equipo no existe")#si no se encuentra el equipo por su ID, se lanza un error indicando que el equipo no existe




class ServicioAsesoria(Servicio):#sub clase de servicios que maneja las asesorías

    def __init__(self, temas):#guarda el listamos de los temas disponibles para asesoría, con su ID, nombre y precio por hora
        self.temas = temas

    def describir(self):#muestra el listado de temas disponibles para asesoría, con su ID, nombre y precio por hora
        texto = "Asesorías:\n"
        for t in self.temas:
            texto += f"{t['id']} - {t['nombre']} - ${t['precio_hora']}/hora\n"#devuelve el resumen completo de los temas disponibles para asesoría, con su ID, nombre y precio por hora
        return texto

    def calcular_costo(self, id_tema, horas):#calcula el costo de una asesoría, buscando el tema por su ID y multiplicando su precio por hora por la cantidad de horas solicitadas
        for t in self.temas:
            if t["id"] == id_tema:#realiza una busqueda del tema por su ID en la lista de temas disponibles
                return t["precio_hora"] * horas#calcula el costo de una asesoría, buscando el tema por su ID y multiplicando su precio por hora por la cantidad de horas solicitadas

        raise ValueError("Tema no existe")#si no se encuentra el tema por su ID, se lanza un error indicando que el tema no existe