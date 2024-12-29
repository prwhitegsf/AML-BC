
filter_data = [
    ({'actor'   : 'all',
    'sex'       : 'all', 
    'statement'  : 'all',
    'emotion'    : 'all',
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'actor'   : 'all',
    'sex'       : 'male', 
    'statement'  : 'all',
    'emotion'    : 'all',
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'actor'   : 'all',
    'sex'       : 'male', 
    'statement'  : '1',
    'emotion'    : ['calm','happy','sad'],
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'actor'   : 'all',
    'sex'       : 'female', 
    'statement'  : '1',
    'emotion'    : ['all','calm','happy','sad'],
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    })]        


incompat_filters = [
    ({'actor'   : '1',
    'sex'       : 'female', 
    'statement'  : '1',
    'emotion'    : ['all','calm','happy','sad'],
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'actor'   : '2',
    'sex'       : 'male', 
    'statement'  : 'all',
    'emotion'    : ['all'],
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    })
]




label_filters = [
    ({'actor'   : '1',
    'sex'       : 'all', 
    'statement'  : '1',
    'emotion'    : ['angry'],
    'intensity'  : '1',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'actor'   : '2',
    'sex'       : 'all', 
    'statement'  : '1',
    'emotion'    : ['happy'],
    'intensity'  : '2',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }),
    ({'actor'   : 'all',
    'sex'       : 'male', 
    'statement'  : 'all',
    'emotion'    : 'all',
    'intensity'  : 'all',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    })]

filter_two_results = {
    'actor'     :'1',
    'sex'       : 'all', 
    'statement'  : '1',
    'emotion'    : 'calm',
    'intensity'  : '1',
    'num_mels'   : '128',
    'num_mfcc'   : '40',
    'submit'     : 'Submit'
    }