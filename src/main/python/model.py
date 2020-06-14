# model.py
# D. Thiebaut
# This is the model part of the Model-View-Controller
# The class holds the name of a text file and its contents.
# Both the name and the contents can be modified in the GUI
# and updated through methods of this model.
#
from collections import OrderedDict
from pathlib import Path
from xlrd import open_workbook

class Model:
    def __init__( self ):
        '''
        Initializes the two members the class holds:
        the file name and its contents.
        '''
        self.filePath = None
        self.folder = None
        self.fileName = None
        self.resFilePath = None
        # default value
        self.colName = ['TIME', 'AV', 'AI']
        self.maxCol = [0, 1, 1000]

    def isValid( self, path ):
        '''
        returns True if the path exists and can be
        opened.  Returns False otherwise.
        '''
        p = Path(str(path))
        return p.exists()

    def getFilePath( self ):
        '''
        Returns the path of the file name member.
        '''
        return self.filePath

    def setFilePath( self, filePath ):
        '''
        sets the member filePath to the value of the argument
        if the file exists.  Otherwise resets the filePath.
        '''
        if self.isValid( filePath ):
            self.filePath = filePath
            self._setResFilePath(filePath)

    def getFolder( self ):
        '''
        Returns the name of the folder name member.
        '''
        return self.folder

    def setFolder( self, folder ):
        '''
        sets the member folder to the value of the argument
        if the folder exists.  Otherwise resets the folder.
        '''
        if self.isValid( folder ):
            self.folder = folder
            self._setResFilePath(folder)

    def getResFilePath( self ):
        return self.resFilePath

    def _setResFilePath( self, path ):
        p = Path(str(path))
        if self.folder and not p.is_dir():
            name = p.name.split('.')
            resFileName = '.'.join(name[0:-1]) + '.csv'
            self.resFilePath = str(Path(self.folder) / resFileName)
        elif self.filePath and p.is_dir():
            name = Path(self.filePath).name.split('.')
            resFileName = '.'.join(name[0:-1]) + '.csv'
            self.resFilePath = str(Path(path) / resFileName)

    def setColName( self, text ):
        if text:
            self.colName = [s.strip() for s in text.split(',')]

    def getColName( self ):
        return self.colName

    def setMaxCol( self, text ):
        if text:
            try:
                self.maxCol = [int(s) for s in text.split(',')]
            except:
                pass

    def getMaxCol( self ):
        return self.maxCol

    def extract( self ):
        workbook = open_workbook(self.filePath)

        # init final sheet and column number limit
        final_sheet = OrderedDict()
        max_num = {}
        col_cnt = {}
        for (i, name) in enumerate(self.colName):
            final_sheet[name] = []
            max_num[name] = self.maxCol[i]
            col_cnt[name] = 0

        for sheet_name in workbook.sheet_names():
            worksheet = workbook.sheet_by_name(sheet_name)
            nrows = worksheet.nrows
            # check if the sheet is empty
            if nrows > 1:
                header = worksheet.row_values(0)
                for name in self.colName:
                    try:
                        if col_cnt[name] < max_num[name]:
                            idx = header.index(name)
                            col = worksheet.col_values(idx)
                            # add sheet name to each column header
                            col[0] = f'{str(col[0])}({sheet_name})'
                            final_sheet[name].append(col)
                            col_cnt[name] = col_cnt[name] + 1
                    except:
                        # not target column
                        pass

        # transpose final_sheet
        res = []
        for k in final_sheet:
            res.extend(final_sheet[k])
        size_c = len(res)
        # size_r is the max length of column
        size_r = max([len(l) for l in res])
        s = []
        for rr in range(size_r):
            l = [str(res[i][rr]) if rr < len(res[i]) else ' ' for i in range(size_c)]
            s.append(','.join(l))

        with open(self.resFilePath, 'w') as f:
            f.write('\n'.join(s))
