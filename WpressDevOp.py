import os


import subprocess
from stat import *



class Dominio:
    nombre = ""
    usuario = ""
    es_wordpress = False


users_home_dir = '/home'
def lista_dominios(imprime = True):
    dominios = []
    ipaddress = ""

    if imprime:
        print("####  Lista Dominios del servidor " + ipaddress)

    for usuario in os.listdir(users_home_dir):
        if imprime:
            print("Usuario: " + usuario)
        try:
            wordpress = ""
            webs = os.path.join(users_home_dir, usuario, "web")
            for dominio in os.listdir(webs):
                if os.path.exists((os.path.join(webs, dominio, 'public_html', 'wp-config.php'))):
                    wordpress = " ** Con Wordpress ** "
                dom = Dominio()
                dom.nombre = dominio
                dom.es_wordpress = True if len(wordpress) > 1 else False
                dom.usuario = usuario
                if imprime:
                    print("    Dominio: " + dom.nombre + " " + wordpress + " Wpress:" + str(dom.es_wordpress)
                          + " usuario:" + dom.usuario)
                dominios.append(dom)
        except Exception as e:
            print(" Error --> " + str(e))
    if imprime:
        print("#### FIN de Lista Dominios del servidor " + ipaddress)
    return dominios

debug = False


def crea_regla_disable(Lines, path_htaccess):
    if ("#### Bantics Bloqueo Wordpres xmlrpc ####\n" in Lines):
        print("Tiene la linea")
    else:
        print("No tiene la linea")
        with open(path_htaccess, "a+") as f:
            f.write(' \n')
            f.write('#### Bantics Bloqueo Wordpres xmlrpc ####\n')
            f.write('<Files xmlrpc.php>\n')
            f.write('Order Deny,Allow\n')
            f.write('Deny from all\n')
            f.write('</Files>\n')
            f.write('#### Fin de Bantics BLoqueo Wordpres xmlrpc ####\n')
            f.close()

def disable_xmlrpc_via_htaccess():
    print("Lista Dominios del servidor ")
    #     lista de domininios /home/p1078fac/web/facttic.org.ar/public_html/
    for usuario in os.listdir(users_home_dir):
        print("Usuario: " + usuario)
        try:
            wordpress = ""
            webs = os.path.join(users_home_dir, usuario, "web")
            for dominio in os.listdir(webs):
                if os.path.exists((os.path.join(webs, dominio, 'public_html', 'wp-config.php'))):
                    wordpress = " ** Con Wordpress ** "
                    path_htaccess = os.path.join(webs, dominio, 'public_html', '.htaccess')
                    if not os.path.exists((path_htaccess)):
                        crea_regla_disable([], path_htaccess)

                    else:
                        print("Wordpress con .htaccess")
                        file1 = open(path_htaccess, 'r')
                        Lines = file1.readlines()
                        crea_regla_disable(Lines, path_htaccess)

        except Exception as e:
            print(" Error --> " + str(e))


def reparar_permisos_wp(nombre_dominio):
    this_path = os.path.curdir

    # verificar el dominio y a que usuario corresponde:
    dominios = lista_dominios(imprime=False)
    dominio_encontrado = False
    for dom_in_use in dominios:
        if nombre_dominio in dom_in_use.nombre:
            dominio_encontrado=True
            print("Dominio verificado")
            comando = this_path + "/reparaPermisosWP.sh"
            os.chmod(comando, S_IRUSR | S_IWUSR | S_IXUSR | S_IROTH | S_IWOTH | S_IXOTH )
            ruta = os.path.join(users_home_dir, dom_in_use.usuario, "web", dom_in_use.nombre, "public_html")
            print("*-* Se corre reparaPermisosWP: ", comando + " " + ruta + dom_in_use.usuario)
            subprocess.run([comando, ruta + dom_in_use.usuario])
            # subprocess.run(["/bin/bash", "-x " + comando + " " + ruta + dom_in_use.usuario])
    if not dominio_encontrado:
        print("**** No se encontro ", nombre_dominio, "en este servidor ****")


def Main():
    print("Wordpress Bantics DevOps strageThings :D\n")
    print("1) Lista de dominios en el servidor\n")
    print("2) Poner .htacces disable a los dominios wpress que no lo tengan")
    print("3) Reparar Permisos de un dominio wordpress")
    # print("4) Reparar Permisos de todos dominios wordpress de todos los usuarixs")
    print("q) Salir\n")
    i = input("Elegi una Opcion \n")

    while i not in ['q']:
        if i == '1':
            lista_dominios()

        if i == '2':
            disable_xmlrpc_via_htaccess()

        if i == '3':
            input_dominio = input("Ingresa el nombre de dominio:\n")
            reparar_permisos_wp(input_dominio)
            # reparar_permisos_wp(lista_dominio)

        i = input("Elegi una Opcion \n")


if __name__ == "__main__":
    Main()