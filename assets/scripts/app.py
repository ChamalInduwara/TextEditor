import sys
import os
import pywinstyles
import assets.scripts.variables as vary

from PyQt6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QFont, QTextOption
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QStatusBar, QComboBox, QSpinBox, QTabWidget, QDialog, QPlainTextEdit,
    QLabel, QVBoxLayout, QDialogButtonBox, QHBoxLayout, QFileDialog, QListWidget, QPushButton, QStackedLayout,
    QWidget, QGridLayout, QRadioButton, QCheckBox
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        vary.main_window = self
        self.setWindowTitle('Text Editor')
        self.setWindowIcon(QIcon('assets/images/icon.ico'))
        self.setGeometry(vary.x, vary.y, vary.width, vary.height)
        self.setting_toolbars_menu_bars_statusbar()

    def setting_toolbars_menu_bars_statusbar(self):
        self.newAction = QAction(QIcon(f'assets/images/new-{vary.theme}'), '&New', self)
        self.newAction.setShortcut(QKeySequence('Ctrl+n'))
        self.newAction.setStatusTip('Create new file')
        self.newAction.triggered.connect(self.newActionHandler)

        self.openAction = QAction(QIcon(f'assets/images/open-{vary.theme}'), '&Open', self)
        self.openAction.setShortcut(QKeySequence('Ctrl+o'))
        self.openAction.setStatusTip('Open a file')
        self.openAction.triggered.connect(lambda: self.openSaveFileActionHandler(0))

        self.saveAction = QAction(QIcon(f'assets/images/save-{vary.theme}'), '&Save', self)
        self.saveAction.setShortcut(QKeySequence('Ctrl+s'))
        self.saveAction.setStatusTip('Save current file')
        self.saveAction.triggered.connect(lambda: self.openSaveFileActionHandler(1))

        self.saveAsAction = QAction(QIcon(f'assets/images/save-as-{vary.theme}'), 'S&ave as', self)
        self.saveAsAction.setShortcut(QKeySequence('Ctrl+shift+s'))
        self.saveAsAction.setStatusTip('Save current file')
        self.saveAsAction.triggered.connect(lambda: self.openSaveFileActionHandler(2))

        self.closeAction = QAction(QIcon(f'assets/images/close-{vary.theme}'), '&Close', self)
        self.closeAction.setShortcut(QKeySequence('Ctrl+q'))
        self.closeAction.setStatusTip('Close current file')
        self.closeAction.triggered.connect(lambda: self.closeTabAction(vary.tab_number))

        self.settingsAction = QAction(QIcon(f'assets/images/settings-{vary.theme}'), '&Preferences', self)
        self.settingsAction.setShortcut(QKeySequence('Ctrl+p'))
        self.settingsAction.setStatusTip('Open preferences')
        self.settingsAction.triggered.connect(self.openPreferences)

        self.exitAction = QAction('&Exit', self)
        self.exitAction.setShortcut(QKeySequence('Escape'))
        self.exitAction.setStatusTip('Exit Text Editor')
        self.exitAction.triggered.connect(lambda: sys.exit())

        self.undoAction = QAction(QIcon(f'assets/images/undo-{vary.theme}'), '&Undo', self)
        self.undoAction.setShortcut(QKeySequence('Ctrl+z'))
        self.undoAction.setStatusTip('Undo the recent changes')
        self.undoAction.triggered.connect(lambda: self.tabs.widget(vary.tab_number).undo())

        self.redoAction = QAction(QIcon(f'assets/images/redo-{vary.theme}'), '&Redo', self)
        self.redoAction.setShortcut(QKeySequence('Ctrl+shift+z'))
        self.redoAction.setStatusTip('Redo the recent changes')
        self.redoAction.triggered.connect(lambda: self.tabs.widget(vary.tab_number).redo())

        self.selectAction = QAction(QIcon(f'assets/images/select-{vary.theme}'), '&Select All', self)
        self.selectAction.setShortcut(QKeySequence('Ctrl+a'))
        self.selectAction.setStatusTip('Select all text')
        self.selectAction.triggered.connect(lambda: self.tabs.widget(vary.tab_number).selectAll())

        self.copyAction = QAction(QIcon(f'assets/images/copy-{vary.theme}'), '&Copy', self)
        self.copyAction.setShortcut(QKeySequence('Ctrl+c'))
        self.copyAction.setStatusTip('Copy the selected text')
        self.copyAction.triggered.connect(lambda: self.tabs.widget(vary.tab_number).copy())

        self.cutAction = QAction(QIcon(f'assets/images/cut-{vary.theme}'), 'Cu&t', self)
        self.cutAction.setShortcut(QKeySequence('Ctrl+x'))
        self.cutAction.setStatusTip('Cut the selected text')
        self.cutAction.triggered.connect(lambda: self.tabs.widget(vary.tab_number).cut())

        self.pasteAction = QAction(QIcon(f'assets/images/paste-{vary.theme}'), '&Paste', self)
        self.pasteAction.setShortcut(QKeySequence('Ctrl+v'))
        self.pasteAction.setStatusTip('Paste the text from clipboard')
        self.pasteAction.triggered.connect(lambda: self.tabs.widget(vary.tab_number).paste())

        self.deleteAction = QAction(QIcon(f'assets/images/delete-{vary.theme}'), '&Delete', self)
        self.deleteAction.setShortcut(QKeySequence('delete'))
        self.deleteAction.setStatusTip('Delete')
        self.deleteAction.triggered.connect(self.deleteActionHandler)

        self.clearAction = QAction(QIcon(f'assets/images/clear-{vary.theme}'), 'C&lear All', self)
        self.clearAction.setShortcut(QKeySequence('shift+delete'))
        self.clearAction.setStatusTip('Clear all text')
        self.clearAction.triggered.connect(lambda: self.tabs.widget(vary.tab_number).clear())

        self.fileToolAction = QAction('Toggle &File Toolbar', self)
        self.fileToolAction.setShortcut(QKeySequence('ctrl+f'))
        self.fileToolAction.setStatusTip('Toggle files toolbar')
        self.fileToolAction.triggered.connect(lambda: self.toggleActionHandler(0))

        self.editToolAction = QAction('Toggle &Edit Toolbar', self)
        self.editToolAction.setShortcut(QKeySequence('ctrl+e'))
        self.editToolAction.setStatusTip('Toggle edit toolbar')
        self.editToolAction.triggered.connect(lambda: self.toggleActionHandler(1))

        self.statusAction = QAction('Toggle &Status Bar', self)
        self.statusAction.setShortcut(QKeySequence('ctrl+b'))
        self.statusAction.setStatusTip('Toggle status bar')
        self.statusAction.triggered.connect(lambda: self.toggleActionHandler(2))

        self.fontFamily = QComboBox()
        self.fontFamily.setStatusTip('Choose font family')
        self.fontFamily.addItems(vary.fonts)
        self.fontFamily.setCurrentIndex(vary.index)
        self.fontFamily.setMaxCount(vary.num)
        self.fontFamily.setEditable(True)
        self.fontFamily.currentIndexChanged.connect(lambda: self.changeFontActionHandler(0))

        self.fontSize = QSpinBox()
        self.fontSize.setStatusTip('Choose font size')
        self.fontSize.setValue(vary.active_font[1])
        self.fontSize.setRange(0, 72)
        self.fontSize.valueChanged.connect(lambda: self.changeFontActionHandler(1))

        self.menu = self.menuBar()

        self.fileMenu = self.menu.addMenu('&File')
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.closeAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.settingsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)

        self.editMenu = self.menu.addMenu('&Edit')
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addAction(self.deleteAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.selectAction)
        self.editMenu.addAction(self.clearAction)

        self.viewMenu = self.menu.addMenu('&View')
        self.viewMenu.addAction(self.fileToolAction)
        self.viewMenu.addAction(self.editToolAction)
        self.viewMenu.addAction(self.statusAction)

        self.fileToolBar = QToolBar('Files')
        self.fileToolBar.setMovable(False)
        self.fileToolBar.setIconSize(QSize(30, 30))
        self.fileToolBar.addAction(self.newAction)
        self.fileToolBar.addAction(self.openAction)
        self.fileToolBar.addAction(self.saveAction)
        self.fileToolBar.addAction(self.saveAsAction)
        self.fileToolBar.addAction(self.closeAction)
        self.fileToolBar.addSeparator()

        self.editToolBar = QToolBar('Edit')
        self.editToolBar.setMovable(False)
        self.editToolBar.setIconSize(QSize(30, 30))
        self.editToolBar.addWidget(self.fontFamily)
        self.editToolBar.addWidget(self.fontSize)
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.undoAction)
        self.editToolBar.addAction(self.redoAction)
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.copyAction)
        self.editToolBar.addAction(self.cutAction)
        self.editToolBar.addAction(self.pasteAction)
        self.editToolBar.addAction(self.deleteAction)
        self.editToolBar.addSeparator()
        self.editToolBar.addAction(self.selectAction)
        self.editToolBar.addAction(self.clearAction)

        self.addToolBar(self.fileToolBar)
        self.addToolBar(self.editToolBar)

        self.setStatusBar(QStatusBar(self))
        self.setting_central_widgets()

    def setting_central_widgets(self):
        self.tabs = QTabWidget()
        self.tabs.setMovable(False)
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeTabAction)
        self.tabs.currentChanged.connect(self.tabChange)
        self.tabs.setFocus()

        self.text_box_1 = QPlainTextEdit()
        vary.QFont = QFont(vary.active_font[0], vary.active_font[1])
        self.text_box_1.setFont(vary.QFont)
        if vary.doc_info[0] == 0:
            self.text_box_1.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
            self.text_box_1.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        elif vary.doc_info[0] == 1:
            self.text_box_1.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
            self.text_box_1.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.text_box_1.setTabStopDistance(vary.doc_info[1])

        if vary.interface[0] == 1:
            self.fileToolBar.setVisible(True)
        elif vary.interface[0] == 0:
            self.fileToolBar.setVisible(False)
        if vary.interface[1] == 1:
            self.editToolBar.setVisible(True)
        elif vary.interface[1] == 0:
            self.editToolBar.setVisible(False)
        if vary.interface[2] == 1:
            self.statusBar().setVisible(True)
        elif vary.interface[2] == 0:
            self.statusBar().setVisible(False)

        self.tabs.addTab(self.text_box_1, 'New Doc 1')

        self.setCentralWidget(self.tabs)

    def deleteActionHandler(self):
        text = self.tabs.widget(vary.tab_number).toPlainText()
        text = text[:-1]
        self.tabs.widget(vary.tab_number).setPlainText(text)

    def changeFontActionHandler(self, event):
        if event == 0:
            vary.active_font[0] = self.fontFamily.currentText()
        elif event == 1:
            vary.active_font[1] = int(self.fontSize.value())

        vary.QFont = QFont(vary.active_font[0], vary.active_font[1])
        for i in range(0, vary.tab_count):
            self.tabs.widget(i).setFont(vary.QFont)

        text = f'{vary.active_font[0]}\n{vary.active_font[1]}'
        file = open('assets/data/font.txt', 'w')
        file.write(text)

    def openPreferences(self):
        dialog = Settings(self)
        if dialog.exec():
            for i in range(0, vary.tab_count):
                self.tabs.widget(i).setFont(vary.QFont)

    def toggleActionHandler(self, event):
        if event == 0:
            if self.fileToolBar.isHidden():
                self.fileToolBar.setVisible(True)
                vary.interface[0] = 1
            else:
                self.fileToolBar.setVisible(False)
                vary.interface[0] = 0

        elif event == 1:
            if self.editToolBar.isHidden():
                self.editToolBar.setVisible(True)
                vary.interface[1] = 1
            else:
                self.editToolBar.setVisible(False)
                vary.interface[1] = 0

        elif event == 2:
            if self.statusBar().isHidden():
                self.statusBar().setVisible(True)
                vary.interface[2] = 1
            else:
                self.statusBar().setVisible(False)
                vary.interface[2] = 0

        text = f'{vary.interface[0]}\n{vary.interface[1]}\n{vary.interface[2]}'
        file = open('assets/data/int.txt', 'w')
        file.write(text)

    def openSaveFileActionHandler(self, event):
        if event == 0:
            fname = QFileDialog.getOpenFileName(self, 'Open File', 'D:\\', 'Text files (*.txt);; All files (*.*)')
            if not fname[0] == '':
                try:
                    vary.file_loc[vary.tab_count] = fname[0]
                    text = open(vary.file_loc[vary.tab_count], 'r').read()
                    full_name = os.path.basename(vary.file_loc[vary.tab_count])
                    self.entry = QPlainTextEdit()
                    vary.tab_count += 1
                    self.entry.setFont(vary.QFont)
                    self.entry.setPlainText(text)
                    if vary.doc_info[0] == 0:
                        self.entry.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
                        self.entry.setWordWrapMode(QTextOption.WrapMode.NoWrap)
                    elif vary.doc_info[0] == 1:
                        self.entry.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
                        self.entry.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
                    self.entry.setTabStopDistance(vary.doc_info[1])
                    self.tabs.addTab(self.entry, full_name)
                except Exception as e:
                    print(e)
        elif event == 1:
            if not self.tabs.widget(vary.tab_number).document().isModified():
                return
            else:
                if vary.file_loc[vary.tab_number] == '':
                    self.openSaveFileActionHandler(2)
                else:
                    with open(vary.file_loc[vary.tab_number], 'w') as f:
                        f.write(self.tabs.widget(vary.tab_number).toPlainText())
        elif event == 2:
            if not self.tabs.widget(vary.tab_number).document().isModified():
                return
            else:
                fname = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files(*.txt);;All files(*.*)')
                vary.file_loc[vary.tab_number] = fname[0]
                with open(vary.file_loc[vary.tab_number], 'w') as f:
                    f.write(self.tabs.widget(vary.tab_number).toPlainText())
                full_name = os.path.basename(vary.file_loc[vary.tab_number])
                self.tabs.setTabText(vary.tab_number, full_name)

    def newActionHandler(self):
        self.entry = QPlainTextEdit()
        self.entry.setFont(vary.QFont)
        if vary.doc_info[0] == 0:
            self.entry.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
            self.entry.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        elif vary.doc_info[0] == 1:
            self.entry.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
            self.entry.setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
        self.entry.setTabStopDistance(vary.doc_info[1])
        vary.tab_count += 1
        array = []
        for i in range(0, vary.tab_count):
            array.append(self.tabs.tabText(i))
        rem_ar = []
        for i in range(0, len(array)):
            if 'New Doc ' in array[i]:
                array[i] = array[i].replace('New Doc ', '')
            else:
                rem_ar.append(array[i])
        for i in rem_ar:
            array.remove(i)
        for i in range(0, len(array)):
            array[i] = int(array[i])
        for i in range(1, 10000000):
            if i not in array:
                self.tabs.addTab(self.entry, f'New Doc {i}')
                break

    def tabChange(self, event):
        vary.tab_number = event

    def closeTabAction(self, event):
        try:
            if self.tabs.widget(event).toPlainText() != '':
                dialog = DialogOne(self)
                if dialog.exec():
                    self.tabs.removeTab(event)
                    vary.tab_count -= 1
                else:
                    pass
            else:
                self.tabs.removeTab(event)
                vary.tab_count -= 1

            vary.file_loc.pop(event)
        except Exception as e:
            print(e)

    def resizeEvent(self, event):
        vary.width = self.width()
        vary.height = self.height()
        text = f'{vary.width}\n{vary.height}'
        file = open('assets/data/winfo.txt', 'w')
        file.write(text)

    def closeEvent(self, event):
        dialog = DialogTwo(self)
        if dialog.exec():
            event.accept()
        else:
            event.ignore()


class Settings(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Text Editor - Preferences')
        # self.resize(QSize(550, 300))
        self.list = QListWidget()
        self.list.addItems(['Appearance', 'Document Settings', 'Document Information'])
        self.list.setCurrentRow(0)
        self.list.currentRowChanged.connect(self.changeStack)

        self.lbl_1 = QLabel('Appearance')
        self.lbl_1.setObjectName('title')
        self.lbl_1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.gap = QLabel('')
        self.lbl_2 = QLabel('Select Theme: ')
        self.lbl_2.setObjectName('topic')
        self.checkOne = QRadioButton('Dark theme')
        self.checkOne.released.connect(lambda: self.themeChangeAction('dark'))
        self.checkTwo = QRadioButton('Light theme')
        self.checkTwo.released.connect(lambda: self.themeChangeAction('light'))
        self.lbl_17 = QLabel('Interface: ')
        self.lbl_17.setObjectName('topic')
        self.checkFive = QCheckBox('File ToolBar')
        self.checkFive.released.connect(lambda: self.toggleInterfaceAction(self.checkFive.isChecked(), 0))
        self.checkSix = QCheckBox('Edit ToolBar')
        self.checkSix.released.connect(lambda: self.toggleInterfaceAction(self.checkSix.isChecked(), 1))
        self.checkSeven = QCheckBox('Status Bar')
        self.checkSeven.released.connect(lambda: self.toggleInterfaceAction(self.checkSeven.isChecked(), 2))

        if vary.theme == 'dark':
            self.checkOne.setChecked(True)
            self.checkTwo.setChecked(False)
        elif vary.theme == 'light':
            self.checkTwo.setChecked(True)
            self.checkOne.setChecked(False)

        if vary.interface[0] == 1:
            self.checkFive.setChecked(True)
        elif vary.interface[0] == 0:
            self.checkFive.setChecked(False)
        if vary.interface[1] == 1:
            self.checkSix.setChecked(True)
        elif vary.interface[1] == 0:
            self.checkSix.setChecked(False)
        if vary.interface[2] == 1:
            self.checkSeven.setChecked(True)
        elif vary.interface[2] == 0:
            self.checkSeven.setChecked(False)

        text = vary.main_window.tabs.widget(vary.tab_number).toPlainText()
        text = text.replace('\n', '')

        self.lbl_3 = QLabel('Document Information')
        self.lbl_3.setObjectName('title')
        self.lbl_3.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lbl_4 = QLabel('Document Name: ')
        self.lbl_4.setObjectName('topic')
        self.lbl_5 = QLabel(vary.main_window.tabs.tabText(vary.tab_number))
        self.lbl_6 = QLabel('Document Location: ')
        self.lbl_6.setObjectName('topic')
        self.lbl_7 = QLabel(vary.file_loc[vary.tab_number])
        self.lbl_8 = QLabel('Line Count: ')
        self.lbl_8.setObjectName('topic')
        self.lbl_9 = QLabel(f'{vary.main_window.tabs.widget(vary.tab_number).blockCount()}')
        self.lbl_10 = QLabel('Word Count: ')
        self.lbl_10.setObjectName('topic')
        self.lbl_11 = QLabel(f'{len(text)}')

        self.lbl_12 = QLabel('Document Settings')
        self.lbl_12.setObjectName('title')
        self.lbl_12.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.lbl_13 = QLabel('Word Wrap: ')
        self.lbl_13.setObjectName('topic')
        self.checkThree = QRadioButton('Enable')
        self.checkThree.released.connect(lambda: self.toggleWordWrapAction(1))
        self.checkFour = QRadioButton('Disable')
        self.checkFour.released.connect(lambda: self.toggleWordWrapAction(0))
        self.lbl_14 = QLabel('Tab Length: ')
        self.lbl_14.setObjectName('topic')
        self.tabSize = QSpinBox()
        self.tabSize.setValue(vary.doc_info[1])
        self.tabSize.setRange(10, 30)
        self.tabSize.setSingleStep(5)
        self.tabSize.valueChanged.connect(self.tabLengthAction)
        self.lbl_15 = QLabel('Font Family: ')
        self.lbl_15.setObjectName('topic')
        self.fontFamily = QComboBox()
        self.fontFamily.addItems(vary.fonts)
        self.fontFamily.setCurrentIndex(vary.index)
        self.fontFamily.setMaxCount(vary.num)
        self.fontFamily.setEditable(True)
        self.fontFamily.currentTextChanged.connect(lambda: self.changeFontActionHandler(0))
        self.lbl_16 = QLabel('Font Size: ')
        self.lbl_16.setObjectName('topic')
        self.fontSize = QSpinBox()
        self.fontSize.setValue(vary.active_font[1])
        self.fontSize.setRange(0, 72)
        self.fontSize.valueChanged.connect(lambda: self.changeFontActionHandler(1))

        if vary.doc_info[0] == 1:
            self.checkThree.setChecked(True)
            self.checkFour.setChecked(False)
        elif vary.doc_info[0] == 0:
            self.checkFour.setChecked(True)
            self.checkThree.setChecked(False)

        self.saveBtn = QPushButton('Save')
        self.saveBtn.clicked.connect(lambda: self.saveActionHandler(0))
        self.okBtn = QPushButton('Ok')
        self.okBtn.clicked.connect(lambda: self.saveActionHandler(1))

        self.appearanceStack = QGridLayout()
        self.appearanceStack.addWidget(self.lbl_1, 0, 0, 1, 2)
        self.appearanceStack.addWidget(self.lbl_2, 1, 0, 2, 1)
        self.appearanceStack.addWidget(self.checkOne, 1, 1)
        self.appearanceStack.addWidget(self.checkTwo, 2, 1)
        self.appearanceStack.addWidget(self.lbl_17, 3, 0, 2, 1)
        self.appearanceStack.addWidget(self.checkFive, 3, 1)
        self.appearanceStack.addWidget(self.checkSix, 4, 1)
        self.appearanceStack.addWidget(self.checkSeven, 5, 1)
        self.appearanceStack.addWidget(self.gap, 6, 0, 1, 2)
        self.containerOne = QWidget()
        self.containerOne.setLayout(self.appearanceStack)

        self.docSetStack = QGridLayout()
        self.docSetStack.addWidget(self.lbl_12, 0, 0, 1, 2)
        self.docSetStack.addWidget(self.lbl_13, 1, 0, 2, 1)
        self.docSetStack.addWidget(self.checkThree, 1, 1)
        self.docSetStack.addWidget(self.checkFour, 2, 1)
        self.docSetStack.addWidget(self.lbl_14, 3, 0)
        self.docSetStack.addWidget(self.tabSize, 3, 1)
        self.docSetStack.addWidget(self.lbl_15, 4, 0)
        self.docSetStack.addWidget(self.fontFamily, 4, 1)
        self.docSetStack.addWidget(self.lbl_16, 5, 0)
        self.docSetStack.addWidget(self.fontSize, 5, 1)
        self.containerTwo = QWidget()
        self.containerTwo.setLayout(self.docSetStack)

        self.docInfoStack = QGridLayout()
        self.docInfoStack.addWidget(self.lbl_3, 0, 0, 1, 2)
        self.docInfoStack.addWidget(self.lbl_4, 1, 0)
        self.docInfoStack.addWidget(self.lbl_5, 1, 1)
        self.docInfoStack.addWidget(self.lbl_6, 2, 0)
        self.docInfoStack.addWidget(self.lbl_7, 2, 1)
        self.docInfoStack.addWidget(self.lbl_8, 3, 0)
        self.docInfoStack.addWidget(self.lbl_9, 3, 1)
        self.docInfoStack.addWidget(self.lbl_10, 4, 0)
        self.docInfoStack.addWidget(self.lbl_11, 4, 1)
        self.containerThree = QWidget()
        self.containerThree.setLayout(self.docInfoStack)

        self.stacked = QStackedLayout()
        self.stacked.addWidget(self.containerOne)
        self.stacked.addWidget(self.containerTwo)
        self.stacked.addWidget(self.containerThree)

        self.lay_one = QHBoxLayout()
        self.lay_one.addWidget(self.list)
        self.lay_one.addLayout(self.stacked)

        self.lay_two = QHBoxLayout()
        self.lay_two.addWidget(self.saveBtn)
        self.lay_two.addWidget(self.okBtn)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.lay_one)
        self.layout.addLayout(self.lay_two)

        self.setLayout(self.layout)

    def changeFontActionHandler(self, event):
        if event == 0:
            vary.active_font[0] = self.fontFamily.currentText()
        elif event == 1:
            vary.active_font[1] = int(self.fontSize.value())

    def tabLengthAction(self, event):
        vary.doc_info[1] = event

    def toggleWordWrapAction(self, event):
        vary.doc_info[0] = event

    def toggleInterfaceAction(self, event, item):
        if event:
            num = 1
        else:
            num = 0
        vary.interface[item] = num

    def themeChangeAction(self, event):
        vary.theme = event

    def changeStack(self, event):
        self.stacked.setCurrentIndex(event)

    def saveActionHandler(self, event):
        vary.QFont = QFont(vary.active_font[0], vary.active_font[1])
        vary.main_window.fontFamily.setCurrentIndex(vary.fonts.index(vary.active_font[0]))
        vary.main_window.fontSize.setValue(vary.active_font[1])

        for i in range(0, vary.tab_count):
            if vary.doc_info[0] == 0:
                vary.main_window.tabs.widget(i).setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
                vary.main_window.tabs.widget(i).setWordWrapMode(QTextOption.WrapMode.NoWrap)
            elif vary.doc_info[0] == 1:
                vary.main_window.tabs.widget(i).setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
                vary.main_window.tabs.widget(i).setWordWrapMode(QTextOption.WrapMode.WrapAnywhere)
            vary.main_window.tabs.widget(i).setTabStopDistance(vary.doc_info[1])

        if vary.interface[0] == 1:
            vary.main_window.fileToolBar.setVisible(True)
        elif vary.interface[0] == 0:
            vary.main_window.fileToolBar.setVisible(False)
        if vary.interface[1] == 1:
            vary.main_window.editToolBar.setVisible(True)
        elif vary.interface[1] == 0:
            vary.main_window.editToolBar.setVisible(False)
        if vary.interface[2] == 1:
            vary.main_window.statusBar().setVisible(True)
        elif vary.interface[2] == 0:
            vary.main_window.statusBar().setVisible(False)

        text = f'{vary.theme}'
        file = open('assets/data/theme.txt', 'w')
        file.write(text)
        file.close()
        text = f'{vary.width}\n{vary.height}'
        file = open('assets/data/winfo.txt', 'w')
        file.write(text)
        file.close()
        text = f'{vary.interface[0]}\n{vary.interface[1]}\n{vary.interface[2]}'
        file = open('assets/data/int.txt', 'w')
        file.write(text)
        file.close()
        text = f'{vary.active_font[0]}\n{vary.active_font[1]}'
        file = open('assets/data/font.txt', 'w')
        file.write(text)
        file.close()
        text = f'{vary.doc_info[0]}\n{vary.doc_info[1]}'
        file = open('assets/data/docinfo.txt', 'w')
        file.write(text)
        file.close()

        styleSheet = open(f'assets/style/{vary.theme}.qss', 'r').read()
        vary.app.setStyleSheet(styleSheet)
        vary.main_window.newAction.setIcon(QIcon(f'assets/images/new-{vary.theme}'))
        vary.main_window.openAction.setIcon(QIcon(f'assets/images/open-{vary.theme}'))
        vary.main_window.saveAction.setIcon(QIcon(f'assets/images/save-{vary.theme}'))
        vary.main_window.saveAsAction.setIcon(QIcon(f'assets/images/save-as-{vary.theme}'))
        vary.main_window.closeAction.setIcon(QIcon(f'assets/images/close-{vary.theme}'))
        vary.main_window.settingsAction.setIcon(QIcon(f'assets/images/settings-{vary.theme}'))
        vary.main_window.undoAction.setIcon(QIcon(f'assets/images/undo-{vary.theme}'))
        vary.main_window.redoAction.setIcon(QIcon(f'assets/images/redo-{vary.theme}'))
        vary.main_window.selectAction.setIcon(QIcon(f'assets/images/select-{vary.theme}'))
        vary.main_window.copyAction.setIcon(QIcon(f'assets/images/copy-{vary.theme}'))
        vary.main_window.cutAction.setIcon(QIcon(f'assets/images/cut-{vary.theme}'))
        vary.main_window.pasteAction.setIcon(QIcon(f'assets/images/paste-{vary.theme}'))
        vary.main_window.deleteAction.setIcon(QIcon(f'assets/images/delete-{vary.theme}'))
        vary.main_window.clearAction.setIcon(QIcon(f'assets/images/clear-{vary.theme}'))

        if event == 1:
            self.close()


class DialogOne(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Text Editor - File Close Warning')

        img = QPixmap('assets/images/warning.png')
        img = img.scaledToWidth(70)

        self.lbl_0 = QLabel()
        self.lbl_0.setPixmap(img)

        self.lbl = QLabel('This action will clear all the text in the given document.')
        self.lbl_1 = QLabel('Do you want to proceed?')

        self.btn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.btn_box = QDialogButtonBox(self.btn)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)

        self.lay_1 = QVBoxLayout()
        self.lay_1.addWidget(self.lbl)
        self.lay_1.addWidget(self.lbl_1)

        self.lay_2 = QHBoxLayout()
        self.lay_2.addWidget(self.lbl_0)
        self.lay_2.addLayout(self.lay_1)

        self.lay = QVBoxLayout()
        self.lay.addLayout(self.lay_2)
        self.lay.addWidget(self.btn_box)

        self.setLayout(self.lay)


class DialogTwo(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Text Editor - Exit Warning')
        self.resize(QSize(300, 100))

        img = QPixmap('assets/images/warning.png')
        img = img.scaledToWidth(70)

        self.lbl_0 = QLabel()
        self.lbl_0.setPixmap(img)

        self.lbl = QLabel('All unsaved data will be lost.')
        self.lbl_1 = QLabel('Do you want to proceed?')

        self.btn = QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No

        self.btn_box = QDialogButtonBox(self.btn)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)

        self.lay_1 = QVBoxLayout()
        self.lay_1.addWidget(self.lbl)
        self.lay_1.addWidget(self.lbl_1)

        self.lay_2 = QHBoxLayout()
        self.lay_2.addWidget(self.lbl_0)
        self.lay_2.addLayout(self.lay_1)

        self.lay = QVBoxLayout()
        self.lay.addLayout(self.lay_2)
        self.lay.addWidget(self.btn_box)

        self.setLayout(self.lay)


def main():
    vary.app = QApplication(sys.argv + ['-platform', 'windows:darkmode=1'])
    styleSheet = open(f'assets/style/{vary.theme}.qss', 'r').read()
    vary.app.setStyleSheet(styleSheet)
    window = MainWindow()
    pywinstyles.apply_style(window, 'dark')
    window.show()
    vary.app.exec()
