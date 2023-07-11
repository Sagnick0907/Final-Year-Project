# Final-Year-Project
# Optical Mark Recognition using Python & OpenCV  

## Table of Content
  * [Demo](#demo)
  * [Overview](#overview)
  * [Goal](#goal)
  * [Technical Aspect](#technical-aspect)
  * [Technologies Used](#technologies-used)

## Demo
![image](https://github.com/Sagnick0907/Final-Year-Project/assets/76872499/ed8884d6-9d38-4620-a127-4480fa26857e)
![2nd image](https://github.com/Sagnick0907/Final-Year-Project/assets/76872499/2f13e811-424e-4cfc-8c15-2505cff5e97e)
Result:  
![Final 2nd img](https://github.com/Sagnick0907/Final-Year-Project/assets/76872499/ca89223c-c4eb-4d69-b58c-63601dfc3e8c)


## Overview  
Optical Mark Recognition (OMR) is the process of reading information that people mark on surveys, tests and other paper documents. The concept behind this paper is to develop a system that can check and evaluate the MCQ answers using the webcam. Till date many institutions and organization held many exams where user is provided with a separate question and answer sheet, where answer is multiple choice option, each option may be a square or circle and user is supposed to either tick or fill it using pen or pencil. In our project, we are going to create an Optical Mark Recognition algorithm in python using OpenCV right from scratch on PyCharm IDE. We can either use a student’s pre-saved OMR sheet image or use the webcam to scan the OMR sheet. The code produces instantaneous results which includes display of correct and wrong marked answers along with the final result over the image of student’s OMR sheet. We can also design the code such that we can handle different types of question format (number of questions & options). There would be not much problem even if the image is a slightly tilted view of the sheet but clear images and properly darkened circles are advisable. There is an additional functionality to save the resultant image also. A single OMR solution helps design, scan, and read OMR sheets in very less time. We can re-read the faulty data or make additional features to calculate the chances of cheating. So, with an OMR software, it is easy for educational intuitions to streamline the entire task thus increasing accuracy and time management.   

## Motivation and Goal  
At present OMR technology is very expensive because of which regular educational institutions cannot avail it and thus resort to manual checking of papers where they note down all the answers and match them with official answer key for each given student to obtain the result. On an average based on number of question’s evaluating each paper may take around 5 minutes. Hence if there are 100 students then it will take around 500 minutes or 8.3 hours of long monotonous evaluation. The main purpose of our project is to save money, time and manpower and also increase accuracy by automating this trivial task of checking and matching the answers for thousands of papers. Our OMR application might not match the flexibility and performance of a high-level OMR scanner used by various institutes yet but it fulfils the basic needs of various institutions and organizations.  

## Technical Aspect  

Our proposed methodology involves generating results from a marked OMR sheets using inbuilt image transformation functions, contour detection and display functions. We will be using OpenCV library in the back-end and Tkinter library for UI. 
Firstly, we design the OMR template for the question which we will be scanning. 
![image](https://github.com/Sagnick0907/Final-Year-Project/assets/76872499/040b0292-85af-455c-af2e-0d4440eae31f) | ![image](https://github.com/Sagnick0907/Final-Year-Project/assets/76872499/37487be8-2508-4b32-b156-8dce73ceee68)
 |  
Then we will discuss the detailed backend working of our system and cover the basic intuition of how system is working. 
1.	For taking inputs, we have 2 options: (i). To take a snapshot of the answer sheet and select it from the target directory or, (ii). Produce the output over the answer sheet in real-time using webcam. For this, we have used webCamFeed and cv2.VideoCapture() named functions from OpenCV. 
2.	Then we will create multiple copies of the image in Gray scale format, used Gaussian blur to create blurred format & Canny function to detect edges. This makes it helpful for easily detecting marked/ highlighted points by user. The high blur helps reduce the high frequency noise, that means distortion of image. Also created a custom function for displaying multiple images simultaneously.
3.	The next step will be to extract the biggest contour from the given image. We will use the cv2.findContours and custom-made complex functions to find all the 4-cornered point contours sorted in descending order (Here, the largest rectangle bounds the bubbles/options & the 2nd largest figure is where the result is to be displayed).
4.	After getting the outline, we used a reorder function to find & fix the 4 corner points of that contour so that they don’t get jumbled up later. We then use getPerspectiveTransform() such that it gives top-down, bird’s eye view of previous 2 images. This gives a get 90-degree view of our image.  
5.	The 5th step is to extract bubble options present within the answer page for this we again use perspective transformation and binarization. In order to find the bubbles within image there are many ways. Here use SplitBoxes() custom function to split the rectangle image into horizontal and vertical slices as per the no. of question and choices and then store the resultant square images in a nested array and return it.
6.	In order to know which option is marked, we will iterate through all the images one by one for each row and find the image/option with the maximum number of pixels and store this option as the answer of that row in a resultant matrix. Now we create a function that checks whether each highlighted answer is correct or not. Here one has to provide the array of our answer before. Now iterate through the resultant array that was obtained earlier and compare each option with the actual answer array to check whether it is correct or not.
7.	Now for the grading, we compare the result we got above with the actual result and calculate the percentage.
8.	Finally, we will display the answer. The correct answer is highlighted with green colour whereas wrong answer is highlighted with red colour using cv2.circle function of OpenCV. We do an inverse transformation of these highlighted circles so that they appear on the original mark sheet. Similarly, we display the percentage obtained on the answer box of the image.

For the frontend section we used the following approach:
1.	We used Tkinter GUI Toolkit for building the GUI for our OMR evaluation software.
2.	In it we included labels and buttons for designing the GUI using grid methodology.
3.	Three buttons are created: Upload Image button, Check Score button and Webcam live Checking button.
4.	Then connected the appropriate functions for the different functionalities of the buttons.

![image](https://github.com/Sagnick0907/Final-Year-Project/assets/76872499/8ad4e338-52e4-4daf-9766-6954d0f07a00)

## Technologies Used
- Pycharm
- Tkinter Library
- Concepts used : Random Forest Regressor + Hyperparameter Tuning(Randomized CV)
- Libraries: pandas, numpy, seaborn, matplotlib, sk-learn, etc.
