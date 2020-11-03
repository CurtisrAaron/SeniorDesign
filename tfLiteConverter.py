import tensorflow as tf
import glob, os, os.path

#tfLiteConverter is a script that converts tensorflow models to tensorflow lite models

count = 0
tffilelist = glob.glob(os.path.join('./tfModels', "*"))

if len(tffilelist)  == 0:
    print("no models found")
    exit()

for model in tffilelist:
    print(str(count) + " " + model)
    count += 1

val = -1
while val == -1:
    try:
        val = int(input("Enter number of model you would like to convert: "))
        if val < 0 or val > (len(tffilelist)- 1):
            val = -1
            print("please enter a valid input")
            count = 0
            print("models to convert - ")

            for model in tffilelist:
                print(str(count) + " " + model)
                count += 1
    except:
        pass

modelname = tffilelist[val]

model = tf.keras.models.load_model(modelname)

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save the model.
with open(f'./tfLiteModels/{modelname.split("/")[2]}.tflite', 'wb') as f:
    f.write(tflite_model)