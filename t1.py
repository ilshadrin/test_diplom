from flask import Flask, render_template, request, jsonify
from netmiko import ConnectHandler

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
    ip_address = request.args.get('ip_address', 0, type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0, type=str)
    ###Устанавливаем сессию:
    net_connect = ConnectHandler(device_type='cisco_ios', ip=ip_address, username=login, password=password)
    ###Проверяем, что действительно законнектились:
    net_connect_answer = str(net_connect.find_prompt())
    if net_connect_answer.endswith("#") or net_connect_answer.endswith('>'):
        connect_result = 'Connection Succeed'
    else:
        connect_result = 'Connection Failed. Please check preferencies'
    return jsonify(result_correct=connect_result)
    ###Рвем сессию:
    net_connect.disconnect()
#ВВОД command_run  по кнопкам
@my_flask_app .route('/command_run')
def command_run():
    
    command_run = request.args.get('command_run', 0, type=str)
    ip_address = request.args.get('ip_address', 0,  type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0,  type=str)

    ip_address_ping_trace = request.args.get('ip_address_ping_trace', 0, type=str)
    ###Установка сессии:
    net_connect = ConnectHandler(device_type='cisco_ios', ip=ip_address, username=login, password=password)

#обработка ping и trace

    if request.args.get('command_run', 0, type=str) in ('ping', 'trace'):
        print('я тут')
        ###print(command_run  +  ' + ip_address_ping_trace + 
        command_to_push = command_run  +  ' + ip_address_ping_trace +  '
        print(command_to_push)
        res_command_run = net_connect.send_command(command_to_push) 
        ##telnet.write(command_run  +  ' + ip_address_ping_trace + 
        ##time.sleep(0.5)

#обработка остальных команд

    else:
        res_command_run = net_connect.send_command(command_run)

    return jsonify(result_command_run = res_command_run)
     ###Рвем сессию:
    net_connect.disconnect()


 #конфигурационный режим

@my_flask_app .route('/configure_mode')
def configure_mode():


#получение исходных данных


    configure_command = request.args.get('configure_command', 0,  type=str)

    print('НАИМЕНОВАНИЕ КОМАНДЫ!!!!!!!!!', configure_command)

    ip_address = request.args.get('ip_address', 0,  type=str)
    login = request.args.get('login', 0, type=str)
    password = request.args.get('password', 0,  type=str)

#начальные данные для конфигурации интерфейса
    interface_name= request.args.get('interface_name', 0,  type=str)
    interface_ip_address = request.args.get('interface_ip_address', 0, type=str)
    interface_mask = request.args.get('interface_mask', 0, type=str)

#начальные данные для конфигурации маршрутов
    network_ip_address= request.args.get('network_ip_address', 0,  type=str)
    network_mask = request.args.get('network_mask', 0, type=str)
    next_hop_ip = request.args.get('next_hop_ip', 0, type=str)


#начальные данные для конфигурации ospf

    ospf_process_id= request.args.get('ospf_process_id', 0,  type=str)
    ospf_ip_address_interface = request.args.get('ospf_ip_address_interface', 0, type=str)
    ospf_mask= request.args.get('ospf_mask', 0, type=str)
    ospf_area= request.args.get('ospf_area', 0, type=str)


#начальные данные для конфигурации BGP

    bgp_as_self = request.args.get('bgp_as_self', 0,  type=str)
    bgp_ip_address_neighbor = request.args.get('bgp_ip_address_neighbor', 0, type=str)  
    bgp_as_neighbor = request.args.get('bgp_as_neighbor', 0, type=str)


    
    
#вход на роутер и в  конфигурационный режим




#создаем интерфейс
   # if configure_command=='configure_interface':
        
#прописываем маршурты
    # elif configure_command=='configure_route':
        

# запускаем ospf
  #  elif configure_command=='configure_ospf':
        


# запускаем BGP
   # elif configure_command=='configure_bgp':

    
  

    

#    res_configure_mode = telnet .read_very_eager().decode('utf-8')
 #   return jsonify(result_configure_mode = res_configure_mode)


    
  
    
    
    


if __name__=="__main__":
    my_flask_app.run(port = 5011, debug = True) # debug=True - рестартует сайт при изменении файла .py