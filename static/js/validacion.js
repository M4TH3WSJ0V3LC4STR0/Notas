const inputs = document.querySelectorAll('#formulario input');
const formulario = document.getElementById('formulario');

const expresiones = {
	usuario: /^[a-zA-Z0-9\_\-]{4,16}$/, // Letras, numeros, guion y guion_bajo
	nombre: /^[a-zA-ZÀ-ÿ\s]{1,40}$/, // Letras y espacios, pueden llevar acentos.
	password: /^.{4,12}$/, // 4 a 12 digitos.
	correo: /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/,
	telefono: /^\d{7,14}$/ // 7 a 14 numeros.
}

const campos = {
  usuario: false,
  password: false
}

const validarFormulario = (e) => {
  switch (e.target.name) {
    case "usernameLogin":
      if (expresiones.usuario.test(e.target.value)) {
        document.getElementById('user-group').classList.remove('formulario__grupo-incorrecto');
        document.getElementById('user-group').classList.add('formulario__grupo-correcto');
        document.querySelector('#user-group .formulario__input-error').classList.remove('formulario__input-error-activo');
        campos.usuario = true;
      } else {
        document.getElementById('user-group').classList.add('formulario__grupo-incorrecto');
        document.querySelector('#user-group .formulario__input-error').classList.add('formulario__input-error-activo');
        campos.usuario = false;
      } /* comporbamos el valor que tengamos en test("accedemos al input y traemos el valor") */
    break;
    case  "passwordLogin":
      if (expresiones.password.test(e.target.value)) {
        document.getElementById('password-group').classList.remove('formulario__grupo-incorrecto');
        document.getElementById('password-group').classList.add('formulario__grupo-correcto');
        document.querySelector('#password-group .formulario__input-error').classList.remove('formulario__input-error-activo');
        campos.password = true;
      } else {
        document.getElementById('password-group').classList.add('formulario__grupo-incorrecto');
        document.querySelector('#password-group .formulario__input-error').classList.add('formulario__input-error-activo');
        campos.password = false;
      } /* comporbamos el valor que tengamos en test("accedemos al input y traemos el valor") */
    break;
  }
}

inputs.forEach((input) =>{
  input.addEventListener('keyup', validarFormulario);
  input.addEventListener('blur', validarFormulario);
});


formulario.addEventListener('submit',(e) => {
  
  if(campos.usuario && campos.password) {
    formulario.submit();
  } else {
    e.preventDefault();
    document.getElementById('formulario__mensaje').classList.add('formulario__mensaje-activo');
  }
});

/* inputs.forEach((input) =>{
  input.addEventListener('keyup', () => {
    console.log('Tecla levantada');
  });
  input.addEventListener('blur',()=>{
    console.log('mouse');
  });
}); */













/* inputs.forEach( (input) => {
  input.addEventListener('keyup', input)
  input.addEventListener('blur', validarFormulario)
  console.log('keyup')
}); */