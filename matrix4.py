import random
from multiprocessing import Pool, cpu_count
import numpy as np
import asyncio

# Для создания рандомных значений для матриц
def random_matrix():
    a, b = map(int, input("For matrix1, a,b: ").split())
    c, d = map(int, input("For matrix2, c,d: ").split())
    # Создаем две случайные матрицы размером NxM
    A = np.random.randint(0, 10, size=(a, b))
    B = np.random.randint(0, 10, size=(c, d))
    return A, B

# Функция перемножения элементов матриц
def element(index, A, B):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    with open("output_file.txt", 'a') as file:
        file.write(f'\n({i},{j}): {res}\n')
    return res

# Функция для распараллеливания вычислений
def parallel_multiply_matrices(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Количество столбцов матрицы A должно быть равно количеству строк матрицы B")

    # Создаем список индексов для каждого элемента результирующей матрицы
    indices = [(i, j) for i in range(len(A)) for j in range(len(B[0]))]

    # Создаем пул процессов, используя количество доступных ядер процессора
    with Pool(cpu_count()) as pool:
        # Выполняем перемножение элементов матриц параллельно с помощью функции element
        result_elements = pool.starmap(element, [(index, A, B) for index in indices])

    # Преобразуем список результатов в матрицу
    result_matrix = np.reshape(result_elements, (len(A), len(B[0])))

    return result_matrix

if __name__ == '__main__':
    
    #A = [[5, 5], [5, 5]]
    #B = [[4, 4], [4, 4]]

    # Рандомное заполнение
    A, B = random_matrix()

    try:
        # Выполняем перемножение матриц с использованием многопроцессорности
        result = parallel_multiply_matrices(A, B)
        with open("output_file.txt", 'a') as file:
            file.write(f'\n(result): \n{result}')

        # Выводим результат
        print("Matrix A:")
        print(A)
        print("\nMatrix B:")
        print(B)
        print("\nResult:")
        print(result)
    except ValueError as e:
        print(e)
