import traceback

from flask import Flask, render_template, request, jsonify
import scripts.webcrawler
import sqlite3 as sql
import random as rand
import json
from flask import jsonify


database_location = "./database/"
database_location = "/var/www/html/server/database/"
database_name = database_location + "mc_project13.db"
random_num = str(rand.randrange(0,1000))
print_debug_flag = True
random_input_flag = True


app = Flask(__name__)

@app.route('/')
def render():
    return render_template('myfile.html')

# @app.route('/suggestions')
# def getSuggestions():
# 	print request.method
# 	if request.method == 'GET':
# 		return "No input file specified"
# 	else:
# 		return render_template('myfile.html')

# @app.route('/suggestions/movies')
# def getMovies():
# 	return jsonify({'data':'Movie Data'})


def print_debug(output,start = "*",end = "*"):
    if print_debug_flag:
        print start * 100
        print output
        print end * 100

def check_dict_for_mandatory_keys(check_dict, keys):
    present = set(keys).issubset(check_dict)
    return present


def insert_users_new(user_name,password,user_email_id):
    sql_output = {}
    sql_output["success"] = True
    sql_output["message"] = ""
    sql_connection = sql.connect(database_name)
    try:
        sql_cursor = sql_connection.cursor()
        if random_input_flag:
            random_num = str(rand.randrange(0, 1000))
            user_name = user_name + "_" + str(random_num)
            user_email_id = user_email_id + "_" + str(random_num)
        insert_query = "INSERT INTO users(username,password,email) VALUES('%s','%s','%s')" % (user_name,password,user_email_id)
        sql_cursor.execute(insert_query)
        sql_connection.commit()
    except Exception as e:
        sql_connection.rollback()
        sql_output["success"] = False
        sql_output["message"] = str(traceback.format_exc())
    finally:
        sql_connection.close()
    return sql_output

def select_users_where(key,value):
    sql_output = {}
    sql_output["success"] = True
    sql_output["message"] = ""
    sql_output["result"] = []
    sql_connection = sql.connect(database_name)
    try:
        sql_cursor = sql_connection.cursor()
        select_query = "Select * From users Where %s = '%s' " % (key, value)
        sql_cursor.execute(select_query)
        sql_result = sql_cursor.fetchall()
        sql_output["result"] = sql_result
    except Exception as e:
        sql_output["success"] = False
        sql_output["message"] = str(traceback.format_exc())
    finally:
        sql_connection.close()
    return sql_output

def select_users_for_user_name(user_name):
    return select_users_where("username",user_name)

def select_users_for_user_email_id(user_email_id):
    return select_users_where("email",user_email_id)


@app.route("/users/login",methods=["GET"])
def users_login():
    output = {}
    output["success"] = False
    output["message"] = "Login API Called"
    output["exception"] = False
    try:
        request_args = request.args.to_dict()
        required_arg_keys = ["user_name","password"]
        if check_dict_for_mandatory_keys(request_args, required_arg_keys):
            request_user_name = request_args["user_name"]
            request_password = request_args["password"]
            sql_result = select_users_for_user_name(request_user_name)
            if sql_result["success"]:
                query_output = sql_result["result"]
                # print_debug(str(query_output))
                if len(query_output) == 0:
                    # output["message"] = "Sorry Username Not Found"
                    output["message"] = "Check Username or Password"
                else:
                    for cur_output in query_output:
                        cur_user_name = cur_output[3]
                        cur_password = cur_output[5]
                        if ( cur_user_name == request_user_name ) and ( cur_password == request_password):
                            output["success"] = True
                            output["message"] = "User Login Successful"
                            break
                    if not output["success"]:
                        output["message"] = "Check Username or Password"
            else:
                raise Exception(sql_result["message"])
        else:
            raise ValueError("Required Arguments missing , Mandatory Arguments are = " + str(required_arg_keys) )
    except ValueError as ve:
        output["message"] = ve.message
        output["exception"] = True
    except Exception as e:
        print_debug(str(traceback.format_exc()), "!", "#")
        output["message"] = str(traceback.format_exc())
        output["exception"] = True
    return jsonify(output)

@app.route("/users/register",methods=["GET"])
def users_register():
    output = {}
    output["success"] = False
    output["message"] = "Register API Called"
    output["exception"] = False
    try:
        request_args = request.args.to_dict()
        required_arg_keys = ["user_name","password","email_id"]
        if check_dict_for_mandatory_keys(request_args, required_arg_keys):
            request_user_name = request_args["user_name"]
            request_password = request_args["password"]
            request_email_id = request_args["email_id"]
            sql_result = select_users_for_user_name(request_user_name)
            if not sql_result["success"] : raise Exception(sql_result["message"])
            query_output_user_name = sql_result["result"]
            sql_result = select_users_for_user_email_id(request_email_id)
            if not sql_result["success"]: raise Exception(sql_result["message"])
            query_output_user_email_id = sql_result["result"]
            if len(query_output_user_name) == 0 and len(query_output_user_email_id) == 0:
                sql_result = insert_users_new(request_user_name,request_password,request_email_id)
                if sql_result["success"] == True:
                    output["success"] = True
                    output["message"] = "User Registration Successful"
                else:
                    raise Exception(sql_result["message"])
            else:
                cur_output = []
                cur_output.append("User Registration Failed")
                if len(query_output_user_name) > 0 :
                    cur_output.append("Sorry Username Taken")
                if len(query_output_user_email_id) > 0 :
                    cur_output.append("Sorry EmailId Taken")
                output["message"] = ",".join(cur_output)
        else:
            raise ValueError("Required Arguments missing , Mandatory Arguments are = " + str(required_arg_keys) )
    except ValueError as ve:
        output["message"] = ve.message
        output["exception"] = True
    except Exception as e:
        print_debug(str(traceback.format_exc()),"!","#")
        output["message"] = str(traceback.format_exc())
        output["exception"] = True
    return jsonify(output)

if __name__=='__main__':
    app.run(debug=True, port=3134)