'''
Created on Apr 26, 2017

@author: William
'''
from edu.gmu.cs.ai.cs580.project.imageclassification import DatasetLoader
from keras.models import load_model

# returns a compiled model
# identical to the previous one
model = load_model('C:/KerasModels/Model 2017-04-25 19-11-59/CarIdentificationModel.h5')
print("Model has been reloaded.")

(x_predict, y_predict, z_predict) = DatasetLoader.getDatasetForPrediction([0])
print("Dataset is loaded.")

modelPredictions = model.predict(x_predict)
print("Got predictions.")

predictCarCorrect = 0
predictCarNotCorrect = 0
predictNotCarCorrect = 0
predictNotCarNotCorrect = 0

imgNum = 0
totalImages = y_predict.shape[0]
while imgNum < totalImages:
    actual = y_predict[imgNum]
    prediction = 1

    if modelPredictions[imgNum][0] > modelPredictions[imgNum][1]:
        prediction = 0

    if prediction == 1:
        if actual == 1:
            predictCarCorrect += 1
            if predictCarCorrect <= 10:
                print("TP: " + str(z_predict[imgNum]))
        else:
            predictCarNotCorrect += 1
            if predictCarNotCorrect <= 10:
                print("FP: " + str(z_predict[imgNum]))

    elif prediction == 0:
        if actual == 0:
            predictNotCarCorrect += 1
            if predictNotCarCorrect <= 10:
                print("TN: " + str(z_predict[imgNum]))
        else:
            predictNotCarNotCorrect += 1
            if predictNotCarNotCorrect <= 10:
                print("FN: " + str(z_predict[imgNum]))
    else:
        print("Ooops - bad prediction value")

    imgNum += 1

print("Got predictions.")
print("predictCarCorrect = " + str(predictCarCorrect))
print("predictCarNotCorrect = " + str(predictCarNotCorrect))
print("predictNotCarCorrect = " + str(predictNotCarCorrect))
print("predictNotCarNotCorrect = " + str(predictNotCarNotCorrect))
