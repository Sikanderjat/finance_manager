import sqlite3
import os
import hashlib 
conn = sqlite3.connect('finance_manager.db')
c = conn.cursor()
#SESSION_FILE = 'session.json'
def register_user(username,email, password,con_password):
    password_hash1 = hashlib.sha256(password.encode()).hexdigest()
    password_hash2 = hashlib.sha256(con_password.encode()).hexdigest()
    if password_hash1==password_hash2:
        conn = sqlite3.connect('finance_manager.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username,email, password_hash,con_password_hash) VALUES (?, ?,?,?)", 
                    (username,email,password_hash1,password_hash2))
            conn.commit()
            user=username
            access="User registered successfully."
            run=f"{access},\nWelcome {user}"
            return run,True
        except sqlite3.IntegrityError:
            if c.execute("SELECT 1 FROM users WHERE email = ?", (email,)).fetchone():
                error = "Email already exists."
                return error, False
            
            else:
                error = "Username already exists."
            return error, False
    else:
        error="Passwords not match."
        return error,False
conn.close()


def login_user(username, password):
    conn = sqlite3.connect('finance_manager.db')
    c = conn.cursor()
    c.execute("SELECT password_hash,id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    if result and result[0] == hashlib.sha256(password.encode()).hexdigest():
        user=username
        id=result[1]
        access="Login successful."
        
        run=f"{access},\nWelcome {user},Your ID is {id}"
        
        #with open(SESSION_FILE, 'w') as f:
        #    f.write(username)
        return run,True
    else:
        error="Invalid username or password."
        return error, False
conn.close()
# login_user("sikander","123")






def logout():
    
    if os.path.exists(SESSION_FILE):
        
        os.remove(SESSION_FILE)
        print("You have been logged out.")
    else:
        print("No active session found.")

conn.close()
