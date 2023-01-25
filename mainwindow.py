from calculation import Peak, Background, gaussian_noise
import pyqtgraph as pg
from PyQt5 import QtCore,uic
from PyQt5.QtWidgets import (QMainWindow,
                            QWidget,
                            QPushButton,
                            QLineEdit,
                            QCheckBox,
                            QListWidget,
                            QRadioButton)

class Ui(QMainWindow):
    def __init__(self):
        super().__init__()

        # load the ui file
        uic.loadUi("mainwindow.ui",self)

        # set title
        self.setWindowTitle("Spectrum Simulation")

        #widgets default values
        self.min_n.setText('0')
        self.max_n.setText('1000')
        self.peak_channel.setText('0')
        self.peak_counts.setText('0')
        self.peak_fwhm.setText('0')
        self.bg1.setText('0')
        self.bg2.setText('0')
        self.bg3.setText('0')
        self.bg4.setText('0')
        
        #initialisation of graph points lists
        self.x = []
        self.y = []

        # initalisation of main spectrum contributions(background and peaks) !!! zero element is ALWAYS background
        self.contributions = [Background()]

        #????????????????????????
        self.noise_value = []

        #connections between signals and slots
        self.apply.clicked.connect(self.update_mainwindow)
        self.clear.clicked.connect(self.clear_all)
        self.del_item.clicked.connect(self.list_widget_cleaner)
        self.noise.toggled.connect(self.make_noise)
        
        #show main window
        self.show()

    #methods for interaction with window
    def update_mainwindow(self):
        #disable spectrum channels(x) range
        self.activate({self.min_n: True, self.max_n: True})
        #reinitialisation of graph points lists
        self.x = [i for i in range(int(self.min_n.text()),int(self.max_n.text()))]
        self.y = [0 for i in range(int(self.min_n.text()),int(self.max_n.text()))]
        self.graph.clear()
        #append background to the widget list and y coordinates list 
        self.contributions[0].set_background(float(self.bg1.text()),float(self.bg2.text()),float(self.bg3.text()),float(self.bg4.text()))
        if all([self.list_widget.item(i).text() != 'Background\t' for i in range(len(self.list_widget))]):
            self.list_widget.insertItem (0,'Background\t')
        self.y = [self.contributions[0].get_value_at_point(self.x[i]) for i in range(len(self.y))]
        #append peaks to the widget list and y coordinates list
        if all([self.list_widget.item(i).text()[5:] != self.peak_channel.text() for i in range(len(self.list_widget))]):       
            self.list_widget.addItem('Peak\t'+self.peak_channel.text())
            self.contributions.append(Peak(int(self.peak_counts.text()),int(self.peak_channel.text()),float(self.peak_fwhm.text())))
        for peak in self.contributions[1:]:
            self.y = [self.y[i]+peak.get_value_at_point(self.x[i]) for i in range(len(self.y))]
        #pen initialusation and graph plot
        pen = pg.mkPen(color=(0, 0, 0), width=1, style=QtCore.Qt.DashLine)        
        self.graph.plot(self.x, self.y, pen=pen,symbol='o',symbolSize=3)
    
    #activate/deactivate widgets 
    def activate(self,widgets):
        for widget, accessibility in widgets.items():
            if type(widget) == type(QLineEdit()):
                widget.setReadOnly(accessibility)
            else:
                widget.setEnabled(accessibility)

    def list_widget_cleaner(self):
        #loop over all selected widget list elements
        for item in self.list_widget.selectedItems():
            #remove selected items from widget list
            self.list_widget.takeItem(self.list_widget.row(item))
            #remove selected items from contribution list
            if item.text() == 'Background\t':
                self.y = [self.y[i]-self.contributions[0].get_value_at_point(self.x[i]) for i in range(len(self.y))]
            else:
                for peak in self.contributions[1:]:
                    if peak.mean == int(item.text()[5:]):
                        self.y = [self.y[i]-peak.get_value_at_point(self.x[i]) for i in range(len(self.y))]
                        self.contributions.remove(peak)
        #graph replot 
        self.graph.clear()
        if len(self.list_widget)==0:
            self.x = []
            self.y = []
        pen = pg.mkPen(color=(0, 0, 0), width=1, style=QtCore.Qt.DashLine)        
        self.graph.plot(self.x, self.y, pen=pen,symbol='o',symbolSize=3)

    def make_noise(self):
        self.noise_value = gaussian_noise(self.y,self.noise.isChecked(), self.noise_value)
        self.y = [abs(self.y[i]+self.noise_value[i]) for i in range(len(self.y))]    
        #graph replot 
        self.graph.clear()
        pen = pg.mkPen(color=(0, 0, 0), width=1, style=QtCore.Qt.DashLine)        
        self.graph.plot(self.x, self.y, pen=pen,symbol='o',symbolSize=3)
        if self.noise.isChecked():
            self.activate({self.apply:False, self.clear:False})
        else:
            self.activate({self.apply:True, self.clear:True})

    def clear_all(self):
        #enable spectrum channels(x) range 
        self.activate({self.min_n: False, self.max_n: False})
        #primal initalisation
        self.x = []
        self.y = []
        self.contributions = [Background()]
        self.graph.clear()
        self.list_widget.clear()