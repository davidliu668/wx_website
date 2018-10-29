from django.core.management.base import BaseCommand
from ....ims.models import *
import logging
import xlrd


logger = logging.getLogger(__name__)


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = 'ims_import.xlsx'

        workbook = xlrd.open_workbook(path)
        ws = workbook.sheets()[0]

        row_num = ws.nrows
        col_num = ws.ncols

        print 'col_num: {}, row_num: {}'.format(col_num, row_num)

        title_line = ws.row_values(0)
        col_index = 0

        MColName.objects.all().delete()

        for col in title_line:
            colname = col.encode('utf8', 'ignore').strip()
            mColName = MColName(col_index=col_index, col_name=colname)
            mColName.save()
            col_index += 1

        print 'import {} col names'.format(col_index)

        row_index = 1
        import_num = 0
        skip_num = 0

        while row_index < row_num:
            data_line = ws.row_values(row_index)
            row_index += 1

            m_id = data_line[0].encode('utf8', 'ignore').strip()
            qs = MInfo.objects.filter(f01=m_id)
            if qs.count() > 0:
                skip_num += 1
                continue

            mInfo = self.gen_minfo(data_line)
            mInfo.save()

            import_num += 1

        print 'import {} data lines, skip {} data lines'.format(import_num, skip_num)

    def get_value(self, data_line, index):
        if index >= len(data_line):
            return ''

        val = data_line[index]

        if isinstance(val, unicode):
            return val.encode('utf8', 'ignore').strip()

        return str(val)

    def gen_minfo(self, data_line):
        mInfo = MInfo()
        index = 0

        mInfo.f01 = self.get_value(data_line, index)
        index += 1
        mInfo.f02 = self.get_value(data_line, index)
        index += 1
        mInfo.f03 = self.get_value(data_line, index)
        index += 1
        mInfo.f04 = self.get_value(data_line, index)
        index += 1
        mInfo.f05 = self.get_value(data_line, index)
        index += 1
        mInfo.f06 = self.get_value(data_line, index)
        index += 1
        mInfo.f07 = self.get_value(data_line, index)
        index += 1
        mInfo.f08 = self.get_value(data_line, index)
        index += 1
        mInfo.f09 = self.get_value(data_line, index)
        index += 1
        mInfo.f10 = self.get_value(data_line, index)
        index += 1

        mInfo.f11 = self.get_value(data_line, index)
        index += 1
        mInfo.f12 = self.get_value(data_line, index)
        index += 1
        mInfo.f13 = self.get_value(data_line, index)
        index += 1
        mInfo.f14 = self.get_value(data_line, index)
        index += 1
        mInfo.f15 = self.get_value(data_line, index)
        index += 1
        mInfo.f16 = self.get_value(data_line, index)
        index += 1
        mInfo.f17 = self.get_value(data_line, index)
        index += 1
        mInfo.f18 = self.get_value(data_line, index)
        index += 1
        mInfo.f19 = self.get_value(data_line, index)
        index += 1
        mInfo.f20 = self.get_value(data_line, index)
        index += 1

        mInfo.f21 = self.get_value(data_line, index)
        index += 1
        mInfo.f22 = self.get_value(data_line, index)
        index += 1
        mInfo.f23 = self.get_value(data_line, index)
        index += 1
        mInfo.f24 = self.get_value(data_line, index)
        index += 1
        mInfo.f25 = self.get_value(data_line, index)
        index += 1
        mInfo.f26 = self.get_value(data_line, index)
        index += 1
        mInfo.f27 = self.get_value(data_line, index)
        index += 1
        mInfo.f28 = self.get_value(data_line, index)
        index += 1
        mInfo.f29 = self.get_value(data_line, index)
        index += 1
        mInfo.f30 = self.get_value(data_line, index)
        index += 1

        mInfo.f31 = self.get_value(data_line, index)
        index += 1
        mInfo.f32 = self.get_value(data_line, index)
        index += 1
        mInfo.f33 = self.get_value(data_line, index)
        index += 1
        mInfo.f34 = self.get_value(data_line, index)
        index += 1
        mInfo.f35 = self.get_value(data_line, index)
        index += 1
        mInfo.f36 = self.get_value(data_line, index)
        index += 1
        mInfo.f37 = self.get_value(data_line, index)
        index += 1
        mInfo.f38 = self.get_value(data_line, index)
        index += 1
        mInfo.f39 = self.get_value(data_line, index)
        index += 1
        mInfo.f40 = self.get_value(data_line, index)
        index += 1

        mInfo.f41 = self.get_value(data_line, index)
        index += 1
        mInfo.f42 = self.get_value(data_line, index)
        index += 1
        mInfo.f43 = self.get_value(data_line, index)
        index += 1
        mInfo.f44 = self.get_value(data_line, index)
        index += 1
        mInfo.f45 = self.get_value(data_line, index)
        index += 1
        mInfo.f46 = self.get_value(data_line, index)
        index += 1
        mInfo.f47 = self.get_value(data_line, index)
        index += 1
        mInfo.f48 = self.get_value(data_line, index)
        index += 1
        mInfo.f49 = self.get_value(data_line, index)
        index += 1
        mInfo.f50 = self.get_value(data_line, index)
        index += 1

        mInfo.f61 = self.get_value(data_line, index)
        index += 1
        mInfo.f62 = self.get_value(data_line, index)
        index += 1
        mInfo.f63 = self.get_value(data_line, index)
        index += 1
        mInfo.f64 = self.get_value(data_line, index)
        index += 1
        mInfo.f65 = self.get_value(data_line, index)
        index += 1
        mInfo.f66 = self.get_value(data_line, index)
        index += 1
        mInfo.f67 = self.get_value(data_line, index)
        index += 1
        mInfo.f68 = self.get_value(data_line, index)
        index += 1
        mInfo.f69 = self.get_value(data_line, index)
        index += 1
        mInfo.f70 = self.get_value(data_line, index)
        index += 1

        return mInfo
