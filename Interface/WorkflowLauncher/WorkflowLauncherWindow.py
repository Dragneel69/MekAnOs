from PyQt5.QtCore import QDateTime, Qt, QTimer, QSize, QMargins, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QFileDialog, QFrame, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QMainWindow, QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTableWidgetItem, QTabWidget, QTextEdit,
        QTreeWidget, QTreeWidgetItem, QScrollArea, QSplitter, QStackedLayout, QTabWidget, QTabBar,
        QToolButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QIcon, QFont

from MekAnos.Data.Excel_Reader import read_dataset_info
from MekAnos.Interface.WorkflowLauncher.Dataset_tab import DatasetTab
from MekAnos.Interface.WorkflowLauncher.Segmentation_tab import SegmentationTab
from MekAnos.Interface.WorkflowLauncher.Mesh_tab import MeshTab
from MekAnos.Interface.WorkflowLauncher.Mekamesh_tab import Mekamesh_tab

import numpy as np
import math

import sys

__version__ = '1.0'


class WorkflowLauncherWindow(QDialog):
    def __init__(self, parent=None):
        super(WorkflowLauncherWindow, self).__init__(parent)

        self.parentWindow = parent
        self.originalPalette = QApplication.palette()
        self.setWindowTitle("Workflow Launcher - " + __version__)
        self.styleName = 'Fusion'
        QApplication.setStyle(QStyleFactory.create(self.styleName))
        QApplication.setPalette(self.originalPalette)
        self.setStyleSheet('QGroupBox{font-size: 11pt;}'
                           'QGroupBox::title{color: #003066;}')

        self.setMinimumSize(1200, 600)

        # main layout
        self.mainLayout = QGridLayout()
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setLayout(self.mainLayout)

        # Tab layout
        self.tabWidget = QWidget()
        self.tabLayout = QHBoxLayout()
        self.tabLayout.setSpacing(0)
        self.tabLayout.setContentsMargins(QMargins(0, 0, 0, 0))
        self.tabWidget.setLayout(self.tabLayout)
        self.tab_creator = QTabWidget()
        self.tab_creator.currentChanged.connect(self.current_tab_changed)
        self.tabLayout.addWidget(self.tab_creator)

        # Dataset file reader widget
        self.dataset_file_reader_widget = QWidget()
        self.dataset_file_reader_layout = QHBoxLayout()
        self.pathEditdatasetReader = QTextEdit('D:\MekAnOs_workflow\MekAnos\Data\Samples.xlsx')
        self.pathSearcher = QPushButton('Browse')
        self.pathSearcher.clicked.connect(self.open_dataset_file)
        self.refreshButton = QPushButton('Open / Refresh')
        self.dataset_file_reader_layout.addWidget(self.refreshButton)
        self.refreshButton.clicked.connect(self.refresh_dataset_file)
        self.dataset_file_reader_widget.setLayout(self.dataset_file_reader_layout)
        self.dataset_file_reader_layout.addWidget(self.pathSearcher)
        self.dataset_file_reader_layout.addWidget(self.pathEditdatasetReader)

        # Pack all widgets
        self.mainLayout.addWidget(self.dataset_file_reader_widget, 0, 0)
        self.dataset_file_reader_widget.setMaximumHeight(42)
        self.mainLayout.addWidget(self.tabWidget, 1, 0)

        self.create_dataset_tab()
        self.create_segmentation_tab()
        self.create_mesh_tab()
        self.create_mekamesh_tab()
        self.create_boundary_tab()
        self.create_simulation_tab()
        #self.process_tab()

    def refresh_dataset_file(self):
        self.datasets_file_path = self.pathEditdatasetReader.toPlainText()
        self.fill_tree_dataset()

    def open_dataset_file(self):
        # Open file explorer and get path
        fileDialog = QFileDialog()
        fileDialog.setDirectory('D:\MekAnOs_workflow\MekAnos\Data')
        filename = fileDialog.getOpenFileName()
        self.datasets_file_path = filename[0]
        self.pathEditdatasetReader.setText(self.datasets_file_path)
        self.fill_tree_dataset()
        self.last_tab_index = 0
        self.tab_creator.setCurrentIndex(0)

    def current_tab_changed(self):

        if self.tab_creator.currentIndex() != 0:
            self.datasetTab.get_selected_samples()
            self.datasets = self.datasetTab.datasetTree.datasets
        if self.tab_creator.currentIndex() >= 1 and self.last_tab_index == 0:
            self.fill_segmentation_tab()
        if self.tab_creator.currentIndex() >= 2 and self.last_tab_index == 1:
            self.fill_mesh_tab()

        self.last_tab_index = self.tab_creator.currentIndex()

    def create_dataset_tab(self):
        self.datasetTab = DatasetTab(self)
        self.tab_creator.addTab(self.datasetTab, 'Dataset')

    def create_segmentation_tab(self):
        self.segmentationTab = SegmentationTab(self)
        self.tab_creator.addTab(self.segmentationTab, 'Segmentation')
        self.tab_creator.setTabEnabled(1, False)

    def create_mesh_tab(self):
        self.mesh_tab = MeshTab(self)

        self.tab_creator.addTab(self.mesh_tab, 'Mesh')
        self.tab_creator.setTabEnabled(2, False)

    def create_mekamesh_tab(self):

        self.mekameshTab = Mekamesh_tab(self)

        self.tab_creator.addTab(self.mekameshTab, 'Mekamesh')
        self.tab_creator.setTabEnabled(3, False)

    def create_boundary_tab(self):
        self.boundaryTree = QTreeWidget()
        self.boundaryTree.setMinimumHeight(150)
        self.boundaryTree.setStyleSheet('QTreeWidget{font-size:10pt;}')
        self.boundaryTree.setColumnCount(9)
        self.tab_creator.addTab(self.boundaryTree, 'Boundary conditions')
        self.tab_creator.setTabEnabled(4, False)

    def create_simulation_tab(self):
        self.simulationTree = QTreeWidget()
        self.simulationTree.setMinimumHeight(150)
        self.simulationTree.setStyleSheet('QTreeWidget{font-size:10pt;}')
        self.simulationTree.setColumnCount(9)
        self.tab_creator.addTab(self.simulationTree, 'Simulation')
        self.tab_creator.setTabEnabled(5, False)

    def fill_tree_dataset(self):
        self.datasetTab.datasetTree.fill()

        for i in range(7):
            self.tab_creator.setTabEnabled(i, True)

    def fill_segmentation_tab(self):
        self.segmentationTab.segTree.fill()

    def fill_mesh_tab(self):
        pass







if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)  # for logos with good resolution
    window = WorkflowLauncherWindow()
    window.show()
    app.exec_()