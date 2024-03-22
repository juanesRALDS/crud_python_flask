// app.js


async function visualizarFoto(evento){
    const files = evento.target.files
    const archivo = files [0]
    let filename = archivo.name
    let extension = filename.split(',').pop()
    extension = extension.toLowerCase()
    if(extension!=='jpg'){
        fileFoto.value=""
        swal.fire("Seleccionar", "La imagen debe ser en formato JPG", "warning")
    }else{
        base64URL = await encodeFileAsBase64URL(archivo);
        const objectURL = URL.createObjectURL(archivo)
        imagenProducto.setAttribute("src",objectURL)
    }
}
/**
 * Returns a file in Base64URL format.
 * @param {File} file
 * @return {Promise<string>}
 */
async function encodeFileAsBase64URL(file) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        reader.addEventListener('loadend', () => {
            resolve(reader.result);
        });
        reader.readAsDataURL(file);
    });
  };



  function agregarProducto() {
    // Obtener los datos del formulario
    const codigo = document.getElementById('codigo').value;
    const nombre = document.getElementById('nombre').value;
    const precio = document.getElementById('precio').value;
    const categoria = document.getElementById('cdCategoria').value;
    const foto = base64url; // Esta es la imagen en formato base64 obtenida del archivo seleccionado
    
    // Crear un objeto FormData con los datos del formulario
    const formData = new FormData();
    formData.append('codigo', codigo);
    formData.append('nombre', nombre);
    formData.append('precio', precio);
    formData.append('categoria', categoria);
    formData.append('foto', foto);

    // Enviar los datos al servidor
    fetch('/agregarProducto', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta del servidor, por ejemplo, mostrar un mensaje de éxito o actualizar la lista de productos
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}



base64url = null


async function visualizarFoto(evento) {
    const files = evento.target.files
    const archivo = files[0]
    let filename = archivo.name
    let extension = filename.split(".").pop()
    extension = extension.toLowerCase()
    if (extension!== "jpg"){
        fileFoto.value = "";
        swal.fire("Seleccionar", "La imagen debe ser en formato JPG", "warning")
    }else{
         base64url = await encodeFileAsBase64URL(archivo)
         const objetURL = URL.createObjectURL(archivo)
         imagenProducto.setAttribute("src",objetURL)

    }
   
    
}


  fetch('/obtenerCategorias')
  .then(response => response.json())
  .then(data => {
    const categorias = JSON.parse(data.categorias);
    // Ahora categorias es una lista de objetos JSON que puedes iterar
    categorias.forEach(categoria => {
      // Hacer algo con cada categoría, por ejemplo:
      console.log(categoria.nombre);
    });
  });
