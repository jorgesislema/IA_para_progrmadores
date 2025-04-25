import pytest
from parte1.func import es_primo
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'parte1')))

class TestEsPrimo:

    # Happy Paths - Números primos conocidos
    def test_es_primo_numeros_primos(self):
        primos = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        for num in primos:
            assert es_primo(num) is True

    # Happy Paths - Números no primos conocidos
    def test_es_primo_numeros_no_primos(self):
        no_primos = [0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20]
        for num in no_primos:
            assert es_primo(num) is False

    # Edge Cases - Números negativos
    def test_es_primo_numeros_negativos(self):
        negativos_primos = [-2, -3, -5, -11, -13]
        for num in negativos_primos:
            assert es_primo(num) is False
        negativos_no_primos = [-1, -4, -6]
        for num in negativos_no_primos:
            assert es_primo(num) is False

    # Edge Cases - Cero y uno
    def test_es_primo_cero_y_uno(self):
        assert es_primo(0) is False
        assert es_primo(1) is False

    # Edge Cases - Números grandes (para evaluar eficiencia, aunque la función actual no es muy eficiente)
    def test_es_primo_numeros_grandes(self):
        assert es_primo(1000003) is True
        assert es_primo(1000004) is False

    # Edge Cases - Tipos de datos no enteros
    def test_es_primo_tipos_no_enteros(self):
        with pytest.raises(TypeError):
            es_primo(2.3)
        with pytest.raises(TypeError):
            es_primo(3.9)
        with pytest.raises(TypeError):
            es_primo("tres")
        with pytest.raises(TypeError):
            es_primo(None)
        with pytest.raises(TypeError):
            es_primo(True)
        with pytest.raises(TypeError):
            es_primo(False)

    # Edge Cases - Inputs inusuales
    def test_es_primo_inputs_inusuales(self):
        with pytest.raises(TypeError):
            es_primo("cinco")
        with pytest.raises(TypeError):
            es_primo(None)
        with pytest.raises(TypeError):
            es_primo([])

    # Edge Cases - Precisión en punto flotante (números muy cercanos a primos)
    def test_es_primo_float_cercanos_a_primos(self):
        assert es_primo(19.000000000000004) is True
        assert es_primo(23.000000000000004) is True