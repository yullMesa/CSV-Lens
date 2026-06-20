// --- LÓGICA DE SEGURIDAD SIMPLIFICADA ---
const currentPath = window.location.pathname;

// 1. Si NO estamos en una página pública, verificamos el login
if (!currentPath.includes('login.html') && !currentPath.includes('register.html') && !currentPath.includes('index.html')) {
    
    // Verificamos si existe la sesión en el navegador
    const isLogged = localStorage.getItem('isLoggedIn');
    
    // Si no está logueado, lo mandamos al login inmediatamente
    if (isLogged !== 'true') {
        console.log("Acceso denegado, redirigiendo al login...");
        window.location.href = 'login.html';
    }
}

// --- LÓGICA DE INTERFAZ (Se ejecuta solo si los elementos existen) ---
document.addEventListener('DOMContentLoaded', () => {
    
    // Buscamos el botón de registro
    const btnRegistrar = document.getElementById('btnRegistrar');
    
    // Solo si el botón existe en la página actual, configuramos el evento
    if (btnRegistrar) {
        btnRegistrar.addEventListener('click', async () => {
            // 1. Obtener valores
            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');
            
            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();

            // 2. Validación básica
            if (!username || !password) {
                alert('Por favor, completa todos los campos.');
                return;
            }

            // 3. Crear el formato para FastAPI
            const params = new URLSearchParams();
            params.append('user_name', username);
            params.append('password', password);

            try {
                const response = await fetch('http://127.0.0.1:8000/register', {
                    method: 'POST',
                    body: params
                });

                const result = await response.json();

                if (response.ok) {
                    alert('Usuario registrado!');
                    window.location.href = 'index.html';
                } else {
                    alert('Error del servidor: ' + (result.detail || 'Error desconocido'));
                }
            } catch (error) {
                console.error('Error de conexión:', error);
                alert('No se pudo conectar con el servidor.');
            }
        });
    }
});

//login

const btnLogin = document.getElementById('btnLogin');
if (btnLogin) {
    btnLogin.addEventListener('click', async () => {
    // 1. Capturamos los valores
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // 2. Creamos el objeto FormData (esto es lo que espera Form en FastAPI)
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            // ¡IMPORTANTE! No pongas headers. Deja que el navegador ponga el 'Content-Type' automático.
            body: formData 
        });

        const data = await response.json();
        
        if (response.ok) {
            console.log("¡Éxito! Respuesta:", data);
            localStorage.setItem('isLoggedIn', 'true');
            window.location.href = 'mura.html';
        } else {
            console.error("Error de validación (422):", data);
            alert("Error: " + JSON.stringify(data));
        }
    } catch (error) {
        console.error("Error de red:", error);
    }
});
} else {
    // Esto es solo para depurar, puedes quitarlo después
    console.log("El botón btnLogin no existe en esta página, ignorando...");
}
