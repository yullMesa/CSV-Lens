function renderPage(page) {
    const app = document.getElementById('app');
    
    // Aquí defines qué mostrar según la opción
    const content = {
        'home': '<h1>Inicio</h1><p>Bienvenido al dashboard principal.</p>',
        'noticias': '<h1>Noticias</h1><p>Cargando últimas noticias...</p>',
        'perfil': '<h1>Perfil</h1><p>Configuración de usuario.</p>'
    };

    app.innerHTML = content[page] || '<h1>404</h1>';
}