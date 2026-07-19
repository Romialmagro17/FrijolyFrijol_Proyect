document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('formulario-registro');
    const contenedor = document.getElementById('contenedor-lista');
    const contador = document.getElementById('contador-reg');
    
    // Lista donde guardaremos los datos (Pre-Flask)
    let listaIdeas = [];

    formulario.addEventListener('submit', (e) => {
        e.preventDefault();

        // Validaciones Bootstrap
        if (!formulario.checkValidity()) {
            formulario.classList.add('was-validated');
            return;
        }

        // Crear objeto y guardar en arreglo
        const nuevaIdea = {
            titulo: document.getElementById('nombre').value,
            categoria: document.getElementById('categoria').value
        };
        listaIdeas.push(nuevaIdea);

        // Actualizar UI
        renderizar();
        formulario.reset();
        formulario.classList.remove('was-validated');
    });

    // Función para dibujar los datos (Estructura repetitiva)
    function renderizar() {
        contenedor.innerHTML = '';
        listaIdeas.forEach((idea, index) => {
            // Condicional: Cambia el estilo según la categoría
            const colorClase = idea.categoria === 'Trabajo' ? 'border-primary' : 'border-success';
            
            contenedor.innerHTML += `
                <div class="col">
                    <div class="card ${colorClase} p-3 border-2 shadow-sm">
                        <h5>${idea.titulo}</h5>
                        <p class="text-muted">Categoría: ${idea.categoria}</p>
                        <button class="btn btn-sm btn-outline-danger" onclick="eliminar(${index})">Eliminar</button>
                    </div>
                </div>
            `;
        });
        contador.textContent = listaIdeas.length;
    }

    // Función global para eliminar
    window.eliminar = (index) => {
        listaIdeas.splice(index, 1);
        renderizar();
    };
});