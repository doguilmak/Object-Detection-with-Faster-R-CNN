# -*- coding: utf-8 -*-
"""use_objectdetection_faster_r_cnn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1N4D5likdq3Ju2oOqMpe8Mna3dxt_WeuI

**<h1 align=center><font size = 5>Object Detection with Faster R-CNN</font></h1>**

<br>

<img src="https://cdn.shopify.com/s/files/1/0533/4158/5598/articles/how-to-run-tensorflow-object-detection-in-real-time-with-raspberry-v2-csi-camera-on-nvidia-jetson-nano-447485.jpg?v=1659971239" width=1000 height=500 alt="https://www.forecr.io/blogs/ai-algorithms/how-to-run-tensorflow-object-detection-in-real-time-with-raspberry-v2-csi-camera-on-nvidia%C2%AE-jetson%E2%84%A2-nano%E2%84%A2">

<small>Picture Source: <a href="https://www.forecr.io/blogs/ai-algorithms/how-to-run-tensorflow-object-detection-in-real-time-with-raspberry-v2-csi-camera-on-nvidia%C2%AE-jetson%E2%84%A2-nano%E2%84%A2">forecr</a>

<br>

<h2>Description</h2>

<br>

<h3>Context</h3>

<p>Faster R-CNN is a method for object detection that uses region proposal. In this lab, you will use Faster R-CNN pre-trained on the coco dataset. You will learn how to detect several objects by name and to use the likelihood of the object prediction being correct.</p>

<br>

<h3>Training for Object Detection</h3>
<p>Object detection is based on two principles. The first is the learnable parameters in the created rectangle (box), and the second is the size of the created box (coordinate information). While the model is being trained, ground truth and prediction values ​​are evaluated with the difference of squares. Evaluations depend on the size of the ground truth rectangles created through functions. The functions calculate the difference between the ground truth box and the predicted rectangle.</p>

<br>

<h3>Object Detection Models</h3>

<p>Types of Object Detection Sliding window techniques are slow. Fortunately, there are two major types of object detection that speed up the process. <i>Region-based object detection</i> breaks up the image into regions and performs a prediction, while <i>Single-Stage object detection </i>uses the entire image.</p>

<ul>
<li><i>Region-Based Convolutional Neural Network (R-CNN)</i> are usually more accurate but slower; they include R-CNN, fast RCNN and Faster RCNN.</li>

<li><i>Single-Stage</i> methods are faster but less accurate and include techniques like Single Shot Detection (SSD) and You Only Look Once (YOLO).</li>
</ul>

<br>

<p>In the following two labs, you will use Faster RCNN for prediction. You will train an SSD model, even though SSD is considerably faster than other methods, it will still take a long time to train. Therefore we will train most of the model for you, and you will train the model for the last few iterations.</p>

<br>

<h3>Faster R-CNN</h3>

<p>Faster R-CNN uses the more convenient Region Proposal Network instead of costly selective search.</p>

<p>Faster R-CNN can be analyzed in two stages:</p>

<ul>
  <li><b>Region Proposal Network (RPN):</b> The first stage, RPN, is a deep convolutional neural network for suggesting regions. RPN takes any size of input as input and generates a rectangular proposal that may belong to a set of objects based on the object score. It makes this suggestion by shifting a small mesh over the feature map generated by the convolutional layer.</li>

  <li><b>Fast R-CNN:</b> These calculations produced by RPN are inserted into the Fast R-CNN architecture and the class of the object is estimated with a classifier and the bounding box is estimated with a regressor.</li>
</ul>

<br>

<h3>Keywords</h3>
<ul>
  <li>Faster R-CNN</li>
  <li>Object Detection</li>
  <li>ResNet-50-FPN</li>
  <li>COCO</li>
</ul>

<br>
    
<h3>Sources</h3>
<ul>
    <li><a href="https://www.ibm.com/">IBM</a></li>
    <li><a href='https://github.com/jsantarc'>Joseph Santarcangelo</a></li>
    <li><a href="https://pytorch.org/vision/main/models/generated/torchvision.models.detection.retinanet_resnet50_fpn.html">PyTorch</a></li>
    <li><a href='https://arxiv.org/abs/1506.01497'>Computer Vision and Pattern Recognition - Cornell University<a/></li>
    <li><a href='https://pillow.readthedocs.io/en/stable/index.html?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkCV0101ENCoursera25797139-2021-01-01'>Pillow Docs</a></li>
    <li><a href='https://opencv.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkCV0101ENCoursera25797139-2021-01-01'>OpenCV</a></li>
    <li><a href="https://www.forecr.io/blogs/ai-algorithms/how-to-run-tensorflow-object-detection-in-real-time-with-raspberry-v2-csi-camera-on-nvidia%C2%AE-jetson%E2%84%A2-nano%E2%84%A2">forecr</a></li>
    <li>Gonzalez, Rafael C., and Richard E. Woods. "Digital image processing." (2017).</li>
</ul>

<br>

<h1>Objective for this Notebook</h1>

<p>Apply Object detection with Faster R-CNN to classify predetermined objects using objects name and/or to use the likelihood of the object.</p>

<div class="alert alert-block alert-info" style="margin-top: 20px">
<li><a href="https://#importing_libraries">Import Libraries and Define Auxiliary Functions</a></li>
<li><a href="https://#load_faster_rcnn">Load Pre-trained Faster R-CNN</a></li>
<li><a href="https://#object_localization">Object Localization</a></li>
<li><a href="https://#test_model_uploaded">Test Model With an Uploaded Image</a></li>
<br>
<p></p>
Estimated Time Needed: <strong>30 min</strong>
</div>

<hr>

Download the image for the labs:
"""

! wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-CV0101EN-Coursera/images%20/images_part_5/DLguys.jpeg
! wget https://www.ajot.com/images/uploads/article/quantas-car-v-plane-TAKE-OFF.jpg
! wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-CV0101EN-Coursera/images%20/images_part_5/istockphoto-187786732-612x612.jpeg
! wget https://cdn.webrazzi.com/uploads/2015/03/andrew-ng1.jpg

"""<br>

<a id="importing_libraries"></a>

<h2 align=center>Import Libraries and Define Auxiliary Functions</h2>

Deep-learning libraries, may have to update:

You may need to install and import <code>condacolab</code> if you are going to use the notebook on Colab.
"""

!pip install -q condacolab
import condacolab
condacolab.install()

! conda install pytorch=1.1.0 torchvision -c pytorch -y

import torchvision
from torchvision import  transforms 
import torch
from torch import no_grad

"""Importing <code>request</code> library for getting data from the web

"""

import requests

"""libraries  for image processing and visualization

"""

import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

"""This function will assign a string name to a predicted class and eliminate predictions whose likelihood  is under a threshold.

"""

def get_predictions(pred, threshold=0.8, objects=None):
    """
    This function will assign a string name to a predicted class and eliminate predictions whose likelihood  is under a threshold 
    
    pred: a list where each element contains a tuple that corresponds to information about  the different objects; Each element includes a tuple with the class yhat, probability of belonging to that class and the coordinates of the bounding box corresponding to the object 
    image : frozen surface
    predicted_classes: a list where each element contains a tuple that corresponds to information about  the different objects; Each element includes a tuple with the class name, probability of belonging to that class and the coordinates of the bounding box corresponding to the object 
    thre
    """


    predicted_classes= [(COCO_INSTANCE_CATEGORY_NAMES[i],p,[(box[0], box[1]), (box[2], box[3])]) for i,p,box in zip(list(pred[0]['labels'].numpy()),pred[0]['scores'].detach().numpy(),list(pred[0]['boxes'].detach().numpy()))]
    predicted_classes=[  stuff  for stuff in predicted_classes  if stuff[1]>threshold ]
    
    if objects  and predicted_classes :
        predicted_classes=[ (name, p, box) for name, p, box in predicted_classes if name in  objects ]
    return predicted_classes

"""Draws box around each object

"""

def draw_box(pred_class, img, rect_th=2, text_size=0.5, text_th=2, download_image=False, img_name="img"):
    """
    draws box around each object 
    
    predicted_classes: a list where each element contains a tuple that corresponds to information about the different objects; Each element includes a tuple with the class name, probability of belonging to that class and the coordinates of the bounding box corresponding to the object 
    image : frozen surface 
   
    """
    image = (np.clip(cv2.cvtColor(np.clip(img.numpy().transpose((1, 2, 0)), 0, 1), cv2.COLOR_RGB2BGR), 0, 1) * 255).astype(np.uint8).copy()

    for predicted_class in pred_class:
      
      label=predicted_class[0]
      probability=predicted_class[1]
      box=predicted_class[2]
      t = round(box[0][0].tolist())
      l = round(box[0][1].tolist())
      r = round(box[1][0].tolist())
      b = round(box[1][1].tolist())

      # Giving brief information about rectange, class and probability.
      from colorama import Fore
      from colorama import Style
      print(f"\nLabel: {Fore.GREEN}{label}{Style.RESET_ALL}")
      print(f"Box coordinates: {t}, {l}, {r}, {b}")
      print(f"Probability: {probability}")

      # Drawing rectangle and adding text on the picture based on their class and size.
      cv2.rectangle(image, (t, l), (r, b), (0, 255, 0), rect_th)
      cv2.rectangle(image, (t, l), (t+110, l+17), (255, 255, 255), -1)
      cv2.putText(image, label, (t+10, l+12),  cv2.FONT_HERSHEY_SIMPLEX, 
                  text_size, (0,255,0), thickness=text_th)
      cv2.putText(image, label+": "+str(round(probability, 2)), 
                  (t+10, l+12),  cv2.FONT_HERSHEY_SIMPLEX, text_size, 
                  (0, 255, 0),thickness=text_th)

    # Plotting image
    image = np.array(image)
    plt.figure(figsize=(15, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if download_image:
      plt.savefig(f'{img_name}.png')
    else:
      pass
    plt.show()
    
    del(img)
    del(image)

"""This function  will speed up your code by freeing memory:

"""

def save_RAM(image_=False):
    global image, img, pred
    torch.cuda.empty_cache()
    del(img)
    del(pred)
    if image_:
        image.close()
        del(image)

"""<br>

<a id="load_faster_rcnn"></a>

<h2 align=center>Load Pre-trained Faster R-CNN</h2>

<a href='https://arxiv.org/abs/1506.01497?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkCV0101ENCoursera25797139-2021-01-01'>Faster R-CNN</a> is a model that predicts both bounding boxes and class scores for potential objects in the image  pre-trained on <a href="https://cocodataset.org/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkCV0101ENCoursera25797139-2021-01-01">COCO</a>. Faster R-CNN model with a ResNet-50-FPN backbone from <a href='https://arxiv.org/abs/1506.01497'>the Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks paper.</a>

<br>
"""

model_ = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model_.eval()

for name, param in model_.named_parameters():
    param.requires_grad = False
print("done")

"""the function calls Faster R-CNN <code> model\_ </code> but save RAM:

"""

def model(x):
    with torch.no_grad():
        yhat = model_(x)
    return yhat

"""Here are the 91 classes.

"""

COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]
len(COCO_INSTANCE_CATEGORY_NAMES)

"""<br>

<a id="object_localization"></a>

<h2 align=center>Object Localization</h2>

In Object Localization we locate the presence of objects in an image and indicate the location with a bounding box. Consider the image of <a href="https://www.linkedin.com/in/andrewyng">Andrew Ng</a>
"""

img_path='andrew-ng1.jpg'
half = 0.5
image = Image.open(img_path)

image.resize([int(half * s) for s in image.size] )
plt.figure(figsize=(15, 10))
plt.imshow(image)
plt.show()

"""<p>We will create a transform object to convert the image to a tensor.</p>

"""

transform = transforms.Compose([transforms.ToTensor()])

img = transform(image)

"""<p>Let's print out our image:</p>"""

img

"""<p>We can make a prediction,The output is a dictionary with several predicted classes, the probability of belonging to that class and the coordinates of the bounding box corresponding to that class.</p>

"""

pred = model([img])

"""<p><b>note</b>:  if you call <code>model\_(\[img])</code>  directly but it will use more RAM</p>

"""

len(pred[0]['labels'])

"""we have the 2  different class predictions, ordered by likelihood scores for potential objects.

"""

pred[0]['labels']

"""We have the likelihood of each class:

"""

pred[0]['scores']

"""<p>The class number corresponds to the index of the list with the corresponding  category name.</p>

"""

index=pred[0]['labels'][0].item()
COCO_INSTANCE_CATEGORY_NAMES[index]

"""<p>We have the coordinates of the bounding box.</p>

"""

bounding_box=pred[0]['boxes'][0].tolist()
bounding_box

"""<p>These components correspond to the top-left corner and bottom-right corner of the rectangle, more precisely: <b>top(t), left(l), bottom(b), right(r).</b></p>

<p>We need to round them, otherwise we can't show it on picure.</p>
"""

t, l, r, b = [round(x) for x in bounding_box]
print(t, l, r, b)

"""We convert the tensor to an OpenCV array and plot an image with the box:

"""

img_plot=(np.clip(cv2.cvtColor(np.clip(img.numpy().transpose((1, 2, 0)), 0, 1), cv2.COLOR_RGB2BGR), 0, 1) * 255).astype(np.uint8)
cv2.rectangle(img_plot, (t, l), (r, b), (0, 255, 0), 10) # Draw Rectangle with the coordinates
plt.figure(figsize=(15, 10))
plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
plt.show()
del img_plot, t, l, r, b

"""We can localize objects; we do this using the function <code>get_predictions</code>. The input  is the predictions <code>pred</code> and the <code>objects</code> you would like to localize.

<b>Loss equasion:</b>

$$||box\ - \hat{box}||^2 = (y_{min} - \hat{y_{min}})^2 + (y_{max} - \hat{y_{max}})^2 + (x_{min} - \hat{x_{min}})^2 + (x_{max} - \hat{x_{max}})^2$$

<br>
"""

pred_class=get_predictions(pred, objects="person")
draw_box(pred_class, img)

del pred_class

"""We can set a threshold <code>threshold</code>. Here we set the  threshold 1 i.e Here we set the  threshold 1 i.e. 100% likelihood.

"""

get_predictions(pred, threshold=1, objects="person")

"""Here we have no output as the likelihood is not 100%.  Let's try a threshold of 0.98 and use the function  draw_box to draw the box and plot the class and it's rounded likelihood.

"""

pred_thresh=get_predictions(pred, threshold=0.98, objects="person")
draw_box(pred_thresh, img, download_image=True, img_name="andrew_BOX")
del pred_thresh

"""Delete objects to save memory, we will run this after every cell:

"""

save_RAM(image_=True)

"""We can locate multiple objects, consider the following <a href='https://www.kdnuggets.com/2015/03/talking-machine-deep-learning-gurus-p1.html?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkCV0101ENCoursera25797139-2021-01-01'>image</a>, we can detect the people in the image.

"""

img_path='DLguys.jpeg'
image = Image.open(img_path)
image.resize([int(half * s) for s in image.size])
plt.figure(figsize=(15, 10))
plt.imshow(np.array(image))
plt.show()

"""we can set a threshold to detect the object, 0.9 seems to work.

"""

img = transform(image)
pred = model([img])
pred_thresh=get_predictions(pred, threshold=0.8)
draw_box(pred_thresh, img, rect_th=1, text_size= 0.5, text_th=1)

del pred_thresh

"""Or we can use objects parameter:

"""

pred_obj=get_predictions(pred,objects="person")
draw_box(pred_obj, img, rect_th=1,text_size= 0.5, text_th=1, download_image=True, img_name="dl_guys_IBM_BOX")

del pred_obj

"""If we set the threshold too low, we will detect objects that are not there.

"""

pred_thresh=get_predictions(pred,threshold=0.01)
draw_box(pred_thresh, img, rect_th= 1, text_size=0.5, text_th=1)

del pred_thresh

"""the following lines will speed up your code by using less RAM.

"""

save_RAM(image_=True)

"""## Object Detection

In Object Detection we find the classes as well detect the objects in an image. Consider the following <a href="https://www.dreamstime.com/stock-image-golden-retriever-puppy-lying-parakeet-perched-its-head-weeks-old-next-to-british-shorthair-kitten-sitting-image30336051?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkCV0101ENCoursera25797139-2021-01-01">image</a>
"""

img_path='istockphoto-187786732-612x612.jpeg'
image = Image.open(img_path)
image.resize( [int(half * s) for s in image.size])
plt.figure(figsize=(15, 10))
plt.imshow(np.array(image))
plt.show()
del img_path

"""If we set a threshold, we can detect all objects whose likelihood is above that threshold.

"""

img = transform(image)
pred = model([img])
pred_thresh=get_predictions(pred,threshold=0.97)
draw_box(pred_thresh,img,rect_th=1, text_size=1, text_th=1, download_image=True, img_name="dog_cat_bird_BOX")

del pred_thresh

"""We can specify the objects we would like to classify, for example, cats and dogs:

"""

# img = transform(image)
# pred = model([img])
pred_obj=get_predictions(pred, objects=["dog","cat"])
draw_box(pred_obj, img,rect_th=1, text_size= 0.5, text_th=1)
del pred_obj

"""If we set the threshold too low, we may detect objects with a low likelihood of being correct; here, we set the threshold to 0.7, and we incorrectly  detect a cat

"""

# img = transform(image)
# pred = model([img])
pred_thresh=get_predictions(pred, threshold=0.70, objects=["dog", "cat"])
draw_box(pred_thresh, img, rect_th= 1, text_size=1, text_th=1)

del pred_thresh

save_RAM(image_=True)

"""We can detect other objects. Consider the following <a href='https://www.flickr.com/photos/watts_photos/27581126637?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkCV0101ENCoursera25797139-2021-01-01'>image</a>; We can detect cars and airplanes

"""

img_path='quantas-car-v-plane-TAKE-OFF.jpg'
image = Image.open(img_path)
image.resize( [int(half * s) for s in image.size])
plt.figure(figsize=(15, 10))
plt.imshow(np.array(image))
plt.show()
del img_path

img = transform(image)
pred = model([img])
pred_thresh=get_predictions(pred, threshold=0.997)
draw_box(pred_thresh, img, download_image=True, img_name="car_plane_BOX")
del pred_thresh

save_RAM(image_=True)

"""<br>

<a id="test_model_uploaded"></a>

<h2 align=center>Test Model With an Uploaded Image</h2>

Replace with the name of your image as seen in your directory into <code>img_path</code> variable.
"""

from pathlib import Path
print("Directory Path:", Path().absolute())

img_path = str(Path().absolute())+'/me.jpg'
image = Image.open(img_path)
plt.figure(figsize=(10, 15))
plt.imshow(np.array(image))
plt.show()

img = transform(image )
pred = model(img.unsqueeze(0))
pred_thresh=get_predictions(pred,threshold=0.95)
draw_box(pred_thresh, img, download_image=True, img_name="me_BOX")

"""<br>

<h1>Contact Me<h1>
<p>If you have something to say to me please contact me:</p>

<ul>
  <li>Twitter: <a href="https://twitter.com/Doguilmak">Doguilmak</a></li>
  <li>Mail address: doguilmak@gmail.com</li>
</ul>
"""

from datetime import datetime
print(f"Changes have been made to the project on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
