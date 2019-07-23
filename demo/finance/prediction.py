from demo.settings import BASE_DIR
import os
path=os.path.join(BASE_DIR, 'finance','static','prediction')

encoding_order=['FWB2_1', 'FWB1_3', 'FWB2_3', 'FWB1_6', 'FWB1_5']
predictor_description = {'FWB1_3':'Because of my money situation...I will never have the things I want in life',
     'FWB1_5':'I am just getting by financially',
     'FWB1_6':'I am concerned that the money I have or will save won\'t last',
     'FWB2_1':'Giving a gift...would put a strain on my finances for the month',
     'FWB2_3':'I am behind with my finances'}

def make_prediction(selection_dict, encoding_order):
     import numpy as np
     import joblib
     encoder=joblib.load(os.path.join(path,'fwb_encoder'))
     fwb_model=joblib.load(os.path.join(path,'fwb_model'))
     input_data=np.array([selection_dict[p] for p in encoding_order]).reshape(1,-1)
     input_data=encoder.transform(input_data)
     pred=fwb_model.predict(input_data)[0]
     return pred
