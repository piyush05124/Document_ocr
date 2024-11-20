import hashlib
import base64




def encrypt(sample_string):
    # sample_string = "GeeksForGeeks is the best"
    sample_string_bytes = sample_string.encode("ascii")

    base64_bytes = base64.b64encode(sample_string_bytes)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def decrypt(base64_string):


# base64_string =" R2Vla3NGb3JHZWVrcyBpcyB0aGUgYmVzdA =="
    base64_bytes = base64_string.encode("ascii")

    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")
    return sample_string


# pas = encrypt('piyush@123')
# print(pas)

# sample_sctring = pas
# print(f"Decoded string: {decrypt(sample_sctring)}")
