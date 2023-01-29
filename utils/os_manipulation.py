import glob
import os
import shutil
import tempfile
import time

import allure

import core.context as ctx

default_timeout = 60


def add_new_directory(name_directory):
    with allure.step('Добавляем новую папку'):
        path = os.path.join(tempfile.gettempdir(), name_directory)
        if not os.path.exists(path):
            os.mkdir(path)
        print(f'*****************************{path = }')
        return path


def check_file_in_dir_present(file_name, timeout=10):
    with allure.step('Получаем наличие файла в директории'):
        count = 1
    end_time = time.time() + timeout
    name_directory = ctx.DOWNLOAD_FOLDER
    path = os.path.join(tempfile.gettempdir(), name_directory)
    while True:
        with allure.step(f'Ждем 1 секунду. Проверяем наличие файла в директории, попытка {count}'):
            if file_name in os.listdir(path):
                return True
            if time.time() > end_time:
                return False
            else:
                count += 1
                time.sleep(1)


def check_file_start_to_download():
    with allure.step('Проверяем, что началась загрузка файла'):
        path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
    end_time = time.time() + 5
    while True:
        if len(os.listdir(path)):
            return False
        time.sleep(1)
        if time.time() > end_time:
            break
    raise Exception('Не началась загрузка файла')


def delete_directory(path_directory):
    with allure.step('Удаляем папку'):
        print(f'/////////////////{delete_directory} : {path_directory}')
        os.rmdir(path_directory)


def delete_file(file_path):
    with allure.step('Удаляем файл'):
        os.unlink(file_path)


def delete_files_of_directory():
    with allure.step('Удаляем содержимое папки'):
        path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Ошибка удаления {file_path}. Причина: {e}')


def get_amount_files_of_directory():
    with allure.step('Получаем количество файлов в папке'):
        path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
        return len(os.listdir(path))


def get_size_file(file_name):
    with allure.step('Получаем размер файла'):
        return os.path.getsize(os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER, file_name))


def wait_until_file_downloading():
    with allure.step('Ожидаем загрузки файла'):
        end_time = time.time() + default_timeout
        path = os.path.join(tempfile.gettempdir(), ctx.DOWNLOAD_FOLDER)
        while True:
            if not glob.glob(path + '\\*.crdownload'):
                return False
            time.sleep(2)
            if time.time() > end_time:
                break
        raise Exception('Не загрузился файл')
