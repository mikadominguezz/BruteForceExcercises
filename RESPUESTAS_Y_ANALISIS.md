# 🎯 Guía Rápida de Respuestas - Ejercicio de Cracking de Hashes

## PARTE 1: Identificar Algoritmo y Crackear

### Pregunta 1: ¿Cuál es el algoritmo?

**Hash:** `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8`

**Respuesta:** **SHA-256**

**Justificación:**
```
Longitud del hash: 64 caracteres hexadecimales
64 caracteres = 256 bits = SHA-256

Tabla de referencia:
- 32 caracteres (128 bits) = MD5
- 40 caracteres (160 bits) = SHA-1
- 56 caracteres (224 bits) = SHA-224
- 64 caracteres (256 bits) = SHA-256 ✓
- 96 caracteres (384 bits) = SHA-384
- 128 caracteres (512 bits) = SHA-512
```

### Pregunta 2: ¿Cuál es la contraseña?

**Respuesta:** `password123` (suposición - ejecuta el script para ver)

**Formato:** Se obtiene al encontrar la palabra en rockyou.txt que cumple:
```
SHA-256("password123") == 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
```

### Pregunta 3: ¿Cuánto tiempo tardó?

**Respuesta:** Depende del hardware, típicamente **20-60 segundos**

**Factores:**
- CPU speed
- Velocidad de lectura del disco
- Posición de la palabra en el diccionario
- Tamaño del diccionario (rockyou.txt: ~14M palabras)

---

## PARTE 2: MD5 + Salt Conocido

### Datos del sistema:
```
Hash: 2484b2d1aec71de2ca87f88af401a6af
Salt: 99
Algoritmo: MD5
```

### Identificación del algoritmo:
```
Longitud del hash: 32 caracteres hexadecimales = MD5
```

### Fórmula:
```
hash_objetivo == MD5(palabra + "99")  O  MD5("99" + palabra)
```

### Tiempo esperado:
```
Similar a Parte 1 (o ligeramente más rápido)
Razón: El salt es CONOCIDO, así que no añade complejidad
      Solo probamos: 14M palabras × 1 salt = 14M intentos

No: 14M palabras × 1000 salts (eso sería si fuera desconocido)
```

### Comparación Parte 1 vs Parte 2:
```
┌─────────────────────────────────────────┐
│ Parte 1: ~30 segundos (SHA-256 sin salt)│
│ Parte 2: ~30 segundos (MD5 + salt 99)   │
│                                         │
│ Diferencia: MÍNIMA (algoritmo débil     │
│ pero salt NO añade complejidad)         │
└─────────────────────────────────────────┘
```

---

## PARTE 3: MD5 + Salt Desconocido (0-999)

### Datos del sistema:
```
Hash: c59a6c90ca92d23d0fe0435c21a00e39
Salt: Desconocido (0-999)
Algoritmo: MD5
```

### Fórmula:
```
Para cada salt i (0 a 999):
    Para cada palabra en diccionario:
        hash_calculado = MD5(palabra + str(i))
        SI hash_calculado == hash_objetivo:
            ENCONTRADA!
```

### Complejidad:
```
Intentos = 1000 salts × 14,000,000 palabras
         = 14,000,000,000 intentos
         
Ratio frente a Parte 1: 14B / 14M = 1000x más intentos
```

### Tiempo esperado:
```
┌─────────────────────────────────────────────────────────┐
│ Parte 1: 30 segundos      → 14 millones de intentos    │
│ Parte 3: 30 segundos × 1000 = 8.3 horas              │
│                                                         │
│ En realidad, un poco menos por optimizaciones del SO   │
│ Rango realista: 4-12 horas                             │
└─────────────────────────────────────────────────────────┘
```

---

## ❓ RESPUESTAS DEFINITIVAS A LAS PREGUNTAS

### Pregunta 1: ¿Por qué el Salt de solo 3 dígitos aumentó tanto el tiempo?

**RESPUESTA COMPLETA:**

El aumento de tiempo se debe a un **factor multiplicativo de 1000**:

#### Explicación técnica:

**Sin salt:**
```python
# Parte 1: Una sola posibilidad por palabra
for palabra in diccionario:
    hash = SHA256(palabra)
    # Total: 14 millones de operaciones
```

**Con salt 0-999:**
```python
# Parte 3: 1000 posibilidades por palabra
for salt in range(0, 1000):           # ← Bucle NUEVO
    for palabra in diccionario:
        hash = MD5(palabra + salt)
        # Total: 14 mil millones de operaciones
```

#### Por qué esto es crucial en criptografía:

| Aspecto | Sin Salt | Con Salt (3 dígitos) |
|---------|----------|----------------------|
| Hashes únicos por palabra | 1 | 1,000 |
| Rainbow tables viables | ✓ Sí | ✗ No (10B+ combinaciones) |
| Precomputación | ✓ Posible | ✗ Imposible (costo prohibitivo) |
| Tiempo de ataque | Minutos | Horas-Días |
| Escalabilidad de defensa | Fija | Lineal con tamaño del salt |

#### Analogy:
```
Búsqueda sin salt:
  "Buscar todas las palabras en un diccionario"
  → 14 millones de búsquedas

Búsqueda con salt 0-999:
  "Buscar todas las palabras en 1000 diccionarios diferentes"
  → 14 mil millones de búsquedas

Multiplicador: 1000x
```

#### Conclusión para la pregunta:
```
"El salt de solo 3 dígitos aumentó el tiempo en APROXIMADAMENTE 1000x"

Porque: Transforma un espacio de búsqueda de 14M en 14B posibilidades
```

---

### Pregunta 2: Si el Salt fuera de 16 caracteres aleatorios, ¿sería posible este ataque?

**RESPUESTA: NO, sería COMPUTACIONALMENTE IMPOSIBLE**

#### Cálculo de complejidad:

**Salt de 3 dígitos (como en Parte 3):**
```
Rango: 0-999
Posibilidades: 1,000 salts
Factor multiplicativo: 1,000x
Tiempo estimado: Horas con diccionario
```

**Salt de 16 caracteres aleatorios (estándar moderno):**
```
Caracteres disponibles: ~95 (letras, dígitos, símbolos)
Posibilidades: 95^16 ≈ 4.7 × 10^31
Factor multiplicativo: 470,000,000,000,000,000,000,000,000,000x

Comparación:
Ratio = 4.7 × 10^31 / 1,000
      = 4.7 × 10^28 (470 septillones de veces más)
```

#### Análisis de viabilidad:

**Escenario 1: GPU moderna**
```
Velocidad típica: 1 billion MD5/segundo (1 GPU optimizada)
Salts para probar: 4.7 × 10^31
Tiempo = 4.7 × 10^31 / (1 × 10^9) = 4.7 × 10^22 segundos

Conversión:
= 4.7 × 10^22 / (3.15 × 10^7 sec/año)
= 1.5 × 10^15 años
= 100,000 veces más viejo que el universo (13.8 × 10^9 años)
```

**Escenario 2: Supuesto datacenter futurista**
```
GPUs: 1 millón (hipotético)
Velocidad total: 10^15 MD5/segundo
Tiempo = 4.7 × 10^31 / 10^15 = 4.7 × 10^16 segundos
       = ~1.5 × 10^9 años
       = 100 veces más viejo que el universo
```

#### Conclusión:

```
┌─────────────────────────────────────────────────────────┐
│ Con salt de 16 caracteres aleatorios:                   │
│                                                         │
│ ✗ IMPOSIBLE atacar por fuerza bruta de salts            │
│ ✗ IMPOSIBLE usar rainbow tables                         │
│ ✗ IMPOSIBLE precomputar (130+ bits = 10^39 valores)    │
│                                                         │
│ Tiempo de ataque por fuerza bruta: INFINITO (billones) │
│                                                         │
│ RESPUESTA: NO, es prácticamente imposible               │
└─────────────────────────────────────────────────────────┘
```

#### Por qué esto es importante:

```
Este es el principio fundamental de la seguridad moderna:
- Un salt LARGO y ALEATORIO no se ataca con fuerza bruta
- El atacante debe volver a: ataques de diccionario inteligentes
- O encontrar el salt de otra manera (ej: en la BD, no encriptado)
- O romper el algoritmo criptográfico (imposible con SHA-256)

Esto es por lo que BCrypt, Argon2, etc. usan salts largos
```

---

### Pregunta 3: ¿Qué es más seguro: SHA-256 sin salt, o MD5 con salt desconocido?

**RESPUESTA: MD5 con salt desconocido es CONSIDERABLEMENTE más seguro**

#### Comparación directa:

**SHA-256 SIN SALT:**
```
✓ FORTALEZAS:
  - Algoritmo criptográficamente fuerte
  - Resistente a colisiones (no conocidas)
  - Funciona bien para datos no sensibles

✗ DEBILIDADES CRÍTICAS:
  - VULNERABLE A RAINBOW TABLES
  - "rainbow table SHA-256" tiene billones de valores precalculados
  - Mismo password → SIEMPRE el mismo hash
  - Atacante puede verificar múltiples passwords en paralelo
  - Un usuario ≠ El mismo password en otro sitio con mismo hash

VECTOR DE ATAQUE: Rainbow table lookup O diccionario simple
TIEMPO DE ATAQUE: Segundos a minutos
ESCALA DE RIESGO: ⭐⭐⭐⭐⭐ (MUY ALTO)
```

**MD5 CON SALT DESCONOCIDO (incluso 3 dígitos):**
```
✓ FORTALEZAS:
  - El salt PREVIENE rainbow tables
  - 1000+ hashes diferentes por password
  - Mismo password en dos usuarios = HASHES DIFERENTES
  - Precomputación imposible (14 mil millones de combinaciones)
  - Fuerza bruta es el único ataque viable

✗ DEBILIDADES:
  - MD5 tiene colisiones conocidas (pero no aplicables aquí)
  - Salt muy corto (3 dígitos en lugar de 16+ caracteres)
  - Aún vulnerable a ataque inteligente de fuerza bruta

VECTOR DE ATAQUE: Fuerza bruta de diccionario × salts
TIEMPO DE ATAQUE: Horas a días (vs. segundos/minutos)
ESCALA DE RIESGO: ⭐⭐ (BAJO-MEDIO)
```

#### Tabla comparativa:

```
╔═══════════════════════════════════════════════════════════════════╗
║ Característica          │ SHA-256 sin salt │ MD5 + salt 0-999    ║
╠═════════════════════════╪═════════════════════════════════════════╣
║ Rainbow tables viables  │ ✓ SÍ (vulnerable)│ ✗ NO               ║
║ Rainbow table tamaño    │ ~150GB (+)       │ ~150TB irrelevante  ║
║ Precomputación útil     │ ✓ SÍ            │ ✗ NO (demasiados)   ║
║ Fuerza bruta simple     │ ✓ Rápido        │ ✗ Muy lento         ║
║ Igualdad de hashes      │ ✓ Predecible    │ ✗ Impredecible      ║
║ Tiempo crack típico     │ < 1 minuto      │ 4-12 horas          ║
║ Complejidad             │ O(n)            │ O(n × 1000)         ║
║ Vulnerabilidad conocida │ ✓ SÍ (rainbow)  │ ✗ NO (salt)         ║
╚═══════════════════════════════════════════════════════════════════╝
```

#### Conclusión formal:

```
┌─────────────────────────────────────────────────────────────┐
│ SEGURIDAD:                                                  │
│                                                             │
│ MD5 con salt desconocido >> SHA-256 sin salt               │
│                                                             │
│ "Mayor" es por factor de:                                   │
│ • 1000x más intentos requeridos (si salt es desconocido)   │
│ • Inmunidad a rainbow tables                               │
│ • Imposibilidad de precomputación                          │
│                                                             │
│ CONCLUSIÓN:                                                 │
│ El SALT es más importante que la fuerza del algoritmo      │
│ cuando se trata de defensa contra ataques de diccionario   │
└─────────────────────────────────────────────────────────────┘
```

#### Ranking de seguridad real (mejor a peor):

```
1. ⭐⭐⭐⭐⭐ SHA-256 + salt de 16 caracteres + iteraciones
   → Sistemas modernos: bcrypt, scrypt, argon2

2. ⭐⭐⭐⭐  MD5 + salt de 16 caracteres (incluso sin iteraciones)
   → Mejor que sin salt, aunque MD5 es débil

3. ⭐⭐⭐   MD5 + salt de 3 dígitos (este ejercicio)
   → Mediocre: algo de protección, pero aún atacable

4. ⭐⭐    SHA-256 sin salt
   → Malo: vulnerable a rainbow tables y rápido de crackear
   
5. ⭐     MD5 sin salt
   → Muy malo: débil + sin protección
```

#### Explicación FINAL:

```
¿Por qué el salt es MÁS importante que el algoritmo?

1. RAINBOW TABLES cambian TODO
   - Sin salt: adversario puede precomputar
   - Con salt: precomputación inútil (10 billones de opciones)

2. FACTOR MULTIPLICATIVO
   - Salt desconocido = 1000x más intentos necesarios
   - Hace la defensa mucho más costosa para atacante
   
3. DISUASIÓN PRÁCTICA
   - SHA-256 sin salt: "mirar en tabla precalculada" = instantáneo
   - MD5 + salt: fuerza bruta = horas/días = NO VIABLE

MORALEJA: 
Un algoritmo débil con salt fuerte > 
Un algoritmo fuerte sin salt

Por eso NUNCA usamos SHA-256 directo para passwords.
Por eso SIEMPRE usamos bcrypt/argon2 (salt incluido).
```

---

## 📋 Respuestas Cortas Para Entregar

Si necesitas respuestas concisas para un documento:

### Pregunta 1: ¿Cuál es el algoritmo de la Parte 1?
**R:** SHA-256 (identificado por la longitud de 64 caracteres hexadecimales)

### Pregunta 2: ¿Cuánto tiempo tardó la Parte 1?
**R:** [Varía según el hardware, típicamente 20-60 segundos]

### Pregunta 3: Comparación Parte 2 vs Parte 1 - ¿Tardó más o menos?
**R:** Similar (no más de 10-20% diferencia), porque el salt es CONOCIDO. No añade complejidad.

### Pregunta 4: ¿Por qué aumentó tanto el tiempo en Parte 3?
**R:** Multiplicador de 1000x. Cada palabra del diccionario (14M) × 1000 salts posibles = 14 mil millones de intentos.

### Pregunta 5: ¿Sería posible atacar con salt de 16 caracteres?
**R:** NO. Sería computacionalmente imposible. ~4.7 × 10^31 posibles salts requeriría más tiempo que la edad del universo incluso con hardware hipotético.

### Pregunta 6: ¿Qué es más seguro?
**R:** MD5 con salt desconocido es más seguro que SHA-256 sin salt. El salt (incluso débil) es más crítico que la fortaleza del algoritmo contra ataques de diccionario.

---

**Generado para:** Ejercicio de Criptografía - Cracking de Contraseñas  
**Dificultad:** Intermedia  
**Tiempo esperado:** 1-2 horas (sin contar Parte 3)
