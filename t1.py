from flask import Flask, render_template, request, jsonify

#для телнета
import getpass
import telnetlib
import time




my_flask_app = Flask(__name__)

#ЗАПУСК САЙТА

@my_flask_app.route('/')
def input(): 
    return render_template('show_date.html')

#ПРОВЕРКА КОРРЕКТНОСТИ ВВЕДЕННЫХ ЛОГИНА, ПАРОЛЯ И IP
@my_flask_app.route('/correct')
def correct(): 
    ip_adress = request.args.get('ip_adress', 0, type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0, type=str)

 
    #itog=ip_adress, login,  password
    print(ip_adress)
    print(login)
    print(password)

    telnet = telnetlib.Telnet(ip_adress)
    telnet.read_until(b"Username:")
    telnet.write(login.encode('utf-8')+ b'\n')
    telnet.read_until(b"Password: ")
    telnet.write(password.encode('utf-8')+ b'\n')
    time.sleep(0.5)

    print('успешно залогинились')

    itog = telnet .read_very_eager().decode('utf-8')
    print(itog)
    
    print('itog.find', itog.find('#'))
    itog2 =' '
    if itog.find('#')>0:
        itog2 ='успешно'
    else:
        itog2 ='не успешно'

    print('itog2', itog2)

      
    return jsonify(result_correct=itog2)


#ВВОД КОМАНДЫ ДЛЯ МАРШРУТИЗАТОРА
@my_flask_app .route('/command')
def command():

    command = request.args.get('command', 0, type=str).encode('utf-8')
    print('команда 2 ', command )
    res=' '

    ip_adress = request.args.get('ip_adress', 0,  type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0,  type=str)


    print('ip_adress ', ip_adress)
    print('login  ' , login)
    print('password ', password)

    telnet = telnetlib.Telnet(ip_adress)

    #telnet.set_debuglevel(6) #дебаг

    telnet.read_until(b"Username:")
    telnet.write(login.encode('utf-8')+ b'\n')
    telnet.read_until(b"Password: ")
    telnet.write(password.encode('utf-8')+ b'\n')
    time.sleep(0.5)

    print('успешно залогинились')

    telnet.write(command + b'\n')
    time.sleep(0.5)
    time.sleep(0.5)
    print('ввели команду')
    res = telnet .read_very_eager().decode('utf-8')
    print('вывод команды', res)


    return jsonify(result_command = res)





#ВВОД command_run всех команд по кнопкам
@my_flask_app .route('/command_run')
def command_run():
    res_command_run=' '

    command_run= request.args.get('command_run', 0, type=str).encode('utf-8')
    ip_adress = request.args.get('ip_adress', 0,  type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0,  type=str)


    telnet = telnetlib.Telnet(ip_adress)

    telnet.read_until(b"Username:")
    telnet.write(login.encode('utf-8')+ b'\n')
    telnet.read_until(b"Password: ")
    telnet.write(password.encode('utf-8')+ b'\n')
    time.sleep(0.5)  
    telnet.write(command_run + b'\n')
    time.sleep(0.5)
    res_command_run= telnet .read_very_eager().decode('utf-8')
    return jsonify(result_command_run = res_command_run)




if __name__=="__main__":
    my_flask_app.run(port = 5011, debug = True) # debug=True - рестартует сайт при изменении файла .py