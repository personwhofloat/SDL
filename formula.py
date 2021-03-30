try:
    from StringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

def render_latex(formula, fontsize=12, dpi=200, format_='svg'):
    """Renders LaTeX formula into image."""
    fig = plt.figure()
    text = fig.text(0, 0, u'${0}$'.format(formula), fontsize=fontsize)

    fig.savefig(BytesIO(), dpi=dpi)  # triggers rendering

    bbox = text.get_window_extent()
    width, height = bbox.size / float(dpi) + 0.05
    fig.set_size_inches((width, height))

    dy = (bbox.ymin / float(dpi)) / height
    text.set_position((0, -dy))

    buffer_ = BytesIO()
    fig.savefig(buffer_, dpi=dpi, transparent=True, format=format_)
    plt.close(fig)
    buffer_.seek(0)

    return buffer_.getvalue()
def gen(variables, parameters,subs,idx):
    try:
        params = np.random.choice(parameters,4)
        varis = np.random.choice(variables,2)
        sub = np.random.choice(subs, 4)
        # print(sub)
        params[0] += sub[0]
        params[1] += sub[1]
        varis[0] = varis[0] + sub[2]
        varis[1] = varis[1] + sub[3]
        RHS = operation(operation(params[0],params[1]),varis[0])
        LHS = operation(operation(params[2],params[3]),varis[1])
        #print(RHS,LHS)
        image_bytes = render_latex(f'{LHS}= {RHS}', format_='png')
        with open(f'formula/formula_{idx}.png', 'wb') as image_file:
            image_file.write(image_bytes)
    except:
        gen(variables,parameters,subs,idx)
def operation(a,b):
    operations = ['^','+','-',' ','/','(','sum']
    special = ['/','(','sum']
    op = np.random.choice(operations)
    if op not in special:
        return str(a)+op+str(b)
    elif op == 'sum':
        return '\sum '+str(a) +' '+ str(b)
    elif op == '(':
        return '('+str(a)+np.random.choice(operations[:3])+str(b)+')'
    else:
        return '\\frac{%s}{%s}'%(a,b)
if __name__ == '__main__':
    
    variables = ['x','y','z','t']
    parameters = ['a','b','c','d','\\alpha','\\beta','\\gamma']
    subs = ['_{%i}'%i for i in range(4)]
    # subs.append('_n')
    # subs.append('')
    for idx in tqdm(range(2000)):
        gen(variables,parameters,subs,idx)

