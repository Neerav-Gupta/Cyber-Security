from PIL import Image

DIVIDEINGFACTOR = 4 # Number of most significant binary digits to include of the encoding image

def encode():
  im1 = Image.open(input('Enter the image to hide in path: '))
  im2 = Image.open(input('Enter the image to hide path: '))
  if im1.size[0] < im2.size[0] or im1.size[1] < im2.size[1]:
    raise ValueError('Image is too big to hide.')
  for i in range(im1.size[0]):
    for j in range(im1.size[1]):
      pix1 = im1.getpixel((i, j))
      pix2 = im2.getpixel((i, j)) if i < im2.size[0] and j < im2.size[1] else (0, 0, 0)
      r1 = bin(pix1[0])[2:]
      g1 = bin(pix1[1])[2:]
      b1 = bin(pix1[2])[2:]
      r1 = (8-len(r1))*'0'+r1
      g1 = (8-len(g1))*'0'+g1
      b1 = (8-len(b1))*'0'+b1
      r2 = bin(pix2[0])[2:]
      g2 = bin(pix2[1])[2:]
      b2 = bin(pix2[2])[2:]
      r2 = (8-len(r2))*'0'+r2
      g2 = (8-len(g2))*'0'+g2
      b2 = (8-len(b2))*'0'+b2
      r = int(r1[:8-DIVIDEINGFACTOR]+r2[:DIVIDEINGFACTOR], 2)
      g = int(g1[:8-DIVIDEINGFACTOR]+g2[:DIVIDEINGFACTOR], 2)
      b = int(b1[:8-DIVIDEINGFACTOR]+b2[:DIVIDEINGFACTOR], 2)
      newpix = (r, g, b)
      im1.putpixel((i, j), newpix)
  im1.save(input('Enter the name of the new image: '), format="PNG")

def decode():
  im = Image.open(input('Enter the image path: '))
  width, height = im.size
  original_size = (0, 0)
  for i in range(im.size[0]):
    for j in range(im.size[1]):
      pix = im.getpixel((i, j))
      r,g,b = pix
      r = bin(r)[2:]
      g = bin(g)[2:]
      b = bin(b)[2:]
      r = (8-len(r))*'0'+r
      g = (8-len(g))*'0'+g
      b = (8-len(b))*'0'+b
      r = int(r[8-DIVIDEINGFACTOR:]+('0'*(8-DIVIDEINGFACTOR)), 2)
      g = int(g[8-DIVIDEINGFACTOR:]+('0'*(8-DIVIDEINGFACTOR)), 2)
      b = int(b[8-DIVIDEINGFACTOR:]+('0'*(8-DIVIDEINGFACTOR)), 2)
      newpix = (r, g, b)
      if newpix != (0, 0, 0):
        original_size = (i + 1, j + 1)
      im.putpixel((i, j), newpix)
  im = im.crop((0, 0, original_size[0], original_size[1]))
  im.save(input('Enter the name of the decoded image: '), format="PNG")

if __name__ == "__main__":
  command = input("What do you want to do? (1. encode/2. decode): ")
  if command == "1":
    encode()
  elif command == "2":
    decode()
  else:
    print("Invalid command.")