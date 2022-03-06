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
    global totalTiempoProcesos # servirá para hacer el promedio 
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
    totalTiempoProcesos.append(tiempoTotal)
    print("Ha tomado %d hacer %s proceso" %(tiempoTotal, name))
    
"""IMPORTACIONES"""    
import simpy
import random
import numpy as np # servirá para sacar la desviación estándar 

"""VARIABLES"""  
env = simpy.Environment() # Ambiente
RAM = simpy.Container(env, init=100, capacity=100) # la capacidad de la RAM
CPU = simpy.Resource(env,capacity = 1) # La capacidad del CPU
random.seed(1) # fijar el inicio de random
processes = 25  # fijar cantidad de procesos, deben de ser 5,50,100,150 y 200
totalTiempoProcesos = [] # se guardan los datos 
for i in range(processes): #aquí se coloca la cantidad de procesos
    newProceso = random.expovariate(1.0/10) # espacio en memoria entre 1 y 10 de cantidad a solicitar
    cantInstrucciones = random.expovariate(1.0/10) # instrucciones entre 1 y 10 de cantidad a solicitar
    env.process(memory(env,RAM, CPU, 'Proceso %d' %i, newProceso, cantInstrucciones, 3)) # se realiza el proceso
                                                                                         # el 3 es porque realiza tres instrucciones, este número puede variar
env.run() 

"""ESTADÍSTICOS"""
suma=0
for i in totalTiempoProcesos:
    suma+=i
stDev = np.std(totalTiempoProcesos)

print("La media de %d procesos es %d con una desviación estándar de %d" %(processes, suma/processes, stDev))