from EX1_TC1 import EX1_TC1


class EX1_TC1_Library(object):
    """Test library for testing *Calculator* business logic.

    Interacts with the calculator directly using its ``push`` method.
    """

    def __init__(self):
        self._tc1 = EX1_TC1()
        self._pro = ''
        self._ele = ''

    def Launch_App(self, application):
        """Launch the specified ``application``.

        Will try to launch the specify application.

        Examples:
        | Launch App | Calc|
        | Launch App | C:\\Windows\\System32\\calc.exe |
        """
        self._tc1.Launch(application)

    def Title_should_be(self, expected):
        """Verifies that the opened Application is expected``.

        Example:
        | Launch App     | 'Calc' |
        | Title Should Be | 'Calculator'|
        """
        if self._tc1.Get_WindowTitle() != expected:
            raise AssertionError('%s != %s' % (self._tc1.Get_WindowTitle(), expected))

    def Open_CSV(self, filename):
        """Open the specified CSV file``.

        Example:
        | Open CSV     | Sample.csv|
        | Open CSV | D:\\Robot\\EX1_TC1\\Sample.csv|
        """
        if self._tc1.OpenCSV(filename) == 0:
            raise AssertionError('Cannot open ' + filename + ' CSV file!')

    def Load_Row(self, rows):
        """Load data from the specified Row of CSV file``.
           Row index start from 0

        Example:
        | Load Row     | 0|
        | Load Row | 1-2|
        | Load Row | All|
        """
        if rows.find('All') != -1:
            self._ele = self._tc1.TraversalCSV_Elements(0, 99999)

        elif rows.find('-') == -1:
            self._ele = self._tc1.TraversalCSV_Elements(int(rows))

        else:
            begin = int(rows[:int(rows.find('-'))])
            end = int(rows[(int(rows.find('-'))) + 1:])
            rowlen = (end - begin) + 1
            self._ele = self._tc1.TraversalCSV_Elements(begin,rowlen)

        if len(self._ele) == 0:
            raise AssertionError('No data in row or cannot read from Row ' + rows + ' of CSV file!')

        for e in self._ele:
            print(e)


    def Close_App(self):
        #print("Call self._tc1.Close_App()")
        self._tc1.Close_App()
