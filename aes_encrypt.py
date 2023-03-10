from PIL import Image 
from Crypto.Cipher import AES
from Crypto import Random
import hashlib 
 
filename = "tux.png" 
filename_out = "tux_aes" 
format = "png" 
global_key = "secret"
#key = hashlib.sha256(key.encode()).digest()[:16] #encode key to byte -> hash algorithm
 
# AES requires that plaintexts be a multiple of 16, so we have to pad the data 
def pad(data): 
    return data + b"\x00"*(16-len(data)%16)  
 
# Maps the RGB  
def convert_to_RGB(data): 
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data)) if i % 3 == d], [0, 1, 2])) 
    pixels = tuple(zip(r,g,b)) 
    return pixels 
     
def process_aes_ecb(filename, filename_out, key): 
    # Opens image and converts it to RGB format for PIL 
    key = hashlib.sha256(key.encode()).digest()[:16] #encode key to byte -> hash algorithm
    im = Image.open(filename) 
    data = im.convert("RGB").tobytes()  
 
    # Since we will pad the data to satisfy AES's multiple-of-16 requirement, we will store the original data length and "unpad" it later. 
    original = len(data)  
 
    # Encrypts using desired AES mode (we'll set it to ECB by default) 
    new = convert_to_RGB(aes_ecb_encrypt(key, pad(data))[:original])  
     
    # Create a new PIL Image object and save the old image data into the new image. 
    im2 = Image.new(im.mode, im.size) 
    im2.putdata(new) 

    #Save image
    format = "png"
    im2.save(filename_out+"."+format, format) 

def process_aes_cbc(filename, filename_out, key): 
    #encode key to byte -> hash algorithm
    key =  hashlib.sha256(key.encode()).digest()[:16] 
    
    # Opens image and converts it to RGB format for PIL
    im = Image.open(filename) 
    data = im.convert("RGB").tobytes()  
 
    # Since we will pad the data to satisfy AES's multiple-of-16 requirement, we will store the original data length and "unpad" it later. 
    original = len(data)  
 
    # Encrypts using desired AES mode (we'll set it to ECB by default) 
    new = convert_to_RGB(aes_cbc_encrypt(key, pad(data))[:original])  
     
    # Create a new PIL Image object and save the old image data into the new image. 
    im2 = Image.new(im.mode, im.size) 
    im2.putdata(new) 

    #Save image 
    format = "png"
    im2.save(filename_out+"."+format, format) 
 
# CBC 
def aes_cbc_encrypt(key, data, mode=AES.MODE_CBC):
    IV = Random.new().read(AES.block_size)
    aes = AES.new(key, mode, IV) 
    new_data = aes.encrypt(data) 
    return new_data 
# ECB 
def aes_ecb_encrypt(key, data, mode=AES.MODE_ECB):
    aes = AES.new(key, mode) 
    new_data = aes.encrypt(data) 
    return new_data 
 