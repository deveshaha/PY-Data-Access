##Escribe un programa en Python para la gestión de un Polideportivo cuyos clientes pueden matricularse en varios deportes. La aplicación creada se conectará con una base de datos Postgres para guardar y consultar los datos. 

import sys
import psycopg2
import re

from Cliente import Clientes

conx = None
conx = psycopg2.connect("dbname=postgres user=postgres password=postgres")


def ddbb_connection():
    # Conexión a la base de datos en Postgresql 
    print()  
    print("PRUEBA DE CONEXIÓN A POSTGRES Y VERSIÓN DE LA BASE DE DATOS")  
    print()  

    conx = psycopg2.connect("dbname=postgres user=postgres password=postgres") 
    cur = conx.cursor()

    print("Conexión a la Base de Datos Postgres")  
    
    try: 
        conx 
        print("Estableciendo conexión a la base de datos ...")  
        cur 
        print ("Conectado!\n")  
        cur.execute('select version()')  
        version = cur.fetchone()  
        print ("versión de PostgreSQL\n", version)  
    
    except:  
        print ("No se puede conectar con la Base de Datos") 

    finally:
        if conx is not None:
            conx.close()
            print("Conexión cerrada")

    return cur, conx

def costumer_table_creation():

    cur = conx.cursor()

    try:
        #cur.execute("DROP TABLE IF EXISTS clientes")
        cur.execute("CREATE TABLE IF NOT EXISTS clientes (id SERIAL PRIMARY KEY, dni VARCHAR(9) UNIQUE NOT NULL, nombre VARCHAR(50) NOT NULL, fecha_nacimiento DATE NOT NULL, telefono VARCHAR(9) NOT NULL)")
        conx.commit()
        print("Tabla clientes creada correctamente")
        print()

    except:
        print("Error: No se ha podido crear la tabla clientes")
        print("Error: ", sys.exc_info()[1])

def add_client():

    cur = conx.cursor()

    dni = input("Introduce el dni del cliente: ")
    try:
        if re.match("^[0-9]{8,8}[A-Za-z]$", dni):
            cur.execute("SELECT * FROM clientes WHERE dni = %s", (dni,))
            if cur.fetchone() != None:
                print("Error: El cliente ya existe")
        else:
            print("Error: El dni no es válido")
            add_client()
    except:
        print("Error: No se ha podido dar de alta al cliente")
        #Print the error
        print("Error: ", sys.exc_info()[1])

    nombre = input("Introduce el nombre del cliente: ")
    telefono = input("Introduce el telefono del cliente: ")
    try:
        if re.match("^[0-9]{9,9}$", telefono):
            cur.execute("SELECT * FROM clientes WHERE telefono = %s", (telefono,))
            if cur.fetchone() != None:
                print("Error: El cliente ya existe")
    except:
        print("Error: No se ha podido dar de alta al cliente")

    fecha_nacimiento = input("Introduce la fecha de nacimiento del cliente: ")
    # try:
    #     ##check if matches regex yyyy-mm-dd
    #     if not re.match("^(0\\d|1[012])/([012]\\d|3[01])/\\d{4}$", fecha_nacimiento):
    #         print("Error: La fecha de nacimiento no es válida")
    #         add_client()
    # except:
    #     print("Error: No se ha podido dar de alta al cliente")
    #     #Print the error
    #     print("Error: ", sys.exc_info()[1])

    try:
        cur.execute("INSERT INTO clientes (dni, nombre, fecha_nacimiento, telefono) VALUES (%s, %s, %s, %s)", (dni, nombre, fecha_nacimiento, telefono))
        conx.commit()
        print("Cliente dado de alta correctamente")
    except:
        print("Error: No se ha podido dar de alta al cliente")
        #Print the error
        print("Error: ", sys.exc_info()[1])

def delete_client():
    cur = conx.cursor()
    try:
        dni = input("Introduce el dni del cliente: ")
        cur.execute("DELETE FROM clientes WHERE dni = %s", (dni,))
        conx.commit()

    except:
        print("Error: No se ha podido dar de baja al cliente")

def show_client():
    cur = conx.cursor()
    try:
        dni = input("Introduce el dni del cliente: ")
        # execute the query: example SELECT * FROM clientes WHERE dni = '20608949Y'
        query = "SELECT dni, nombre, fecha_nacimiento, telefono FROM clientes WHERE dni = %s"
        cur.execute(query, (dni,))
        cliente = cur.fetchone()
        print()
        if cliente == None:
            print("El cliente no existe")
        else:
            objCliente = Clientes(cliente[0], cliente[1], cliente[2], cliente[3])
            print("Datos del cliente:")
            print()
            print(objCliente.__datos__())

    except:
        print("Error: No se ha podido mostrar los datos del cliente")
        print("Error: ", sys.exc_info()[1])

def show_all_clients():
    cur = conx.cursor()
    try:    
        cur.execute("SELECT * FROM clientes")
        print()
        print("Datos del cliente")
        print()
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row[0], row[1], row[2], row[3], row[4])
        print()
    except:
        print("Error: No se ha podido mostrar los datos de los clientes")
        print("Error: ", sys.exc_info()[1])

def sport_table_creation():
    cur = conx.cursor()
    try:
        #cur.execute("DROP TABLE IF EXISTS deportes")
        query = "CREATE TABLE IF NOT EXISTS deportes (id SERIAL PRIMARY KEY, nombre VARCHAR(50) UNIQUE NOT NULL, precio INTEGER NOT NULL)"
        cur.execute(query)
        conx.commit()
        print("Tabla deportes creada correctamente")
        print()

    except:
        print("Error: No se ha podido crear la tabla deportes")
        print("Error: ", sys.exc_info()[1])

def add_sport():
    #Los deportes que ofrece el polideportivo son:  tenis, natación, atletismo, baloncesto y futbol. 

    cur = conx.cursor()

    print("Refreshing table deportes...")
    print()
    try:
        cur.execute("DELETE FROM deportes")
        conx.commit()
        print("Refreshing table deportes completed")
        print()
    except:
        print("Error: Refreshing table deportes failed")
        #Print the error
        print("Error: ", sys.exc_info()[1])


    try:
        cur.execute("INSERT INTO deportes (nombre, precio) VALUES (%s, %s)", ("tenis", 10))
        cur.execute("INSERT INTO deportes (nombre, precio) VALUES (%s, %s)", ("natación", 15))
        cur.execute("INSERT INTO deportes (nombre, precio) VALUES (%s, %s)", ("atletismo", 20))
        cur.execute("INSERT INTO deportes (nombre, precio) VALUES (%s, %s)", ("baloncesto", 25))
        cur.execute("INSERT INTO deportes (nombre, precio) VALUES (%s, %s)", ("futbol", 30))
        conx.commit()
        print("Deportes añadidos correctamente")
    except:
        print("Error: No se ha podido añadir los deportes")
        #Print the error
        print("Error: ", sys.exc_info()[1])

def client_sport_table_creation():

    cur = conx.cursor()

    try:
        #cur.execute("DROP TABLE IF EXISTS clientes_deportes")
        #this table will get dni from clientes and name form deportes, also will have a horario field
        query = "CREATE TABLE IF NOT EXISTS clientes_deportes (id SERIAL PRIMARY KEY, dni VARCHAR(9) NOT NULL, nombre VARCHAR(50) NOT NULL, horario VARCHAR(50) NOT NULL, FOREIGN KEY (dni) REFERENCES clientes(dni), FOREIGN KEY (nombre) REFERENCES deportes(nombre))"
        cur.execute(query)
        conx.commit()
        print("Tabla clientes_deportes creada correctamente")
        print()

    except:
        print("Error: No se ha podido crear la tabla clientes_deportes")
        print("Error: ", sys.exc_info()[1])

def add_client_sport():
    cur = conx.cursor()
    try:
        dni = input("Introduce el dni del cliente: ")
        cur.execute("SELECT * FROM clientes WHERE dni = %s", (dni,))
        if cur.fetchone() == None:
            print("Error: El cliente no existe")
            add_client_sport()
        else:
            nombre = input("Introduce el nombre del deporte: ")
            cur.execute("SELECT * FROM deportes WHERE nombre = %s", (nombre,))
            if cur.fetchone() == None:
                print("Error: El deporte no existe")
                add_client_sport()
            else:
                horario = input("Introduce el horario del deporte: ")
                try:
                    if re.match("^[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}$", horario):
                        cur.execute("SELECT * FROM clientes_deportes WHERE dni = %s AND nombre = %s", (dni, nombre))
                        if cur.fetchone() != None:
                            print("Error: El cliente ya esta matriculado en ese deporte")
                        else:
                            cur.execute("INSERT INTO clientes_deportes (dni, nombre, horario) VALUES (%s, %s, %s)", (dni, nombre, horario))
                            conx.commit()
                            print("Cliente matriculado correctamente")
                    else:
                        print("Error: El horario no es válido")
                        add_client_sport()
                except:
                    print("Error: No se ha podido matricular al cliente")
                    #Print the error
                    print("Error: ", sys.exc_info()[1])
    except:
        print("Error: No se ha podido matricular al cliente")
        #Print the error
        print("Error: ", sys.exc_info()[1])

ddbb_connection()
costumer_table_creation()
sport_table_creation()
add_sport()
client_sport_table_creation()

usr = int(input("Selecciona una opcion \n 1. Dar de alta un cliente con sus datos personales \n 2. Dar de baja un cliente \n 3. Mostrar los datos personales de un cliente o de todos \n 4. Matricular a un cliente en un deporte \n 5. Desmatricular a un cliente en un deporte \n 6. Mostrar los deportes de un cliente \n 7. Salir \n"))
    
match usr: 

    case 1:
        print("Dar de alta un cliente con sus datos personales \n")
        add_client()

    case 2:
        print("Dar de baja a un cliente \n")
        delete_client()

    case 3:
        print("Mostrar los datos personales de un cliente o todos \n")

        case = int(input("Selecciona una opcion \n 1. Mostrar los datos de un cliente \n 2. Mostrar los datos de todos los clientes \n"))

        match case:
            case 1:
                show_client()
            case 2:
                show_all_clients()
                #go back to main menu
                #usr = int(input("Selecciona una opcion \n 1. Dar de alta un cliente con sus datos personales \n 2. Dar de baja un cliente \n 3. Mostrar los datos personales de un cliente o de todos \n 4. Matricular a un cliente en un deporte \n 5. Desmatricular a un cliente en un deporte \n 6. Mostrar los deportes de un cliente \n 7. Salir \n"))
            case _:
                print("El número introducido no es válido")

    case 4:
        ##Ejercicio 4
        print("Matricular a un cliente en un deporte \n")
        register_client_sport()



    case 5:
        ##Ejercicio 5
        print("Ejercicio 5: \n")

    case 6:
        ##Ejercicio 6
        print("Ejercicio 6: \n")

    case 7:
        print("Saliendo del programa")
        conx.close()
        exit()
        
    case _:
        print("El número introducido no es válido")




