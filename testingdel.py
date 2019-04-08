import warnings
from PIL import Image
from skimage.measure import compare_ssim
from skimage.transform import resize
from scipy.stats import wasserstein_distance
from scipy.misc import imsave
from scipy.ndimage import imread
import numpy as np
import cv2
import os.path
##
# Globals
##

warnings.filterwarnings('ignore')

# specify resized image sizes
height = 2**10
width = 2**10

##
# Functions
##

def get_img(path, norm_size=True, norm_exposure=False):
  '''
  Prepare an image for image processing tasks
  '''
  # flatten returns a 2d grayscale array
  img = imread(path, flatten=True).astype(int)
  print(type(img))
  # resizing returns float vals 0:255; convert to ints for downstream tasks
  if norm_size:
    img = resize(img, (height, width), anti_aliasing=True, preserve_range=True)
  if norm_exposure:
    img = normalize_exposure(img)
  return img


def get_histogram(img):
  '''
  Get the histogram of an image. For an 8-bit, grayscale image, the
  histogram will be a 256 unit vector in which the nth value indicates
  the percent of the pixels in the image with the given darkness level.
  The histogram's values sum to 1.
  '''
  h, w = img.shape
  hist = [0.0] * 256
  for i in range(h):
    for j in range(w):
      hist[img[i, j]] += 1
  return np.array(hist) / (h * w) 


def normalize_exposure(img):
  '''
  Normalize the exposure of an image.
  '''
  img = img.astype(int)
  hist = get_histogram(img)
  # get the sum of vals accumulated by each position in hist
  cdf = np.array([sum(hist[:i+1]) for i in range(len(hist))])
  # determine the normalization values for each unit of the cdf
  sk = np.uint8(255 * cdf)
  # normalize each position in the output image
  height, width = img.shape
  normalized = np.zeros_like(img)
  for i in range(0, height):
    for j in range(0, width):
      normalized[i, j] = sk[img[i, j]]
  return normalized.astype(int)


def earth_movers_distance(path_a, path_b):
  '''
  Measure the Earth Mover's distance between two images
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    TODO
  '''
  img_a = get_img(path_a, norm_exposure=True)
  img_b = get_img(path_b, norm_exposure=True)
  hist_a = get_histogram(img_a)
  hist_b = get_histogram(img_b)
  return wasserstein_distance(hist_a, hist_b)


def structural_sim(path_a, path_b):
      '''
      Measure the structural similarity between two images
      @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
      @returns:
    {float} a float {-1:1} that measures structural similarity
      between the input images
      '''
      print('yo1')
      img_a = get_img(path_a)
      print('yo2')
      img_b = get_img(path_b)
      print('yo3')
      sim, diff = compare_ssim(img_a, img_b, full=True)
      return sim


def pixel_sim(path_a, path_b):
  '''
  Measure the pixel-level similarity between two images
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    {float} a float {-1:1} that measures structural similarity
      between the input images
  '''
  img_a = get_img(path_a, norm_exposure=True)
  img_b = get_img(path_b, norm_exposure=True)
  return np.sum(np.absolute(img_a - img_b)) / (height*width) / 255


def sift_sim(path_a, path_b):
  '''
  Use SIFT features to measure image similarity
  @args:
    {str} path_a: the path to an image file
    {str} path_b: the path to an image file
  @returns:
    TODO
  '''
  # initialize the sift feature detector
  orb = cv2.ORB_create()

  # get the images
  img_a = cv2.imread(path_a)
  img_b = cv2.imread(path_b)

  # find the keypoints and descriptors with SIFT
  kp_a, desc_a = orb.detectAndCompute(img_a, None)
  kp_b, desc_b = orb.detectAndCompute(img_b, None)

  # initialize the bruteforce matcher
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

  # match.distance is a float between {0:100} - lower means more similar
  matches = bf.match(desc_a, desc_b)
  similar_regions = [i for i in matches if i.distance < 70]
  if len(matches) == 0:
    return 0
  return len(similar_regions) / len(matches)

img_a = 'Normalized/020_1.bmp'
img_b = ''
folder = 'Normalized'

shifts = []
structsims = []
files = sorted(os.listdir(folder))
print(files)
realshifts = [[]]
realstructsims = [[]]
len(files)
for i in files:
    if i =='.DS_Store':
        continue
    img_a = folder + '/'+i
    print(img_a)
    x = Image.open(img_a)
    l,h = x.size
    if (l < 100 or h < 100) :      ## To be handled
        list.append(realshifts,list())
        list.append(realstructsims,list())
        print(l)
        continue
    shifts = []
    structsims = []
    emds = []
    ##delete below one ::::::: 
    img_a = folder + '/'+'111_1.bmp'
    for filename in files:
        if filename =='.DS_Store':          
            list.append(shifts,0)
            continue
        #print('i is '+filename)
        img_b = folder + '/'+filename
        print('img_b is '+img_b)
        x = Image.open(img_b)
        l,h = x.size
        if (l < 100 or h < 100) :      ## To be handled
            print(l)
            #list.append(structsims,0)
            list.append(shifts,0)
            list.append(emds,0)
            continue

        #----------------- Just tryign the histogram one-------------
        emd = earth_movers_distance(img_a, img_b)
        #structural_sim_1 = structural_sim(img_a,img_b)
    
        #pixel_sim = pixel_sim(img_a,img_b)
        #sift_sim = sift_sim(img_a,img_b)
        sift_sim_1 = sift_sim(img_a,img_b)
    
        #emd = earth_movers_distance(img_a,img_b)
        #print(structural_sim, pixel_sim, sift_sim, emd)
        ### Will remove comment later  ---print('structural_sim is '+str(structural_sim_1))
        print('sift is __ :' + str(sift_sim_1))
        list.append(shifts,sift_sim_1)
        list.append(emds,emd)
        #list.append(structsims,structural_sim_1)
        
    list.append(realshifts,shifts)
    list.append(realstructsims,structsims)


#checking ...
cnt = 0
for j in range(0,len(shifts)):
    if shifts[j] == 1:
            print(str(j))
            cnt= cnt+1
print('cnt is '+ str(cnt))

for i in range(0,len(realshifts)):
    print('for i '+ str(i))
    cnt = 0;
    
    for j in range(0,len(realshifts[i])):
        if realshifts[i][j] == 1 and realstructsims[i][j] > 0.2255:
            print(str(j))
            cnt= cnt+1
    print('cnt is '+ str(cnt))

##REALSHIFTS SAVED IN CSV FORMAT :::
import numpy as np
for i in range(0,len(realshifts)):
    if len(realshifts[i]) >0 :
        np.savetxt("realshifts"+str(i)+".csv", realshifts[i], delimiter=",", fmt='%s')
        np.savetxt("realstructsims"+str(i)+".csv", realstructsims[i], delimiter=",", fmt='%s')



"""
filenames = sorted(os.listdir('Normalized'))  # List all the items in root_dir
for i in filenames:
    print(i)
    img_b = i
    if i =='.DS_Store':          
        continue
  # get the similarity values
    print('error')
    print('imags are' + img_a + img_b)
"""
