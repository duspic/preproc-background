from PIL import Image, ImageEnhance, ImageFilter

def scale_to(image, size:int):
    """
    size should be 512 or 1024.
    ofc other sizes are possible
    """
    width,height = image.size
    
    # in case the image isn't square-shaped,
    # the larger side gets scaled to value "size"
    
    if width >=height:
        factor = size/width
    else:
        factor = size/height
        
    new_width = round(width*factor)
    new_height = round(height*factor)
    
    image_scaled = image.resize((new_width,new_height))
    return image_scaled

def create_mask(image, width:int, height:int):
    res = Image.new("RGBA", (width,height), (255,255,255))
    
    enhancer = ImageEnhance.Brightness(image)
    dark_object = enhancer.enhance(0.3)
    
    res.paste(dark_object, mask=dark_object)
    return res

def img2img_blend(composition):
  # this should call the img2img api
  # for now, just return the already blended img
  return Image.open("gen4-blended.png")

def erode_mask(noback, size):
  mask = Image.new("RGBA", (size,size))
  enhancer = ImageEnhance.Brightness(noback)
  white_object = enhancer.enhance(100)
  mask.paste(white_object, mask=white_object)

  mask = mask.filter(ImageFilter.MinFilter(11))
  return mask

def set_width_height(w_or_h):
  if not w_or_h:
    return 512
  return int(w_or_h)