from PIL import Image
import numpy as np

def encode():
  im = Image.open(input('Enter the image path: '))
  pix_val = im.getdata()
  pix_val_flat = [x for sets in pix_val for x in sets]
  string = input('Enter the string to hide: ')
  if im.size[0]*im.size[1] < len(string):
    raise ValueError('String too long.')
  char_id = 0
  pix_pos = 0
  while char_id < len(string):
    char = string[char_id]
    binary_char = (8-len(bin(ord(char))[2:]))*'0'+bin(ord(char))[2:]
    for i in range(8):
      if binary_char[i] == '0':
        if pix_val_flat[pix_pos] % 2 == 1:
          pix_val_flat[pix_pos] += 1
      else:
        if pix_val_flat[pix_pos] % 2 == 0:
          pix_val_flat[pix_pos] += 1
      pix_pos += 1
    if pix_val_flat[pix_pos] % 2 == 1:
      pix_val_flat[pix_pos] += 1
    pix_pos += 1
    char_id += 1
  pix_val_flat[pix_pos-1] += 1
  format1 = []
  for i in range(0, len(pix_val_flat), 3):
    format1.append((pix_val_flat[i], pix_val_flat[i+1], pix_val_flat[i+2]))
  num_rows = (len(format1) + im.size[0] - 1) // im.size[0]
  format2 = []
  for i in range(num_rows):
    start = i * im.size[0]
    end = min((i + 1) * im.size[0], len(format1))
    format2.append(format1[start:end])
  array = np.array(format2, dtype=np.uint8)
  new_image = Image.fromarray(array)
  new_image.save(input('Enter the name of the new image: '), format="PNG")

def decode():
  im = Image.open(input('Enter the image path: '))
  pix_val = im.getdata()
  pix_val_flat = [x for sets in pix_val for x in sets]
  text = ""
  terminal_num = 0
  pix_pos = 0
  while terminal_num % 2 == 0:
    bin_str = ""
    for i in range(8):
        if pix_val_flat[pix_pos] % 2 == 0:
          bin_str += '0'
        else:
          bin_str += '1'
        pix_pos += 1
    text += chr(int(bin_str, 2))
    terminal_num = pix_val_flat[pix_pos]
    pix_pos += 1
  print("Output: {}".format(text))

if __name__ == "__main__":
  command = input("What do you want to do? (1. encode/2. decode): ")
  if command == "1":
    encode()
  elif command == "2":
    decode()
  else:
    print("Invalid command.")