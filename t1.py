from flask import Flask, render_template, request, jsonify

#для телнета
import getpass
import telnetlib
import time




my_flask_app = Flask(__name__)

#ЗАПУСК САЙТА

@my_flask_app.route('/')
def input(): 
    return render_template('web_morda.html')



#ПРОВЕРКА КОРРЕКТНОСТИ ВВЕДЕННЫХ ЛОГИНА, ПАРОЛЯ И IP
@my_flask_app.route('/correct')
def correct(): 
    ip_adress = request.args.get('ip_adress', 0, type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0, type=str)
    telnet = telnetlib.Telnet(ip_adress)
    telnet.read_until(b"Username:")
    telnet.write(login.encode('utf-8')+ b'\n')
    telnet.read_until(b"Password: ")
    telnet.write(password.encode('utf-8')+ b'\n')
    time.sleep(0.5)
    itog = telnet .read_very_eager().decode('utf-8')
    itog2 =' '
    if itog.find('#')>0:
        itog2 ='успешно'
    else:
        itog2 ='не успешно'      
    return jsonify(result_correct=itog2)



#ВВОД command_run  по кнопкам
@my_flask_app .route('/command_run')
def command_run():
    
    command_run = request.args.get('command_run', 0, type=str).encode('utf-8')
    ip_adress = request.args.get('ip_adress', 0,  type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0,  type=str)

    ip_adress_ping_trace = request.args.get('ip_adress_ping_trace', 0, type=str).encode('utf-8')


    telnet = telnetlib.Telnet(ip_adress)
    telnet.read_until(b"Username:")
    telnet.write(login.encode('utf-8')+ b'\n')
    telnet.read_until(b"Password: ")
    telnet.write(password.encode('utf-8')+ b'\n')
    time.sleep(0.5)

#обработка ping и trace

    if request.args.get('command_run', 0, type=str) in ('ping', 'trace'):
        print('я тут')
        print(command_run  + b' ' + ip_adress_ping_trace + b'\n')

        telnet.write(command_run  + b' ' + ip_adress_ping_trace + b'\n')
        time.sleep(0.5)

#обработка остальных команд

    else:
        telnet.write(command_run + b'\n')
        time.sleep(0.5)

    res_command_run= telnet .read_very_eager().decode('utf-8')
    return jsonify(result_command_run = res_command_run)



 #конфигурационный режим

@my_flask_app .route('/configure_mode')
def configure_mode():


#получение исходных данных


    configure_command = request.args.get('configure_command', 0,  type=str)

    print('НАИМЕНОВАНИЕ КОМАНДЫ!!!!!!!!!', configure_command)

    ip_adress = request.args.get('ip_adress', 0,  type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0,  type=str)

#начальные данные для конфигурации интерфейса
    interface_name= request.args.get('interface_name', 0,  type=str).encode('utf-8')
    interface_ip_adress = request.args.get('interface_ip_adress', 0, type=str).encode('utf-8')
    interface_mask = request.args.get('interface_mask', 0, type=str).encode('utf-8')

#начальные данные для конфигурации саб интерфейса
    interface_vlan = request.args.get('interface_vlan', 0, type=str).encode('utf-8')

#начальные данные для конфигурации маршрутов
    network_ip_adress= request.args.get('network_ip_adress', 0,  type=str).encode('utf-8')
    network_mask = request.args.get('network_mask', 0, type=str).encode('utf-8')
    next_hop_ip = request.args.get('next_hop_ip', 0, type=str).encode('utf-8')


#начальные данные для конфигурации ospf

    ospf_process_id= request.args.get('ospf_process_id', 0,  type=str).encode('utf-8')
    ospf_ip_adress_interface = request.args.get('ospf_ip_adress_interface', 0, type=str).encode('utf-8')
    ospf_mask= request.args.get('ospf_mask', 0, type=str).encode('utf-8')
    ospf_area= request.args.get('ospf_area', 0, type=str).encode('utf-8')


#начальные данные для конфигурации BGP

    bgp_as_self = request.args.get('bgp_as_self', 0,  type=str).encode('utf-8')
    bgp_ip_adress_neighbor = request.args.get('bgp_ip_adress_neighbor', 0, type=str).encode('utf-8')  
    bgp_as_neighbor = request.args.get('bgp_as_neighbor', 0, type=str).encode('utf-8')


    
    
#вход на роутер и в  конфигурационный режим


    telnet = telnetlib.Telnet(ip_adress)
    telnet.read_until(b"Username:")
    telnet.write(login.encode('utf-8')+ b'\n')
    telnet.read_until(b"Password: ")
    telnet.write(password.encode('utf-8')+ b'\n')
    time.sleep(0.5)
    telnet.write(b'conf t\n')
    time.sleep(0.5)


#создаем интерфейс
    if configure_command=='configure_interface':
        print('создаем интерфейс')
        telnet.write(b'interface ' + interface_name  + b'\n')
        time.sleep(0.5)
        telnet.write(b'ip add '  + b' ' + interface_ip_adress + b' ' + interface_mask + b'\n')
        time.sleep(0.5)

#прописываем маршурты
    elif configure_command=='configure_route':
        print('пописываем маршрут')
        telnet.write(b'ip route ' + network_ip_adress + b' '+ network_mask + b' ' +  next_hop_ip  + b'\n')
        time.sleep(0.5)


# запускаем ospf
    elif configure_command=='configure_ospf':
        telnet.write(b'router ospf ' + ospf_process_id + b'\n')
        time.sleep(0.5)
        telnet.write(b'network ' + ospf_ip_adress_interface + b' ' + ospf_mask + b' area ' + ospf_area + b'\n')
        time.sleep(0.5)


# запускаем BGP
    elif configure_command=='configure_bgp':

        telnet.write(b'router bgp ' + bgp_as_self+ b'\n')
        time.sleep(0.5)
        telnet.write(b'neighbor  ' + bgp_ip_adress_neighbor + b' remote-as ' + bgp_as_neighbor + b'\n')
        time.sleep(0.5)

  

    

    res_configure_mode = telnet .read_very_eager().decode('utf-8')
    return jsonify(result_configure_mode = res_configure_mode)


    
  
    
    
    


if __name__=="__main__":
    my_flask_app.run(port = 5011, debug = True) # debug=True - рестартует сайт при изменении файла .py