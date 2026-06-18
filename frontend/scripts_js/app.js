const contenedor = document.getElementById('app'); // Asegúrate de que este ID coincida con tu HTML
const slides = [
  { texto: "MURA: EL PODER DE LOS DATOS Y LA SEGURIDAD INFORMÁTICA.", descripcion: "Transformamos información compleja en decisiones inteligentes. Explora el futuro de tu análisis.", imagen: "../css/image/carrusel/seguridad.png" },
  { texto: "Perfil de usuario", descripcion: "Gestiona tu cuenta", imagen: "img2.png" },
  { texto: "Seguridad", descripcion: "Monitoreo en tiempo real", imagen: "img3.png" }
];

// DECLARA LA VARIABLE AQUÍ (Faltaba esto en tu código)
let indiceActual = 0;

function renderizarSlide(slide) {
  contenedor.innerHTML = `
    <div class="slide-activo">
        <div class="slide-texto">
            <h2>${slide.texto}</h2>
            <p>${slide.descripcion}</p>
        </div>
        <div class="slide-imagen">
            <img src="${slide.imagen}" alt="Imagen">
        </div>
    </div>
  `;
}

function siguienteSlide() {
  const s = slides[indiceActual];
  renderizarSlide(s);
  
  // Ahora sí la variable existe y puedes incrementarla
  indiceActual = (indiceActual + 1) % slides.length;
}

// Llamadas iniciales
siguienteSlide();
setInterval(siguienteSlide, 4200);