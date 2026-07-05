document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('formulario-registro');
    const contenedorLista = document.getElementById('contenedor-lista');
    const contador = document.getElementById('contador-reg');

    const actualizarContador = () => {
        if (contador) contador.textContent = contenedorLista.children.length;
    };

    formulario.addEventListener('submit', (event) => {
        event.preventDefault(); // Detiene la recarga de página

        if (!formulario.checkValidity()) {
            formulario.classList.add('was-validated');
        } else {
            const titulo = document.getElementById('nombre').value;
            const categoria = document.getElementById('categoria').value;

            // Crear tarjeta dinámica
            const div = document.createElement('div');
            div.className = 'col';
            div.innerHTML = `
                <div class="card p-3 shadow-sm border-0">
                    <h5>${titulo}</h5>
                    <p class="text-muted mb-2">Categoría: ${categoria}</p>
                    <button class="btn btn-outline-danger btn-sm w-100 eliminar-btn">Eliminar</button>
                </div>
            `;

            // Lógica de eliminación
            div.querySelector('.eliminar-btn').addEventListener('click', () => {
                div.remove();
                actualizarContador();
            });

            contenedorLista.appendChild(div);
            
            // Limpiar formulario y resetear validaciones
            formulario.reset();
            formulario.classList.remove('was-validated');
            actualizarContador();
        }
    });
});