
from serial import Serial
from time import sleep
ser = Serial('COM9',9600)
if ser.isOpen():
    ser.close()
ser.open()
# db = sql.connect("C:/Users/Casper/Desktop/DjangoProjelerim/aboneTakipSistemi/aboneTakipSistemi/db.sqlite3")
# imlec = db.cursor()
while True:
    ser.write(b"STATE")
    sleep(1)
    res = ser.readline()
    text = res.decode()
    print(text)
