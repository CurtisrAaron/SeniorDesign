from DbModels import *
import matplotlib.pyplot as plt

# graph the accuracy vs transmission mode
def graphAccuracy(filename = '', showPlot = False):
    connect("Senior-Design-Project", host='mongodb://localhost/test')
    observations = MetaData.objects()

    # lets figure out which transmitter modes exist in this database
    fields = []
    for observation in observations:
        if observation.transmitter_mode not in fields:
            fields.append(observation.transmitter_mode)

    # lets figureout what the model did and didn't get correct
    accuracy = []
    counts = []
    for field in fields:
        numCorrect = len(MetaData.objects(((Q(model_vetted_status='good') & Q(status='good')) | (Q(model_vetted_status='bad') & Q(status='bad'))) & Q(transmitter_mode=field)))
        numTotal = len(MetaData.objects(transmitter_mode = field))
        accuracy.append(numCorrect / numTotal)
        counts.append(numTotal)
    
    fields.append('total')
    totalCount = len(MetaData.objects())
    counts.append(totalCount)
    accuracy.append(len(MetaData.objects(((Q(model_vetted_status='good') & Q(status='good')) | (Q(model_vetted_status='bad') & Q(status='bad'))))) / totalCount)
    # lets plot
    x_pos = [i for i, _ in enumerate(fields)]
    plt.figure(figsize=(10, 10))
    plt.margins(0.4)
    plt.subplots_adjust(left=0.2)
    rects = plt.barh(x_pos, accuracy, color='blue', height = 0.7)
    plt.ylabel("Transmitter mode")
    plt.xlabel("Accuracy")
    plt.margins(x = .35, y=0.02)
    plt.title(f"{filename} - Accuracy vs transmitter mode ")

    plt.yticks(x_pos, fields, rotation = 0)

    for rect, count in zip(rects, counts):
            width = rect.get_width()
            plt.text(width * 1.05 + 0.10, rect.get_y() - 0*rect.get_height()/1.,
                    'acc = %.2f' % width + ', n =  %d' % count,
                    ha='center', va='bottom', rotation = 0)
    if filename != '':
        plt.savefig('./graphs/' + filename, dpi=200)
    if __name__ == '__main__' or showPlot:
        plt.show()
    plt.close()

# calculate accuracy vs score of the CNN model
def scoreDensity():
    connect("Senior-Design-Project", host='mongodb://localhost/test')
    binWidth = 0.01
    fields = []
    accuracy = []
    counts = []
    lowerBound = 0.0
    for i in range(1, int(1 / binWidth) + 1):
        upperBound = i * binWidth
        fields.append(f"{lowerBound:.2f} {upperBound:.2f}")

        numCorrect = len(MetaData.objects(((Q(model_vetted_status='good') & Q(status='good')) | (Q(model_vetted_status='bad') & Q(status='bad'))) & (Q(model_score__lt = upperBound) & Q(model_score__gte = lowerBound))))
        numTotal = len(MetaData.objects(Q(model_score__lt = upperBound) & Q(model_score__gte = lowerBound)))
        if numTotal > 0:
            accuracy.append(numCorrect / numTotal)
        else:
            accuracy.append(0)
        counts.append(numTotal)
        lowerBound = upperBound

    # lets plot
    x_pos = [i for i, _ in enumerate(fields)]
    plt.figure(figsize=(15, 15))
    plt.margins(0.4)
    plt.subplots_adjust(left=0.2)
    rects = plt.barh(x_pos, accuracy, color='blue', height = 0.7)
    plt.ylabel("Transmitter mode")
    plt.xlabel("Accuracy")
    plt.margins(x = .35, y=0.02)
    plt.title(f" - Accuracy vs model score ")

    plt.yticks(x_pos, fields, rotation = 0)

    for rect, count in zip(rects, counts):
            width = rect.get_width()
            plt.text(width * 1.05 + 0.10, rect.get_y() - 0*rect.get_height()/1.,
                    'acc = %.2f' % width + ', n =  %d' % count,
                    ha='center', va='bottom', rotation = 0)
    plt.show()
    plt.close()

if __name__ == '__main__':
    graphAccuracy('')
    scoreDensity()
