import subprocess


def checkout(cmd: str, text: str) -> bool:
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if result.returncode == 0 and (text in result.stdout or text in result.stderr):
        return True

    return False


def get_cmd_stdout(cmd: str) -> str:
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"


def test_task1_file_list():
    # проверка вывода списка файлов (l)
    result1 = checkout(f"cd {tst}; 7z a {out}/arx2", "Everything is Ok")
    result2 = checkout(f"cd {out}; 7z l arx2.7z", "qwe")
    result3 = checkout(f"cd {out}; 7z l arx2.7z", "rty")

    assert result1 and result2 and result3, "task1_file_list FAIL"


def test_task1_file_full_paths():
    # проверка разархивирования с путями (x)
    result1 = checkout(f"cd {tst}; 7z a {out}/arx2", "Everything is Ok")
    result2 = checkout(f"cd {out}; 7z x arx2.7z -o {folder1} -y", "Everything is Ok")
    result3 = checkout(f"cd {folder1}{tst}; ls", "qwe")
    result4 = checkout(f"cd {folder1}{tst}; ls", "rty")

    assert result1 and result2 and result3 and result4, "task1_file_full_paths FAIL"


def test_task2_hash():
    # Проверка, что хеш совпадает с рассчитанным командой crc32
    result1 = checkout(f"cd {tst}; 7z a {out}/arx2", "Everything is Ok")
    output1 = get_cmd_stdout(f"cd {out}; 7z h arx2.7z")
    output2 = get_cmd_stdout(f"cd {out}; crc32 arx2.7z").upper()

    assert result1 and (output2 in output1), "task2_hash FAIL"