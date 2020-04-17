from datetime import date,datetime
import sqlite3
def post_date_time(id,prd):
    conn=sqlite3.connect('datetime.db')     #detect_types=sqlite3.PARSE_DECLTYPES
    key=0            
    cursor=conn.execute('select '+str(prd)+' from date_time '+'WHERE ID='+str(id))
    for row in cursor:
        profile=row
    key=1
    if (key == 1):
        conn.execute('UPDATE date_time SET '+str(prd)+'=?'+' WHERE ID=?',(datetime.now(),str(id)))
    for row in cursor:
        profile=row
    conn.commit()
    conn.close()
    



