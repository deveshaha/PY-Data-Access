##Escribe un programa en Python para la gestión de un Polideportivo cuyos clientes pueden matricularse en varios deportes. La aplicación creada se conectará con una base de datos Postgres para guardar y consultar los datos. 

import sys
import psycopg2
import re

conx = psycopg2.connect("dbname=postgres user=postgres password=postgres") 
cur = conx.cursor()

def ddbb_connection():
    # Conexión a la base de datos en Postgresql 
    print()  
    print("PRUEBA DE CONEXIÓN A POSTGRES Y VERSIÓN DE LA BASE DE DATOS")  
    print()  
 
    conx = None
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
    try:
        #cur.execute("DROP TABLE IF EXISTS clientes")
        cur.execute("CREATE TABLE clientes (id SERIAL PRIMARY KEY, dni VARCHAR(9) UNIQUE NOT NULL, nombre VARCHAR(50) NOT NULL, fecha_nacimiento DATE NOT NULL, telefono VARCHAR(9) NOT NULL)")
        conx.commit()
        print("Tabla clientes creada correctamente")
        print()

    except:
        print("Error: No se ha podido crear la tabla clientes")
        print("Error: ", sys.exc_info()[1])

def add_client():
    #get conx and cur data from ddbb_connection()

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
    try:
        dni = input("Introduce el dni del cliente: ")
        cur.execute("DELETE FROM clientes WHERE dni = %s", (dni,))
        conx.commit()

    except:
        print("Error: No se ha podido dar de baja al cliente")

def show_client():
    try:
        dni = input("Introduce el dni del cliente: ")
        # execute the query: example SELECT * FROM clientes WHERE dni = '20608949Y'
        # TODO
        query = "SELECT * FROM clientes WHERE dni = %s"
        cur.execute(query, (dni,))
        print()
    except:
        print("Error: No se ha podido mostrar los datos del cliente")
        print("Error: ", sys.exc_info()[1])

def show_all_clients():
    try:    
        cur.execute("SELECT * FROM clientes")
        print()
        print("Datos de los clientes")
        print()
        while True:
            row = cur.fetchone()
            if row == None:
                break
            print(row)
        print()
    except:
        print("Error: No se ha podido mostrar los datos de los clientes")

def sport_table_creation():
    try:
        #cur.execute("DROP TABLE IF EXISTS deportes")
        cur.execute("CREATE TABLE deportes (nombre VARCHAR(50) NOT NULL, precio INTEGER NOT NULL)")
        conx.commit()
        print("Tabla deportes creada correctamente")
        print()

    except:
        print("Error: No se ha podido crear la tabla deportes")
        print("Error: ", sys.exc_info()[1])

def add_sport():
    #Los deportes que ofrece el polideportivo son:  tenis, natación, atletismo, baloncesto y futbol. 
    #check if sport exists
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

ddbb_connection()
costumer_table_creation()
sport_table_creation()
add_sport()

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




