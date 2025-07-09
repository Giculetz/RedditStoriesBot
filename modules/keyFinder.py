import os
import fnmatch

def cauta_cel_mai_recent_fisier(director, nume_partial, extensie):
    cel_mai_recent = None
    timp_maxim = -1

    for root, dirs, files in os.walk(director):
        for file in files:
            if fnmatch.fnmatch(file, f"*{nume_partial}*.{extensie}"):
                cale_completa = os.path.join(root, file)
                timp_modificare = os.path.getmtime(cale_completa)
                if timp_modificare > timp_maxim:
                    timp_maxim = timp_modificare
                    cel_mai_recent = cale_completa

    return cel_mai_recent
