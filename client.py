import database

HOST = "127.0.0.1"

Connection = database.connect(HOST, 'Jovanni')
Table = Connection.get("Vasquez")


#Table.put("Mango", ["lagartija", "iguana", "lagarto"])
#Table.put("Mango", "Toma")
#Table.delete("Mango")
#List = Table.get("Mango")
#print(List)
#Table.update("Mango", "Toma")



Table.close()