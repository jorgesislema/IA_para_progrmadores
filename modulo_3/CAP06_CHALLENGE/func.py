"""  
Esta función recibe un número entero y devuelve True si es primo, False si no lo es.
"""
import math

def es_primo(num):
    if num <= 1: 
        return False
    if num == 2:  
        return True
    if num % 2 == 0:  
        return False
    
 
    for i in range(3, math.isqrt(num) + 1, 2):
        if num % i == 0:
            return False
    return True
