import time


suret_var = 0
fotocek = 0
while fotocek < 5:
    if suret_var:
        fotocek += 1
        print("[auto] foto çelildi 5 /", fotocek)
        time.sleep(5)
print("bitti", fotocek)