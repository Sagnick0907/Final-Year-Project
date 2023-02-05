import cv2
import numpy as np
import utils
import time

########################################################################
pathImage = "a.jpg"
heightImg = 700
widthImg = 700
questions = 5
choices = 5
ans = [1, 2, 0, 2, 4]
########################################################################

while True:
    start = time.time()
    img = cv2.imread(pathImage)

    img = cv2.resize(img, (widthImg, heightImg))  # RESIZE IMAGE
    imgFinal = img.copy()
    imgBlank = np.zeros((heightImg, widthImg, 3), np.uint8)  # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)  # ADD GAUSSIAN BLUR
    imgCanny = cv2.Canny(imgBlur, 10, 70)  # APPLY CANNY

    try:
        # FIND ALL COUNTOURS
        imgContours = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy()  # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)  # DRAW ALL DETECTED CONTOURS
        rectCon = utils.rectContour(contours)  # FILTER FOR RECTANGLE CONTOURS
        biggestPoints = utils.getCornerPoints(rectCon[0])  # GET CORNER POINTS OF THE BIGGEST RECTANGLE
        gradePoints = utils.getCornerPoints(rectCon[1])  # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE

        if biggestPoints.size != 0 and gradePoints.size != 0:
            # BIGGEST RECTANGLE WARPING
            biggestPoints = utils.reorder(biggestPoints)  # REORDER FOR WARPING
            cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20)  # DRAW THE BIGGEST CONTOUR
            pts1 = np.float32(biggestPoints)  # PREPARE POINTS FOR WARP
            pts2 = np.float32([[0, 0], [widthImg, 0], [0, heightImg], [widthImg, heightImg]])  # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2)  # GET TRANSFORMATION MATRIX
            imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))  # APPLY WARP PERSPECTIVE

            # SECOND BIGGEST RECTANGLE WARPING
            cv2.drawContours(imgBigContour, gradePoints, -1, (255, 0, 0), 20)  # DRAW THE BIGGEST CONTOUR
            gradePoints = utils.reorder(gradePoints)  # REORDER FOR WARPING
            ptsG1 = np.float32(gradePoints)  # PREPARE POINTS FOR WARP
            ptsG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])  # PREPARE POINTS FOR WARP
            matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)  # GET TRANSFORMATION MATRIX
            imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))  # APPLY WARP PERSPECTIVE

            # APPLY THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)  # CONVERT TO GRAYSCALE
            imgThresh = cv2.threshold(imgWarpGray, 170, 255, cv2.THRESH_BINARY_INV)[1]  # APPLY THRESHOLD AND INVERSE

            # GET INDIVIDUAL BOXES
            boxes = utils.splitBoxes(imgThresh)
            # cv2.imshow("Split Test ", boxes[3])

            # OBTAINING THE NUMBER OF NON-ZERO PIXELS FOR EACH BOX
            countR = 0
            countC = 0
            myPixelVal = np.zeros((questions, choices))  # TO STORE THE NON ZERO VALUES OF EACH BOX
            for image in boxes:
                # cv2.imshow(str(countR)+str(countC),image)
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countR][countC] = totalPixels
                countC += 1
                if (countC == choices):
                    countC = 0
                    countR += 1

            # FIND THE USER ANSWERS AND PUT THEM IN A LIST
            myIndex = []
            for x in range(0, questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr == np.amax(arr))
                myIndex.append(myIndexVal[0][0])
            # print("USER ANSWERS",myIndex)

            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading = []
            for x in range(0, questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:
                    grading.append(0)
            # print("GRADING",grading)
            score = (sum(grading) / questions) * 100  # FINAL GRADE
            print("SCORE",score)

            # DISPLAYING ANSWERS
            utils.showAnswers(imgWarpColored, myIndex, grading, ans)  # DRAW DETECTED ANSWERS
            utils.drawGrid(imgWarpColored)  # DRAW GRID
            imgRawDrawings = np.zeros_like(imgWarpColored)  # NEW BLANK IMAGE WITH WARP IMAGE SIZE
            utils.showAnswers(imgRawDrawings, myIndex, grading, ans)  # DRAW ON NEW IMAGE
            invMatrix = cv2.getPerspectiveTransform(pts2, pts1)  # INVERSE TRANSFORMATION MATRIX
            imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg))  # INV IMAGE WARP

            # DISPLAY GRADE
            imgRawGrade = np.zeros_like(imgGradeDisplay, np.uint8)  # NEW BLANK IMAGE WITH GRADE AREA SIZE
            cv2.putText(imgRawGrade, str(int(score)) + "%", (70, 100)
                        , cv2.FONT_HERSHEY_COMPLEX, 3, (0, 255, 255), 3)  # ADD THE GRADE TO NEW IMAGE
            invMatrixG = cv2.getPerspectiveTransform(ptsG2, ptsG1)  # INVERSE TRANSFORMATION MATRIX
            imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg))  # INV IMAGE WARP

            # SHOW ANSWERS AND GRADE ON FINAL IMAGE
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1, 0)
            imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1, 0)

            # IMAGE ARRAY FOR DISPLAY
            imageArray = ([img, imgGray, imgCanny, imgContours],
                          [imgBigContour, imgThresh, imgWarpColored, imgFinal])
            cv2.imshow("Final Result", imgFinal)

    except:
        print("Image cannot be processed.")
        imageArray = ([img, imgGray, imgCanny, imgContours],
                      [imgBlank, imgBlank, imgBlank, imgBlank])

    end = time.time()
    print("Time Taken: ", end-start)
    # LABELS FOR DISPLAY
    lables = [["Original", "Gray", "Edges", "Contours"],
              ["Biggest Contour", "Threshold", "Warpped", "Final"]]

    stackedImage = utils.stackImages(imageArray, 0.5, lables)

    cv2.imshow('Result', stackedImage)
    cv2.waitKey(5000)