import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.svm import SVC,LinearSVC
from sklearn import preprocessing
import numpy as np
from io import BytesIO
from flask import g
from matplotlib.figure import Figure

'''
def show_label_distribution(sess):

    label_count = sess['label_count']
    non_label_count = sess['non_label_count']
    width = 0.25

    fig = Figure(figsize=(2, 3),layout='constrained')
    ax= fig.subplots()
    rects= ax.bar('not angry',non_label_count,width)
    ax.bar_label(rects, label_type='edge')

    rects= ax.bar('angry',label_count,width)
    ax.bar_label(rects, label_type='edge')

    ax.set_title('Distribution of labels')
    ax.tick_params(axis='y',labelsize=7)
    ax.tick_params(axis='y',labelsize=7)
    ax.title.set_size(10)
    #ax.set_xticks(x+width,xlabels)
    ax.set_ylim(0, 1500)
# use save to file instead
    buf = BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    return buf
'''
class EvaluateResults():

    def __init__(self):
        # add vars for label distribution text
        # the function for that basically takes any form setting that't not 'all'
        self.features = []
        self.labels = []
        self.X_train= []
        self.X_test= []
        self.y_train= []
        self.y_test = []
        self.label_ids=[]
        self.label_desc=""


    def make_label_distribution_labels(self,record):

        label_string = ['Labeled records: ']

        if record.filters['actor'] != 'all':
            label_string.append(f'actor: {record.filters['actor']} ')

        if record.filters['sex'] != 'all':
             label_string.append(f'sex: {record.filters['sex']} ')

        if record.filters['statement'] != 'all':
            label_string.append(f'statement: {record.filters['statement']} ')

        if len(record.filters['emotion']) != 0 and record.filters['emotion'][0] != 'all':

            em = [emo for emo in record.filters['emotion']]
        
            
            label_string.append(f'emotion(s): {em} ')
     

        if record.filters['intensity'] != 'all':
             label_string.append(f'intensity: {record.filters['intensity'] } ')


        label_string.append(f'mels: {record.filters['num_mels']}')
        label_string.append(f'mfccs: {record.filters['num_mfcc']}')

        return label_string

    def _load_np(self, record):
        
        n_mels= int(record.filters['num_mels'])
        n_mfcc = int(record.filters['num_mfcc'])
        self.label_ids = record.ids

        np_path = f'datasets/RAVDESS/features/mfcc/ravdess_{n_mels}_{n_mfcc}.npy'
        data = np.load(np_path, allow_pickle=True)
        return data
    
    def _apply_labels_to_np(self,record):
        ds = self._load_np(record)
        df = pd.DataFrame(ds,columns=['features','feature_viz','id'])
        df['label'] = df['id'].isin(self.label_ids)
        return df


    def make_feature_and_label_arrays(self,record):

        df = self._apply_labels_to_np(record)
        if 'label' in df.columns:
            self.features = np.vstack(df['features'])
            self.labels = np.array(df['label'])

        
       


# then maybe I can set these to return features/labels and set them up to be inputs for split dataset
# # or not   
    def scale_features(self):
        self.features = StandardScaler().fit_transform(self.features)

    def encode_labels(self):
        self.labels = preprocessing.LabelEncoder().fit_transform(self.labels)
    
    def split_dataset(self, test_size=0.2):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.features,
            self.labels,
            test_size=test_size)
        
    def get_train_metrics(self,model, features,_labels):
        # obtain scores
        model.fit(features,_labels)
        scoring = ['recall','precision','accuracy']
        scores = cross_validate(model, features, _labels,scoring=scoring,cv=5)
        return scores
    
    def arrange_scores(self, res):
        num_tests = len(res['test_recall'])
        arr2D = []
        for i in range(num_tests):
            row = [round(res['test_recall'][i],2), round(res['test_precision'][i],2),round(res['test_accuracy'][i],2)]
            arr2D.append(row)
        return arr2D


    def get_SVC_scores(self):
        svc = SVC(
            C = 1.0,
            gamma='auto',
            class_weight='balanced',
            kernel='rbf')

        scores = self.get_train_metrics(svc, self.X_train,self.y_train)  
        return self.arrange_scores(scores)
    
    def get_LinearSVC_scores(self):
        linear_svc = LinearSVC(
            C = 1.0,
            class_weight='balanced',
            fit_intercept=False)
        
        scores = self.get_train_metrics(linear_svc, self.X_train,self.y_train)
        return self.arrange_scores(scores)