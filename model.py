# model.py
# D. Thiebaut
# This is the model part of the Model-View-Controller
# The class holds the name of a text file and its contents.
# Both the name and the contents can be modified in the GUI
# and updated through methods of this model.
#
from collections import OrderedDict
import xlrd

class Model:
    def __init__( self ):
        '''
        Initializes the two members the class holds:
        the file name and its contents.
        '''
        self.fileName = None
        self.resFileName = None
        # default value
        self.colName = ['TIME', 'AV', 'AI']
        self.maxCol = [0, 1, 1000]

    def isValid( self, fileName ):
        '''
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        '''
        try:
            file = open( fileName, 'r' )
            file.close()
            return True
        except:
            return False

    def setFileName( self, fileName ):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        if self.isValid( fileName ):
            self.fileName = fileName
            res = fileName.split('.')
            self.resFileName = '.'.join(res[0:-1]) + '.csv'

    def getFileName( self ):
        '''
        Returns the name of the file name member.
        '''
        return self.fileName

    def getResFileName( self ):
        return self.resFileName

    def setColName( self, text ):
        if text is not None:
            self.colName = [s.strip() for s in text.split(',')]

    def getColName( self ):
        return self.colName

    def setMaxCol( self, text ):
        if text is not None:
            try:
                self.maxCol = [int(s) for s in text.split(',')]
            except:
                pass

    def getMaxCol( self ):
        return self.maxCol

    def writeDoc( self ):
        '''
        Writes the string that is passed as argument to a
        a text file with name equal to the name of the file
        that was read, plus the suffix ".bak"
        '''

        workbook = xlrd.open_workbook(self.fileName)

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
                            final_sheet[name].append(worksheet.col_values(idx))
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

        with open(self.resFileName, 'w') as f:
            f.write('\n'.join(s))
