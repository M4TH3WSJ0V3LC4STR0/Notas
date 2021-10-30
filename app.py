import os
from sqlite3 import Error
from flask import Flask, render_template, flash, request, redirect, session
from flask.sessions import SessionInterface
import db 
import hashlib

app = Flask(__name__)
app.secret_key = os.urandom(24)

# <------------------LOGIN, SALIR Y HOME ------------------->

# Ruta principal ---------------------------------------------------------->
@app.route('/')
def raiz():
    #Validación de sesion activa
    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
             admin = 'Administrador'
             doc = 'Docente'
             estu = 'Estudiante'
             if admin == resultSet[6]:
                 return redirect('/home')
             elif doc == resultSet[6]:
                 return redirect('/home')
             elif estu == resultSet[6]:
                 return redirect('/home')
             else:
                 return render_template('login.html')
        else:
             return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/home')
def casa():
    #validacion de sesion activa
    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                return render_template('homeadmin.html')
            elif doc == resultSet[6]:
                return render_template('homedocente.html')
            elif estu == resultSet[6]:
                return render_template('homeestudiante.html')
            else:
                return render_template('/login.html')
        else:
            return redirect('/')
    else:
        return redirect('/')


# Ruta para home
@app.route('/login', methods=('GET', 'POST'))
def login():
    # Validación de usuarios
    if request.method == 'POST':
        usuario = request.form['usernameLogin']
        clave = request.form['passwordLogin']

        #Encriptando password
        password = clave
        passbyte = password.encode("utf-8")
        n = hashlib.sha256(passbyte)
        claveHash = n.digest()

        # inicio de sesión
        session.clear()
        session['UserLogin'] = usuario
        session['PassLogin'] = clave
        session['Rol'] = db.get_user_db(usuario)[6]

        resultSet = db.get_user_db(usuario)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'

            #Validar login 
            
            if usuario == resultSet[4] and claveHash == resultSet[5] and admin == resultSet[6]:
                return redirect('/home')
            elif usuario == resultSet[4] and claveHash == resultSet[5] and doc == resultSet[6]:
                return redirect('/home')
            elif usuario == resultSet[4] and claveHash == resultSet[5] and estu == resultSet[6]:
                return redirect('/home')
            else:
                flash('Usuario o contraseña incorrectos', 'error')
                return render_template('login.html')

        else:
            flash('Llene todos los campos', 'error')
            return redirect('/')

    else:
        return redirect('/')


@app.route('/salir')
def salir():
    #Cerrar sesion activa
    session.clear()
    return redirect('/')
# <------------------------------------------------------->

#<--------Register y usuarios----------->
@app.route('/Lista_Usuarios')
def listausuarios():
     #Validacion de sesion activa

    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                resultSet = db.list_tabla_db()
                return render_template('listausuarios.html', tablaUsuarios = resultSet)
            elif doc == resultSet[6]:
                return redirect('/home')
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')
    else:
        return redirect('/')


@app.route('/Registro_Usuarios')
def registrousuarios():

    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                return render_template('registrousuarios.html')
            elif doc == resultSet[6]:
                return redirect('/home')
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')
    else:
        return redirect('/')
    
    

@app.route('/Register', methods = ['POST','GET'] )
def register():  
    if 'UserLogin' in session:      
        if request.method == 'POST':
            nombre = request.form['nameRegistro']        
            apellido = request.form['apellidoRegistro']
            email = request.form['emailRegistro']
            usuario = request.form['usernameRegistro']
            clave = request.form['passwordRegistro']
            rol = request.form['rolRegistro']
            password = clave
            passbyte = password.encode("utf-8")
            n = hashlib.sha256(passbyte)
            db.add_user_db(nombre,apellido,email,usuario,n.digest(),rol)
            flash('Registro Exitoso', 'success')
            return render_template('registrousuarios.html')
        else: 
            flash('Error al ingresar los datos', 'error')
            return render_template('homeadmin.html')
    else:
        return redirect('/')

# Ruta que permite obtener un usuario dada su id --------------------------------->
@app.route('/Lista_Usuarios/Editar/<id_usuario>',  methods = ['POST','GET'])
def getUsuario(id_usuario):

    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                resultSet = db.list_tabla_db()
                data = db.get_user_by_id(id_usuario)
                return render_template('editarusuario.html',  usuario = data[0])
            elif doc == resultSet[6]:
                return redirect('/home')
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')
    else:
        return redirect('/')


  

# Ruta que permite actualizar los datos de un usuario --------------------------------->

@app.route('/Lista_Usuarios/Actualizar/<id_usuario>', methods = ['POST','GET'])
def editarusuario(id_usuario):
    if 'UserLogin' in session:
        if request.method == 'POST':
            nombre = request.form['nameRegistro']        
            apellido = request.form['apellidoRegistro']
            email = request.form['emailRegistro']
            usuario = request.form['usernameRegistro']
            clave = request.form['passwordRegistro']
            rol = request.form['rolRegistro']

            #Password encriptada
            password = clave
            passbyte = password.encode("utf-8")
            n = hashlib.sha256(passbyte)

            actualizar_usuario = db.update_usuario(nombre, apellido, email, usuario, n.digest(), rol, id_usuario)
            
            flash('Usuario actualizado Exitosamente', 'success')
            return redirect('/Lista_Usuarios')
        else:
            flash('Por favor ingresa informacion', 'error')
            return render_template('editarusuario.html')

    else:
        return redirect('/')

# Ruta que me permite eliminar un usuario ---------------------------------------------------------------->
@app.route('/Lista_Usuarios/Eliminar/<id_usuario>', methods = ['GET'])
def EliminarUsuario(id_usuario):
    if 'UserLogin' in session and session['Rol']=='Administrador':
        if db.delete_usuario(id_usuario):
            flash('Usuario eliminado con éxito', 'success')
            return redirect('/Lista_Usuarios')
        else:
            flash('No se pudo eliminar el usuario', 'warning')
            return redirect('/Lista_Usuarios')
    else:
        flash('Usted no tiene los permisos suficientes', 'warning')
        return redirect('/home')

#<-----------[ MATERIAS ]--------------------------------------------------------->

# ruta que contiene muestra todas las materias ------------------------------------>
  
@app.route('/Materias', methods = ['GET'])
def verMaterias():
    if 'UserLogin' in session:
        idUsuario = db.get_user_db(session['UserLogin'])[0]
        lista_materias = db.get_all_materias()
        lista_matriculas = db.get_all_matriculas(idUsuario)
        rolUsuario = session['Rol']
        return render_template('listarmaterias.html', matriculas=lista_matriculas, materias = lista_materias, rol = rolUsuario)
    else:
      return redirect('/')

# ruta que permite crear una materia ----------------------------------------------->

@app.route('/Materias/Registrar', methods = ['GET', 'POST'])
def CrearMateria():   
    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            #Validacion para registro de Materias de rol administrador
            if admin == resultSet[6]:
                if request.method == 'POST':
                    nombre = request.form['nombre']
                    nivel = request.form['nivel']
                    horario = request.form['horario']
                    docente = request.form['profesor']

                    agregar_materia = db.add_materia(nombre, nivel, horario, docente)
                    flash('Ah creado una materia Exitosamente', 'success')
                    return redirect('/Materias')
                else :
                    flash('Por favor ingresa una materia', 'warning')
                    return render_template('materia.html')

            #Validacion para registro de materias de rol docente,
            # como no tiene permisos lo manda a /home
            elif doc == resultSet[6]:
                return redirect('/home')

            #Validacion para registro de materias de rol estudiante,
            # como no tiene permisos lo manda a /home        
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')      
    else:
        return redirect('/')

# ruta que permite obtener una materia dada su id para ser editada -------------------------------------->

@app.route('/Materias/Editar/<id_materia>',  methods = ['POST','GET'])
def getMateria(id_materia):

    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                data = db.get_materia_by_id(id_materia)
                return render_template('editarmateria.html',  materia = data[0])
            elif doc == resultSet[6]:
                return redirect('/home')
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')
    else:
        return redirect('/')




# Ruta que permite actualizar los datos de una materia --------------------------------->

@app.route('/Materias/Actualizar/<id_materia>', methods = ['POST','GET'])
def EditarMateria(id_materia):
    if 'UserLogin' in session:
        if request.method == 'POST':
            nombre = request.form['nombre']
            nivel = request.form['nivel']
            horario = request.form['horario']
            docente = request.form['profesor']

            actualizar_materia = db.update_materia(nombre, nivel, horario, docente, id_materia)
        
            flash('Materia actualizada Exitosamente', 'success')
            return redirect('/Materias')
        else:
            flash('Por favor ingresa informacion', 'error')
            return render_template('editarmateria.html')
    else:
        return redirect('/')

@app.route('/Materias/Eliminar/<id_materia>', methods = ['GET','POST'])
def EliminarMateria(id_materia):

    if 'UserLogin' in session and session['Rol']=='Administrador':
        if db.delete_materia(id_materia):
            flash('Materia eliminada con éxito', 'success')
            return redirect('/Materias')
        else:
            flash('No se pudo eliminar la materia')
            return redirect('/Materias')
    else:
        flash('Usted no tiene los permisos suficientes', 'warning')
        return redirect('/')
#<-------------------------------------->


#<-------------------------------------->

# <----------------------------------------------[ACTIVIDADES] ---------------------------------------------------------------------------------------------------------->

# para entrar a la pagina principal
@app.route('/registrar_actividad')
def entrada():

    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                return render_template('registraractividad.html')
            elif doc == resultSet[6]:
                return render_template('registraractividad.html')
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')
    else:
        return redirect('/')


    

# Con esta puedes darle al boton de  ingresar y asi mismo registrar a la actividad


@app.route('/registradito', methods=['POST','GET'])
def registrar():
    if 'UserLogin' in session:
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            fechaInicio = request.form['fecha_inicio']
            fechaFin = request.form['fecha_final']
            nota = request.form['nota']
            idMateria = request.form['id_materia']
            db.add_Activity_insert(descripcion, fechaInicio,
                                fechaFin, nota, idMateria)
            flash('Registro Exitoso', 'success')
            return redirect('listar_actividades')
        else:
            flash('Error al ingresar datos', 'error')
            return render_template('registraractividad.html')
    else:
        return redirect('/')

# Aquí ves la lista de actividades
# renderiza el template y convierte al conjunto resultante (resulSet) en un vector de datos, done se va a llevar a el atributo de la etiqueta HTML (listaractividades.html) = Atributo(name) = (name="activities")


@app.route('/listar_actividades')
def listarActividad():
    #validacion de sesion activa
    if 'UserLogin' in session:
        rolUsuario = session['Rol']
        resulSet = db.get_Activity()
        return render_template('listaractividades.html', activities=resulSet, rol = rolUsuario)
    else:
      return redirect('/')

# Aquí le das el vector data al vecto contacto y lo distribuye segun su pocision en el ciclo del formulario para poder ver la tabla de editaractividades.html.
# Aqui lo editas, Traes los datos de la db (bases de datos) con la funcion (get_contact()) dandole el id a la funcion para que trabaje en db y se almacena en el vector data (data = db.get_contact(id)).
# El vector data hace aparecer la fila [1]row, y asi sucesivamentese se van agregando los datos


# Aqui tomas la variable (data) data = db.get_contact y le agregas la informacion de la base de datos que obtienes por medio de una id, que es llevada a el archivo db.py para que se ejecute la cosulta de la fila en la que se encuentra ese id (actiId)
# Por lo cual pones todos los datos en el atributo de la etiqueta html de los input con el nombre name="contact"
@app.route('/edit/<id>')
def get_user_by_id(id):

    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                data = db.get_actividad(id)
                return render_template('editaractividad.html',  contact=data[0])
            elif doc == resultSet[6]:
                data = db.get_actividad(id)
                return render_template('editaractividad.html',  contact=data[0])
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')
    else:
        return redirect('/')

   

# Aqui vas a obtener los datos donde se encuentran los campso input y los vas a llevar al metodo db.update_user() donde van a ir a hacer actualizados por una sentencia sql y son actualizados los datos
@app.route('/update/<id>', methods=['POST', 'GET'])
def updateid(id):
    if 'UserLogin' in session:
        if request.method == 'POST':
            descripcion = request.form['descripcion']
            fechaInicio = request.form['fecha_inicio']
            fechaFin = request.form['fecha_final']
            nota = request.form['nota']
            idMateria = request.form['id_materia']
            solucion = db.update_actividad(
                descripcion, fechaInicio, fechaFin, nota, idMateria, id)
            flash('Registro cambiado con exito', 'success')
            return redirect('/listar_actividades')
        else:
            flash('Error al ingresar datos', 'error')
            return render_template('listaractividades.html')
    else:
        return redirect('/')


# Esta funcion es para borrar la informacion de las actividades segun el id que ingresa a la sentencia sql
# el numero de la fila en la que se encuentra el id es pasado por medio de la url y transportada al metodo db.delete_user(id) donde se realiza la sentencia para eliminar los datos en la fila con el boton eliminar seleccionado
@app.route('/delete/<string:id>', methods = ['GET','POST'])
def delete(id):
    if 'UserLogin' in session and session['Rol']=='Administrador' or session['Rol'] == 'Docente':
        if db.delete_actividad(id):
            flash('Actividad eliminada con éxito', 'success')
            return redirect('/listar_actividades')

        else:
            flash('No se pudo eliminar la actividad')
            return redirect('/Listar_actividades')
    else:
        flash('Usted no tiene los permisos suficientes', 'warning')
        return redirect('/')


# <--------------------------------------------[[COMENTARIO]] --------------------------------------------------------------->

# ruta que contiene la funcion que muestra todas las comentarios ------------------------------------------------------------>
  
@app.route('/Comentarios', methods = ['GET'])
def listaComentarios():
    if 'UserLogin' in session:
        rolUsuario = session['Rol']
        lista_comentarios = db.get_all_comentarios()
        return render_template('listarcomentarios.html', comentarios = lista_comentarios, rol = rolUsuario)
    else:
      return redirect('/')

# ruta que permite crear una materia ----------------------------------------------->

@app.route('/Comentarios/Registrar_comentario', methods = ['GET', 'POST'])
def registrarcomentario():
    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            #Validacion para registro de comentarios de rol administrador
            if admin == resultSet[6]:
                if request.method == 'POST':
                    fecha_creacion_comment = request.form['fechaCreacionComment']
                    descripcion_comment = request.form['descripcionComment']
                    actividad_comment = request.form['actividadComment']
                    docente_comment = request.form['docenteComment']


                    agregar_comentario = db.add_comentario(fecha_creacion_comment, descripcion_comment, actividad_comment, docente_comment)
                    flash('Ah creado un comentario Exitosamente', 'success')
                    return redirect('/Comentarios')

                else :
                    flash('Por favor ingrese informacion del comentario', 'warning')
                    return render_template('registrarcomentario.html')

            #Validacion para registro de comentarios de rol docente
            elif doc == resultSet[6]:
                if request.method == 'POST':
                    fecha_creacion_comment = request.form['fechaCreacionComment']
                    descripcion_comment = request.form['descripcionComment']
                    actividad_comment = request.form['actividadComment']
                    docente_comment = request.form['docenteComment']


                    agregar_comentario = db.add_comentario(fecha_creacion_comment, descripcion_comment, actividad_comment, docente_comment)
                    flash('Ah creado un comentario Exitosamente', 'success')
                    return redirect('/Comentarios')

                else :
                    flash('Por favor ingrese informacion del comentario', 'warning')
                    return render_template('registrarcomentario.html')

            #Validacion para registro de comentarios de rol estudiante,
            # como no tiene permisos lo manda a /home        
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')     
    else:
        return redirect('/')



# ruta que permite obtener una materia dada su id para ser editada -------------------------------------->

@app.route('/Comentarios/Editar_comentario/<id_comment>',  methods = ['POST','GET'])
def getComentario(id_comment):
    
    if 'UserLogin' in session:
        UserSession = session['UserLogin']
        resultSet = db.get_user_db(UserSession)
        if len(resultSet) > 0:
            admin = 'Administrador'
            doc = 'Docente'
            estu = 'Estudiante'
            if admin == resultSet[6]:
                data = db.get_comentario_by_id(id_comment)
                return render_template('editarcomentario.html',  comentario = data[0])
            elif doc == resultSet[6]:
                data = db.get_comentario_by_id(id_comment)
                return render_template('editarcomentario.html',  comentario = data[0])
            elif estu == resultSet[6]:
                return redirect('/home')
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')
    else:
        return redirect('/')


# Ruta que permite actualizar un comentario ------------------------------------------------------------------->
@app.route('/Comentarios/Actualizar_comentario/<id_comment>', methods = ['POST','GET'])
def editarcomentario(id_comment):
    if 'UserLogin' in session:
        if request.method == 'POST':
            fecha_creacion_comment = request.form['fechaCreacionComment']
            descripcion_comment = request.form['descripcionComment']
            actividad_comment = request.form['actividadComment']
            docente_comment = request.form['docenteComment']

            actualizar_comentario = db.update_comentario(fecha_creacion_comment, descripcion_comment, actividad_comment, docente_comment, id_comment)
            
            flash('Comentario actualizado Exitosamente', 'success')
            return redirect('/Comentarios')
        else:
            flash('Por favor ingrese informacion', 'error')
            return render_template('editarcomentario.html')
    else:
        return redirect('/')

# Ruta que permite eliminar un comentario --------------------------------------------------------------------->

@app.route('/Comentarios/Eliminar_comentario/<id_comment>', methods = ['GET','POST'])
def EliminarComentario(id_comment):

    if 'UserLogin' in session and session['Rol']=='Administrador' or session['Rol']=='Docente':
        if db.delete_comentario(id_comment):
            flash('Comentario eliminado con éxito', 'success')
            return redirect('/Comentarios')
        else:
            flash('No se pudo eliminar el Comentario', 'warning')
            return redirect('/Comentarios')
    else:
        flash('Usted no tiene los permisos suficientes', 'warning')
        return redirect('/home')


# < -------------------------------------------[[MATRICULA]] ----------------------------------------------------->

# ruta que contiene la acción para matricular una materia ------------------------------------>

@app.route('/Materias/Matricular/<idMateria>', methods=['GET'])
def matricular(idMateria):
    if 'UserLogin' in session:
        idUsuario = db.get_user_db(session['UserLogin'])[0]
        matriculado = db.matricular_materia(idUsuario, idMateria)
        if matriculado:
            return redirect('/Materias')
        else:
            flash (matriculado)
            return redirect('/Materias')
    else:
        return redirect('/')

# Ruta que permite eliminar una materia matriculada --------------------------------------------------------------------->

@app.route('/Materias/Eliminar_matricula/<id_matricula>', methods = ['GET','POST'])
def EliminarMatricula(id_matricula):

    if 'UserLogin' in session and session['Rol']=='Estudiante':
        if  db.delete_matricula(id_matricula):
            flash('Materia desmatriculada con éxito', 'success')
            return redirect('/Materias')
        else:
            flash('No se pudo eliminar la matricula', 'warning')
            return redirect('/Materias')
    else:
        flash('Usted no tiene los permisos suficientes', 'warning')
        return redirect('/home')

# <--------------------------------[[PERFIL DE USUARIO]] -------------------------------------------------->

# Ruta que me permite ver el perfil de usuario ------------------------------------------------------------>
@app.route('/Perfil', methods = ['GET'])
def perfil():
    if 'UserLogin' in session:
        usuario = db.get_user_db(session['UserLogin'])
        rolUsuario = session['Rol']
        return render_template('perfil.html', usuario = usuario, rol = rolUsuario)
    else:
        return redirect('/')

# <------------------------------------------ [[MAIN O EJECUCION DEL PROGRAMA]] ------------------------------------------------------------------>

if __name__ == '__main__':
    app.run(debug=True)
