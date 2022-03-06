""" hace la simulacion de una memoria RAM
    recibe como parametros:
        env -> ambiente de trabajo
        ram -> el espacio de la ram 100GB
        cpu -> procesador de recursos con capacidad indicada
        name -> nombre del proceso
        space_process -> espacio de memoria que requiere el proceso
        inst_process -> totalidad de instrucciones del proceso
        tiempo_intruccion -> es la cantidad de instrucciones que realiza el cpu
"""
def memory(env, ram, cpu, name, space_process, inst_process, tiempo_instruccion):
    tiempoInicio = env.now # tiempo en el que inicia el proceso
    # estado new -> entra en cola de la ram
    with ram.get(space_process) as espacio:
         yield espacio
         print('%s se le ha asignado espacio en memoria, pasara a estado ready. Utiliza %d de espacio' %(name, space_process))         
         # si ya se obtuvo espacio entonces pasa a estado de ready
    
    # estado ready -> se solicita el cpu si puede atender este proceso
    with cpu.request() as estado:
        yield estado
        print('%s sera atendido por el CPU, pasara a estado running.' % name)
        # puede cambiar a estado de running
        # solo ejecutara tiempo_instruccion
        # se debe de disminuir las instrucciones
        
        inst_process -= tiempo_instruccion
        siWaiting = random.randint(1,2)
        yield  env.timeout(siWaiting)
    
    # finalizando el proceso
    ram.put(space_process)
    tiempoTotal = env.now - tiempoInicio
    print("Ha tomado %d hacer %s proceso" %(tiempoTotal, name))
    
"""IMPORTACIONES"""    
import simpy
import random

"""VARIABLES"""  
env = simpy.Environment() # Ambiente
RAM = simpy.Container(env, init=100, capacity=100) # la capacidad de la RAM
CPU = simpy.Resource(env,capacity = 1) # La capacidad del CPU

for i in range(5): #aquí se coloca la cantidad de procesos
    newProceso = random.expovariate(1.0/10) # espacio en memoria entre 1 y 10 de cantidad a solicitar
    cantInstrucciones = random.expovariate(1.0/10) # instrucciones entre 1 y 10 de cantidad a solicitar
    env.process(memory(env,RAM, CPU, 'Proceso %d' %i, newProceso, cantInstrucciones, 3)) # se realiza el proceso
                                                                                # el 3 es porque realiza tres instrucciones
env.run() 