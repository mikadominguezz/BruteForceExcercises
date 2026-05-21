"""
Durante la clase, se pide que puedan encontrar la password y salt del siguiente hash.
Se sabe que el SALT tiene 3 dígitos.
968587884750727ee05016d360474d33
"""

import hashlib
import time
import os

# Cómo correr esta parte:
# python3 parte4.py

targetHash = "968587884750727ee05016d360474d33"
dictionary = "rockyou.txt"
saltRange = range(0, 1000)  # 0 a 999 (3 dígitos)

def detectAlgorithm(hash_str):
    """Detecta el algoritmo basado en la longitud del hash"""
    length = len(hash_str)
    
    if length == 32:
        return ['md5']
    elif length == 40:
        return ['sha1']
    elif length == 64:
        return ['sha256']
    elif length == 128:
        return ['sha512']
    else:
        # Si no reconoce, intenta todos
        return ['md5', 'sha1', 'sha256', 'sha512']

def getHashFunction(algorithm):
    """Retorna la función de hash correspondiente"""
    if algorithm == 'md5':
        return hashlib.md5
    elif algorithm == 'sha1':
        return hashlib.sha1
    elif algorithm == 'sha256':
        return hashlib.sha256
    elif algorithm == 'sha512':
        return hashlib.sha512
    else:
        return hashlib.md5

def breakHashWithUnknownSalt(targetHash, dictionary, saltRange):
    """Try to crack a hash with an unknown 3-digit salt"""
    
    # Detectar algoritmos posibles
    possible_algorithms = detectAlgorithm(targetHash)
    
    print(f"[*] Salt: Desconocido (0-999)")
    print(f"[*] Hash objetivo: {targetHash}")
    print(f"[*] Longitud del hash: {len(targetHash)} caracteres")
    print(f"[*] Algoritmos posibles: {', '.join([a.upper() for a in possible_algorithms])}")
    print()
    
    # Verificar que el diccionario existe
    if not os.path.exists(dictionary):
        print(f"[!] ERROR: El archivo '{dictionary}' no existe")
        print(f"[!] Por favor descarga rockyou.txt desde: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")
        return None
    
    # Cargar el diccionario en memoria (una sola vez)
    print(f"[*] Cargando diccionario en memoria...")
    try:
        with open(dictionary, 'r', encoding='latin-1') as file:
            passwords = [line.strip() for line in file if line.strip()]
        print(f"[*] Diccionario cargado: {len(passwords):,} contraseñas")
    except Exception as e:
        print(f"[!] ERROR al leer diccionario: {e}")
        return None
    
    print(f"[*] Iniciando ataque con salt desconocido (fuerza bruta de salts)...")
    print(f"[*] Rango de salts a probar: {min(saltRange)} - {max(saltRange)} (1000 combinaciones)")
    print(f"[*] Estrategia: Por cada algoritmo, salt y contraseña")
    print()
    
    start_time = time.time()
    totalAttempts = 0
    
    # Probar con cada algoritmo posible
    for algorithm in possible_algorithms:
        print(f"[*] ===== Probando algoritmo: {algorithm.upper()} =====")
        hash_func = getHashFunction(algorithm)
        
        # Probar con salt al final
        print(f"[*] Probando con salt al final...")
        for idx, password in enumerate(passwords):
            if idx % 100000 == 0:
                elapsed = time.time() - start_time
                print(f"[*] Contraseña {idx:,} (tiempo transcurrido: {elapsed:.1f}s)")
            
            for salt in saltRange:
                salt_str = str(salt)
                
                # Probar: contraseña + salt
                saltedText = password + salt_str
                calculatedHash = hash_func(saltedText.encode()).hexdigest()
                
                totalAttempts += 1
                
                if calculatedHash == targetHash:
                    end_time = time.time()
                    total_time = end_time - start_time
                    
                    print()
                    print("=" * 60)
                    print(f"[+] ¡CONTRASEÑA ENCONTRADA!")
                    print(f"[+] Algoritmo: {algorithm.upper()}")
                    print(f"[+] Contraseña: {password}")
                    print(f"[+] Salt: {salt_str}")
                    print(f"[+] Texto hasheado: {saltedText}")
                    print(f"[+] Hash verificado: {calculatedHash}")
                    print(f"[+] Intentos totales: {totalAttempts:,}")
                    print(f"[+] Tiempo total: {total_time:.6f} segundos")
                    print("=" * 60)
                    
                    return {
                        'password': password,
                        'salt': salt_str,
                        'algorithm': algorithm,
                        'attempts': totalAttempts,
                        'time': total_time,
                        'salt_position': 'final'
                    }
        
        # Probar con salt al inicio
        print(f"[*] Probando con salt al inicio...")
        for idx, password in enumerate(passwords):
            if idx % 100000 == 0:
                elapsed = time.time() - start_time
                print(f"[*] Contraseña {idx:,} (tiempo transcurrido: {elapsed:.1f}s)")
            
            for salt in saltRange:
                salt_str = str(salt)
                
                # Probar: salt + contraseña
                saltedText = salt_str + password
                calculatedHash = hash_func(saltedText.encode()).hexdigest()
                
                totalAttempts += 1
                
                if calculatedHash == targetHash:
                    end_time = time.time()
                    total_time = end_time - start_time
                    
                    print()
                    print("=" * 60)
                    print(f"[+] ¡CONTRASEÑA ENCONTRADA!")
                    print(f"[+] Algoritmo: {algorithm.upper()}")
                    print(f"[+] Contraseña: {password}")
                    print(f"[+] Salt: {salt_str}")
                    print(f"[+] Texto hasheado: {saltedText}")
                    print(f"[+] Hash verificado: {calculatedHash}")
                    print(f"[+] Intentos totales: {totalAttempts:,}")
                    print(f"[+] Tiempo total: {total_time:.6f} segundos")
                    print("=" * 60)
                    
                    return {
                        'password': password,
                        'salt': salt_str,
                        'algorithm': algorithm,
                        'attempts': totalAttempts,
                        'time': total_time,
                        'salt_position': 'inicio'
                    }
        
        print()
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print()
    print("=" * 60)
    print(f"[!] Contraseña NO encontrada en ningún algoritmo")
    print(f"[!] Intentos totales: {totalAttempts:,}")
    print(f"[!] Tiempo total: {total_time:.6f} segundos")
    print("=" * 60)
    
    return None

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════╗")
    print("║   PARTE 4: CRACKEAR HASH CON SALT DESCONOCIDO           ║")
    print("║     (Detecta automáticamente: MD5, SHA-1, SHA-256...)   ║")
    print("║              (Salt: 0-999 - 3 dígitos)                  ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    resultado = breakHashWithUnknownSalt(targetHash, dictionary, saltRange)
    
    if resultado:
        print()
        print("[*] Resumen del análisis:")
        print(f"    - Algoritmo encontrado: {resultado['algorithm'].upper()}")
        print(f"    - Salt encontrado: {resultado['salt']}")
        print(f"    - Contraseña: {resultado['password']}")
        print(f"    - Posición del salt: {resultado['salt_position']}")
        print(f"    - Tiempo de ataque: {resultado['time']:.6f} segundos")
        print(f"    - Intentos totales: {resultado['attempts']:,}")
