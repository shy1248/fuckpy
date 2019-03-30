#!/usr/bin/env python
# -*- coding=UTF-8 -*-
'''
@Author: shy
@Email: yushuibo@ebupt.com / hengchen2005@gmail.com
@Version: v1.0
@Licence: GPLv3
@Description: A simple toolkit for write anfd read excel file
@Since: 2019-03-29 19:35:10
@LastTime: 2019-03-30 14:06:02
'''

import os
import sys
from zipfile import BadZipfile

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.styles import Font
from openpyxl.styles import Border
from openpyxl.styles import Side
from openpyxl.styles import PatternFill
from openpyxl.styles import colors
from openpyxl.styles import Alignment
from openpyxl.styles import NamedStyle
from openpyxl.utils.cell import get_column_letter
from openpyxl.worksheet.dimensions import ColumnDimension

from simplelogger import logger


class ExcelUtil(object):

    def __init__(self):
        __style = NamedStyle(name='simple')
        __style.font = Font(bold=True, size=11, color=colors.WHITE)
        __style.fill = PatternFill(patternType='solid', fgColor=colors.BLUE)
        bd = Side(style='thin', color=colors.BLACK)
        self.__border = Border(left=bd, top=bd, right=bd, bottom=bd)
        __style.border = self.__border
        self.__alignment = Alignment(horizontal='center', vertical='center')
        __style.alignment = self.__alignment
        self.__header_style = __style

    def write(self, file, data, sheet=None, is_overwrite=False):
        '''Write data to excel file.
        
        Arguments:
            file {str} -- The absolute name of excel file
            data {dict} -- The data dict which will write to excel file. The dict must
                has 2 keys: title, data. The title's value is a tuple which cantains a
                work sheet headers. If let it a non list, which means there is no heaers
                will attache. The key of the data's value is a list of tulpes, one tuple
                is one row.
        
        Keyword Arguments:
            sheet {str} -- The name of destnation sheet.
            is_overwrite {bool} -- when the destnation file exist, it will be overwrite
                when this flag is true (default: {False})
        '''

        if not is_overwrite and os.path.isfile(file):
            logger.error(
                'The destination file {} is already exist, abort!'.format(file))
            sys.exit(1)

        if len(data) != 2 or 'title' not in data or 'data' not in data:
            logger.error('Can\'t parse the source data dictionary, abort.')
            sys.exit(1)

        title = data['title']
        rows = data['data']
        if not (title and isinstance(title, tuple)):
            logger.error('The title must be a non tuple object, abort.')
            sys.exit(1)
        if not isinstance(rows, list):
            logger.error('The data of rows must be a list object, abort.')
            sys.exit(1)

        wb = Workbook()
        if sheet:
            ws = wb.create_sheet(sheet, index=0)
        else:
            ws = wb.active

        ws.print_options.horizontalCentered = True
        ws.print_options.verticalCentered = True

        max_width = {}
        for i in range(len(title)):
            ws.cell(
                row=1, column=1 + i, value=title[i]).style = self.__header_style
        for row_id, row in enumerate(rows, start=2):
            for column_id, column in enumerate(row, start=1):
                if isinstance(column, unicode):
                    curr_with = len(column.encode('utf-8')) + 1
                else:
                    curr_with = len(str(column)) + 1
                last_width = max_width.get(column_id)
                if not last_width or curr_with > last_width:
                    max_width[column_id] = curr_with
                cell = ws.cell(row=row_id, column=column_id, value=column)
                cell.border = self.__border
                cell.alignment = self.__alignment
                ws.column_dimensions[get_column_letter(
                    column_id)].width = max_width.get(column_id)
        wb.save(file)

    def read(self, file, sheet, rows=[], columns=[]):
        '''Read data from excel file.
        
        Arguments:
            file {str} -- The absolute path of the destination file
            sheet {str ot int} -- The name or index of the destination sheet
        
        Keyword Arguments:
            rows {list} -- Row filters, a list which cantains destination row numbers (default: {[]})
            columns {list} -- Column filters, a list which cantains destination column numbers (default: {[]})
        
        Returns:
            list -- A list of rows, and a tuple for each row
        '''

        if not os.path.isfile(file):
            logger.error(
                'The destination file {} does\'t not exist, abort.'.format(
                    file))
            sys.exit(1)
        if rows and not isinstance(rows, list):
            logger.error('Type error, parameter rows must be a list.')
            sys.exit(1)
        if columns and not isinstance(columns, list):
            logger.error('Type error, parameter columns must be a list.')
            sys.exit(1)
        if filter(lambda x: not isinstance(x, int) or x <= 0, rows):
            logger.error('The row filters must be non zero positive integers.')
            sys.exit(1)
        if filter(lambda x: not isinstance(x, int) or x <= 0, columns):
            logger.error('The column filters must be non zero positive integers.')
            sys.exit(1)
        try:
            wb = load_workbook(file)
            if isinstance(sheet, str) or isinstance(sheet, unicode):
                ws = wb.get_sheet_by_name(sheet)
            elif isinstance(sheet, int):
                ws = wb.get_sheet_by_name(wb.get_sheet_names()[sheet - 1])
            else:
                logger.error(
                    'Invalid value for parameter sheet, must be string for sheet name or int for sheet index.'
                )
                sys.exit(1)

            if rows and not columns:
                data = [
                    tuple([
                        ws.cell(row=x, column=y).value
                        for y in range(1, ws.max_column + 1)
                    ])
                    for x in rows
                ]
            elif not rows and columns:
                data = [
                    tuple([ws.cell(row=x, column=y).value
                           for y in columns])
                    for x in range(1, ws.max_row + 1)
                ]
            elif rows and columns:
                data = [
                    tuple([ws.cell(row=x, column=y).value
                           for y in columns])
                    for x in rows
                ]
            else:
                data = [
                    tuple([
                        ws.cell(row=x, column=y).value
                        for y in range(1, ws.max_column + 1)
                    ])
                    for x in range(1, ws.max_row + 1)
                ]
            return data
        except BadZipfile:
            logger.error(
                'Load excel file {} failed, invalid file format.'.format(file))
            sys.exit(1)
        except KeyError:
            logger.error('Worksheet {} does\'t exist.'.format(sheet))
            sys.exit(1)


if __name__ == "__main__":
    excel = ExcelUtil()
    # Usage for write function
    logger.info('Startting write...')
    title = (('ID', u'中文', 'DESCRIPTION'))
    data = [(0, u'苹果', u'手机和电脑'), (1, u'微软', 'Opertion System'),
            (2, 'Lenove', '')]
    data = {'title': title, 'data': data}
    excel.write(
        file='/Users/shy/Desktop/test.xlsx',
        data=data,
        sheet=u'测试',
        is_overwrite=True)
    logger.info('Wrtie success!')

    # Usage for read function
    logger.info('Startting read...')
    data = excel.read(
        '/Users/shy/Desktop/test30.xlsx',
        sheet=3,
        rows=[i for i in range(10, 20)],
        columns=[2, 5, 254])
    for row in data:
        print
        for cell in row:
            print(cell),
    print
    logger.info('Read finish!')
