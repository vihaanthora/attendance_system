from flask import Flask, render_template, request, redirect, url_for, session, send_file
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'mysecretkey'

def modify_ref(name):
    mod_name = name.upper().split()
    return ((" ").join(mod_name[:3]))

def modify_g(name):
    mod_name = name.upper().split()
    try :
        mod_name.remove('IITI')
    except ValueError:
        pass
    return((" ").join(mod_name))

#getting name from attendance.txt
def split_string(s):
    a = ""
    for ch in s:
        if(0 <= ord(ch)-ord('0') <= 9):
            break
        a += ch
    return a

#mark attendance
def mark_attendance():
    attendance = open('attendance.txt', 'r')
    df = pd.read_csv('reference.csv')
    df["Name"] = df["Name"].apply(modify_ref)
    didProxy = []
    df['Attendance'] = 0
    for i in attendance:
        j = next(attendance)
        roll = j.split()[0]
        g_name = modify_g(split_string(i))
        row = df.loc[df['RollNo.'].astype(str) == roll]
        if row.empty:
            continue
        ref_name = row["Name"].to_string(index=False)
        if g_name == ref_name:
            df.loc[df['RollNo.'].astype(str) == roll, "Attendance"] = 1
        else:
            row = df.loc[df["Name"] == g_name]
            if row.empty:
                didProxy.append(["NOT IN BATCH", g_name, ref_name])
                continue
            df.loc[df["Name"] == g_name, "Attendance"] = 0
            roll = df.loc[df["Name"] == g_name, "RollNo."].to_string(index=False)
            didProxy.append([roll, g_name,ref_name])
    
    absent = df.loc[df['Attendance'] == 0, ["RollNo.","Name"]].set_index('RollNo.').to_dict()["Name"]
    df.to_csv('final-attendance.csv', index=False)
    return absent, didProxy

@app.route('/', methods=['GET'])
def main():
    session.pop('loggedin', None)
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def home():
    session['loggedin'] = True
    if request.method == 'POST':
        attendance_file= request.files['attfile']
        attendance_file.filename = 'attendance.txt'
        attendance_file.save(attendance_file.filename)
        ref_file = request.files['reffile']
        ref_file.filename = 'reference.csv'
        ref_file.save(ref_file.filename)
        absent, didProxy = mark_attendance()
    return render_template('details.html', absent_dict = absent, proxy_list = didProxy)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	return redirect(url_for('main'))

@app.route('/get_csv')
def get_csv():
    if 'loggedin' in session:
        csv_file = 'final-attendance.csv'
        csv_path = os.path.join(csv_file)
        print(csv_path)
        return send_file(csv_path, as_attachment=True, attachment_filename=csv_file)
    return redirect(url_for('logout'))
    
if __name__ == '__main__':
    app.run(debug=True)