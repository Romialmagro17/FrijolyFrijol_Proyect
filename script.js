document.addEventListener('DOMContentLoaded', () => {
    const formulario = document.getElementById('formulario-registro');
    const contenedor = document.getElementById('contenedor-lista');
    const contador = document.getElementById('contador-reg');
    const alertaCont = document.getElementById('alerta-contenedor');
    const spinner = document.getElementById('spinner-carga');
    
    let listaIdeas = [];

    formulario.addEventListener('submit', (e) => {
        e.preventDefault();
        if (!formulario.checkValidity()) {
            formulario.classList.add('was-validated');
            return;
        }

        const nuevaIdea = {
            titulo: document.getElementById('nombre').value,
            categoria: document.getElementById('categoria').value
        };
        listaIdeas.push(nuevaIdea);

        // Mostrar alerta de éxito
        alertaCont.innerHTML = `<div class="alert alert-success mt-2">Idea registrada con éxito.</div>`;
        setTimeout(() => alertaCont.innerHTML = '', 3000);

        renderizar();
        formulario.reset();
        formulario.classList.remove('was-validated');
    });

    function renderizar() {
        spinner.classList.remove('d-none'); // Mostrar Spinner
        contenedor.innerHTML = '';

        setTimeout(() => {
            spinner.classList.add('d-none'); // Ocultar Spinner
            listaIdeas.forEach((idea, index) => {
                contenedor.innerHTML += `
                    <div class="col">
                        <div class="card custom-card p-3 border-2 shadow-sm">
                            <h5>${idea.titulo}</h5>
                            <p class="text-muted">Categoría: ${idea.categoria}</p>
                            <button class="btn btn-sm btn-outline-danger" onclick="eliminar(${index})">Eliminar</button>
                        </div>
                    </div>
                `;
            });
            contador.textContent = listaIdeas.length;
        }, 500);
    }

    window.eliminar = (index) => {
        listaIdeas.splice(index, 1);
        renderizar();
    };
});