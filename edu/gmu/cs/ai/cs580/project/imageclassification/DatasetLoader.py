from PIL import Image
from edu.gmu.cs.ai.cs580.project.imageclassification import Constants
from os import listdir
from os.path import isfile, isdir, join, exists, getsize

def load_image(file_path):
    # imgFile = open(file_path, 'rb')
    # imgContent = imgFile.read()
    imgObj = Image.open(file_path).convert("RGB")
    bytelist = list(imgObj.getdata())
    expandedbytelist = list(sum(bytelist, ()))

    return expandedbytelist

    # imgArr = array(imgObj)
    # test = imgObj.getpixel((35, 23))

    # imgObj.get
    # print(imgContent.shape)
    # #print(len(expandedbytelist))
    # print(expandedbytelist[0])

    # print(test)

    # newArr1 = [item for sublist in imgArr for item in sublist]
    # newArr2 = [item for newArr1 in imgArr for item in sublist]

    # print(newArr2.shape)


'''
     Use 20% of the images for testing. Specify a number (0-4) to indicate which images to add to the test set.
'''
def getDataset(testDataSuffixList = [0]):
    baseFolderDir = Constants.BASE_DATASET_FOLDER
    trainingImages = []
    trainingResult = []
    testImages = []
    testResult = []

    subjectFolders = listdir(baseFolderDir)

    for subjectFolder in subjectFolders:
        fullSubjectFolder = baseFolderDir + subjectFolder
        if isdir(fullSubjectFolder):
            annotationFilePath = fullSubjectFolder + "/annotation.txt"
            print("Annotation file = " + annotationFilePath)

            annotationFile = open(annotationFilePath)
            fileContents = annotationFile.readlines();

            searchTerm = fileContents[0].rstrip()
            result = int(fileContents[1].rstrip())
            imageCount = int(fileContents[2].rstrip())

            print("search term = " + str(searchTerm) + ", result = " + str(result) + ", count = " + str(imageCount))

            subjectImageFolder = fullSubjectFolder + "/Thumbnails_36_24/"
            imageNumber = 1

            while imageNumber <= imageCount:
                imageFilename = subjectImageFolder + str(imageNumber).zfill(4) + '.jpg'
                if exists(imageFilename) and isfile(imageFilename):
                    imageSize = getsize(imageFilename)
                    if imageSize > 0:
                        imageArray = load_image(imageFilename)
                        if imageNumber % 10 in testDataSuffixList:
                            testImages.append(imageArray)
                            testResult.append(result)
                        else:
                            trainingImages.append(imageArray)
                            trainingResult.append(result)

                imageNumber += 1


    trainingSet = (trainingImages, trainingResult)
    testSet = (testImages, testResult)

    return trainingSet, testSet

    # onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


x, y = getDataset([0])
print("Training size = " + str(len(x[0])))
print("Test size = " + str(len(y[0])))

# load_image("C:/imageDownloads/2017-04-14 15-05-00 (Mitsubishi Lancer)/Thumbnails_36_24/0001.jpg")


