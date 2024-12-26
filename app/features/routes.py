from flask import render_template, request,g
from flask import session as sess
from app.features import bp
from app.forms import DataSetFilterForm, NextRecord

from datetime import datetime, timezone

from app.features.feature_extractors import AudioFeatures, get_audio_data
import app.visualizers as viz
from app.session_manager import SessionManager


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/feature-extractor', methods=['GET', 'POST'])
def feature_extractor():
    print(datetime.now(timezone.utc))
    s = SessionManager()
    g.form = DataSetFilterForm()
    next_button = NextRecord()   
    
    if request.method == 'GET':
        
        print('init')
        s.init_sess(sess)  
        
      

    if request.method == 'POST':
        # add check user funciton here
        if g.form.submit.data:
            s.set_record_list(sess)

            
        if next_button.next.data:
            
            s.get_next_record(sess)

        
    af1 = AudioFeatures(sess)
    audio_file = af1.save_audio_to_file()
    img_file=viz.get_feature_extraction_plots(af1)


    print(datetime.now(timezone.utc))        
    return render_template('feature-extractor.html',
        title='Home', 
        audio_file= audio_file,
        img_file=img_file,
        next_button=next_button, 
        record_text=s.message)

