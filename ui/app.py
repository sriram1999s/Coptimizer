from flask import Flask, request, jsonify
from flask.templating import render_template
import json
import subprocess
import os
import sys

cwd = os.getcwd()
tester_dir_ = os.path.abspath(os.path.join(cwd, os.pardir)) + '/tester'
sys.path.append(tester_dir_)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize_code', methods = ['POST', 'GET'])
def optimize_code():
    import criterion_controller_gui
    code = request.form['code']
    menu_opt_json_str = request.form['menu_opt_json_str']

    # write GUI input code to testfile
    with open('testfile.c', 'w') as f:
        f.write(code)

    # write GUI selected flags to json file
    with open('flags.json', 'w') as f:
        f.write(menu_opt_json_str)

    menu_opt_json_str = json.loads(menu_opt_json_str)
    flag_command = 'Coptimizer sf'

    # set GUI flags : UNROLL,COMPILE_INIT,INLINE,IF_TO_SWITCH,TAIL_RECURSION,JAMMING
    for flag in menu_opt_json_str:
        if menu_opt_json_str[flag]:
            flag_command += ' ' + flag[5:]

    subprocess.run(flag_command, shell = True)

    run_command = 'Coptimizer ox testfile.c'
    subprocess.run(run_command, shell = True)

    ret_arr = {}
    with open('output.c', 'r') as f:
        ret_arr['op'] = f.read()
    with open('../env/check_input', 'r') as f:
        ret_arr['inp_json'] = f.read()

    # get suggested run count and completion time
    ret_dict = criterion_controller_gui.compile()

    # merge two dictionaries : code + suggested_runc + ...
    ret_arr = {**ret_arr, **ret_dict}
    return jsonify(ret_arr)

@app.route('/metrics', methods = ['POST', 'GET'])
def metrics():
    import criterion_controller_gui
    inp_code = request.form['inp_code']
    runc_ = request.form['runc_']

    with open('inp.txt', 'w') as f:
        f.write(inp_code)

    # execute the scripts to get avg. metrics
    runc_temp = runc_
    runc_ = 100
    if runc_temp != '':
        # if num_runs given or else default num_runs = 100 for validate
        runc_ = int(runc_temp)
    met_dict = criterion_controller_gui.validate(runc_)

    ret_arr = {}
    with open('unop_output.txt', 'r') as f:
        ret_arr['unop_output'] = f.read()
    with open('op_output.txt', 'r') as f:
        ret_arr['op_output'] = f.read()
    
    # merge two dictionaries : outputs + avg. metrics
    ret_arr['met_op'] = met_dict
    return jsonify(ret_arr)

if __name__ == '__main__':
    app.run(debug = True)

'''
@app.route('/metrics', methods = ['POST', 'GET'])
def metrics():
    import criterion_controller_gui
    inp_code = request.form['inp_code']
    with open('inp.txt', 'w') as f:
        f.write(inp_code)

    run_command = 'python3 ../tester/tester_controller.py testfile.c output.c > met_op.txt'
    subprocess.run(run_command, shell = True)

    ret_arr = {}
    with open('unop_output.txt', 'r') as f:
        ret_arr['unop_output'] = f.read()
    with open('op_output.txt', 'r') as f:
        ret_arr['op_output'] = f.read()
    with open('met_op.txt', 'r') as f:
        ret_arr['met_op'] = f.read()
    
    return jsonify(ret_arr)
'''