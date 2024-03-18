import math as m


def convert_array_to_string(arr):
    return ''.join(str(x) for x in arr)

# Exemple d'utilisation
entiers = [1, 2, 3, 4, 5]
chaine = convert_array_to_string(entiers)
print(chaine)

def rsa(plainText,n,e):
    cipherText  = []
    codeChart = "abcdefghijklmnopqrstuvwxyz"

    for key in codeChart:
        for i in plainText:
            if key == i:
                char = codeChart.index(key)
                # print(char)
                c = int(m.pow(char, e) % n)
                # print(c)
                cipherText.append(c)
    strcov= convert_array_to_string(cipherText)           
    return strcov






message = "hi"

print(rsa(message, 33, 3))
print(" -----------Dechiffrement--------")

