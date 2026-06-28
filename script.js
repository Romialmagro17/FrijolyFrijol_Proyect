// 1. Selección de elementos del DOM
const formulario = document.getElementById('formulario-registro');
const nombreInput = document.getElementById('nombre');
const categoriaSelect = document.getElementById('categoria');
const descripcionInput = document.getElementById('descripcion');
const mensajeValidacion = document.getElementById('mensaje-validacion');
const contenedorLista = document.getElementById('contenedor-lista');
const contadorRegistros = document.getElementById('contador-registros');

// Variable para el control del contador de videos/reseñas
let totalElementos = 0;

// 2. Escuchar el evento 'submit' del formulario
formulario.addEventListener('submit', function(evento) {
    // Evitar que la página se recargue por defecto
    evento.preventDefault();

    // Obtener y limpiar los valores de los campos
    const nombre = nombreInput.value.trim();
    const categoria = categoriaSelect.value;
    const descripcion = descripcionInput.value.trim();

    // 3. Validación de campos vacíos
    if (nombre === '' || categoria === '' || descripcion === '') {
        mostrarMensaje('Por favor, completa todos los campos para registrar el contenido.', 'danger');
        return; // Detiene la ejecución si hay campos vacíos
    }

    // Limpiamos mensajes de error si pasa la validación
    mensajeValidacion.innerHTML = '';

    // 4. Crear el nuevo elemento dinámicamente
    crearTarjetaContenido(nombre, categoria, descripcion);

    // 5. Actualizar el contador, limpiar el formulario y dar mensaje de éxito
    actualizarContador(1);
    formulario.reset();
    mostrarMensaje('¡Contenido agregado exitosamente al registro!', 'success');
});

// Función para mostrar alertas dinámicas con Bootstrap
function mostrarMensaje(texto, tipo) {
    mensajeValidacion.innerHTML = `
        <div class="alert alert-${tipo} alert-dismissible fade show m-0" role="alert">
            ${texto}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
}

// Función para armar la estructura con createElement y appendChild
function crearTarjetaContenido(nombre, categoria, descripcion) {
    // Columna contenedora responsiva
    const col = document.createElement('div');
    col.className = 'col';

    // Tarjeta estilizada con Bootstrap
    const card = document.createElement('div');
    card.className = 'card h-100 border-start border-warning border-3 shadow-sm';

    // Cuerpo de la tarjeta
    const cardBody = document.createElement('div');
    cardBody.className = 'card-body d-flex justify-content-between align-items-start';

    // Contenedor del texto informativo
    const infoDiv = document.createElement('div');
    
    const titulo = document.createElement('h5');
    titulo.className = 'card-title mb-1 text-capitalize fw-bold';
    titulo.textContent = nombre;

    const badgeCategoria = document.createElement('span');
    // Color según la categoría seleccionada
    badgeCategoria.className = categoria === 'Unboxing' ? 'badge bg-primary mb-2' : 'badge bg-success mb-2';
    badgeCategoria.textContent = categoria;

    const textoDescripcion = document.createElement('p');
    textoDescripcion.className = 'card-text small text-muted text-break';
    textoDescripcion.textContent = descripcion;

    // Construir la jerarquía del texto
    infoDiv.appendChild(titulo);
    infoDiv.appendChild(badgeCategoria);
    infoDiv.appendChild(textoDescripcion);

    // Botón para eliminar el registro
    const botonEliminar = document.createElement('button');
    botonEliminar.className = 'btn btn-sm btn-outline-danger ms-2 align-self-center';
    botonEliminar.textContent = 'Eliminar';
    
    // Evento click para remover la tarjeta
    botonEliminar.addEventListener('click', function() {
        col.remove();
        actualizarContador(-1);
    });

    // Ensamblar todo el bloque
    cardBody.appendChild(infoDiv);
    cardBody.appendChild(botonEliminar);
    card.appendChild(cardBody);
    col.appendChild(card);

    // Insertar el bloque en la interfaz
    contenedorLista.appendChild(col);
}

// Función para actualizar el badge del total general
function actualizarContador(valor) {
    totalElementos += valor;
    contadorRegistros.textContent = totalElementos;
}