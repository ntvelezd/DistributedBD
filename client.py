import yadb

HOST = "127.0.0.1"

myConnection = yadb.connect(HOST, 'Jovanni')
myTable = myConnection.get("Vasquez")


#myTable.put("Mango", ["lagartija", "iguana", "lagarto"])
# myTable.put("Mango", "Toma")
#myTable.delete("Mango")
#lista = myTable.get("Mango")
#print(lista)
#myTable.update("Mango", "Toma")



myTable.close()