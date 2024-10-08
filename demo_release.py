
import argparse
import matplotlib.pyplot as plt

from colorizers import *

# handel argrs
parser = argparse.ArgumentParser()
parser.add_argument('-i','--img_path', type=str, default='imgs/me.jpeg')
parser.add_argument('--use_gpu', action='store_true', help='whether to use GPU')
parser.add_argument('-o','--save_prefix', type=str, default='saved', help='will save into this file with {eccv16.png, siggraph17.png} suffixes')
options = parser.parse_args() 

# load colorizers
colorizer_eccv16 = eccv16(pretrained=True).eval()
colorizer_siggraph17 = siggraph17(pretrained=True).eval()
if(options.use_gpu):
	colorizer_eccv16.cuda()
	colorizer_siggraph17.cuda()

# default size to process images is 256x256
# grab L channel in both original ("orig") and resized ("rs") resolutions
img = load_img(options.img_path)
(tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
if(options.use_gpu):
	tens_l_rs = tens_l_rs.cuda()
	
img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
out_img_eccv16 = postprocess_tens(tens_l_orig, colorizer_eccv16(tens_l_rs).cpu())
out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

plt.imsave('%s_eccv16.png'%options.save_prefix, out_img_eccv16)
plt.imsave('%s_siggraph17.png'%options.save_prefix, out_img_siggraph17) #%s = palce holder

plt.figure(figsize=(12,8))
plt.subplot(2,2,1)
plt.imshow(img)
plt.title('Original image')
plt.axis('off')

plt.subplot(2,2,2)
plt.imshow(img_bw)
plt.title('Input image')
plt.axis('off')

plt.subplot(2,2,3)
plt.imshow(out_img_eccv16)
plt.title('Output image (ECCV 16)')
plt.axis('off')

plt.subplot(2,2,4)
plt.imshow(out_img_siggraph17)
plt.title('Output image (SIGGRAPH 17)')
plt.axis('off')
plt.show()