import subprocess

def r_spec(command='Rscript', duration, path, temp, path2script):
        ''' command - команда запуска скрипта R
            duration - продолжительность файла в секундах
            path - путь где лежат файлы для анализа './data/voice/clips/'
            temp - путь для записи csv файла './data/tmpcsv/'
            path2script - путь до скрипта на R './R/spectr.R'
        ''' 
        cmd = [command, path2script] + [name, duration, path, temp] # Build subprocess command
        p = subprocess.Popen(cmd, 
                             stdin=subprocess.PIPE, 
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, 
                             shell=True)