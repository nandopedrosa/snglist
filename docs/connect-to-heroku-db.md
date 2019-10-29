Connect to Heroku DB via command line interface:

1. To see all PostgreSQL databases provisioned by your application and the identifying characteristics of each (such as database size, status, number of tables, and PG version), use the heroku pg:info

2. To establish a psql session with your remote database, use heroku pg:psql

batch script - cat /Users/fernando/Desktop/insertbancas.sql | heroku pg:psql

sqlite3 as inserts:
sqlite3 data.db
.output output.sql
.dump table_name
.quit

