import sqlite3
from fun import get_id
from module import sohwan

def update_db(user_name):
    con = sqlite3.connect('./test.db')
    cur = con.cursor()
    query = "select * from USER_LIST where name = '%s';" %user_name
    print(query)
    cur.execute(query)

    if not cur.fetchall()   :
        new = get_id(user_name)
        print("none")
        cur.execute("insert into USER_LIST(name,id,accountID) VALUES(?,?,?);",(new.name,new.id,new.accountID))
    
    
    con.commit()
    con.close()



if __name__ == '__main__':
    user_name = '꼬꼬팜'
    store_db(user_name)