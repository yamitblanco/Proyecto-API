document.addEventListener('DOMContentLoaded', function () {

  // 1. Validación del formulario para agregar productos
  const formularioProducto = document.getElementById('formulario_producto');
  if (formularioProducto) {
    formularioProducto.addEventListener('submit', function (e) {
      e.preventDefault();

      const nombre_producto = document.getElementById('nombre_producto').value.trim();
      const estado = document.getElementById('estado').value;
      const ubicacion = document.getElementById('ubicacion').value.trim();
      const cantidad = document.getElementById('cantidad').value;
      const precio = document.getElementById('precio').value;

      if (!nombre_producto || !estado || !ubicacion || !cantidad || !precio) {
        Swal.fire({
          icon: 'warning',
          title: 'Campos incompletos',
          text: 'Por favor, completa todos los campos obligatorios.',
          confirmButtonText: 'OK'
        });
        return;
      }

      Swal.fire({
        icon: 'success',
        title: 'Producto agregado',
        text: `El producto "${nombre_producto}" se ha guardado correctamente.`,
        confirmButtonText: 'Perfecto'
      }).then(() => {
        formularioProducto.submit();  // Envía el formulario después de la validación exitosa
      });
    });
  }

  // 2. Validación del formulario de registro de usuario
  const registroForm = document.getElementById('registro');
  if (registroForm) {
    registroForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const nombres = document.getElementById('nombres').value.trim();
      const primerApellido = document.getElementById('primer_apellido').value.trim();
      const segundoApellido = document.getElementById('segundo_apellido').value.trim();
      const fechaNacimiento = document.getElementById('fecha_nacimiento').value;
      const telefono = document.getElementById('telefono').value.trim();
      const email = document.getElementById('email').value.trim();
      const contraseña = document.getElementById('contraseña').value;

      if (!nombres || !primerApellido || !segundoApellido || !fechaNacimiento || !telefono || !email || !contraseña) {
        Swal.fire({
          icon: 'warning',
          title: 'Campos incompletos',
          text: 'Por favor, completa todos los campos del formulario.',
          confirmButtonText: 'OK'
        });
        return;
      }

      Swal.fire({
        icon: 'success',
        title: 'Registro exitoso',
        text: `Bienvenido, ${nombres}. Tu cuenta ha sido registrada correctamente.`,
        confirmButtonText: 'Continuar'
      }).then(() => {
        registroForm.submit();  // Envía el formulario después de la validación exitosa
      });
    });
  }

  // 3. Mostrar mensajes flash desde el backend (Flask/Django)
  if (window.flashMessages && window.flashMessages.length > 0) {
    window.flashMessages.forEach(msg => {
      Swal.fire({
        icon: msg.category,
        title: msg.category === 'success' ? 'Éxito' : 'Error',
        text: msg.message,
        confirmButtonText: 'OK'
      });
    });
  }

  // 4. Validación del formulario de "registrarse" si contiene formulario
  const registrarse = document.getElementById('registrarse');
  if (registrarse) {
    const form = registrarse.querySelector('form');
    if (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();

        const nombres = document.getElementById('nombres').value.trim();
        const primerApellido = document.getElementById('primer_apellido').value.trim();
        const segundoApellido = document.getElementById('segundo_apellido').value.trim();
        const fechaNacimiento = document.getElementById('fecha_nacimiento').value;
        const telefono = document.getElementById('telefono').value.trim();
        const email = document.getElementById('email').value.trim();
        const contraseña = document.getElementById('contraseña').value;

        if (!nombres || !primerApellido || !segundoApellido || !fechaNacimiento || !telefono || !email || !contraseña) {
          Swal.fire({
            icon: 'warning',
            title: 'Campos incompletos',
            text: 'Por favor, completa todos los campos del formulario.',
            confirmButtonText: 'OK'
          });
          return;
        }

        Swal.fire({
          icon: 'success',
          title: 'Registro exitoso',
          text: `Bienvenido, ${nombres} ${primerApellido}. Tu cuenta ha sido registrada correctamente.`,
          confirmButtonText: 'Continuar'
        }).then(() => {
          // Espera 1.5 segundos antes de enviar el formulario
          setTimeout(() => {
            form.submit();
          }, 1500);
        });
      });
    }
  }

  // 5. Validación del formulario de inicio de sesión
  const loginForm = document.getElementById('inicio_sesionv2');
  if (loginForm) {
    loginForm.addEventListener('submit', function (e) {
      e.preventDefault();

      const email = document.getElementById('email').value.trim();
      const contraseña = document.getElementById('contraseña').value;

      if (!email || !contraseña) {
        Swal.fire({
          icon: 'warning',
          title: 'Campos incompletos',
          text: 'Por favor, completa todos los campos obligatorios.',
          confirmButtonText: 'OK'
        });
        return;
      }

      // Extrae el nombre del usuario a partir del email (antes del @)
      let nombre = email.split('@')[0].replace(/\./g, ' ');
      nombre = nombre.split(' ').map(p => p.charAt(0).toUpperCase() + p.slice(1).toLowerCase()).join(' ');

      Swal.fire({
        icon: 'success',
        title: 'Inicio de sesión exitoso',
        text: `Bienvenido "${nombre}".`,
        confirmButtonText: 'Perfecto'
      }).then(() => {
        loginForm.submit();  // Envía el formulario después de la validación exitosa
      });
    });
  }

});
