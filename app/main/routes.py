from flask import render_template, request,g,flash,redirect, url_for
from flask import session as sess
from app.main import bp
from app.main.forms import DataSetFilterForm, NextRecord, NextAudioRecord

from datetime import datetime, timezone

from app.main.utils.feature_extractors import AudioFeatures, get_audio_data
import app.main.utils.visualizers as viz
from app.main.utils.session_manager import SessionManager


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
            if s.check_incompatable_filters():
                flash("Incompatible actor and sex settings: ")
                flash(s.flashed)
                return redirect(url_for('main.feature_extractor'))
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
        record_count_text=s.message,
        record_text=s.curr_record_info,
        record_id=s.curr_id)


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
            if s.check_incompatiable_filters():
                flash("Incompatible actor and sex settings: ")
                flash(s.flashed)
                return redirect(url_for('main.get_label_mfccs'))
            s.set_labels_list(sess)


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
        record_count_text=s.message, 
        record_text=s.curr_record_info,
        record_id=s.curr_id)