# -*- coding: utf-8 -*-
import os
from sqlalchemy import Table
from models.mysql.system import db_engine, meta

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    full_name = os.path.join(root_path, 'models/mysql.py')

    with open(full_name, 'w') as f:
        f.write('# -*- coding: utf-8 -*-\r\n\r\n')
        f.write('from sqlalchemy import Table, select\r\n')
        f.write('from utils.my_sql import Mysql\r\n\r\n')
        f.write('mysql_obj = Mysql()\r\n')
        f.write('meta = mysql_obj.meta\r\n')
        f.write('db_engine = mysql_obj.db_engine\r\n\r\n')

        table_list = db_engine.table_names()
        print(table_list)
        for table_name in table_list:
            tmp_table = Table(table_name, meta, autoload=True, autoload_with=db_engine)
            # 表注释
            f.write('# ' + tmp_table.comment.replace(r'\r\n', '') + '\r\n')
            # 定义表
            f.write('{table_name} = Table("{table_name}", meta, autoload=True, autoload_with=db_engine)\r\n\r\n'.format(table_name=table_name))


if __name__ == '__main__':
    main()
