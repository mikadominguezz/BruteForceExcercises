# Análisis de Ataques a Hashes de Contraseñas con Fuerza Bruta

Este proyecto contiene un análisis práctico de técnicas de cracking de contraseñas usando fuerza bruta y diccionarios, demostrando la importancia del salt y algoritmos criptográficos fuertes.

## Estructura del Proyecto

```
ataque-fuerza-bruta/
├── parte1.py                            # SHA-256 sin salt
├── parte2.py                            # MD5 + salt conocido
├── parte3.py                            # MD5 + salt desconocido (0-999)
└── README.md                            # Este archivo
```

### 1. Ejecutar Cada Parte

**Parte 1 (SHA-256 sin salt)**
```bash
python3 parte1.py
```

**Parte 2 (MD5 + salt conocido)**
```bash
python3 parte2.py
```

**Parte 3 (MD5 + salt desconocido)**
```bash
python3 parte3.py
```

---

## Glosario

**Qué significa import hashlib:**

The hashlib module is a built-in Python library that provides a common interface for many
secure hash and message digest algorithms (such as SHA-256, SHA-512, and MD5).
It is widely used for securely storing passwords, verifying data integrity, and creating digital signatures.

Básicamente permite calcular hashes (md5, sha-1, sha-256, etc.).

[W3Schools] (https://www.w3schools.com/python/ref_module_hashlib.asp)

**Qué significa import os**

Is a built-in Python module that lets you interact with your operating system.

Básicamente permite validar si el archivo rockyou.txt existe antes de abrirlo.

[GeekForGeeks] (https://www-geeksforgeeks-org.translate.goog/python/os-module-python-examples/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=sge)

**Qué significa SHA**

In cybersecurity, SHA stands for Secure Hash Algorithm. It is a set of cryptographic functions that take an input (like a password, a file, or a message) and convert it into a fixed-size, unique string of characters—acting as a digital fingerprint.

[Sectigo] (https://www.sectigo.com/blog/what-is-sha-encryption)

**Qué significa MD5**

MD5 (Message-Digest Algorithm 5) is a widely used cryptographic hash function that takes input data of any size and converts it into a unique, fixed-length 128-bit (16-byte) string. It acts as a digital fingerprint to verify data integrity, though it is no longer secure for high-level encryption.

Básicamente es un algoritmo de hash que convierte cualquier texto en cadena hexadecimal de 128 bits (32 caracteres).

[Okta] (https://www.okta.com/identity-101/md5/)

**Qué significa SALT**

In cybersecurity, a salt is a string of random data added to a password before it is hashed and stored in a database. It prevents attackers from using pre-computed "rainbow tables" to easily guess weak passwords.

[Hypr] (https://www.hypr.com/security-encyclopedia/salt)

Por ejemplo:

SHA256("password") → siempre el mismo hash

SHA256("password" + "99") → hash diferente
SHA256("password" + "47") → hash completamente distinto

---

## PARTE 1: Identificar Algoritmo y Crackear SHA-256 (sin salt)

### Datos
- **Hash**: `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`
- **Algoritmo**: SHA-256 (identificado por la longitud: 64 caracteres)
- **Salt**: Ninguno

### Qué hace
1. Identifica que el hash tiene 64 caracteres → SHA-256
2. Lee el diccionario rockyou.txt línea por línea
3. Para cada palabra, calcula: `SHA-256(palabra)`, es decir lo hashea segun el algoritmo identificado, en este caso el sha-256.
4. Compara con el hash objetivo
5. Mide el tiempo total

### Seguridad
**MUY DÉBIL** - Sin salt, es vulnerable a:
- Rainbow tables (tablas precalculadas)
- Ataques paralelos masivos
- Se crackea relativamente rápido

### Ejecución
```bash
python3 parte1.py
```

---

## PARTE 2: MD5 + Salt Conocido

### Datos
- **Hash**: `2484b2d1aec71de2ca87f88af401a6af`
- **Algoritmo**: MD5
- **Salt**: `99`
- **Estructura**: SHA-256(contraseña + salt) O SHA-256(salt + contraseña)

### Qué hace
1. Sabe que es MD5 (longitud: 32 caracteres)
2. Para cada palabra del diccionario:
   - Calcula: `MD5(palabra + "99")`
   - Si no encuentra, intenta: `MD5("99" + palabra)`
3. Compara con el hash objetivo
4. Mide y compara el tiempo con Parte 1

### Seguridad
**DÉBIL** - Problemas:
- MD5 es criptográficamente débil (colisiones conocidas)
- Salt muy corto (2 dígitos)
- Pero mejor que SHA-256 sin salt gracias al salt

### Comparación con Parte 1
- Si el salt es CONOCIDO: tiempo similar
- Si el salt fuera DESCONOCIDO: mucho más lento

### Ejecución
```bash
python3 parte2.py
```

---

## PARTE 3: MD5 + Salt Desconocido (0-999)

### Datos
- **Hash**: `c59a6c90ca92d23d0fe0435c21a00e39`
- **Algoritmo**: MD5
- **Salt**: Desconocido (pero sabemos que es 0-999)
- **Estructura**: MD5(contraseña + salt) O MD5(salt + contraseña)

### Qué hace
1. BUCLE 1: Para cada salt de 0 a 999:
   - BUCLE 2: Para cada palabra del diccionario:
     - Calcula: `MD5(palabra + salt_str)`
     - Compara con hash objetivo
2. Si no encuentra, intenta con salt al principio
3. Mide el tiempo total

### Seguridad
 **MEDIANO** - Limitaciones:
- Cada palabra ahora tiene 1000 hashes posibles
- Hace el ataque 1000x más costoso
- Pero aún es viable con diccionario (rockyou.txt tiene 14M+ palabras)
- No es viable con 16+ caracteres aleatorios

### Complejidad
```
Intentos = Número de salts × Palabras en diccionario
        = 1000 × 14,000,000
        = 14,000,000,000 intentos
```

### Ejecución
```bash
python3 parte3.py
```

---

## RESPUESTAS A LAS PREGUNTAS

### 1. ¿Por qué el Salt de solo 3 dígitos aumentó tanto el tiempo?

Sin salt, el atacante prueba cada palabra una vez contra el hash. Con Salt de 3 dígitos (0-999), tiene que probar cada palabra 1000 veces, una por cada salt posible. Si rockyou.txt tiene 14 millones de palabras, el espacio de búsqueda pasa de 14M a 14.000 millones de intentos. El tiempo se multiplica directamente 1000x.

**Ejemplo:**
```
Word "password":
- Sin salt: 1 hash posible
- Con salt: 1000 hashes posibles (password0, password1, ..., password999)

14M palabras × 1000 salts = 14 mil millones de intentos
```

---

### 2. Si el Salt fuera de 16 caracteres aleatorios, ¿sería posible este ataque?

No, no se podría y sería prácticamente imposible.

Si usas un conteo combinatorio te das cuenta más facilmente:

Longitud de Salt (L), cada posición puede tomar A valores, y el número total de Salts posibles es N=A^L.

Salt de 16 caracteres aleatorios:
- Usando alfabeto alfanuméricos: minúsculas (26) + mayúsculas (26) + digitos (10)= 62 y hay 16 caracteres. N=62^16 quedarian aprox 4.7x10^28. Recorred este ese espacio tomaría muchísimo tiempo, imposible cantidad. Por eso los sistemas modernos utilizan salts de 16-32 bytes generados aleatoriamente para que el ataque de fuerza bruta sobre el salt se vuelva computacionalmente imposible.

---

### 3. ¿Qué es más seguro: SHA-256 sin salt, o MD5 con salt desconocido?

MD5 con salt desconocido es más seguro.

**SHA-256 SIN SALT**

- Existen tablas rainbow (tabla de hashes precalculados para muchas contraseñas comunes) y funcionan.
- El ataque de diccionario directo es 1 hash por palabra.
- La velocidad del algoritmo es rápida.
- No hay colisiones conocidas.

**MD5 CON SALT DESCONOCIDO**

- Las tablas rainbow son inútiles.
- El ataque de diccionario directo es 1000 + hashes por palabra o más.
- La velocidad del algorimo es rápida también.
- Tiene colisiones conocidas.

SHA-256 sin salt es vulnerable porque solo necesitas encontrar la palabra en una tabla precalculada ("password" siempre tiene el mismo hash). El salt rompe esa ventaja aunque el algoritmo sea más débil.

Lo ideal sería un algoritmo lento como bcrypt/argon2 y salt aleatorio largo:
- Algoritmo fuerte (SHA-256, BLAKE2, etc.)
- Salt largo y aleatorio (16+ caracteres)
- Derivación lenta (pbkdf2, bcrypt, scrypt, argon2)


## PARTE 4: Ejercicio En Clase

Durante la clase, se pide que puedan encontrar la password y salt del siguiente hash.
Se sabe que el SALT tiene 3 dígitos.
968587884750727ee05016d360474d33

Como es tan largo el proceso de encontrar la contraseña, les dejo los resultados del ataque.

```bash
╔════════════════════════════════════════════════════════╗
║   PARTE 4: CRACKEAR HASH CON SALT DESCONOCIDO          ║
║     (Detecta automáticamente: MD5, SHA-1, SHA-256...)  ║
║              (Salt: 0-999 - 3 dígitos)                 ║
╚════════════════════════════════════════════════════════╝

[*] Salt: Desconocido (0-999)
[*] Hash objetivo: 968587884750727ee05016d360474d33
[*] Longitud del hash: 32 caracteres
[*] Algoritmos posibles: MD5

[*] Cargando diccionario en memoria...
[*] Diccionario cargado: 14,344,381 contraseñas
[*] Iniciando ataque con salt desconocido (fuerza bruta de salts)...
[*] Rango de salts a probar: 0 - 999 (1000 combinaciones)
[*] Estrategia: Por cada algoritmo, salt y contraseña

[*] ===== Probando algoritmo: MD5 =====
[*] Probando con salt al final...
[*] Contraseña 0 (tiempo transcurrido: 0.0s)
[*] Contraseña 100,000 (tiempo transcurrido: 55.9s)
[*] Contraseña 200,000 (tiempo transcurrido: 111.9s)
[*] Contraseña 300,000 (tiempo transcurrido: 167.9s)
[*] Contraseña 400,000 (tiempo transcurrido: 223.7s)
[*] Contraseña 500,000 (tiempo transcurrido: 279.4s)
[*] Contraseña 600,000 (tiempo transcurrido: 335.3s)
[*] Contraseña 700,000 (tiempo transcurrido: 391.0s)
[*] Contraseña 800,000 (tiempo transcurrido: 446.8s)
[*] Contraseña 900,000 (tiempo transcurrido: 502.7s)
[*] Contraseña 1,000,000 (tiempo transcurrido: 558.4s)
[*] Contraseña 1,100,000 (tiempo transcurrido: 614.4s)
[*] Contraseña 1,200,000 (tiempo transcurrido: 670.6s)
[*] Contraseña 1,300,000 (tiempo transcurrido: 726.7s)
[*] Contraseña 1,400,000 (tiempo transcurrido: 783.3s)
[*] Contraseña 1,500,000 (tiempo transcurrido: 839.5s)
[*] Contraseña 1,600,000 (tiempo transcurrido: 895.7s)
[*] Contraseña 1,700,000 (tiempo transcurrido: 951.7s)
[*] Contraseña 1,800,000 (tiempo transcurrido: 1008.1s)
[*] Contraseña 1,900,000 (tiempo transcurrido: 1064.3s)
[*] Contraseña 2,000,000 (tiempo transcurrido: 1120.6s)
[*] Contraseña 2,100,000 (tiempo transcurrido: 1176.7s)
[*] Contraseña 2,200,000 (tiempo transcurrido: 1233.2s)
[*] Contraseña 2,300,000 (tiempo transcurrido: 1289.6s)
[*] Contraseña 2,400,000 (tiempo transcurrido: 1345.9s)
[*] Contraseña 2,500,000 (tiempo transcurrido: 1402.7s)
[*] Contraseña 2,600,000 (tiempo transcurrido: 1459.2s)
[*] Contraseña 2,700,000 (tiempo transcurrido: 1515.7s)
[*] Contraseña 2,800,000 (tiempo transcurrido: 1572.5s)
[*] Contraseña 2,900,000 (tiempo transcurrido: 1629.0s)
[*] Contraseña 3,000,000 (tiempo transcurrido: 1685.5s)
[*] Contraseña 3,100,000 (tiempo transcurrido: 1741.8s)
[*] Contraseña 3,200,000 (tiempo transcurrido: 1797.9s)
[*] Contraseña 3,300,000 (tiempo transcurrido: 1854.9s)
[*] Contraseña 3,400,000 (tiempo transcurrido: 1910.7s)
[*] Contraseña 3,500,000 (tiempo transcurrido: 1967.4s)
[*] Contraseña 3,600,000 (tiempo transcurrido: 2023.7s)
[*] Contraseña 3,700,000 (tiempo transcurrido: 2080.5s)
[*] Contraseña 3,800,000 (tiempo transcurrido: 2136.4s)
[*] Contraseña 3,900,000 (tiempo transcurrido: 2192.4s)
[*] Contraseña 4,000,000 (tiempo transcurrido: 2250.4s)
[*] Contraseña 4,100,000 (tiempo transcurrido: 2306.5s)
[*] Contraseña 4,200,000 (tiempo transcurrido: 2363.5s)
[*] Contraseña 4,300,000 (tiempo transcurrido: 2419.6s)
[*] Contraseña 4,400,000 (tiempo transcurrido: 2476.0s)
[*] Contraseña 4,500,000 (tiempo transcurrido: 2531.8s)
[*] Contraseña 4,600,000 (tiempo transcurrido: 2587.8s)
[*] Contraseña 4,700,000 (tiempo transcurrido: 2644.3s)
[*] Contraseña 4,800,000 (tiempo transcurrido: 2700.8s)
[*] Contraseña 4,900,000 (tiempo transcurrido: 2757.5s)
[*] Contraseña 5,000,000 (tiempo transcurrido: 2813.6s)
[*] Contraseña 5,100,000 (tiempo transcurrido: 2869.8s)
[*] Contraseña 5,200,000 (tiempo transcurrido: 2925.8s)
[*] Contraseña 5,300,000 (tiempo transcurrido: 2983.2s)
[*] Contraseña 5,400,000 (tiempo transcurrido: 3039.9s)
[*] Contraseña 5,500,000 (tiempo transcurrido: 3096.7s)
[*] Contraseña 5,600,000 (tiempo transcurrido: 3152.7s)
[*] Contraseña 5,700,000 (tiempo transcurrido: 3208.4s)
[*] Contraseña 5,800,000 (tiempo transcurrido: 3264.7s)
[*] Contraseña 5,900,000 (tiempo transcurrido: 3320.9s)
[*] Contraseña 6,000,000 (tiempo transcurrido: 3376.8s)
[*] Contraseña 6,100,000 (tiempo transcurrido: 3433.8s)
[*] Contraseña 6,200,000 (tiempo transcurrido: 3489.9s)
[*] Contraseña 6,300,000 (tiempo transcurrido: 3545.6s)
[*] Contraseña 6,400,000 (tiempo transcurrido: 3601.0s)
[*] Contraseña 6,500,000 (tiempo transcurrido: 3656.0s)
[*] Contraseña 6,600,000 (tiempo transcurrido: 3712.0s)
[*] Contraseña 6,700,000 (tiempo transcurrido: 3768.2s)
[*] Contraseña 6,800,000 (tiempo transcurrido: 3823.4s)
[*] Contraseña 6,900,000 (tiempo transcurrido: 3879.8s)
[*] Contraseña 7,000,000 (tiempo transcurrido: 3935.6s)
[*] Contraseña 7,100,000 (tiempo transcurrido: 3991.4s)
[*] Contraseña 7,200,000 (tiempo transcurrido: 4047.1s)
[*] Contraseña 7,300,000 (tiempo transcurrido: 4103.1s)
[*] Contraseña 7,400,000 (tiempo transcurrido: 4160.4s)
[*] Contraseña 7,500,000 (tiempo transcurrido: 4216.5s)
[*] Contraseña 7,600,000 (tiempo transcurrido: 4272.4s)
[*] Contraseña 7,700,000 (tiempo transcurrido: 4328.2s)
[*] Contraseña 7,800,000 (tiempo transcurrido: 4383.4s)
[*] Contraseña 7,900,000 (tiempo transcurrido: 4439.0s)
[*] Contraseña 8,000,000 (tiempo transcurrido: 4494.9s)
[*] Contraseña 8,100,000 (tiempo transcurrido: 4551.5s)
[*] Contraseña 8,200,000 (tiempo transcurrido: 4608.1s)
[*] Contraseña 8,300,000 (tiempo transcurrido: 4664.1s)
[*] Contraseña 8,400,000 (tiempo transcurrido: 4720.2s)
[*] Contraseña 8,500,000 (tiempo transcurrido: 4776.4s)
[*] Contraseña 8,600,000 (tiempo transcurrido: 4832.9s)
[*] Contraseña 8,700,000 (tiempo transcurrido: 4889.3s)
[*] Contraseña 8,800,000 (tiempo transcurrido: 4945.2s)

============================================================
[+] ¡CONTRASEÑA ENCONTRADA!
[+] Algoritmo: MD5
[+] Contraseña: d0ntn33dn0p4ss
[+] Salt: 999
[+] Texto hasheado: d0ntn33dn0p4ss999
[+] Hash verificado: 968587884750727ee05016d360474d33
[+] Intentos totales: 8,856,910,000
[+] Tiempo total: 4976.942111 segundos
============================================================

[*] Resumen del análisis:
    - Algoritmo encontrado: MD5
    - Salt encontrado: 999
    - Contraseña: d0ntn33dn0p4ss
    - Posición del salt: final
    - Tiempo de ataque: 4976.942111 segundos
    - Intentos totales: 8,856,910,000
```
