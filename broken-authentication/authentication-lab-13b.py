print("[", end='')

with open('passwords.txt', 'r') as f:
    lines = f.readlines()

for password in lines:
    print('"' + password.rstrip("\n") + '",', end='')

print('"random"]', end='')