# Mura



## English
Mura is a completely free platform dedicated to personal growth and learning. Currently, our system focuses on three core pillars: **Finance, Habits, and Health**. We are constantly evolving, and more categories will be added soon to help you become a better version of yourself.

## Español
Mura es una plataforma totalmente gratuita dedicada al crecimiento personal y al aprendizaje. Actualmente, nuestro sistema se centra en tres pilares fundamentales: **Finanzas, Hábitos y Salud**. Estamos en constante evolución y pronto añadiremos más categorías para ayudarte a ser una mejor versión de ti mismo.

---
## License / Licencia
This project is licensed under the GNU GPLv3 license. See the [LICENSE](LICENSE) file for more details.
Este proyecto está bajo la licencia GNU GPLv3. Consulta el archivo [LICENSE](LICENSE) para más detalles.


# Pruebas de Seguridad en API FastAPI

Este es un proyecto de práctica para auditar la seguridad de un backend.

## Vulnerabilidades Testeadas:
- **Enumeración de usuarios:** Verificado (Respuesta 401 consistente).
- **Inyecciones (XSS/SQLi):** Testeado mediante fuzzer de Python (Resultados: 422 Unprocessable Entity).
- **Validación de entradas:** Implementada (Límite de 100 caracteres y tipos de datos estrictos).

## Cómo ejecutar las pruebas:
1. Asegúrate de tener instalado `requests`: `pip install requests`
2. Ejecuta el script: `python fuzzer.py`