"""
PART 2: Crack password with MD5 + known salt
Hash: 2484b2d1aec71de2ca87f88af401a6af
Salt: 99
"""

import hashlib
import time
import os

# Cómo correr esta parte:
# python3 parte2.py

targetHash = "2484b2d1aec71de2ca87f88af401a6af"
salt = "99"
""" Un salt es un valor aleatorio que se agrega a la contraseña antes de hashearla. """

dictionary = "rockyou.txt"

def breakHashWithSalt(targetHash, salt, dictionary):
    """Try to crack an MD5 hash with a known salt"""
    
    print(f"[*] Algoritmo: MD5")
    print(f"[*] Salt: {salt}")
    print(f"[*] Hash objetivo: {targetHash}")
    print(f"[*] Longitud del hash: {len(targetHash)} caracteres (indica MD5)")
    print()
    
    # Verificar que el diccionario existe
    if not os.path.exists(dictionary):
        print(f"[!] ERROR: El archivo '{dictionary}' no existe")
        print(f"[!] Por favor descarga rockyou.txt desde: https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt")
        return None
    
    print(f"[*] Iniciando ataque con salt conocido...")
    print(f"[*] Usando diccionario: {dictionary}")
    print(f"[*] Estructura: MD5(contraseña + salt) = hash")
    print()
    
    start_time = time.time()
    attempts = 0
    
    with open(dictionary, 'r', encoding='latin-1') as file:
        for line in file:
            # Eliminar salto de línea
            password = line.strip()
            
            # Crear el string: contraseña + salt
            # Nota: El salt puede agregarse antes o después según el sistema
            # Probamos: contraseña + salt (forma común)
            saltedText = password + salt
            
            # Calcular hash MD5
            calculatedHash = hashlib.md5(saltedText.encode()).hexdigest()
            
            attempts += 1
            
            # Mostrar progreso cada 100,000 intentos
            if attempts % 100000 == 0:
                print(f"[*] Intentos: {attempts:,} | Última palabra: {password}")
            
            # Comparar con el hash objetivo
            if calculatedHash == targetHash:
                end_time = time.time()
                total_time = end_time - start_time
                
                print()
                print("=" * 60)
                print(f"[+] ¡CONTRASEÑA ENCONTRADA!")
                print(f"[+] Contraseña: {password}")
                print(f"[+] Texto hasheado: {saltedText}")
                print(f"[+] Hash verificado: {calculatedHash}")
                print(f"[+] Intentos realizados: {attempts:,}")
                print(f"[+] Tiempo total: {total_time:.6f} segundos")
                print("=" * 60)
                
                return {
                    'password': password,
                    'attempts': attempts,
                    'time': total_time,
                    'salt': salt
                }
    
    # Si no encontró con salt al final, prueba con salt al principio
    print()
    print("[*] Probando con salt al principio de la contraseña...")
    print()
    
    attemptsPrefix = 0
    
    with open(dictionary, 'r', encoding='latin-1') as file:
        for line in file:
            password = line.strip()
            
            # Crear el string: salt + contraseña (forma alternativa)
            saltedText = salt + password
            
            calculatedHash = hashlib.md5(saltedText.encode()).hexdigest()
            
            attemptsPrefix += 1
            
            if attemptsPrefix % 100000 == 0:
                print(f"[*] Intentos: {attemptsPrefix:,} | Última palabra: {password}")
            
            if calculatedHash == targetHash:
                end_time = time.time()
                total_time = end_time - start_time
                
                print()
                print("=" * 60)
                print(f"[+] ¡CONTRASEÑA ENCONTRADA! (salt al inicio)")
                print(f"[+] Contraseña: {password}")
                print(f"[+] Texto hasheado: {saltedText}")
                print(f"[+] Hash verificado: {calculatedHash}")
                print(f"[+] Intentos totales: {attempts + attemptsPrefix:,}")
                print(f"[+] Tiempo total: {total_time:.6f} segundos")
                print("=" * 60)
                
                return {
                    'password': password,
                    'attempts': attempts + attemptsPrefix,
                    'time': total_time,
                    'salt': salt,
                    'salt_position': 'inicio'
                }
    
    end_time = time.time()
    total_time = end_time - start_time
    
    print()
    print("=" * 60)
    print(f"[!] Contraseña NO encontrada")
    print(f"[!] Palabras verificadas: {attempts + attemptsPrefix:,}")
    print(f"[!] Tiempo total: {total_time:.6f} segundos")
    print("=" * 60)
    
    return None

if __name__ == "__main__":
    print("╔════════════════════════════════════════════════════════╗")
    print("║       PARTE 2: CRACKEAR CON MD5 + SALT CONOCIDO        ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    resultado = breakHashWithSalt(targetHash, salt, dictionary)
    
    if resultado:
        print()
        print("[*] Resumen del análisis:")
        print(f"    - Algoritmo: MD5 + Salt")
        print(f"    - Salt: {resultado['salt']}")
        print(f"    - Tiempo de ataque: {resultado['time']:.6f} segundos")
        print(f"    - Contraseña: {resultado['password']}")
