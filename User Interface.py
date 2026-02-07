import sys
from turtledemo.penrose import start

from PyQt6.QtCore import QSize, Qt, QTimer, QRectF
from PyQt6.QtGui import QAction, QIcon, QDoubleValidator, QBrush, QPen, QPolygonF, QPixmap, QPainter, QColor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QDialog, QDialogButtonBox,
    QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QGraphicsItemGroup,
    QToolBar, QToolButton,
    QWidget, QLineEdit, QComboBox, QRadioButton, QButtonGroup,
    QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem,
    QGraphicsEllipseItem, QGraphicsView, QApplication, QGraphicsLineItem, QGraphicsProxyWidget
)

QSS_styling = '''
QMainWindow {
    background-color: white;
    font-family: 'Aptos (Body)';
}

QToolBar {
    background-color: #BFBFBF;   
}

QToolButton {
    color: black;
    font-weight: bold;
    font-size: 22px;
}

QPushButton, QPushButton:disabled[state = 'highlighted'] {
    background-color: #0033CC;
    border-radius: 18px;
    font-weight: bold;
    font-size: 22px;
    color: white;
}

QPushButton:disabled[state = 'greyed'] {
    background-color: #666666;
}

QLabel {
    font-size: 25px;
}

QLabel[type = 'prompt_bar'] {
    border-style: solid;
    border-width: 3px;
    border-radius: 18px;
}

QLabel[type = 'prompt_bar'][role = 'construct_graph'] {
    border-color: #0033CC;
    color: #0033CC;
}

QLabel[type = 'prompt_bar'][role = 'dijkstra'] {
    border-color: #CC00FF;
    color: #CC00FF;
}

QLabel[type = 'prompt_bar'][role = 'nearest_neighbour'] {
    border-color: #FF6600;
    color: #FF6600;
}

QPushButton[type = 'exit'][role = 'graph_construct'] {
    background-color: #0033CC;
}

QPushButton[type = 'exit'][role = 'dijkstra'] {
    background-color: #CC00FF;
}

QPushButton[type = 'exit'][role = 'nearest_neighbour'] {
    background-color: #FF6600;
}

QLabel[type = 'vertex'] {
    border-radius: 38px;
    border-width: 3px;
    border-style: solid;
}

QLabel[type = 'vertex_name'] {
    font_weight: bold;
}

QLabel[type = 'vertex_name'][state = 'default'] {
    color: white;
    text-shadow: 0 0 3px red;
}

QLabel[type = 'vertex_name'][state = 'dijkstra'] {
    color: #CC00FF;
}

QLabel[type = 'arc_weight'] {
    background-color: white;
    color: black;
}
'''

class AddVertexDialog(QDialog):
    def __init__(self, vertices):
        super().__init__()
        self.vertices = vertices
        self.setWindowTitle('Placing a stop')

        #The vertex name input
        self.vertex_name_input = QLineEdit(self)
        self.vertex_name_input.setPlaceholderText('Enter stop name...')

        #The warning if the vertex_name is already used
        self.warning = QLabel(self)
        self.warning.setStyleSheet('color: #FF6464')
        self.warning.hide()

        #The OK & Cancel buttons
        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('Cancel')
        confirm_layout = QHBoxLayout()
        confirm_layout.addWidget(self.ok_button)
        confirm_layout.addWidget(self.cancel_button)

        #Setting a layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.vertex_name_input)
        layout.addWidget(self.warning)
        layout.addLayout(confirm_layout)
        self.setLayout(layout)

        #Setting Cancel to be the only exit
        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        self.ok_button.clicked.connect(self.input_validation)
        self.cancel_button.clicked.connect(self.reject)

    def hide_warning(self):
        self.warning.hide()
        QTimer.singleShot(0, self.adjustSize)

    def input_validation(self):
        #Checking if the vertex name is already used
        if self.vertex_name_input.text() in self.vertices:
            self.warning.setText("You've already used this name. Please choose a different one.")
            self.warning.show()
            self.vertex_name_input.textEdited.connect(self.hide_warning)
        #A presence check
        elif self.vertex_name_input.text() == '':
            self.warning.setText('Please enter a stop name.')
            self.warning.show()
            self.vertex_name_input.textEdited.connect(self.hide_warning)
        #If fully valid...
        else:
            self.accept()

    def get_vertex_name(self):
        return self.vertex_name_input.text()

class AddArcDialog(QDialog):
    def __init__(self, vertices):
        super().__init__()
        self.setWindowTitle('Adding a path')
        vertices.sort()

        #-----------------------------------------------------------
        #ENTERING THE STOPS

        #The vertex drop-down menus
        stop_1_label = QLabel('Between stop: ')
        stop_1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stop_1 = QComboBox()
        self.stop_1.addItems(vertices)

        stop_2_label = QLabel('...and stop: ')
        stop_2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stop_2 = QComboBox()
        self.stop_2.addItems(vertices)

        #Preset values
        self.stop_1.setCurrentIndex(0)
        self.stop_2.setCurrentIndex(1)

        #Checking for loops
        self.stop_1.currentIndexChanged.connect(self.loop_check)
        self.stop_2.currentIndexChanged.connect(self.loop_check)

        #The layout
        stop_input_layout = QHBoxLayout()
        stop_input_layout.addWidget(stop_1_label)
        stop_input_layout.addWidget(self.stop_1)
        stop_input_layout.addWidget(stop_2_label)
        stop_input_layout.addWidget(self.stop_2)
        stop_input_layout.setContentsMargins(0, 0, 0, 0)

        #The input validation warning
        self.stop_input_warning = QLabel(self)
        self.stop_input_warning.setStyleSheet('color: #FF6464')
        self.stop_input_warning.hide()

        #---------------------------------------------------------------------------
        #ENTERING THE ARC WEIGHT

        #The arc weight input
        arc_weight_label = QLabel('Distance: ')
        self.arc_weight_input = QLineEdit(self)
        self.arc_weight_input.setPlaceholderText('Enter a number...')
        self.arc_weight_input.setValidator(QDoubleValidator(0.0001, float('inf'), 4))

        #The layout
        arc_weight_layout = QHBoxLayout()
        arc_weight_layout.addWidget(arc_weight_label)
        arc_weight_layout.addWidget(self.arc_weight_input)

        #The input validation warning
        self.arc_weight_input_warning = QLabel(self)
        self.arc_weight_input_warning.setStyleSheet('color: #FF6464')
        self.arc_weight_input_warning.hide()

        self.arc_weight_input.textEdited.connect(self.hide_arc_weight_warning)


        #---------------------------------------------------------------------------
        #ENTERING THE DIRECTION OPTION

        self.direction_option = QButtonGroup()
        self.directed_choice = QRadioButton('Directed')
        self.undirected_choice = QRadioButton('Undirected')
        self.undirected_choice.setChecked(True) #Preset value

        self.direction_option.addButton(self.directed_choice)
        self.direction_option.addButton(self.undirected_choice)

        direction_option_layout = QHBoxLayout()
        direction_option_layout.addWidget(self.directed_choice)
        direction_option_layout.addWidget(self.undirected_choice)


        #-------------------------------------------------------------------
        #ENTERING THE DIRECTED ROUTES

        #The directed routes
        self.directed_routes = QButtonGroup()
        self.route_1 = QRadioButton(self)
        self.route_2 = QRadioButton(self)
        self.directed_routes.addButton(self.route_1)
        self.directed_routes.addButton(self.route_2)

        #The layout
        directed_route_layout = QVBoxLayout()
        directed_route_layout.addWidget(self.route_1)
        directed_route_layout.addWidget(self.route_2)
        directed_route_layout.setContentsMargins(20, 0, 0, 0) #A small indent

        self.direction_route_container = QWidget(self)
        self.direction_route_container.setLayout(directed_route_layout)

        #Initial routes set
        self.route_1.setText(f'{self.stop_1.currentText()} → {self.stop_2.currentText()}')
        self.route_2.setText(f'{self.stop_2.currentText()} → {self.stop_1.currentText()}')
        self.route_1.setChecked(True)
        self.route_1.hide()
        self.route_2.hide()


        #--------------------------------------------------------------------
        #THE MAIN LAYOUT

        self.main_layout = QVBoxLayout()
        self.main_layout.addLayout(stop_input_layout)
        self.main_layout.addWidget(self.stop_input_warning)
        self.main_layout.addLayout(arc_weight_layout)
        self.main_layout.addWidget(self.arc_weight_input_warning)
        self.main_layout.addLayout(direction_option_layout)

        self.direction_option.buttonClicked.connect(self.show_directed_routes)


        #--------------------------------------------------------------------
        #THE CONFIRMATION BUTTONS

        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('Cancel')

        confirm_layout = QHBoxLayout()
        confirm_layout.addWidget(self.ok_button)
        confirm_layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.confirm_validation)
        self.cancel_button.clicked.connect(self.reject)


        #-------------------------------------------------------------------
        #THE FULL LAYOUT

        self.dialog_layout = QVBoxLayout(self)
        self.dialog_layout.addLayout(self.main_layout)
        self.dialog_layout.addLayout(confirm_layout)
        self.setLayout(self.dialog_layout)

        self.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

    #Preventing a loop
    def loop_check(self):
        loop_present = self.stop_1.currentIndex() == self.stop_2.currentIndex()

        if loop_present:
            self.stop_input_warning.setText('Cannot create a loop. Please choose a different set of stops.')
            self.stop_input_warning.show()
        else:
            self.route_1.setText(f'{self.stop_1.currentText()} → {self.stop_2.currentText()}')
            self.route_2.setText(f'{self.stop_2.currentText()} → {self.stop_1.currentText()}')
            self.stop_input_warning.hide()
            QTimer.singleShot(0, self.adjustSize)

        #Deactivating or reactivating all functions
        self.arc_weight_input.setDisabled(loop_present)
        self.directed_choice.setDisabled(loop_present)
        self.undirected_choice.setDisabled(loop_present)
        self.route_1.setDisabled(loop_present)
        self.route_2.setDisabled(loop_present)

    def show_directed_routes(self, option):
        if option.text() == 'Directed':
            #Showing the route options
            self.main_layout.addWidget(self.direction_route_container)
            self.route_1.show()
            self.route_2.show()
        else:
            self.main_layout.removeWidget(self.direction_route_container)
            self.route_1.hide()
            self.route_2.hide()
            QTimer.singleShot(0, self.adjustSize)

    def confirm_validation(self):
        if self.arc_weight_input.text() == '':
            self.arc_weight_input_warning.setText('Please enter a number.')
            self.arc_weight_input_warning.show()
        else:
            self.accept()

    def hide_arc_weight_warning(self):
        self.arc_weight_input_warning.hide()
        QTimer.singleShot(0, self.adjustSize)

    def get_stop_1(self):
        return self.stop_1.currentText()
    def get_stop_2(self):
        return self.stop_2.currentText()
    def get_arc_weight(self):
        return self.arc_weight_input.text()
    def get_direction(self):
        return self.direction_option.checkedButton().text()
    def get_route(self):
        if self.direction_option.checkedButton().text() == 'Directed':
            return self.directed_routes.checkedButton().text()
        else:
            return None

def update_style(widget):
    widget.style().unpolish(widget)
    widget.style().polish(widget)
    widget.repaint()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1539, 841)
        self.setWindowTitle('Graph Operator')

        # Application measure: 1539 x 841
        # PowerPoint slide: 33.867 x 19.05
        # Margin: 0.2cm (8.8 px -> 9)

        #The graphics scene
        self.workspace = QGraphicsScene(self)
        self.workspace.setSceneRect(QRectF(0, 0, 1539, 841))
        self.workspace.setBackgroundBrush(Qt.GlobalColor.white)

        self.view = QGraphicsView(self.workspace, self)
        self.view.setFrameStyle(0) #Removes any border
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        central = QWidget()
        self.setCentralWidget(central)
        self.workspace_layout = QVBoxLayout(central)
        self.workspace_layout.setSpacing(0)
        self.workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.workspace_layout.addWidget(self.view)

        self.add_vertex = False
        self.add_arc = False
        self.graph = {}

        #-------------------------------------------------
        #TOOLBAR (33.867 x 1)

        #Initialisation
        self.toolbar = QToolBar(self)
        self.addToolBar(self.toolbar)
        self.toolbar.setFixedHeight(44)

        #Fixing the toolbar's position
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)

        #The Undo button
        self.undo_action = QToolButton(self)
        self.undo_action.setIcon(QIcon(r'icons\undo.png'))
        self.undo_action.setIconSize(QSize(34, 34))
        self.undo_action.setFixedSize(34, 34)
        self.undo_action.setToolTip('Undo')

        #The Redo Button
        self.redo_action = QToolButton(self)
        self.redo_action.setIcon(QIcon(r'icons\redo.png'))
        self.redo_action.setIconSize(QSize(34, 34))
        self.redo_action.setFixedSize(34, 34)
        self.redo_action.setToolTip('Redo')

        #Open, Save & Wipe
        self.open_action = QAction('Open')
        self.open_action.setToolTip('Open a previously saved graph')
        self.save_action = QAction('Save')
        self.save_action.setToolTip('Save this graph to a file')
        self.wipe_action = QAction('Wipe')
        self.wipe_action.setToolTip('Delete the graph entirely')

        #Adding spacing for each button
        #From the left
        self.padding = QLabel(self)
        self.padding.setText(' ')
        self.padding.setFixedWidth(9)
        #Before the separator
        self.space = QLabel(self)
        self.space.setText(' ')
        self.space.setFixedWidth(11)
        #After the separator
        self.space_2 = QLabel(self)
        self.space_2.setText(' ')
        self.space_2.setFixedWidth(4)

        #Adding all toolbar functions
        self.toolbar.addWidget(self.padding)
        self.toolbar.addWidget(self.undo_action)
        self.toolbar.addWidget(self.redo_action)
        self.toolbar.addWidget(self.space)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(self.space_2)
        self.toolbar.addAction(self.open_action)
        self.toolbar.addAction(self.save_action)
        self.toolbar.addAction(self.wipe_action)


        #----------------------------------------------------------
        #GRAPH CONSTRUCTION, PROMPT BAR, EXIT PROCESS

        #Add a stop (3.96 x 1.16)
        self.add_vertex_button = QPushButton(self)
        self.add_vertex_button.setText('Add a stop')
        self.add_vertex_button.setFixedSize(160, 51)

        #Add a path (3.96 x 1.16)
        self.add_arc_button = QPushButton(self)
        self.add_arc_button.setText('Add a path')
        self.add_arc_button.setFixedSize(160, 51)

        #Prompt bar (1.16 x 17.36)
        self.prompt_bar = QLabel(self)
        self.prompt_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prompt_bar.setFixedSize(828, 51)
        self.prompt_bar.setProperty('type', 'prompt_bar')
        update_style(self.prompt_bar)
        self.prompt_bar.hide()

        #Exit process (1.16 x 5.4)
        self.exit_button = QPushButton(self)
        self.exit_button.setText('Exit process')
        self.exit_button.setFixedSize(245, 51)
        self.exit_button.hide()

        #Setting the horizontal layout
        self.header_layout = QHBoxLayout(self)
        self.header_layout.setSpacing(9)
        self.header_layout.setContentsMargins(0, 0, 0, 0) #Removing all margins
        self.header_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.header_layout.addWidget(self.add_vertex_button)
        self.header_layout.addWidget(self.add_arc_button)
        self.header_layout.addWidget(self.prompt_bar)
        self.header_layout.addWidget(self.exit_button)

        #Containing the layout in a widget for positioning
        self.header_layout_container = QWidget(self)
        self.header_layout_container.setGeometry(9, 53, 1421, 51)
        self.header_layout_container.setLayout(self.header_layout)


        #---------------------------------------------------------------------------
        #GRAPH ALGORITHMS

        #Dijkstra's icon (2 x 2)
        self.dijkstra_button = QPushButton(self)
        self.dijkstra_button.setFixedSize(91, 91)
        self.dijkstra_button.setIconSize(QSize(91, 91))
        self.dijkstra_button.setToolTip('Find the shortest path from one stop to another')

        #Nearest Neighbour icon (2 x 2)
        self.nearest_neighbour_button = QPushButton(self)
        self.nearest_neighbour_button.setFixedSize(91, 91)
        self.nearest_neighbour_button.setIconSize(QSize(91, 91))
        self.nearest_neighbour_button.setToolTip('Find the shortest path to visit all stops and return')

        #Setting a vertical layout for the mathematical functions
        self.side_layout = QVBoxLayout(self)
        self.side_layout.setSpacing(4)
        self.side_layout.setContentsMargins(0, 0, 0, 0)
        self.side_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        self.side_layout.addWidget(self.dijkstra_button)
        self.side_layout.addWidget(self.nearest_neighbour_button)

        self.side_layout_container = QWidget(self)
        self.side_layout_container.setGeometry(1438, 44, 91, 202)
        self.side_layout_container.setLayout(self.side_layout)


        #--------------------------------------------------------------------------
        #FUNCTION OPERATION

        self.highlight_dijkstra(True)
        self.highlight_nearest_neighbour(True)

        self.vertices = {}

        self.add_vertex_button.clicked.connect(self.adding_a_vertex)
        self.add_arc_button.clicked.connect(self.adding_an_arc)

    def highlight_dijkstra(self, state):
        if state:
            self.dijkstra_button.setIcon(QIcon(r'icons\dijkstra (enabled).png'))
        else:
            self.dijkstra_button.setIcon(QIcon(r'icons\dijkstra (disabled).png'))

    def highlight_nearest_neighbour(self, state):
        if state:
            self.nearest_neighbour_button.setIcon(
                QIcon(r'icons\nearest neighbour (enabled).png'))
        else:
            self.nearest_neighbour_button.setIcon(
                QIcon(r'icons\nearest neighbour (disabled).png'))

    def isolate_role(self, role):
        #Disabling the buttons
        self.add_vertex_button.setEnabled(False)
        self.add_arc_button.setEnabled(False)
        self.dijkstra_button.setEnabled(False)
        self.nearest_neighbour_button.setEnabled(False)

        #Highlighting the appropriate function
        match role:
            case 'add_vertex':
                self.add_vertex_button.setProperty('state', 'highlighted')
                self.add_arc_button.setProperty('state', 'greyed')
            case 'add_arc':
                self.add_arc_button.setProperty('state', 'highlighted')
                self.add_vertex_button.setProperty('state', 'greyed')
            case 'dijkstra':
                self.add_vertex_button.setProperty('state', 'greyed')
                self.add_arc_button.setProperty('state', 'greyed')
                self.highlight_dijkstra(True)
                self.highlight_nearest_neighbour(False)
            case 'nearest_neighbour':
                self.add_vertex_button.setProperty('state', 'greyed')
                self.add_arc_button.setProperty('state', 'greyed')
                self.highlight_dijkstra(False)
                self.highlight_nearest_neighbour(True)

        update_style(self.add_vertex_button)
        update_style(self.add_arc_button)

    def exit_process(self):
        #Resetting the interface
        self.add_vertex_button.setEnabled(True)
        self.add_arc_button.setEnabled(True)
        self.dijkstra_button.setEnabled(True)
        self.nearest_neighbour_button.setEnabled(True)
        self.highlight_dijkstra(True)
        self.highlight_nearest_neighbour(True)
        self.prompt_bar.hide()
        self.exit_button.hide()

    def adding_a_vertex(self):
        self.isolate_role('add_vertex')
        self.add_vertex = True

        #Setting the label
        self.prompt_bar.setText('<strong>Click anywhere</strong> to place a <strong>stop</strong>')
        self.prompt_bar.setProperty('type', 'prompt_bar')
        self.prompt_bar.setProperty('role', 'construct_graph')
        update_style(self.prompt_bar)
        self.prompt_bar.show()

        #Setting the exit button
        self.exit_button.setProperty('type', 'exit')
        self.exit_button.setProperty('role', 'construct_graph')
        update_style(self.exit_button)
        self.exit_button.show()
        self.exit_button.clicked.connect(self.exit_process)

    def adding_an_arc(self):
        self.isolate_role('add_arc')
        vertices = list(self.graph.keys())

        add_arc_dialog = AddArcDialog(vertices)

        if add_arc_dialog.exec() == QDialog.DialogCode.Accepted:
            #Getting all the values
            stop_1 = add_arc_dialog.get_stop_1()
            stop_2 = add_arc_dialog.get_stop_2()
            arc_weight = float(add_arc_dialog.get_arc_weight())
            direction_option = add_arc_dialog.get_direction()
            directed_route = add_arc_dialog.get_route()

            #Updating the graph
            if direction_option == 'Undirected':
                self.graph[stop_1][stop_2] = arc_weight
                self.graph[stop_2][stop_1] = arc_weight
            else:
                if directed_route == f'{stop_1} → {stop_2}':
                    self.graph[stop_1][stop_2] = arc_weight
                else:
                    self.graph[stop_2][stop_1] = arc_weight

            #Drawing the arc
            stop_1_x = self.vertices[stop_1][0]
            stop_1_y = self.vertices[stop_1][1]
            stop_2_x = self.vertices[stop_2][0]
            stop_2_y = self.vertices[stop_2][1]

            arc = QGraphicsLineItem(
                stop_1_x + 5, stop_1_y - 10,
                stop_2_x + 5, stop_2_y - 10
            )
            arc.setPen(QPen(QColor(Qt.GlobalColor.black), 4))
            arc.setZValue(12) #Setting it behind the vertices
            self.workspace.addItem(arc)

            print(self.vertices)
            #Adding the arc weight
            arc_weight_label = QLabel(self)
            arc_weight_label.setText(str(arc_weight))
            arc_weight_label.adjustSize()

            arc_weight_label.setFixedWidth(arc_weight_label.width() + 6)
            arc_weight_label.setFixedHeight(arc_weight_label.height() + 6)
            print(self.vertices)

            #Finding the width difference
            if stop_2_x > stop_1_x: #If stop 2 is further out than stop 1...
                width_place = stop_1_x + (stop_2_x - stop_1_x) // 2
            elif stop_2_x < stop_1_x:
                width_place = stop_2_x + (stop_1_x - stop_2_x) // 2
            else:
                width_place = stop_1_x

            #Finding the height difference
            if stop_2_x > stop_1_x:  # If stop 2 is further out than stop 1...
                height_place = stop_1_y + (stop_2_y - stop_1_y) // 2
            elif stop_2_x < stop_1_x:
                height_place = stop_2_y + (stop_1_y - stop_2_y) // 2
            else:
                height_place = stop_1_y

            # - arc_weight_label.height() // 2

            arc_weight_label.move(width_place - arc_weight_label.width() // 2, height_place)
            arc_weight_label.setStyleSheet('background-color: white; color: black; font-size: 20px; font-weight: bold')
            arc_weight_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            arc_weight_label.adjustSize()
            arc_weight_label.show()


            self.exit_process()

    def mousePressEvent(self, event):

        if self.add_vertex:
            #To stop it triggering in the future
            self.add_vertex = False

            #Finding the position of the mouseclick
            vertex_pos_x = int(event.position().x())
            vertex_pos_y = int(event.position().y())

            #Vertex initialisation
            vertex = QLabel(self)
            vertex.setFixedSize(76, 76)
            vertex.move(int(vertex_pos_x) - 38, int(vertex_pos_y) - 38)

            #Setting the base design
            vertex = QGraphicsEllipseItem(vertex_pos_x, vertex_pos_y, 76, 76)
            vertex.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

            #The placeholder design
            vertex.setBrush(QBrush(QColor(Qt.GlobalColor.transparent)))
            outline = QPen(QColor('#0033CC'), 3)
            outline.setStyle(Qt.PenStyle.DotLine)
            vertex.setPen(outline)
            self.workspace.addItem(vertex)

            #The dialog to set the vertex name
            add_vertex_dialog = AddVertexDialog(list(self.graph.keys()))

            #If OK clicked...
            if add_vertex_dialog.exec() == QDialog.DialogCode.Accepted:
                vertex_name = add_vertex_dialog.get_vertex_name()
                print(346538325834)

                #Setting the default look
                vertex.setBrush(QBrush(QColor(Qt.GlobalColor.red)))
                outline.setColor(QColor(Qt.GlobalColor.white))
                outline.setStyle(Qt.PenStyle.SolidLine)
                vertex.setPen(outline)
                vertex.setZValue(0)
                print(346538325834)

                vertex_label = QLabel(vertex_name)
                vertex_label.setProperty('vertex_name', 'default')
                update_style(vertex_label)
                vertex_label.setProperty('state', 'default')
                update_style(vertex_label)
                vertex_label.adjustSize()

                vertex_label.move(vertex_pos_x + 38 - vertex_label.width() // 2,
                                  vertex_pos_y + 38 - vertex_label.height() // 2)
                print(346538325834)

                proxy = QGraphicsProxyWidget()
                proxy.setWidget(vertex_label)
                self.workspace.addItem(vertex)
                self.workspace.addItem(proxy)
                proxy.setParentItem(vertex)
                vertex.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable | QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)


                self.graph[vertex_name] = {}

                self.vertices[vertex_name] = [vertex_pos_x, vertex_pos_y]

            #...else if Cancel clicked...
            else:
                vertex.hide()

            self.exit_process()

app = QApplication([])
window = MainWindow()
window.setStyleSheet(QSS_styling)
window.show()

app.exec()