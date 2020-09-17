#Modo de uso
#--------------------------------------------------------------------------------------------------------------
'''la presente rutina se encuentra basada en la NSR-10 y el documento (Diseño de elementos de acero sometidos 
a flexion) por Agusztine & Garza y funciona para comprobacion y diseño a flexion de secciones
 en I.

Linea__Descripcion 
 
57   __#Opcion:Permite escoger entre si usar el metodo conservador o no, seleccionar prubar muchos perfiles de la base
       de datos, un perfil de la base de datos o un perfil propio

66   __#Propiedades del acero: E y Fy

73   __#Datos de la viga: Datos como lb, Mmax, y calculo de Cb o Cb propio

90   __#Datos de la seccion: Datos geometricos de la seccion en caso de ser nueva
 
Nota: Ir a numero de linea indicada para hacer uso de cada descripcion


La implementacion del codigo es de autoría propia y puede ser modificado por cualquier persona.Por defecto se prueba
el perfil 172 _ W410X60 aprox. IR406X59.6  correspondiente al ejemplo de Gerdau.

Eliú Pineda Argel
+573167164222
epargel@gmail.com
'''
#--------------------------------------------------------------------------------------------------------------

#Librerias usadas
#---------------------------------------------------------------------------------------------------------------
import math 
import numpy as np
import pandas as pd
import os
#---------------------------------------------------------------------------------------------------------------

#Borrando archivo de salida anterior solo siexiste
#---------------------------------------------------------------------------------------------------------------
if os.path.isfile("out.csv")==True:#Comprueva si el archivo existe, si existe lo elimina
    os.remove("out.csv")
#---------------------------------------------------------------------------------------------------------------

#Converisones
#---------------------------------------------------------------------------------------------------------------
cm2mm=10
cm32mm3=1000
cm42mm4=10000
cm62mm6=1000000

fi=0.9  #Factor de reduccion
perfilc=1#contador
c=1#Para perfiles de doble simetria c=1
#---------------------------------------------------------------------------------------------------------------


#Opcion
#---------------------------------------------------------------------------------------------------------------
MetodoConservador=0 #Cero para NO y uno para Si
prueba=0           #Cero para probar toda la base de datos V.15, 1 para un perfil de la base de datos ó 2 para probar un perfil con datos propios
indicedelperfil=172 #Si desea probar solo un perfil escriba el indice de la fila del perfil revisando el Array L en el explorador de varibles luego de ejecutar el codigo al menos una vez. para usar esta opccion prueba=1
#---------------------------------------------------------------------------------------------------------------



#Propiedades del Acero
#---------------------------------------------------------------------------------------------------------------
conv=1000 
E=200000/conv                 #modulo de young (MPa)
Fy=345/conv                   #Esfuerzo de fluencia (MPa)
#---------------------------------------------------------------------------------------------------------------


#Datos de la viga
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Lb=500*cm2mm             #longitud no arriostrada del perfil mm 500*cm2mm(para ejemplo1)
Mmax=294000                 #Momento maximo requerido N-m 294000(para ejemplo 1)

#Factor de modificacion para pandeo lateral-torcional
Ma=1
Mb=1
Mc=1

Cb=12.5*Mmax/(2.5*Mmax+3*Ma+4*Mb+3*Mc)
if Cb>3:
    Cb=3
Cb=1.95  #Si se desea introducir Cb, en caso negativo comentar esta linea y llenar los datos de momentos 1.95(para ejemplo 1)                 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


#Datos de la seccion--- Se usan solo si prueba=1, si se desea probar solo este tipo de perfil
#---------------------------------------------------------------------------------------------------------------
bpin=(17.8)*cm2mm        #longitud de la aleta
tin=(1.29)*cm2mm         #Espesor aleta
din=(40.70)*cm2mm        #Peralte o altura de a seccion
twin=(0.78)*cm2mm        #Espesor del alma


ryin=4*cm2mm                 #mm
Iyin=1.203*cm42mm4           #mm4
Cwin=464.567*cm62mm6         #mm6
Sxin=1.061*cm32mm3           #mm3
Jin=33*cm42mm4               #mm4
Zxin=1.197*cm32mm3           #mm3

#---------------------------------------------------------------------------------------------------------------


#Database con informacion de perfiles V15
#---------------------------------------------------------------------------------------------------------------
database = pd.read_csv("Database.csv", header=(0), sep=(";"))#seleccion del archivo csv con la base de datos
L = np.asarray(database) #Converssion del dataframe a un arreglo 
#---------------------------------------------------------------------------------------------------------------


Mrmin=200000000000000000000000000000000000000000000000000000000
#loop para probar los primeros 350 perfiles (Perfiles en I)
while perfilc<=351:
    
    if prueba==2:
        perfilc=351 #Garantiza una sola corrida del ciclo
        #Datos para probar un perfil
        #---------------------------------------------------------------------------------------------------------------
        #Perfil a usar prueba  IR406x59.6 _ Datos deben estar en mm
        
        bp=bpin        #longitud de la aleta
        t=tin          #Espesor aleta
        d=din          #Peralte o altura de a seccion
        tw=twin        #Espesor del alma
        
        
        ry=ryin                #mm
        Iy=Iyin                #mm4
        Cw=Cwin                #mm6
        Sx=Sxin                #mm3
        J=Jin                  #mm4
        Zx=Zxin                #mm3
        #---------------------------------------------------------------------------------------------------------------
        
    if prueba==0:
        perfil=perfilc  
        #Datos para diseñar_ prueba todos los perfiles de la base de datos
        #---------------------------------------------------------------------------------------------------------------
        #Perfiles base de datos
        print("Perfil=",L[perfil,1])
        
        bp=(L[perfil,93])       #longitud de la aleta
        t=(L[perfil,101])       #Espesor aleta
        d=(L[perfil,88])        #Peralte o altura de la seccion
        tw=(L[perfil,98])       #Espesor del alma
        
        
        ry=(L[perfil,127])                #mm
        Iy=((L[perfil,124])*1000000)                #mm4
        Cw=(L[perfil,132]*1000000000)                #mm6
        Sx=(L[perfil,122]*1000)                #mm3
        J=((L[perfil,131])*1000)                 #mm4
        Zx=((L[perfil,121])*1000)               #mm3
        #---------------------------------------------------------------------------------------------------------------
        
    if prueba==1:
        perfil=indicedelperfil#Seleccion de 1 perfil
        perfilc=351
        #Datos para diseñar_ prueba un perfil de la base de datos
        #---------------------------------------------------------------------------------------------------------------
        #Perfiles base de datos
        print("Perfil=",L[perfil,1])
        
        bp=(L[perfil,93])       #longitud de la aleta
        t=(L[perfil,101])       #Espesor aleta
        d=(L[perfil,88])        #Peralte o altura de la seccion
        tw=(L[perfil,98])       #Espesor del alma
        
        
        ry=(L[perfil,127])                #mm
        Iy=((L[perfil,124])*1000000)                #mm4
        Cw=(L[perfil,132]*1000000000)                #mm6
        Sx=(L[perfil,122]*1000)                #mm3
        J=((L[perfil,131])*1000)                 #mm4
        Zx=((L[perfil,121])*1000)               #mm3
        #---------------------------------------------------------------------------------------------------------------
        
    
    
    #Calculados a partir de datos de la seccion
    #---------------------------------------------------------------------------------------------------------------
    b=bp/2                 #Longitud de la aleta sobre 2 = bp/2
    h=d-(2*t)              #Peralte del alma
    h0=d-(t)               #Distancia entre centroides de aletas mm
    Iyc=t*(bp**3)/12       #Momento de inercia de la aleta a compresio alrededor del eje y
    #---------------------------------------------------------------------------------------------------------------
    
    
    
    #Clasificacion
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    print("->")
    lamdaP=b/t #Patin
    lamdaA=h/tw#Alma
    
            #Aletas de Perfiles laminados en I
    lamdaPp=0.38*math.sqrt(E/Fy)
    lamdaPr=math.sqrt(E/Fy)
    if lamdaP<lamdaPp:
        print("Patin: Compacto")
    else:
        if lamdaP<lamdaPr:
            print("Patin: No-Compacto")
        else:
            print("Patin: Esbelto")
            
            #Almas de perfiles en I de simetria doble
    lamdaAp=3.76*math.sqrt(E/Fy)
    lamdaAr=5.7*math.sqrt(E/Fy)
    if lamdaA<lamdaAp:
        print("Alma:  Compacta")
    else:
        if lamdaA<lamdaAr:
            print("Alma:  No-Compacta")
        else:
            print("Alma:  Esbelta")
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
            
            
                      
    
    #F.2.6.2 _Seccion compacta en I con simetria doble
    if (lamdaA<lamdaAp) and (lamdaP<lamdaPp):
        entro=1
        print("-")
        print("La seccion es compacta")
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++        
        #Calculo de resistencia por fluencia
        Mp=Fy*Zx
        
        #Calculo de resistencia al pandeo lateral torsional
        #***************************************************************************************************************
                        #Variables Lr
        rts=math.sqrt((math.sqrt(Iy*Cw))/Sx);print(rts)
        #rts=math.sqrt((Iy*h0)/(2*Sx))#Para secciones en I de doble simetria con aletas rectangulares
        #rts puede aproximarse a: rts=bf/math.sqtr(12*(1+((h*tw)/(6*bf*tf))))
        #_______________________________________________________________________________________________________________
        Lp=(1.76*ry)*(math.sqrt(E/Fy));print(Lp)
        Lr=1.95*rts*(E/(0.7*Fy))*math.sqrt(((J*c)/(Sx*h0))+math.sqrt((((J*c)/(Sx*h0))**2)+(6.76*((0.7*Fy/E)**2))));print(Lr)
        print(Lb)
        #***************************************************************************************************************
        if Lb<=Lp:
            Mnplt=Mp
            Mn=Mnplt
        if Lp<Lb<=Lr:
            Mnplt=Cb*(Mp-((Mp-0.7*Fy*Sx)*((Lb-Lp)/(Lr-Lp))))
            if Mnplt<=Mp:
                Mn=Mnplt
            else:
                Mn=Mp
        if Lb>Lr:
            Fcr=((Cb*((np.pi)**2)*E)/((Lb/rts)**2))#*math.sqrt(1+(0.078*J*c*((Lb/rts)**2)/(Sx*h0)));
            print("cfcr",math.sqrt(1+(0.078*J*c*((Lb/rts)**2)/(Sx*h0))))
            print("Fcr=",Fcr)
            Mnplt=Fcr*Sx;print(Mnplt)
            if Mnplt<=Mp:
                Mn=Mnplt
            else:
                Mn=Mp
                
        #Escoger el minimo
        if Mp<=Mn:
            Mn=Mp
        else:
            Mn=Mn
        
        Mr=fi*Mn       
        print("Momento nominal=   ",Mn,"N-m")
        print("Momento resistente=",Mr,"N-m")
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
                                      
    #F.2.6.3 _Seccion en I con simetria doble, con alma compacta y aletas no compactas o esbeltas
        
    if (lamdaA<lamdaAp) and (lamdaP>lamdaPp) and (lamdaP<lamdaPr):
        entro=2
        print("-")
        print("La seccion con alma compacta y aletas no compactas o esbeltas")
        
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
        rts=math.sqrt((math.sqrt(Iy*Cw))/Sx)
        Mp=Fy*Zx
        print(Mp)
        #,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
        
        #Calcuo de resistencia al pandeo lateral torsional      
        #***************************************************************************************************************
        Lp=(1.76*ry)/(math.sqrt(E/Fy))
        Lr=1.95*rts*(E/(0.7*Fy))*math.sqrt(((J*c)/(Sx*h0))+math.sqrt((((J*c)/(Sx*h0))**2)+6.76*((0.7*Fy/E)**2)))
        #***************************************************************************************************************
        
        #Pandeo lateral torcional
        if Lb<=Lp:
            Mnplt=Mp
        else:
            if Lb<=Lr:
                Mnplt=Cb*(Mp-((Mp-(0.7*Fy*Sx))*((Lb-Lp)/(Lr-Lp))))
                if Mnplt<=Mp:
                    Mnplt=Mnplt
                else:
                    Mnplt=Mp
            else:
                Mnplt=Fcr*Sx
                if Mnplt<=Mp:
                    Mnplt=Mnplt
                else:
                    Mnplt=Mp
        
        #Pandeo local de aleta a compresion            
        if lamdaP<=lamdaPr:
            Mnpla=Cb*(Mp-((Mp-0.7*Fy*Sx)*((lamdaP-lamdaPp)/(lamdaPr-lamdaPp))))
        else:
            Kc=4/math.sqrt(h/tw)
            Mnpla=0.9*E*Kc*Sx/(lamdaP**2)
            
        #Escoger el minimo
        if Mnplt<=Mnpla:
            Mn=Mnplt
        else:
            Mn=Mnpla
            
        Mr=fi*Mn       
        print("Momento nominal=   ",Mn,"N-m")
        print("Momento resistente=",Mr,"N-m")
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
    
    #F.2.6.4 _Miembros de seccion I con alma compacta o no compacta
    if (lamdaA>lamdaAp)and (lamdaA<lamdaAr) and (MetodoConservador==0):
        entro=3
        print("-")
        print("Alma no compacta metodo no conservador")
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #Resisten a fluencia en la aleta a compresion
            #Variables
        Sxc=Sx#Modulo elastico de la secion referido a las aletas a compresion_ Sxc=Sx cuando seccion de doble simetria
        Sxt=Sx#Modulo elastico de la secion referido a las aletas a tension_ Sxt=Sx cuando seccion de doble simetria
        Myc=Fy*Sxc
        
        Mp=Zx*Fy
        if Mp>(1.6*Sxc*Fy):
            Mp=(1.6*Sxc*Fy)
            
        hc=h #Igual a h para simetria doble. Para perfiles laminados, dos veces la distancia entre el centroide de la seccion y la cara interna de la aleta menos el filete o radio de la esquina
                    #Rpc
        if Iyc/Iy>0.23:
            if hc/tw<=lamdaAp:
                Rpc=Mp/Myc
            else:
                Rpc=(Mp/Myc)-(((Mp/Myc)-1)*((lamdaA-lamdaAp)/(lamdaAr-lamdaAp)))
                if Rpc<=(Mp/Myc):
                    Rpc=Rpc
                else:
                    Rpc=(Mp/Myc)
        if (Iyc/Iy)<=0.23:
            Rpc=1
                    
            #Resistencia fluencia en la aleta a compresion
        Mnfac=Rpc*Myc
        
        
        if Iyc/Iy<=0.23:
            J=0
        #Resistencia pandeo lateral torsional
        #***************************************************************************************************************
                        #Variables Lp
        bfc=b*2#Ancho de la aleta a compresion igual a bf para simetria doble
        tfc=t#Igual a tf para doble simetria.Espesor de la aleta a compresion
        aw=(hc*tw)/(bfc*tfc)
        rt=bfc/math.sqrt(12*((h0/d)+(aw*(h**2)/(6*h0*d))))
        #rt puede aproximarse a: rt=bfc/(math.sqrt(12*(1+(aw/6))))
                        #Variables Lr
        if (Sxt/Sxc)>=0.7:
            Fl=0.7*Fy
        else:
            if (Fy*Sxt/Sxc)>=(0.5*Fy):
                Fl=Fy*Sxt/Sxc
            else:
                Fl=0.5*Fy        
        #___________________________________________
        Lp=(1.1*rt)/(math.sqrt(E/Fy))
        Lr=1.95*rt*(E/Fl)*math.sqrt((J*c/(Sxc*h0))+math.sqrt(((J*c/(Sxc*h0))**2)+6.76*((Fl/E)**2)))
        #***************************************************************************************************************
        if Lb<=Lp:
            Mnplt=Mnfac
        else:
            if Lb<=Lr:
                Mnplt=Cb*((Rpc*Myc)-(((Rpc*Myc)-(Fl*Sxc))*((Lb-Lp)/(Lr-Lp))))
                if Mnplt>(Rpc*Myc):
                    Mnplt=Rpc*Myc
            else:
                #Calculo de Fcr
                Fcr=((Cb*((np.pi)**2)*E)/((Lb/rt)**2))*math.sqrt(1+(0.078*J*((Lb/rt)**2)/(Sxc*h0)))
                
                #--------------
                Mnplt=Fcr*Sxc
                if Mnplt>(Rpc*Myc):
                    Mnplt=Rpc*Myc
        #***************************************************************************************************************
                    
        #Comprobacion de pandeo local de la aleta a compresion
        #***************************************************************************************************************
        Kc=4/math.sqrt(h/tw)
        if Kc<0.35:
            Kc=0.35
        if Kc>0.76:
            Kc=0.76
            
        if lamdaP<=lamdaPp:
            Mnpla=Mnfac
        else:
            if lamdaP<=lamdaPr:
                Mnpla=(Rpc*Myc)-(((Rpc*Myc)-(Fl*Sxc))*((lamdaP-lamdaPp)/(lamdaPr-lamdaPp)))
            else:
                Mnpla=0.9*E*Kc*Sxc/(lamdaP**2)
                
        #Fluencia en aleta a tension
        #***************************************************************************************************************
        if Sxt>=Sxc:
            Mnat=Mnfac
        else:
            Myt=Fy*Sxt
            if (hc/tw)<=lamdaAp:
                Rpt=Mp/Myt
            else:
                Rpt=(Mp/Myt)-(((Mp/Myt)-1)*((lamdaA-lamdaAp)/(lamdaAr-lamdaAp)))
                if Rpt>(Mp/Myt):
                    Rpt=(Mp/Myt)
            Mnat=Rpt*Myt
            
        #Escoger el minimo    
        Mn=Mnfac
        if Mnplt<Mn:
            Mn=Mnplt
        if Mnpla<Mn:
            Mn=Mnpla
        if Mnat<Mn:
            Mn=Mnat  
        Mr=fi*Mn       
        print("Momento nominal=   ",Mn,"N-m")
        print("Momento resistente=",Mr,"N-m")
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    
    
    #Seccion en I con simetria doble o simple, con alma esbelta F.2.6.5
    if (lamdaA>=lamdaAr) or ((lamdaA>lamdaAp) and (lamdaA<lamdaAr) and (MetodoConservador==1)):
        entro=4
        print("-")
        print("La seccion es con alma esbelta o no esbelta pero con el metodo conservador")
        #***************************************************************************************************************
        Sxc=Sx#Modulo elastico de la secion referido a las aletas a compresion_ Sxc=Sx cuando seccion de doble simetria
        Sxt=Sx#Modulo elastico de la secion referido a las aletas a tension_ Sxt=Sx cuando seccion de doble simetria
        
        Kc=4/math.sqrt(h/tw)
        if Kc<0.35:
            Kc=0.35
        if Kc>0.76:
            Kc=0.76
         
        #Fluencia de la aleta a compresion
        #--------------------------------------------------------------------------------------------------------------
        #aw no debe excedder de 10  
        bfc=b*2#Ancho de la aleta a compresion igual a bf para simetria doble
        tfc=t#Igual a tf para doble simetria.Espesor de la aleta a compresion
        aw=(hc*tw)/(bfc*tfc)
        if aw>10:
            aw=10    
        Rpg=1-((aw/(1200+(300*aw)))*((hc/tw)-(5.7*math.sqrt(E/Fy))))
        if Rpg>1:
            Rpg=1 
            
        Mp=Rpg*Fy*Sxc
        
        #Pandeo lateral torsional   
        #--------------------------------------------------------------------------------------------------------------
        Lp=(1.1*rt)/(math.sqrt(E/Fy))
        Lr=np.pi*rt*math.sqrt(E/(0.7*Fy))
        
        if Lb<=Lp:
            Mnplt=Mp
        else:
            if Lb<Lr:
                Fcr=Cb*(Fy-(0.3*Fy*((Lb-Lp)/(Lr-Lp))))
                if Fcr>Fy:
                    Fcr=Fy
                Mnplt=Rpg*Fcr*Sxc
            else:
                Fcr=Cb*(np.pi**2)*E/((Lb/rt)**2)
                if Fcr>Fy:
                    Fcr=Fy
                Mnplt=Rpg*Fcr*Sxc
                
        #Comprobacion por pandeo local de la aleta a compresion
        #--------------------------------------------------------------------------------------------------------------
        if lamdaP<=lamdaPp:
            Mnpla=Mp
        else:
            if lamdaP<=lamdaPr:
                Fcr=Fy-(0.35*Fy*((lamdaP-lamdaPp)/(lamdaPr-lamdaPp)))
                Mnpla=Rpg*Fcr*Sxc
            else:
                Fcr=0.9*E*Kc/(lamdaP)
                Mnpla=Rpg*Fcr*Sxc
                
        #Fluencia en la aleta a tension
        #--------------------------------------------------------------------------------------------------------------
        if Sxt>=Sxc:
            Mnat=Mp
        else:
            Mnat=Fy*Sxt
        #--------------------------------------------------------------------------------------------------------------
        
            
        #Escoger el minimo    
        Mn=Mp
        if Mnplt<Mn:
            Mn=Mnplt
        if Mnpla<Mn:
            Mn=Mnpla
        if Mnat<Mn:
            Mn=Mnat
        if Mp<Mn:
            Mn=Mp   
        Mr=fi*Mn       
        print("Momento nominal=   ",Mn,"N-m")
        print("Momento resistente=",Mr,"N-m")         
        #***************************************************************************************************************
        
    #Validaciones
    #--------------------------------------------------------------------------
    porcentaje=(Mr/Mmax)*100;print("Trabaja al:",porcentaje,"%")
      
    if Mr<Mrmin and porcentaje>=100 :
        Mrmin=Mr
        shape=L[perfil,84]
        savep=porcentaje
    
    
    file = open("out.csv", "a")
    file. write("% s" %L[perfil,84]+";"+"% s" %Mr +";"+"% s" %porcentaje +";"+"\n")
    file. close()
    #--------------------------------------------------------------------------
    perfilc=perfilc+1#Contador

        
#Veredicto
print("_______________________________________________________") 

if prueba==1 or prueba==2:      
    print("El calculo para el perfil es: ")    
if prueba==0:
    print("El perfil mas eficiente para las condiciones dadas es:") 
    
print(shape)
print("Momento resistente=     ",Mrmin,"N-m")
print("Porcentaje de ocupacion=",savep,"%")
print("_______________________________________________________")
print("Nota: Un documento (out.csv) ha sido guardado en la carpeta donde se ha ejecutado el programa. Perfil_Momento resistente_Ocupacion")
print("Warning!! Si desea conservar su archivo debe renombrarlo")

                              
   







                                

#Notas___________________________________________________________________________________
'''
#Verificacion por cortante
#-----------------------------------------------------------------------------------------------------------------------
Aw=h*tw           #Area de la seccion del alma
Cv=1              #Para perfiles en I
Vn=0.6*Fy*Aw*Cv   #Cortante nominal
Vr=0.9*Vn
#-----------------------------------------------------------------------------------------------------------------------


#Verificacion por deflexion
#-----------------------------------------------------------------------------------------------------------------------
w=w #Carga disribuida
delta=5*w*(Lb**4)/(384*E*Ix)
#-----------------------------------------------------------------------------------------------------------------------
'''


#Notas___________________________________________________________________________________
'''       #Aletas de perfiles armados en I de simetria doble o simple
lamdaPp=0.38*math.sqrt(E/Fy)
lamdaPr=0.95*math.sqrt(Kc*E/Fl)  
'''

'''
print("_________")
print(L[0,0])
x=L[1,19]
s=0
while s<30:
    print(L[s,2])
    s=s+1
'''
'''
#Perfi database
import pandas as pd

database=pd.read_csv("Database.csv", header=0)
print("Esta es su base de datos") #Perfilearia Americana
print(database)
print(database.iloc[[1],[4]])


total=database.iloc[[1],[4]]+database.iloc[[1],[4]]


print(total)


'''

'''
ruta = "Database3.csv"

file = open(ruta,"r")

print(file.read())
print("________")
print(file.splitlines(";"))
'''

'''import numpy as np

matriz=np.loadtxt("Database3.csv", delimiter=(";"))
print(matriz)

N = np.genfromtxt("Database3.csv", delimiter=(";"))
print(N)


'''
