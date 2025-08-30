## Avoid error in Jest execution test

- [ts-jest-mock-import-meta AST transformer](https://github.com/ThomZz/ts-jest-mock-import-meta)


### SECRECTT KEY AND ACCES_TOKEN


- Es una confusión común y es crucial entender la diferencia para mantener la seguridad.
No, la SECRET_KEY del backend NO debe ser compartida con el frontend.
Aquí te explico los puntos clave:
SECRET_KEY (Backend):

    -   Esta clave es exclusiva del backend. Su propósito es firmar y verificar tokens JWT que tu propio backend pueda generar (por ejemplo, si tu FastAPI generara sus propios tokens de sesión, aunque en tu caso te estás apoyando en Supabase para la autenticación), o para otras operaciones criptográficas internas del servidor (como la gestión de sesiones o la encriptación de datos sensibles).

    - Nunca debe ser expuesta en el frontend porque si un atacante la obtiene, podría falsificar tokens o comprometer la seguridad de tu backend.

    - Tal como mencionaste, no está generada por la configuración de Supabase porque es una clave que tu backend utiliza para su propia seguridad.
    - Tokens de Supabase (Frontend y Backend):
        Cuando el frontend se autentica con Supabase, Supabase le devuelve un access_token (un JWT).
    
    - El frontend envía este access_token al backend en el encabezado Authorization (como ya hemos configurado con el interceptor de Axios).

  El backend (que ya has configurado para validar el token) recibe este access_token y lo verifica utilizando la clave pública de Supabase o el SDK de Supabase, no tu SECRET_KEY interna. Supabase es quien firma esos tokens con su propia clave secreta, y tu backend los valida con la clave pública correspondiente.

En resumen:
    SECRET_KEY: Secreta, solo en el backend, para la seguridad interna de tu API de FastAPI.
    access_token de Supabase: Se genera en el servidor de Supabase, se envía al frontend para que lo guarde y luego el frontend lo envía al backend para autenticar cada petición. El backend valida este token con Supabase (o su clave pública).

Lo importante es que la SECRET_KEY que te pedí añadir al .env del backend se mantenga confidencial y solo en el servidor.

## Comando para generar automaticamente el ACCES_KEY

`python -c "import secrets; print(secrets.token_urlsafe(32))"`