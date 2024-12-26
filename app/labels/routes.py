from flask import render_template, request,g
from flask import session as sess
from app.features import bp
from app.forms import DataSetFilterForm, NextRecord,NextAudioRecord
import app.visualizers as viz
from app.session_manager import SessionManager
from app.features.feature_extractors import AudioFeatures

#@bp.route('/', methods=['GET', 'POST'])
#@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/label-selector',methods=['GET','POST'])
def get_label_mfccs():

    s = SessionManager()
    g.form = DataSetFilterForm()
    next_group = NextRecord()
    next_audio_file = NextAudioRecord()

    if request.method == 'GET':
        print('init')
        # set filter defaults
        s.init_sess(sess)  
    
    if request.method == 'POST':
        # add check user function
        if g.form.submit.data:
            s.set_mfcc_labels(sess)


        if next_group.next.data:
            s.get_next_record_group(sess)
        
        if next_audio_file.next_audio_file.data:
            s.get_next_audio_from_group(sess)


    af1 = AudioFeatures(sess)
    audio_file = af1.save_audio_to_file()
    img_file=viz.get_mfcc_plots(sess, af1)

    return render_template('label-selector.html',
        title='Home', 
        audio_file= audio_file,
        img_file=img_file,
        next_group=next_group,
        next_audio_file=next_audio_file, 
        record_text=s.message)