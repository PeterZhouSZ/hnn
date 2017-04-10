from morphology import shapeplot, morphology_to_dict
from mpl_toolkits.mplot3d import Axes3D
import pylab as plt
from neuron import h
from L5_pyramidal import L5Pyr
from L2_pyramidal import L2Pyr
from L2_basket import L2Basket
from L5_basket import L5Basket
from run import *

L2Pyrsecnames =  ['L2Pyr_soma', 'L2Pyr_basal_1', 'L2Pyr_apical_trunk', 'L2Pyr_basal_3', 'L2Pyr_basal_2', 'L2Pyr_apical_oblique', 'L2Pyr_apical_1', 'L2Pyr_apical_tuft']

L5Pyrsecnames =  ['L5Pyr_soma', 'L5Pyr_basal_1', 'L5Pyr_apical_trunk', 'L5Pyr_basal_3', 'L5Pyr_basal_2', 'L5Pyr_apical_oblique', 'L5Pyr_apical_1', 'L5Pyr_apical_2', 'L5Pyr_apical_tuft']

lsecnames = []
for l in [L2Pyrsecnames, L5Pyrsecnames]:
  for s in l:
    lsecnames.append(s)

#ls = list(h.allsec())

ls = []
for c in net.cells_list:
  if type(c) == L5Pyr: # L2Pyr: # L5Basket: # L2Basket:
    lss = c.get_sections()
    for s in lss: ls.append(s)
    break

print('len(ls) = ',len(ls))
#for s in ls: s.nseg=1

cell = net.cells_list[200]
# cell.pos # position used for wiring

h.define_shape()

llx,lly,llz,lldiam = [],[],[],[]
for i in range(200,202,1):
  lx,ly,lz,ldiam = cell.get3dinfo()
  llx.append(lx); lly.append(ly); llz.append(lz); lldiam.append(ldiam)

# pt3dchange(i, x, y, z, diam)

for cell in net.cells_list:  
  cell.translateto(cell.pos[0],cell.pos[1],cell.pos[2])

h.define_shape()

plt.ion()
fig = plt.figure()

allseg = sum([s.nseg for s in ls])

shapeax = plt.subplot(111, projection='3d')
shapeax.set_xlabel('X',fontsize=24)
shapeax.set_ylabel('Y',fontsize=24)
shapeax.set_zlabel('Z',fontsize=24)
#shapeax.view_init(75,66)

#shapeax.set_xlim3d((-425.11876526,  1890.3420929))
#shapeax.set_ylim3d((-173.77793655,  736.48745499))
#shapeax.set_zlim3d((0,100))

defclr = 'k'; selclr = 'r'
shapelines = shapeplot(h,shapeax,lw=8)
#shapelines = shapeplot(h,shapeax,lw=8,cvals=[defclr for i in range(allseg)],picker=5)
#shapelines = shapeplot(h,shapeax,sections=ls,lw=8)

"""
def onclick(event):
  try:
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))
  except:
    pass
"""

# cid = fig.canvas.mpl_connect('button_press_event', onclick)

# net has cells - net.pos_dict has locations
# net.pos_dict.keys()
# dict_keys(['L2_basket', 'evdist', 'extgauss', 'L5_pyramidal', 'extpois', 'extinput', 'L5_basket', 'evprox1', 'evprox0', 'L2_pyramidal'])

"""
def setcolor (ls,clr):
  for l in ls: l.set_color(clr)

def onpick (event):
  thisline = event.artist
  c = thisline.get_color()
  idx = -1
  setcolor(shapelines,defclr)    
  for idx,l in enumerate(shapelines):
    if l == thisline:
      break
  try:
    print('idx is ', idx, 'selected',lsecnames[idx])
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    points = tuple(zip(xdata[ind], ydata[ind]))
    print('onpick points:', points)
    if c == defclr:
      thisline.set_color(selclr)
    else:
      thisline.set_color(defclr)
    print(ind)
    #print(dir(thisline))
  except:
    pass
"""
#cid2 = fig.canvas.mpl_connect('pick_event', onpick)
