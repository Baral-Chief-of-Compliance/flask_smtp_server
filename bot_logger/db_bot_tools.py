import sqlite3


def create_db():
    connection = sqlite3.connect("admin_users.db")

    cursor = connection.cursor()

    cursor.execute("""
create table AdminUser (
AdminUser_id integer primary key AUTOINCREMENT,
AdminUser_chat_id text, 
AdminUser_logger_status text 
)
""")
    
    connection.commit()

    connection.close()


def add_admin(chat_id: str) -> None:
    connection = sqlite3.connect("admin_users.db")

    cursor = connection.cursor()

    cursor.execute(f"""
insert into AdminUser(AdminUser_chat_id, AdminUser_logger_status) 
values (?, ?)
""", (chat_id, "on"))
    
    connection.commit()

    connection.close()
    

def turn_off_logger(chat_id: str) -> None:
    connection = sqlite3.connect("admin_users.db")

    cursor = connection.cursor()

    cursor.execute("update AdminUser set AdminUser_logger_status = ? where AdminUser_chat_id = ?", 
                   ("off", str(chat_id)))
    
    connection.commit()

    connection.close()


def turn_on_logger(chat_id: str) -> None:
    connection = sqlite3.connect("admin_users.db")

    cursor = connection.cursor()

    cursor.execute("update AdminUser set AdminUser_logger_status = ? where AdminUser_chat_id = ?", 
                   ("on", str(chat_id)))
    
    connection.commit()

    connection.close()
    

def get_status_logger(chat_id: str) -> str:

    connection = sqlite3.connect("admin_users.db")

    cursor = connection.cursor()

    cursor.execute("""
select AdminUser.AdminUser_logger_status from AdminUser where AdminUser.AdminUser_chat_id = ?
""", (chat_id, ))
    
    status = cursor.fetchone()

    connection.close()

    return status[0]
