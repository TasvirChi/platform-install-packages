SET SESSION binlog_format = 'STATEMENT';

CALL borhandw.all_tables_to_new();

SET SESSION binlog_format = 'ROW';
