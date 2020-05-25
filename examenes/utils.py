import random
import sympy
import datetime
import ast
from .models import ExamenResuelto
#import re

def random_array(array):
    """"""
    list_int = [0,1,2,3]
    random.shuffle(list_int)
    new_array = [0, 0, 0, 0]
    i = 0
    for index in list_int:
        new_array[index] = array[i]
        i = 1 + i
    return new_array

def calificacion_final(array):
    """"""
    sum_aux_calificacion = 0
    sum_calificacion = 0
    for index in range(0,5):
        sum_calificacion = sum_calificacion + array[index]
        if index != 4:
            sum_aux_calificacion = sum_aux_calificacion + array[index]

    partial_calificacion = regla_de_tres(sum_aux_calificacion)
    if partial_calificacion == "10":
        return partial_calificacion
    else:
        return regla_de_tres(sum_calificacion)


def regla_de_tres(partial_calificacion):
    """ 4                    --> 10
        partial_calificacion --> x
    """
    partial_calificacion = (partial_calificacion*10)/4
    if int(partial_calificacion) == 10:
        return "10"
    else:
        partial_calificacion = float(partial_calificacion)
        return f"{partial_calificacion:.2f}"


# Funciones para crear una pregunta aleatoria
def replace_random_int(pregunta, str_to_change='random'):
    """"""
    count_random = pregunta.count(str_to_change)
    i = 0
    while i < count_random:
        pregunta = pregunta.replace(str_to_change, str(random.randint(1, 3)), 1)
        # pregunta = re.sub(f'{str_to_change}', str(random.randint(1, 10)), pregunta)
        i = i + 1
    return pregunta

def superficies_regladas(pregunta, dependiente='dependiente'):
    """"""
    x, y, z = sympy.symbols('x y z')
    a, b, x0, y0 = sympy.sympify(random.randint(1, 3)), sympy.sympify(random.randint(1, 3)), sympy.sympify(random.randint(1, 3)), sympy.sympify(random.randint(1, 3))
    eq = x**2/a**2 - y**2/b**2 - z
    z0 = x0**2/a**2 - y0**2/b**2
    pregunta = pregunta.replace('x0', str(x0))
    pregunta = pregunta.replace('y0', str(y0))
    pregunta = pregunta.replace('z0', str(z0))
    pregunta = pregunta.replace('ecuacion', str(eq))
    return pregunta

def plano_tangente(pregunta, dependiente='dependiente'):
    """"""
    x, y, z = sympy.symbols('x y z')
    a, b, c = sympy.sympify(2 * random.randint(1, 5)), sympy.sympify(2 * random.randint(1, 5)), sympy.sympify(2 * random.randint(1, 5))
    funcion = x**2/a**2 + y**2/b**2 + z**2/c**2
    constante = sympy.sympify(3)

    x0, y0 = sympy.sympify(random.randint(1, 5)), sympy.sympify(random.randint(1, 5))
    dentro_raiz = constante - x0**2/a**2 - y0**2/b**2
    while dentro_raiz < 0:
        x0, y0 = sympy.sympify(random.randint(1, 5)), sympy.sympify(random.randint(1, 5))
        dentro_raiz = constante - x0**2/a**2 - y0**2/b**2
    z0 = c * sympy.sqrt(dentro_raiz)

    pregunta = pregunta.replace('x0', f'{x0}')
    pregunta = pregunta.replace('y0', f'{y0}')
    pregunta = pregunta.replace('z0', f'{z0}')
    pregunta = pregunta.replace('ecuacion', f'{funcion}={constante}')
    return pregunta

def familia_ortogonales(pregunta):
    """"""
    return pregunta

def quiz_1(pregunta, dependiente='dependiente'):
    """"""
    x, y = sympy.symbols('x y')
    eq = -sympy.sqrt(2)*y + 2 - sympy.Rational(7, 5)*x
    pregunta = pregunta.replace('ecuacion', str(eq))
    return pregunta

def quiz_2(pregunta, dependiente='dependiente'):
    """"""
    x0 = sympy.Rational(2, 3)*sympy.Rational(4, 4)
    y0 = sympy.Rational(1, 8)*sympy.sqrt(32)
    z0 = -1
    pregunta = pregunta.replace('x0', f'{x0}')
    pregunta = pregunta.replace('y0', f'{y0}')
    pregunta = pregunta.replace('z0', f'{z0}')
    return pregunta

crear_pregunta = {
    "default": replace_random_int,
    "superficies_regladas": superficies_regladas,
    "plano_tangente": plano_tangente,
    "familia_ortogonales": familia_ortogonales,
    "ecuacion1": quiz_1,
    "ecuacion2": quiz_2,
}

# Funciones para obtener una pregunta en formato html
def obtener_formato_html(pregunta):
    inicio = pregunta.find("$")
    final = pregunta.rfind("$")
    sympy_str = ast.literal_eval(pregunta[inicio+1:final])

    sympy_obj = sympy.sympify(pregunta[inicio+1:final])
    if isinstance(sympy_str, list):
        sympy_obj = sympy.Matrix(sympy_str)
    # TODO Poisson Geometry, i.e if isinstance(sympy_str, dict):

    sympy_latex = sympy.latex(sympy_obj)
    pregunta_html = f"{pregunta[0: inicio]} ${sympy_latex}$ {pregunta[final+1:]}"
    return pregunta_html

def superficies_regladas_html(pregunta):
    final = pregunta.rfind("$")
    antefinal = pregunta[0:final-1].rfind("$")

    sympy_obj = sympy.sympify(pregunta[antefinal+1:final])
    sympy_latex = sympy.latex(sympy_obj)
    pregunta_html = f"{pregunta[0: antefinal]} ${sympy_latex}$ {pregunta[final+1:]} $= 0$"
    return pregunta_html

def plano_tangente_html(pregunta):
    # Ecuacion
    inicio = pregunta.find("$")
    final = pregunta.find("$", inicio + 1)
    sympy_obj = sympy.sympify(pregunta[inicio+1:final-2])
    sympy_latex = sympy.latex(sympy_obj)

    # Punto
    final_punto = pregunta.rfind("$")
    antefinal = pregunta[0:final_punto-1].rfind("$")
    punto = pregunta[antefinal+2:final_punto-1].strip().split(",")
    punto_latex_aux = []
    for elemento in punto:
        sympy_obj = sympy.sympify(elemento)
        punto_latex_aux.append(sympy.latex(sympy_obj))

    punto_latex = f'({punto_latex_aux[0]}, {punto_latex_aux[1]}, {punto_latex_aux[2]})'
    # Pregunta html
    pregunta_html = f"{pregunta[0: inicio]} ${sympy_latex}{pregunta[final-2:final]}$ {pregunta[final+1:antefinal]} ${punto_latex}$"
    return pregunta_html

def familia_ortogonales_html(pregunta):
    """"""
    return pregunta

def quiz_1_html(pregunta):
    """
    final = pregunta.rfind("$")
    antefinal = pregunta[0:final-1].rfind("$")

    sympy_obj = sympy.sympify(pregunta[antefinal+1:final])
    sympy_latex = sympy.latex(sympy_obj)
    pregunta_html = f"{pregunta[0: antefinal]} ${sympy_latex}= 0$ {pregunta[final+1:]}"
    return pregunta_html
    """
    pregunta_html = "Introduzca de manera adecuada los coeficientes de la siguiente ecuación en los bloques correspondientes: $\\sqrt{2}y + 2 − \\frac{7x}{5} = 0$ ($\\textbf{NOTA}:$ Recuerde, de ser necesario, cambiar los signos a la ecuación para que el coeficinte de la variable $x$ sea un número positivo)"
    return pregunta_html

def quiz_2_html(pregunta):
    """"""
    """
    # Punto
    final_punto = pregunta.rfind("$")
    antefinal = pregunta[0:final_punto-1].rfind("$")
    punto = pregunta[antefinal+1:final_punto].strip().split(",")
    punto_latex_aux = []
    for elemento in punto:
        sympy_obj = sympy.sympify(elemento)
        punto_latex_aux.append(sympy.latex(sympy_obj))

    punto_latex = f'({punto_latex_aux[0]}, {punto_latex_aux[1]}, {punto_latex_aux[2]})'
    # Pregunta html
    pregunta_html = f"{pregunta[0:antefinal]} ${punto_latex}$"
    """
    pregunta_html = "Simplifique las entradas del vector $\\big(\\frac{8}{12}, \\frac{\\sqrt{32}}{8}, -1\\big)$ e ingrese tales valores en las casillas correspondientes (respetando el orden natural de los índices)"
    return pregunta_html

pregunta_html = {
    "default": obtener_formato_html,
    "superficies_regladas": superficies_regladas_html,
    "plano_tangente": plano_tangente_html,
    "familia_ortogonales": familia_ortogonales_html,
    "ecuacion1": quiz_1_html,
    "ecuacion2": quiz_2_html,
}

# Funciones para crear respuestas random
def matriz2x2_options(matriz):
    """"""
    respuestas = list()
    if matriz.is_zero:
        respuestas.append("Sin inversa")
    else:
        respuestas.append(f"${sympy.latex(matriz)}$")

    i = 0
    while i < 3:
        random_matriz = sympy.Matrix([
            [random.randint(-3, 3), random.randint(-3, 3)],
            [random.randint(-3, 3), random.randint(-3, 3)]
        ])
        result = matriz + random_matriz
        respuestas.append(f"${sympy.latex(result)}$")
        i = i + 1

    return random_array(respuestas), True

def transpuesta_options(matriz):
    """"""
    respuestas = list()
    respuestas.append(f"${sympy.latex(matriz)}$")
    i = 0
    while i < 3:
        random_matriz = sympy.Matrix([
            [random.randint(-3, 3), random.randint(-3, 3), random.randint(-3, 3)],
            [random.randint(-3, 3), random.randint(-3, 3), random.randint(-3, 3)],
            [random.randint(-3, 3), random.randint(-3, 3), random.randint(-3, 3)]
        ])
        result = matriz + random_matriz
        respuestas.append(f"${sympy.latex(result)}$")
        i = i + 1

    return random_array(respuestas), True

def superficies_regladas_opcional():
    """"""
    return ["Respuesta 1: (", ",", ",", ") + t (", ",", ",", ").", "break", "Respuesta 2: (", ",", ",", ") + t (", ",", ",", ")."], False

def plano_tangente_opcional():
    """"""
    return ["Respuesta:", "x +", "y +", "z +", "= 0",], False

def quiz_1_options():
    """"""
    return ["Respuesta:", "x +", "y +", "z +", "="], False

def quiz_2_options():
    """"""
    return ["Respuesta: (", ",", ",", ")."], False

def familia_ortogonales_opcional():
    """"""
    a = "$\\{$ rectas por el origen $\\}$ y $\\{$ parábolas con vértice en el origen $\\}$"
    b = "$\\{$ parábolas con vértice en el origen $\\}$ y $\\{$ círculos con centro en el origen $\\}$"
    c = "$\\{$ rectas por el origen $\\}$ y $\\{$ círculos con centro en el origen $\\}$"
    d = "$\\{$ elipses con centro en el origen $\\}$ y $\\{$ parábolas con vértice en el origen $\\}$"
    return random_array([a, b, c, d]), True

respuesta_opcional = {
    "matriz2x2_options": matriz2x2_options,
    "superficies_regladas": superficies_regladas_opcional,
    "plano_tangente": plano_tangente_opcional,
    "familia_ortogonales": familia_ortogonales_opcional,
    "transpuesta_options": transpuesta_options,
    "ecuacion1": quiz_1_options,
    "ecuacion2": quiz_2_options,
}

def custom_respuesta_html(array):
    """"""
    P0_0 = (sympy.sympify(array[0]), sympy.sympify(array[1]), sympy.sympify(array[2]))
    P0_1 = (sympy.sympify(array[6]), sympy.sympify(array[7]), sympy.sympify(array[8]))
    v1_direccion = (sympy.sympify(array[3]), sympy.sympify(array[4]), sympy.sympify(array[5]))
    v2_direccion = (sympy.sympify(array[9]), sympy.sympify(array[10]), sympy.sympify(array[11]))

    return f'${P0_0}+t{v1_direccion}$ y ${P0_1}+t{v2_direccion}$'

def custom_plano_tangente_html(array):
    """"""
    x = sympy.latex(sympy.sympify(array[0]))
    y = sympy.latex(sympy.sympify(array[1]))
    z = sympy.latex(sympy.sympify(array[2]))
    c = sympy.latex(sympy.sympify(array[3]))

    return f'$({x})x +({y})y +({z})z +({c}) = 0$'

def custom_quiz1_respuesta_html(array):
    """"""
    x = sympy.latex(sympy.sympify(array[0]))
    y = sympy.latex(sympy.sympify(array[1]))
    z = sympy.latex(sympy.sympify(array[2]))
    c = sympy.latex(sympy.sympify(array[3]))
    zero = sympy.latex(sympy.sympify(array[4]))
    return f'$({x})x +({y})y + ({z})z + ({c})= {zero}$'


def custom_quiz2_respuesta_html(array):
    """"""
    x = sympy.latex(sympy.sympify(array[0]))
    y = sympy.latex(sympy.sympify(array[1]))
    z = sympy.latex(sympy.sympify(array[2]))

    return f'$({x}, {y}, {z})$'

custom_alumno_respuesta = {
    "superficies_regladas": custom_respuesta_html,
    "plano_tangente": custom_plano_tangente_html,
    "ecuacion1": custom_quiz1_respuesta_html,
    "ecuacion2": custom_quiz2_respuesta_html,
}

# Django method
def save_examen_resuelto(tema, cuenta, calif, tiempo, preguntas, status):
    """"""
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        #
        Examen = ExamenResuelto()
        Examen.tema = tema
        Examen.numero_cuenta = cuenta
        Examen.tiempo = date
        Examen.status_gsheet = str(status)
        Examen.calificacion = str(calif)
        Examen.pregunta1 = str(preguntas[0])
        Examen.respuesta1_correcta = str(preguntas[1])
        Examen.respuesta1_alumno = str(preguntas[2])
        Examen.respuesta1_calif = str(preguntas[3])
        Examen.pregunta2 = str(preguntas[4])
        Examen.respuesta2_correcta = str(preguntas[5])
        Examen.respuesta2_alumno = str(preguntas[6])
        Examen.respuesta2_calif = str(preguntas[7])
        Examen.pregunta3 = str(preguntas[8])
        Examen.respuesta3_correcta = str(preguntas[9])
        Examen.respuesta3_alumno = str(preguntas[10])
        Examen.respuesta3_calif = str(preguntas[11])
        Examen.pregunta4 = str(preguntas[12])
        Examen.respuesta4_correcta = str(preguntas[13])
        Examen.respuesta4_alumno = str(preguntas[14])
        Examen.respuesta4_calif = str(preguntas[15])
        Examen.pregunta5 = str(preguntas[16])
        Examen.respuesta5_correcta = str(preguntas[17])
        Examen.respuesta5_alumno = str(preguntas[18])
        Examen.respuesta5_calif = str(preguntas[19])
        Examen.save()
        return (True, f'[INFO] Calificación guardada en la Base de Datos exitosamente a la cuenta {cuenta}')
    except Exception as e:
        return (False, f'[ERROR] Al guardar calificación en la Base de Datos a la cuenta {cuenta}, ERROR: {e}')
