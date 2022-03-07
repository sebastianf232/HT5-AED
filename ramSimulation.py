"""IMPORTACIONES"""    
import simpy       # simulador
import random      # numeros random
import numpy as np # servirá para sacar la desviación estándar 

"""VARIABLES ARBITRARIAS"""
ramCapacity = 100  # cantidad de espacio
cpuCapacity = 1
processes = 25  # fijar cantidad de procesos, deben de ser 25,50,100,150 y 200
instCPU = 3     # puede cambiar a 3, 5 o 6
intervaloRandom = 1 # para hacer los intervalos de 10, 5 y 1
"""-----------------MÉTODOS------------------"""
""" hace la simulacion de una memoria RAM
    recibe como parametros:
        env -> ambiente de trabajo
        ram -> es la cola con una determinada capacidad
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
    print('%s creado en %.2f con espacio de %.2f' %(name, tiempoInicio, space_process))
    if space_process > ram.capacity:
        print ('%s espera recibir espacio en memoria RAM en el momento %.2f' %(name, env.now))
    else:
        with ram.get(space_process) as nextStep:            
            print('%s se le ha asignado espacio en memoria en %d, pasara a estado ready. Utiliza %.2f de espacio' %(name, env.now, space_process))         
            yield nextStep
            yield env.process(ready(env, ram, cpu, name, nextStep.amount, inst_process, tiempo_instruccion, tiempoInicio))
            # si ya se obtuvo espacio entonces pasa a estado de ready
                 
def ready(env, ram, cpu, name, space, inst_process, tiempo_instruccion, tiempoI):  
    # estado ready -> se solicita el cpu si puede atender este proceso    
    with cpu.request() as estado:
        yield estado
        print(' %s sera atendido por el CPU, pasara a estado running.' % name)
        yield env.process(running(env, ram, name, space, inst_process, tiempo_instruccion, tiempoI))        
        # puede cambiar a estado de running
        # solo ejecutara tiempo_instruccion
        # se debe de disminuir las instrucciones
        
def running(env, ram, name, space_process, inst_process, tiempo_instruccion, tiempoI):    
    terminated = False # se supone aun no ha terminado las instrucciones
    siWaiting = random.randint(1,2)
    while terminated==False:            
        inst_process -= tiempo_instruccion
        yield env.timeout(1) # aumenta en 1 por cada instruccion generada
        
        
        if inst_process > tiempo_instruccion:
            if siWaiting==1:
                print("  %s hace operacion I/O en %d" % (name, env.now))
                yield env.timeout(1)
        else:
            terminated = True # ha terminado de realizar los procesos pertinentes
    
    # finalizando el proceso
    ram.put(space_process)    
    tiempoTotal = env.now - tiempoI
    print("   %s FINALIZADO. Ha tomado %.2f ejecutarlo" %(name, tiempoTotal))
    totalTiempoProcesos.append(tiempoTotal)
    
    
# FUNCIONAMIENTO DEL PROGRAMA
"""VARIABLES"""  
env = simpy.Environment() # Ambiente
RAM = simpy.Container(env, init = ramCapacity, capacity = ramCapacity) # la capacidad de la RAM
CPU = simpy.Resource(env,capacity = cpuCapacity)           # La capacidad del CPU
random.seed(1) # fijar el inicio de random
totalTiempoProcesos = [] # se guardan los datos 

# realización de procesos
for i in range(processes): #aquí se coloca la cantidad de procesos
    newProceso = random.expovariate(1.0/intervaloRandom) # espacio en memoria entre 1 y 10 de cantidad a solicitar
    cantInstrucciones = random.expovariate(1.0/intervaloRandom) # instrucciones entre 1 y 10 de cantidad a solicitar
    env.process(memory(env,RAM, CPU, 'Proceso %d' %i, newProceso, cantInstrucciones, instCPU)) # se realiza el proceso                                                                                         # el 3 es porque realiza tres instrucciones, este número puede variar
env.run() 

"""ESTADÍSTICOS"""
suma=0
for i in totalTiempoProcesos:
    suma+=i
stDev = np.std(totalTiempoProcesos)

print("La media de %d procesos es %.2f con una desviación estándar de %.2f" %(processes, suma/processes, stDev))
