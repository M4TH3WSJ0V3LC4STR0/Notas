import sqlite3
from sqlite3 import Error

dbName = 'database.db'

# funcion que conecta a la base de datos ----------------------------------------------->


def get_db():
    try:
        conn = sqlite3.connect(dbName)
        print('Conectada a BDD')
        return conn
    except Error:
        print(Error)

# funcion que cierra la conexion a la base de datos -------------------------------------->


def close_db(conn):
    print('Cerrando conexion a BDD')
    conn.close()

# Modelo de la clase usuarios ------------------------------------------------------------>

# Buscar usuario en base de datos ------------------------------------------------------------>


def get_user_db(userid):
    conn= get_db()
    cursor= conn.execute("select * from Usuarios where username='"+userid+"';")
    resultSet= cursor.fetchone()
    close_db(conn)
    return resultSet


def get_user_by_id(userid):
    conn = get_db()
    cursor = conn.execute( "select * from Usuarios where id = {}".format(userid))
    resultSet = list(cursor.fetchall())
    close_db(conn)
    return resultSet

# Ingresar usuario a base de datos ------------------------------------------------------------>


def add_user_db(name, apellido, email, usuario, password, rol):
    try:
        conn = get_db()
        conn.execute("insert into Usuarios (name, apellido, email, username, password, roles) values(?,?,?,?,?,?);", (name, apellido, email, usuario, password, rol))
        conn.commit()
        close_db(conn)
        return True
    except Error as error:
        return False

# funcion que actualiza un usuario de base de datos --------------------------------------------------------------------->

def update_usuario(nombre, apellido, correo, nUsuario, clave, tipoUsuario, id):
    try:
        conn = get_db()
        
        conn.execute("UPDATE Usuarios SET name = ?, apellido = ?, email = ?, username = ?, password = ?, roles = ? WHERE id = ?", (nombre, apellido, correo, nUsuario, clave, tipoUsuario, id))
        conn.commit()

        conn.close()
    except Error as error:
        print(error)
        return False

# Ver todos los usuarios ------------------------------------------------------------>


def list_tabla_db():
    conn = get_db()
    cursor = conn.execute("select * from Usuarios")
    resultSet = cursor.fetchall()
    close_db(conn)
    return resultSet

# funcion que elimina un usuario de la base de datos dada su id --------------------------------------------------------------------->
def delete_usuario(id_usuario):
    try:
        conn=get_db()
        conn.execute("delete from Usuarios where id = {}".format(id_usuario))
        conn.commit()
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

# Modelo de la clase Materia --------------------------------------------------------------------->

# funcion que devuelve todas las materias de la base de datos --------------------------------------------------------------------->

def get_all_materias():
    conn = get_db()
    all_materias_query = "select * from Materia"
    cursor = conn.execute(all_materias_query)
    resulSet = cursor.fetchall()

    close_db(conn)
    return resulSet

# funcion que agrega una materia a base de datos --------------------------------------------------------------------->

def add_materia(nombre, nivel, horario, docente):
    try:
        conn = get_db()

        conn.execute("insert into Materia (mateNombre, mateNivel, mateHorario, mateDocente) values (?, ?, ?, ?);", (nombre, nivel, horario, docente))
        conn.commit()

        close_db(conn)
        return True

    except Error as error:
        print(error)
        return False

# funcion que devuelve una materia de la base de datos dada su id --------------------------------------------------------------------->

def get_materia_by_id(id_materia):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM Materia WHERE mateId = {}".format(id_materia))
    resultSet = list(cursor.fetchall())
    close_db(conn)
    return resultSet

# funcion que actualiza una materia a base de datos --------------------------------------------------------------------->

def update_materia(nombre, nivel, horario, docente, id):
    try:
        conn = get_db()
        
        conn.execute("UPDATE Materia SET mateNombre = ?, mateNivel = ?, mateHorario = ?, mateDocente = ? WHERE mateId = ?", (nombre, nivel, horario, docente, id))
        conn.commit()

        conn.close()
    except Error as error:
        print(error)
        return False

# funcion que elimina una materia de la base de datos dada su id --------------------------------------------------------------------->
def delete_materia(id_materia):
    try:
        conn=get_db()

        conn.execute("delete from Materia where mateId = {}".format(id_materia))
        conn.commit()
        
        conn.close()
        return True
    except Error as error:
        print(error)
        return False

# <--------------------------[ACTIVIDAD]--------------------------------------------------->

#Actividades: Obtener e insertar

def get_Activity():
  conn = get_db()
  cursor = conn.execute("select * from Actividad")
  resultados = list(cursor.fetchall())
  close_db(conn)
  return resultados



def add_Activity_insert(descripcion, fechaInicio, fechaFin, nota, idMateria):
  try:
    conn= get_db()
    conn.execute("insert into Actividad (actiDescripcion, actiFechaInicio, actiFechaFin, actiNota, idMateria)values(?,?,?,?,?);", (descripcion, fechaInicio, fechaFin, nota, idMateria))
    conn.commit()
    close_db(conn)
    return True
  except Error as error:
    print(error)
    return False

#Actividades: Editar y eliminar

def get_actividad(id):
  conn = get_db()
  cursor = conn.execute("SELECT * FROM  Actividad WHERE actiId = {}".format(id))
  resultados = list(cursor.fetchall())
  conn.close()
  return resultados

def update_actividad(descripcion, fechaInicio, fechaFin, nota, idMateria,id):
  try:
    conn=get_db()
    conn.execute(
      """ 
      UPDATE Actividad
      SET actiDescripcion = ?,
            actiFechaInicio = ?,
            actiFechaFin = ?,
            actiNota = ?,
            idMateria = ?
            WHERE actiId = ?
            """, (descripcion, fechaInicio, fechaFin, nota, idMateria, id))
    conn.commit()
    close_db(conn)
    return True
  except Error as error:
    print(error)
    return False

def delete_actividad(id):
  try:
    conn=get_db()
    conn.execute("DELETE FROM Actividad WHERE actiId = {}".format(id))
    conn.commit()
    conn.close()
    return True
  except Error as error:
    print(error)
    return False

# <-------------------------------------- [[COMENTARIO]] ----------------------------------------------->

# funcion que agrega un comentario a la base de datos --------------------------------------------------------------------->

def add_comentario(fecha_comentario, descrip_comentario, actividad_id, docente_id):
    try:
        conn = get_db()
        conn.execute("INSERT INTO Comentario (comentFecha, comentDescripcion, idActividad, idUsuario) values (?, ?, ?, ?);", 
        (fecha_comentario, descrip_comentario, actividad_id, docente_id))
        conn.commit()
        close_db(conn)
        return True

    except Error as error:
        print(error)
        return False

# funcion que devuelve todos los comentarios de la base de datos --------------------------------------------------------------------->

def get_all_comentarios():
    conn = get_db()
    all_coments_query = "SELECT * FROM Comentario"
    cursor = conn.execute(all_coments_query)
    resulSet = cursor.fetchall()
    close_db(conn)
    return resulSet

# funcion que devuelve un comentario de la base de datos dada su id --------------------------------------------------------------------->

def get_comentario_by_id(id_comment):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM Comentario WHERE comentId = {}".format(id_comment))
    resultSet = list(cursor.fetchall())
    close_db(conn)
    return resultSet

# funcion que actualiza un comentario de la base de datos --------------------------------------------------------------------->

def update_comentario(fecha_comentario, descrip_comentario, actividad_id, docente_id, id_comment):
    try:
        conn = get_db()
        conn.execute("UPDATE Comentario SET comentFecha = ?, comentDescripcion = ?, idActividad = ?, idUsuario = ? WHERE comentId = ?", 
        (fecha_comentario, descrip_comentario, actividad_id, docente_id, id_comment))
        conn.commit()
        close_db(conn)
    except Error as error:
        print(error)
        return False

# funcion que elimina un comentario de la base de datos dada su id --------------------------------------------------------------------->
def delete_comentario(id_comment):
    try:
        conn=get_db()
        conn.execute("DELETE FROM Comentario WHERE comentId = {}".format(id_comment))
        conn.commit()
        close_db(conn)
        return True
    except Error as error:
        print(error)
        return False

# < ---------------------------------------[[MATRICULA]] ---------------------------------------------------------------->

# funcion que devuelve una matricula de la base de datos dada su id --------------------------------------------------------------------->

def get_matricula_by_id(id_matricula):
    conn = get_db()
    cursor = conn.execute("SELECT * FROM Matricula WHERE matriId = {}".format(id_matricula))
    resultSet = list(cursor.fetchall())
    close_db(conn)
    return resultSet

# Funcion que me permite ver las materias matriculadas

def get_all_matriculas(idUsuario):
    conn = get_db()
    sql = "SELECT * FROM Materia INNER JOIN Matricula on Materia.mateId = Matricula.idMateria WHERE Matricula.idUsuario = ?"
    cursor = conn.execute(sql, (idUsuario, ))
    resulSet = cursor.fetchall()
    close_db(conn)
    return resulSet

# Funcion que me permite matricular una materia -------------------------------------------------------------------------->

def matricular_materia(idUsuario, idMateria):
    try:
        conn = get_db()
        conn.execute("INSERT INTO Matricula (idUsuario, idMateria) values (?, ?);", 
        (idUsuario, idMateria))
        conn.commit()
        close_db(conn)
        return True

    except Error as error:
        print(error)
        return f"hubo un error en {error}"

# funcion que elimina una matricula de la base de datos dada su id --------------------------------------------------------------------->

def delete_matricula(id_matricula):
    try:
        conn=get_db()
        conn.execute("DELETE FROM Matricula WHERE matriId = {}".format(id_matricula))
        conn.commit()
        close_db(conn)
        return True
    except Error as error:
        print(error)
        return False