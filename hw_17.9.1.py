def binary_search(array, element, left, right):
    if left > right:  # если левая граница превысила правую,
        return False  # значит элемент отсутствует

    middle = (right + left) // 2  # находимо середину
    if array[middle] == element:  # если элемент в середине,
        return middle  # возвращаем этот индекс
    elif element < array[middle]:  # если элемент меньше элемента в середине
        # рекурсивно ищем в левой половине
        return binary_search(array, element, left, middle - 1)
    else:  # иначе в правой
        return binary_search(array, element, middle + 1, right)

def validation(index):
    if index < 0:
        print("Слева элементов в списке нет")
    else:
        print("Индекс искомого числа: ", index)

def sortirovka(array):
    for i in range(1, len(array)):
        x = array[i]
        idx = i
        while idx > 0 and array[idx-1] > x:
            array[idx] = array[idx-1]
            idx -= 1
        array[idx] = x

array = list(map(int,input('Введите количество чисел в последовательности через пробел: ').split()))  # Вводим последовательность и преобразуем в список
print('Неотсортированный список', array)  # Выводим список на экран
sortirovka(array)  # Сортируем полученный список
print('Отсортированный список', array)  # Выводим отсортированный список на экран
print('-------------')
element = int(input("Введите любое число: "))  # Вводим число относительно которого ищем предыдущий элемент
array.append(element)  # Добавляем введеный элемент справа списка
sortirovka(array)  # Сортируем полученный новый список
print('Отсортированный список с добавленным числом', array)  # Выводим отсортированный список на экран
print('-------------')
indexPredidushego = binary_search(array, element, 0, list.__len__(array)) - 1  # Осуществляем поиск позиции введенного элемента в списке, определяем индекс элемента слева
validation(indexPredidushego)  # Осуществляем валидацию полученного значения
