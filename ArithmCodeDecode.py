#Elegant code written by Lukas Rascius, simplified by using numpy's longdouble instead of bigfloat

import numpy as np
import math
import string
import unittest
 
def encode(string, N):
  #получаем алфавит a-z
        alphabet = list(map(chr, range(97, 123)))
        #составляем таблицу вероятностей и инициализируем ее пока что равномерным #распределением
        pdftable = dict((letter, alphabet.count(letter)) for letter in set(alphabet))
        cdfarray = np.cumsum(list(pdftable.values()))
        # получим словарь для шифрования 
        cdftable = dict(zip(alphabet, cdfarray))

        # Инициализируем верхнюю и нижнюю границы интервала
        low = np.longdouble(0.0)
        high = np.longdouble(1.0)
        # инициализируем нулём текущее
        current_range = np.longdouble(0.0)
        # инициализируем 0 нижнюю границу диапазона символа
        low_range_of_symbol = np.longdouble(0.0)
        # инициализируем 0 нижнюю границу диапазона символа
        high_range_of_symbol = np.longdouble(0.0)

        symbol = ""

        for i in range(0, int(len(string)), N):
            # получим последнюю часть, если n не делит нацело длину строки, последняя часть будет равна «длина_строки%n» 
            if (i+N) > len(string):
                last = len(string) - i
            # иначе, мы продолжаем цикл с n символов одновременно 
            else:
                last = N
            for j in range(i, i + last):
                symbol = string[j]
                # получаем нижнюю границу диапазона для символа 
                if symbol == 'a':
                    low_range_of_symbol = 0
                else:
                    low_range_of_symbol = (float(cdftable[alphabet[alphabet.index(symbol) - 1]]) / cdftable[alphabet[-1]])  
                # получаем нижнюю границу диапазона для символа
                high_range_of_symbol = (float(cdftable[symbol]) / cdftable[alphabet[-1]])

                # считаем новый диапазон
                current_range = high - low
                # считаем новую верхнюю границу диапазона
                high = low + current_range * high_range_of_symbol
                # считаем новую нижнюю границу диапазона
                low = low + current_range  * low_range_of_symbol

                # получив новый диапазон, обновляем таблицу символов
                pdftable[string[j]]+=1
                cdfarray = np.cumsum(list((coordinate[1]) for coordinate in sorted(pdftable.items())))
                cdftable = dict(zip(alphabet, cdfarray))

        return low, len(string)

def decode(number, length):
        # получим алфавит a-z
        alphabet = list(map(chr, range(97, 123)))
        #составляем таблицу вероятностей и инициализируем ее пока что равномерным #распределением
        pdftable = dict((letter, alphabet.count(letter)) for letter in set(alphabet))
        cdfarray = np.cumsum(list(pdftable.values()))
k 
        cdftable = dict(zip(alphabet, cdfarray))

        # Инициализируем верхнюю и нижнюю границы интервала
        low = np.longdouble(0.0)
        high = np.longdouble(1.0)
        decoded_string = ""

        while True:
            for symbol in alphabet:
                # получаем нижнюю границу диапазона для символа 
                if(symbol == 'a'):
                    low_range_of_symbol = 0
                else:
                    low_range_of_symbol = (float(cdftable[alphabet[alphabet.index(symbol) - 1]]) / cdftable[alphabet[-1]])  
                # получаем верхнюю границу диапазона для символа 
                high_range_of_symbol = (float(cdftable[symbol]) / cdftable[alphabet[-1]])           
                
                # считаем новый диапазон 
                current_range = high - low
                # считаем предположительную верхнюю границу диапазона, #расшифровав который, получим новый символ

                high_candidate = low + current_range * high_range_of_symbol
                # считаем предположительную нижнюю границу диапазона, #расшифровав который, получим новый символ
                low_candidate = low + current_range * low_range_of_symbol
                
                # Если символ находится между предположительными нижней и верхней #границей, это и есть наш следующий символ
                if(low_candidate <= number < high_candidate):
                    decoded_string += symbol
                    # достигнув конца строки, возвращаем расшифрованное сообщение
                    if(len(decoded_string) == length):
                        return decoded_string
                    # обновляем значения границ, чтобы получить следующие предполагаемые границы и раскодировать следующий символ
                    low = low_candidate
                    high = high_candidate
                # получив новый диапазон, обновляем таблицу символов
                    pdftable[symbol]+=1
                    cdfarray = np.cumsum(list((coordinate[1]) for coordinate in sorted(pdftable.items())))
                    cdftable = dict(zip(alphabet, cdfarray))


# A basic unittest to see if the same string is returned from the encoded value
class TestArithmeticCoding(unittest.TestCase):
	def setUp(self):
		self.string = "hello"

	def test_arithmetic(self):
		[number, length] = (encode(self.string, 3))
		string = decode(number, length)
		self.assertTrue(string == self.string)

if __name__ == '__main__':
    unittest.main()
