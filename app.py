from flask import Flask ,render_template,request,session
from finance_manager.database.db_setup import create_user_table,create_expenses_table,create_income_table
create_user_table()
create_expenses_table()
create_income_table()

from finance_manager.authentication.register import register_user,login_user ,logout
from finance_manager.reports import transaction
from finance_manager.reports.final_report import generate_final_report

app=Flask(__name__)

app.secret_key="123"
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/logout")
def logout_user():
    logout()
    return render_template("Home.html" ,msg="Logout Successfully")

@app.route("/Transaction", methods=['POST'])
def afterlogin():
    try:
        if request.method=="POST":
            username = request.form.get("username")
            password=request.form.get("password")
            run,error=login_user(username,password)
            if error:
                user=f"{run}"
                session['username']=username
                return render_template("finance_report.html",user=user)

            else:
                error=f"{run}"
                print(error)
                return render_template("login.html",error=error)
            

    except Exception as e:
        error=e
        return render_template("login.html",error=error)
    
@app.route("/Transaction1",methods=["POST"])
def aftersignup():
    try:
        if request.method=="POST":
            username = request.form.get("username")
            email=request.form.get("email")
            password=request.form.get("password")
            con_password=request.form.get("con_password")
            message, result=register_user(username,email,password,con_password)
            if result:
                session['username']=username
                return render_template("finance_report.html",error=message)

            else:
                error=f"{message}"
                return render_template("signup.html",error=error)
            

    except Exception as e:
        print(e)
        return render_template("signup.html")

@app.route("/finance_report" ,methods=["POST"])
def finance_report():
    try:
        if request.method=="POST":
            username=session.get('username')
            print(username)
            user_input=request.form.get("user_option")
            print(user_input)
            if user_input=="add":                                           #done
            
                return render_template("add_transaction.html")
            
            elif user_input=="delete":                                      #done
                
                return render_template("delete_transaction.html")
            
            elif user_input=="edit":                                       
                
                return render_template("edit_transaction.html")
            
            elif user_input=="show":                                        #done
                                                                            
                return render_template("finance_report.html")
            
            elif user_input=="get_report":                                  #done
                username=session.get('username')
                print("get report calling")
                report=generate_final_report(username)
                return render_template("get_report.html",report=report)
            else:
                return render_template("finance_report.html")
    except Exception as e:
        print(e)
        print("hello")
        return render_template("finance_report.html")

# @app.route("/get_report" ,methods=['POST','GET'])
# def get_report():
#     username=session.get('username')
#     print("get report calling")
#     report=generate_final_report(username)
#     print(report['username'])
#     # print(report)
#     return render_template("get_report.html",report=report)

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    print("add calling")
    # option=input("enter")
    if request.method=="POST":
        print(request.form)
        option=request.form.get("select_option")
        print(option)
        # option=input("enter")
        username=session.get('username')
        if option=="income":
            amount=request.form.get("income_amount")
            description=request.form.get("income_description")
            date=request.form.get("income_date")
            print("income calling")
            transaction.add_transaction('income',username,amount,description,date)
            msg="Income added successfully!"
            return render_template("finance_report.html",msg=msg)
        elif option=="expense":
            amount=request.form.get("expense_amount")
            description=request.form.get("expense_description")
            date=request.form.get("expense_date")
            print("expense calling")
            transaction.add_transaction('expense',username,amount,description,date)
            msg="expense added successfully!"
            return render_template("finance_report.html",msg=msg)
        else:
            print("nothing to show")
            msg="error"
        return render_template("finance_report.html",msg=msg)
        

@app.route("/edit_transaction", methods=["POST"])
def edit_transaction():
    print("edit calling")
    if request.method=="POST":
        print(request.form)
        edit_option=request.form.get("edit_select_option")
        print(edit_option)
        # option=input("enter")
        username=session.get('username')
        if edit_option=="income":
            id=request.form.get("edit_income_id")
            amount=request.form.get("edit_income_amount")
            description=request.form.get("edit_income_description")
            date=request.form.get("edit_income_date")
            print("income calling")
            print(amount,description,date)
            # edit_transaction('expense','sikander',1,100,'hello',11)
            msg=transaction.edit_transaction('income',username,id,amount,description,date)
            return render_template("finance_report.html",msg=msg)
        
        elif edit_option=="expense":
            id=request.form.get("edit_expense_id")
            amount=request.form.get("edit_expense_amount")
            description=request.form.get("edit_expense_description")
            date=request.form.get("edit_expense_date")
            print("expense calling")
            print(amount,description,date)
            msg=transaction.edit_transaction('expense',username,id,amount,description,date)
            return render_template("finance_report.html",msg=msg)
        else:
            print("nothing to show")
        return render_template("finance_report.html")
        

@app.route("/delete_transaction", methods=["POST"])
def delete_transaction():
    print("delete calling")
    if request.method=="POST":
        print(request.form)
        del_option=request.form.get("delete_select_option")
        print(del_option)
        # option=input("enter")
        username=session.get('username')
        if del_option=="income":
            id=request.form.get("delete_income_id")
            description=request.form.get("delete_income_description")
            print("income calling")
            print(id,description)
            msg=transaction.delete_transaction(username,id,'income')
            return render_template("finance_report.html",msg=msg)
        
        elif del_option=="expense":
            id=request.form.get("delete_expense_id")
            description=request.form.get("delete_expense_description")
            print("expense calling")
            print(id,description)
            msg=transaction.delete_transaction(username,id,'expense')
            return render_template("finance_report.html",msg=msg)
        else:
            print("nothing to show")
        return render_template("finance_report.html")
        
@app.route("/show_transaction" ,methods=["POST"])
def show_transaction():
    option=request.form.get("select_option")
    print(option)
    username=session.get('username')
    if option=="income":
        show=transaction.show_transaction('income',username)
        print(show)
        return render_template("finance_report.html",show=show)
                
    elif option=="expense":
        show=transaction.show_transaction('expense',username)
        print(show)
        return render_template("finance_report.html",show=show)
    else:
        return render_template("finance_report.html")



# app.run(host='localhost',port=5500,debug=True)