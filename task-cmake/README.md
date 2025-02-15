# Task Cmake

## Описание задания

Необходимо создать проект и собрать его при помощи CMake, в котором реализован следующий функционал.

## Алгоритм действия

1. Исходный код должен лежать в трех папках `A`, `B`, `C`.
2. Папка `А` содержит скрипт на Python, `preparing.py`, который генерирует заголовочный файл `index.h`. Система будет проверять, что в репозитории не содержится файл `index.h`.
3. В папке `B` лежит библиотека со своим собственным файлом `CMakeLists.txt`. Заголовочный файл - `lib.h`, реализация библиотеки должна содержаться в файле `lib.cpp`.
4. (Простой путь) В папке `С` лежит два файла `main.h` и `main.cpp`, в `main.h` есть строчка `#include "A/index.h"` и строчка `"#include "B/lib.h"`.
5. (Сложный путь) В папке `C` помимо файлов из пункта 4 лежит файл `main_test.cpp` и некоторые другие файлы, которые запускают сборку тестов через Google Test. https://ru.wikipedia.org/wiki/Google_C%2B%2B_Testing_Framework. В файле `main_test.cpp` должен быть запуск тестов, в другом cpp-файле, который собирается в один executable - должны быть реализованы 2 теста:
   - Первый тест проверяет, что файл `A/index.h` содержит корректно сгенерированные данные
   - Второй тест проверяет правильность реализации библиотеки.

**Важно**: проверяющая система считает, что google test стоит в операционной системе!

6. После сборки проекта:
   - (Простой путь) Должна быть создана папка `bin`, в которой должен лежать исполняемый файл `C` с главной точкой входа из файла `main.cpp`.
   - (Простой и сложный путь) В корне репозитория быть создана папка `lib`, в которой должны лежать собранные динамические библиотеки.
   - (Сложный путь) В папке `bin` дополнительно должен лежать исполняемый файл `CTest` с запуском тестов, полученный после сборки `C/main_test.cpp` с исходными файлами, содержащие тесты.

## Требования

1. Используйте приватный репозиторий, при помощи которого вы сдали задание 0. Не забудьте проверить, что в коллабораторах есть пользователь checker.
2. В приватном репозитории создайте ветку task-cmake, в ветке создайте папку task-cmake.
3. Создайте merge request из ветки task-cmake в ветку master, добавьте ревьюера в merge request и не сливайте этот merge request!

## Параметры запуска сборки проекта

Один из вариантов сборки проекта будет запускаться следующими командами:
```bash
mkdir build
cd build
cmake ..
make
```

При этом проверяющая система может в каком-угодно месте создать папку для сборки, используйте переменную для сборки проекта.

## Критерии оценивания

- Создана динамическая библиотека в папке `B`, подключена к папке `С` - 3 балла
- Сгенерирован header в папке `A`, подключен в папке `С` - 3 балла
- Реализован сложный путь с тестированием - 3 балла
- Еще 1 балл ставится, если все условия выполнены.

## Полезная информация

- https://github.com/google/googletest - установка Google Test
- Установка Google Test - https://github.com/google/googletest/blob/master/googletest/README.md#standalone-cmake-project после необходимо сделать make && sudo make install
- https://github.com/akhtyamovpavel/BuildExamples-TP/tree/master/CMakeExamples - здесь можно найти примеры по CMake