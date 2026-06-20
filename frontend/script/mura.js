document.getElementById('btnRegistrar').addEventListener('click', async () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Crear un formato que FastAPI ama
    const params = new URLSearchParams();
    // Asegúrate de que estos nombres coincidan con los argumentos de tu función en FastAPI
    params.append('user_name', username); 
    params.append('password', password);

    try {
        const response = await fetch('http://127.0.0.1:8000/register', {
            method: 'POST',
            body: params // <--- Esto es clave, envías los parámetros como formulario
        });

        const result = await response.json();
        
        if (response.ok) {
            alert('¡Usuario registrado!');
            window.location.href = 'index.html';
        } else {
            alert('Error del servidor: ' + (result.detail || 'Error desconocido'));
        }
    } catch (error) {
        console.error('Error:', error);
    }
});