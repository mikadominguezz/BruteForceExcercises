"""
PART 1: Identify the hash algorithm and crack the password
Hash: 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
"""

import hashlib
import time
import os

# Cómo correr esta parte:
# python3 parte1.py

targetHash = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"
dictionary = "rockyou.txt"

def indentifyAlgorithm(hash_str):
    """Identifica el algorithm basado en la longitud del hash"""
    length = len(hash_str)
    
    algorithms = {
        32: "MD5",
        40: "SHA-1",
        56: "SHA-224",
        64: "SHA-256",
        96: "SHA-384",
        128: "SHA-512"
    }
    
    return algorithms.get(length, "Unknown")

def breakHash(targetHash, dictionary):
    """Try to crack the hash using the dictionary"""
    
    algorithm = indentifyAlgorithm(targetHash)
    print(f"[*] Algoritmo identificado: {algorithm}")
    print(f"[*] Longitud del hash: {len(targetHash)} caracteres")
    print(f"[*] Hash objetivo: {targetHash}")
    print()
    
    # Verificar que el dictionary existe
    if not os.path.exists(dictionary):
        print(f"[!] ERROR: El archivo '{dictionary}' no existe")
        print(f"[!] Por favor descarga rockyou.txt desde: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")
        return None
    
    print(f"[*] Iniciando ataque de dictionary...")
    print(f"[*] Usando dictionary: {dictionary}")
    print()
    
    start_time = time.time()
    attempts = 0
    
    with open(dictionary, 'r', encoding='latin-1') as file:
        for line in file:
            # Eliminar salto de línea
            word = line.strip()
            
            # Calcular hash SHA-256 (según el algorithm identificado)
            calculatedHash = hashlib.sha256(word.encode()).hexdigest()
            
            attempts += 1
            
            # Mostrar progreso cada 100,000 intentos
            if attempts % 100000 == 0:
                print(f"[*] Intentos: {attempts:,} | Última word: {word}")
            
            # Comparar con el hash objetivo
            if calculatedHash == targetHash:
                end_time = time.time()
                total_time = end_time - start_time
                
                print()
                print("=" * 60)
                print(f"[+] ¡CONTRASEÑA ENCONTRADA!")
                print(f"[+] Contraseña: {word}")
                print(f"[+] Hash verificado: {calculatedHash}")
                print(f"[+] Intentos realizados: {attempts:,}")
                print(f"[+] Tiempo total: {total_time:.6f} segundos")
                print("=" * 60)
                
                return {
                    'password': word,
                    'attempts': attempts,
                    'time': total_time,
                    'algorithm': algorithm
                }
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print()
    print("=" * 60)
    print(f"[!] Contraseña NO encontrada")
    print(f"[!] Palabras verificadas: {attempts:,}")
    print(f"[!] Tiempo total: {total_time:.6f} segundos")
    print("=" * 60)
    
    return None

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════╗")
    print("║          PARTE 1: IDENTIFICAR Y CRACKEAR HASH          ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    result = breakHash(targetHash, dictionary)
    
    if result:
        print()
        print("[*] Resumen del análisis:")
        print(f"    - Algoritmo: {result['algorithm']}")
        print(f"    - Tiempo de ataque: {result['time']:.6f} segundos")
        print(f"    - Contraseña: {result['password']}")
