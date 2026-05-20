"""
PART 3: Crack password with MD5 + unknown salt (3 digits: 0-999)
Hash: c59a6c90ca92d23d0fe0435c21a00e39
Salt: desconocido, solo sabemos que es un número de 3 dígitos
"""

import hashlib
import time
import os

# Cómo correr esta parte:
# python3 parte3.py

targetHash = "c59a6c90ca92d23d0fe0435c21a00e39"
dictionary = "rockyou.txt"
saltRange = range(0, 1000)  # 0 a 999 (3 dígitos)

def breakHashWithUnknownSalt(targetHash, dictionary, saltRange):
    """Try to crack an MD5 hash with an unknown 3-digit salt"""
    
    print(f"[*] Algoritmo: MD5")
    print(f"[*] Salt: Desconocido (0-999)")
    print(f"[*] Hash objetivo: {targetHash}")
    print(f"[*] Longitud del hash: {len(targetHash)} caracteres (indica MD5)")
    print()
    
    # Verificar que el diccionario existe
    if not os.path.exists(dictionary):
        print(f"[!] ERROR: El archivo '{dictionary}' no existe")
        print(f"[!] Por favor descarga rockyou.txt desde: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")
        return None
    
    print(f"[*] Iniciando ataque con salt desconocido (fuerza bruta de salts)...")
    print(f"[*] Usando diccionario: {dictionary}")
    print(f"[*] Rango de salts a probar: {min(saltRange)} - {max(saltRange)} (1000 combinaciones)")
    print(f"[*] Estrategia: Por cada salt, probar todas las palabras del diccionario")
    print()
    
    start_time = time.time()
    totalAttemptsSuffix = 0
    
    for salt in saltRange:
        salt_str = str(salt)
        
        if salt % 100 == 0:
            print(f"[*] Probando salt: {salt_str}")
        
        with open(dictionary, 'r', encoding='latin-1') as file:
            for line in file:
                password = line.strip()
                
                # Probar: contraseña + salt
                saltedText = password + salt_str
                calculatedHash = hashlib.md5(saltedText.encode()).hexdigest()
                
                totalAttemptsSuffix += 1
                
                if calculatedHash == targetHash:
                    end_time = time.time()
                    total_time = end_time - start_time
                    
                    print()
                    print("=" * 60)
                    print(f"[+] ¡CONTRASEÑA ENCONTRADA!")
                    print(f"[+] Contraseña: {password}")
                    print(f"[+] Salt: {salt_str}")
                    print(f"[+] Texto hasheado: {saltedText}")
                    print(f"[+] Hash verificado: {calculatedHash}")
                    print(f"[+] Intentos totales: {totalAttemptsSuffix:,}")
                    print(f"[+] Tiempo total: {total_time:.6f} segundos")
                    print("=" * 60)
                    
                    return {
                        'password': password,
                        'salt': salt_str,
                        'attempts': totalAttemptsSuffix,
                        'time': total_time,
                        'salt_position': 'final'
                    }
    
    # Si no encontró con salt al final, prueba con salt al principio
    print()
    print("[*] Probando con salt al principio de la contraseña...")
    print()
    
    totalAttemptsPrefix = 0
    
    for salt in saltRange:
        salt_str = str(salt)
        
        if salt % 100 == 0:
            print(f"[*] Probando salt: {salt_str}")
        
        with open(dictionary, 'r', encoding='latin-1') as file:
            for line in file:
                password = line.strip()
                
                # Probar: salt + contraseña
                saltedText = salt_str + password
                calculatedHash = hashlib.md5(saltedText.encode()).hexdigest()
                
                totalAttemptsPrefix += 1
                
                if calculatedHash == targetHash:
                    end_time = time.time()
                    total_time = end_time - start_time
                    
                    print()
                    print("=" * 60)
                    print(f"[+] ¡CONTRASEÑA ENCONTRADA! (salt al inicio)")
                    print(f"[+] Contraseña: {password}")
                    print(f"[+] Salt: {salt_str}")
                    print(f"[+] Texto hasheado: {saltedText}")
                    print(f"[+] Hash verificado: {calculatedHash}")
                    print(f"[+] Intentos totales: {totalAttemptsSuffix + totalAttemptsPrefix:,}")
                    print(f"[+] Tiempo total: {total_time:.6f} segundos")
                    print("=" * 60)
                    
                    return {
                        'password': password,
                        'salt': salt_str,
                        'attempts': totalAttemptsSuffix + totalAttemptsPrefix,
                        'time': total_time,
                        'salt_position': 'inicio'
                    }
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print()
    print("=" * 60)
    print(f"[!] Contraseña NO encontrada")
    print(f"[!] Intentos totales: {totalAttemptsSuffix + totalAttemptsPrefix:,}")
    print(f"[!] Tiempo total: {total_time:.6f} segundos")
    print("=" * 60)
    
    return None

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════╗")
    print("║      PARTE 3: CRACKEAR CON MD5 + SALT DESCONOCIDO      ║")
    print("║              (Salt: 0-999 - 3 dígitos)                ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    resultado = breakHashWithUnknownSalt(targetHash, dictionary, saltRange)
    
    if resultado:
        print()
        print("[*] Resumen del análisis:")
        print(f"    - Algoritmo: MD5 + Salt (desconocido)")
        print(f"    - Salt encontrado: {resultado['salt']}")
        print(f"    - Contraseña: {resultado['password']}")
        print(f"    - Tiempo de ataque: {resultado['time']:.6f} segundos")
        print(f"    - Intentos totales: {resultado['attempts']:,}")
