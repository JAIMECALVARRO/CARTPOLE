# Necessary only for debugging in Visual Studio Code IDE
try:
    import ptvsd
except:
    pass

import numpy as np

# Import functions from PyQt5 module (creating GUI)
from PyQt5.QtWidgets import (
    QMainWindow,
    QRadioButton,
    QApplication,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QCheckBox,
    QSlider,
    QLineEdit,
    QMessageBox,
    QComboBox,
    QButtonGroup,
)
from PyQt5.QtCore import QThreadPool, QTimer, Qt

import Controllers.controller_mppi as controller_mppi


class MPPIOptionsWindow(QWidget):
    def __init__(self):
        super(MPPIOptionsWindow, self).__init__()

        self.horizon_steps = 50
        self.dd_weight = controller_mppi.dd_weight
        self.ep_weight = controller_mppi.ep_weight
        self.ekp_weight = controller_mppi.ekp_weight * 1.0e1
        self.ekc_weight = controller_mppi.ekc_weight * 1.0e-1
        self.cc_weight = controller_mppi.cc_weight * 1.0e-1
        self.R = controller_mppi.R          # How much to punish Q
        self.LBD = controller_mppi.LBD      # Cost parameter lambda
        self.NU = controller_mppi.NU        # Exploration variance

        layout = QVBoxLayout()

        ### Set Horizon Length
        horizon_options_layout = QVBoxLayout()

        self.horizon_label = QLabel("")
        self.horizon_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        horizon_options_layout.addWidget(self.horizon_label)

        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(10, 300)
        slider.setValue(self.horizon_steps)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setSingleStep(10)
        horizon_options_layout.addWidget(slider)

        slider.valueChanged.connect(self.horizon_length_changed)

        ### Set Cost Weights
        cost_weight_layout = QVBoxLayout()
        
        # Distance difference cost
        self.dd_weight_label = QLabel("")
        self.dd_weight_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.dd_weight_label)
        self.dd_label = QLabel("")
        self.dd_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.dd_label)
        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(0, 990)
        slider.setValue(self.dd_weight)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.setSingleStep(10)
        cost_weight_layout.addWidget(slider)
        slider.valueChanged.connect(self.dd_weight_changed)

        # Potential energy cost
        self.ep_weight_label = QLabel("")
        self.ep_weight_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.ep_weight_label)
        self.ep_label = QLabel("")
        self.ep_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.ep_label)
        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(0, 1e5-1e3)
        slider.setValue(self.ep_weight)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(1e3)
        slider.setSingleStep(1e3)
        cost_weight_layout.addWidget(slider)
        slider.valueChanged.connect(self.ep_weight_changed)

        # Pole kinetic energy cost
        self.ekp_weight_label = QLabel("")
        self.ekp_weight_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.ekp_weight_label)
        self.ekp_label = QLabel("")
        self.ekp_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.ekp_label)
        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(0, 99)
        slider.setValue(self.ekp_weight)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        cost_weight_layout.addWidget(slider)
        slider.valueChanged.connect(self.ekp_weight_changed)

        # Cart kinetic energy cost
        self.ekc_weight_label = QLabel("")
        self.ekc_weight_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.ekc_weight_label)
        self.ekc_label = QLabel("")
        self.ekc_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.ekc_label)
        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(0, 99)
        slider.setValue(self.ekc_weight)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        cost_weight_layout.addWidget(slider)
        slider.valueChanged.connect(self.ekc_weight_changed)

        # Control cost
        self.cc_weight_label = QLabel("")
        self.cc_weight_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.cc_weight_label)
        self.cc_label = QLabel("")
        self.cc_label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        cost_weight_layout.addWidget(self.cc_label)
        slider = QSlider(orientation=Qt.Horizontal)
        slider.setRange(0, 99)
        slider.setValue(self.cc_weight)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(1)
        slider.setSingleStep(1)
        cost_weight_layout.addWidget(slider)
        slider.valueChanged.connect(self.cc_weight_changed)

        ### Set some more MPPI constants
        mppi_constants_layout = QVBoxLayout()

        # Quadratic cost penalty R
        textbox = QLineEdit()
        textbox.setText(str(self.R))
        textbox.textChanged.connect(self.R_changed)
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Quadratic input cost penalty R ="))
        h_layout.addWidget(textbox)
        mppi_constants_layout.addLayout(h_layout)

        # Quadratic cost penalty LBD
        textbox = QLineEdit()
        textbox.setText(str(self.LBD))
        textbox.textChanged.connect(self.LBD_changed)
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Importance of higher-cost rollouts LBD ="))
        h_layout.addWidget(textbox)
        mppi_constants_layout.addLayout(h_layout)

        # Quadratic cost penalty NU
        textbox = QLineEdit()
        textbox.setText(str(self.NU))
        textbox.textChanged.connect(self.NU_changed)
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Exploration variance NU ="))
        h_layout.addWidget(textbox)
        mppi_constants_layout.addLayout(h_layout)

        ### Put together layout
        self.update_labels()
        self.update_slider_labels()
        layout.addLayout(horizon_options_layout)
        layout.addLayout(cost_weight_layout)
        layout.addLayout(mppi_constants_layout)

        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, 400, 50)

        self.show()
        self.setWindowTitle("MPPI Options")

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(100)

        controller_mppi.LOGGING = False

    def horizon_length_changed(self, val: int):
        self.horizon_steps = val
        # TODO: Replace by setter method
        controller_mppi.mpc_samples = self.horizon_steps
        self.update_slider_labels()

    def dd_weight_changed(self, val: int):
        self.dd_weight = val
        # TODO: Replace by setter method
        controller_mppi.dd_weight = self.dd_weight * 1.0
        self.update_slider_labels()
    
    def ep_weight_changed(self, val: int):
        self.ep_weight = val
        # TODO: Replace by setter method
        controller_mppi.ep_weight = self.ep_weight * 1.0
        self.update_slider_labels()
    
    def ekp_weight_changed(self, val: int):
        self.ekp_weight = val
        # TODO: Replace by setter method
        controller_mppi.ekp_weight = self.ekp_weight * 1.0e-1
        self.update_slider_labels()
    
    def ekc_weight_changed(self, val: int):
        self.ekc_weight = val
        # TODO: Replace by setter method
        controller_mppi.ekc_weight = self.ekc_weight * 1.0e1
        self.update_slider_labels()
    
    def cc_weight_changed(self, val: int):
        self.cc_weight = val
        # TODO: Replace by setter method
        controller_mppi.cc_weight = self.cc_weight * 1.0e1
        self.update_slider_labels()

    def R_changed(self, val: str):
        if val == '': val = '0'
        self.R = float(val)
        controller_mppi.R = self.R
    
    def LBD_changed(self, val: str):
        if val == '': val = '0'
        self.LBD = float(val)
        controller_mppi.LBD = self.LBD
    
    def NU_changed(self, val: str):
        if val == '': val = '0'
        self.NU = float(val)
        controller_mppi.NU = self.NU
    
    def update_slider_labels(self):
        self.horizon_label.setText(
            f"Horizon: {self.horizon_steps} steps = {round(self.horizon_steps * controller_mppi.dt, 2)} s"
        )
        self.dd_weight_label.setText(
            f"Distance difference cost weight: {round(self.dd_weight, 2)}"
        )
        self.ep_weight_label.setText(
            f"Pole angle cost weight: {round(self.ep_weight, 2)}"
        )
        self.ekp_weight_label.setText(
            f"Pole kinetic energy cost weight: {round(self.ekp_weight * 1.0e-1, 4)}"
        )
        self.ekc_weight_label.setText(
            f"Cart kinetic energy cost weight: {round(self.ekc_weight * 1.0e1, 3)}"
        )
        self.cc_weight_label.setText(
            f"Control cost weight: {round(self.cc_weight * 1.0e1, 3)}"
        )

    def update_labels(self):
        self.dd_label.setText(
            f"{round(controller_mppi.gui_dd.item(), 2)}"
        )
        self.ep_label.setText(
            f"{round(controller_mppi.gui_ep.item(), 2)}"
        )
        self.ekp_label.setText(
            f"{round(controller_mppi.gui_ekp.item(), 2)}"
        )
        self.ekc_label.setText(
            f"{round(controller_mppi.gui_ekc.item(), 2)}"
        )
        self.cc_label.setText(
            f"{round(controller_mppi.gui_cc.item(), 2)}"
        )
