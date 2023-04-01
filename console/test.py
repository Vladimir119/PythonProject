word = "Загрузка"
import time
print("/ " + word, end="")
while True:
    time.sleep(0.3)
    print("\r- " + word, end="")
    time.sleep(0.3)
    print("\r\\ " + word, end="")
    time.sleep(0.3)
    print("\r/ " + word, end="")
