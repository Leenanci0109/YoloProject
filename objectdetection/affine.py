def exeu(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b // a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def modinv(a, m):
    gcd, x, y = exeu(a, m)
    if gcd != 1:
        return None
    else:
        return x % m


def affine_encrypt(text, a, b):
	e=''
	for t in text.upper().replace(' ', ''):
		e=e.join([chr(((a * (ord(t) - ord('A')) + b) % 26)
                        + ord('A'))
	print(e)
	
     return None
    #return ''.join([chr(((a * (ord(t) - ord('A')) + b) % 26)
                      #  + ord('A')) for t in text.upper().replace(' ', '')])


def affine_decrypt(cipher, a, b):
    return ''.join([chr(((modinv(a, 26) * (ord(c) - ord('A') - b))
                         % 26) + ord('A')) for c in cipher])


text = input("Enter text:")
a, b = 7, 2
encrypted = affine_encrypt(text, a, b)
print('Encrypted Text: {}'.format(encrypted))
print('Decrypted Text: {}'.format(affine_decrypt(encrypted, a, b)))
