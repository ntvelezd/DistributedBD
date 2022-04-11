import json
import os

DIR = os.getcwd()

def create(database, table, key, values):
    os.chdir(DIR + "/DataBases")

    try:

        if os.path.exists(database):
            os.chdir(database)

            if os.path.exists(table):
                os.chdir(table)
                keys_file = open("index.json", "r+")
                file_content = keys_file.read()
                json_keys = json.loads(file_content)

                if key in json_keys:
                    os.chdir(DIR)
                    return {"estado": 409, "mensaje": "La llave ya existe"}

                json_keys[key] = files_for_values(key, values)
                keys_file.seek(0)
                keys_file.write(json.dumps(json_keys))
                keys_file.truncate()
                keys_file.close()
            else:
                os.mkdir(table)
                os.chdir(table)
                values_array = files_for_values(key, values)
                keys_file = open("index.json", "w")
                keys_file.write(json.dumps({key: values_array}))
                keys_file.close()
                
        else:
            os.mkdir(database)
            os.chdir(database)
            os.mkdir(table)
            os.chdir(table)
            values_array = files_for_values(key, values)
            keys_file = open("index.json", "w")
            keys_file.write(json.dumps({key: values_array}))
            keys_file.close()

        os.chdir(DIR)
        return {"estado": 200, "mensaje": "Exito!"}
    except Exception as exception:
        os.chdir(DIR)
        return {"estado": 500, "mensaje": "Error inesperado"}

def delete(database, table, key):
    os.chdir(DIR + "/DataBases")

    try:

        if os.path.exists(database):
            os.chdir(database)

            if os.path.exists(table):
                os.chdir(table)
                keys_file = open("index.json", "r+")
                file_content = keys_file.read()
                json_keys = json.loads(file_content)

                if key in json_keys:
                    for fileName in json_keys[key]:
                        os.remove(fileName) 
                    json_keys.pop(key)
                    keys_file.seek(0)
                    keys_file.write(json.dumps(json_keys))
                    keys_file.truncate()
                    keys_file.close()
                    os.chdir(DIR)
                    return {"estado": 204, "mensaje": "Elemento borrado"}

                os.chdir(DIR)
                return {"estado": 404, "mensaje": "Llave no encontrada"}

            os.chdir(DIR)
            return {"estado": 404, "mensaje": "Tabla no encontrada"}

        os.chdir(DIR)
        return {"estado": 404, "mensaje": "Base de datos no encontrada"}
    except Exception as exception:
        os.chdir(DIR)
        return {"estado": 500, "mensaje": "Error inesperado"}

def update(database, table, key, new_values):
    os.chdir(DIR + "/DataBases")

    try:

        if os.path.exists(database):
            os.chdir(database)

            if os.path.exists(table):
                os.chdir(table)
                keys_file = open("index.json", "r+")
                file_content = keys_file.read()
                json_keys = json.loads(file_content)

                if key in json_keys:
                    for fileName in json_keys[key]:
                        os.remove(fileName) 
                    json_keys[key] = files_for_values(key, new_values)
                    keys_file.seek(0)
                    keys_file.write(json.dumps(json_keys))
                    keys_file.truncate()
                    keys_file.close()
                    os.chdir(DIR)
                    return {"estado": 201, "mensaje": "Modificacion exitosa"}

                os.chdir(DIR)
                return {"estado": 404, "mensaje": "Llave no encontrada"}
            os.chdir(DIR)
            return {"estado": 404, "mensaje": "Tabla no encontrada"}
        os.chdir(DIR)
        return {"estado": 404, "mensaje": "Base de datos no encontrada"}
    except Exception as exception:
        os.chdir(DIR)
        return {"estado": 500, "mensaje": "Error inesperado"}


def read(database, table, key):
    os.chdir(DIR + "/DataBases")

    try:

        if os.path.exists(database):
            os.chdir(database)

            if os.path.exists(table):
                os.chdir(table)
                keys_file = open("index.json", "r+")
                file_content = keys_file.read()
                json_keys = json.loads(file_content)

                if key in json_keys:
                    values_array = list()
                    for fileName in json_keys[key]:
                        file = open(fileName)
                        content = file.read()
                        values_array.append(content)
                        file.close()
                    keys_file.close()
                    os.chdir(DIR)
                    return {"estado": 200, "mensaje": "Exito!", "valores": values_array}

                os.chdir(DIR)
                return {"estado": 404, "mensaje": "Llave no encontrada"}

            os.chdir(DIR)
            return {"estado": 404, "mensaje": "Tabla no encontrada"}

        os.chdir(DIR)
        return {"estado": 404, "mensaje": "Base de datos no encontrada"}
    except Exception as exception:
        os.chdir(DIR)
        return {"estados": 500, "mensaje": "Error inesperado"}

def files_for_values(key, values):
    if(type(values) == str):
        values = values.split(",")
    value_count = 0
    values_array = list()
    for value in values:
        file_name = key + str(value_count) + ".txt"
        value_file = open(file_name, "w")
        value_file.write(value)
        value_file.close()
        values_array.append(file_name)
        value_count += 1    
    return values_array