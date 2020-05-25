import sympy
import random
import ast
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse
from .models import Examen
from .utils import pregunta_html, crear_pregunta, calificacion_final, respuesta_opcional, custom_alumno_respuesta, save_examen_resuelto, random_array
from .soluciones import respuesta_correcta
from .check import respuesta_correcta_check
from google_api.google_api import existe_cuenta, google_cuentas, google_cuentas_tema, agregar_calificacion, existe_calificacion


def examenes_list(request):
    """"""
    examenes = Examen.objects.all()
    return render(request, 'examenes/list.html', {'examenes': examenes})

def examen_detail(request, examen_id):
    """"""
    if examen_id == "2":
        template = 'examenes/tema2.html'
        examen = {"tema": "tema 2", "pregunta_base": "", "preguntas": []}
        cuentas_con_calificacion = google_cuentas_tema("tema 2")
        # Pregunta base
        aa = sympy.sympify(random.randint(1, 10))
        bb = sympy.sympify(random.randint(1, 10))
        pregunta_base = f'$T(x,y) = ({- aa * bb}y, x + {aa + bb}y)$.'
        examen["pregunta_base"] = pregunta_base
        # Preguntas
        matrix_rdn = sympy.Matrix([
            [random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)],
            [random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)],
            [random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)]
        ])
        T1 = f'T(x,y,z) = ({matrix_rdn[0,0]}x + {matrix_rdn[0,1]}y + {matrix_rdn[0,2]}z, {matrix_rdn[1,0]}x + {matrix_rdn[1,1]}y + {matrix_rdn[1,2]}z, {matrix_rdn[2,0]}x + {matrix_rdn[2,1]}y + {matrix_rdn[2,2]}z)'
        T2 = f'T(x,y,z) = ({matrix_rdn[2,0]}x + {matrix_rdn[2,1]}y + {matrix_rdn[2,2]}z, {matrix_rdn[1,0]}x + {matrix_rdn[1,1]}y + {matrix_rdn[1,2]}z, {matrix_rdn[0,0]}x + {matrix_rdn[0,1]}y + {matrix_rdn[0,2]}z)'
        T3 = f'T(x,y,z) = ({matrix_rdn[0,0]}x + {matrix_rdn[0,1]}y + {matrix_rdn[0,2]}z, {matrix_rdn[2,0]}x + {matrix_rdn[2,1]}y + {matrix_rdn[2,2]}z, {matrix_rdn[1,0]}x + {matrix_rdn[1,1]}y + {matrix_rdn[1,2]}z)'
        T4 = f'T(x,y,z) = ({matrix_rdn[1,0]}x + {matrix_rdn[1,1]}y + {matrix_rdn[1,2]}z, {matrix_rdn[0,0]}x + {matrix_rdn[0,1]}y + {matrix_rdn[0,2]}z, {matrix_rdn[2,0]}x + {matrix_rdn[2,1]}y + {matrix_rdn[2,2]}z)'
        options = random_array([T1, T2, T3, T4])
        # respuestas
        TT_matriz = sympy.Matrix([[0, - aa * bb], [1, aa + bb]])
        preguntas = [
            (f'Calcule la matriz de T en la base canónica de $R^2: B = \{{(1,0), (0,1)\}}$', 1, "matrix", [], str(TT_matriz.tolist())),
            (f'Calcule el polinomio característico de $T$', 2, "equation", [], str(TT_matriz.tolist())),
            (f'Calcule los valores propios de $T$', 3, "valores", [], str(TT_matriz.tolist())),
            (f'Calcule los vectores propios de $T$', 4, "vectores", [], str(TT_matriz.tolist())),
            (f'Escriba la transformación lineal que tiene asociada en la base canónica de $R^3$ la siguiente matriz $${sympy.latex(matrix_rdn)}$$', 5, "opcional", options, T1),
        ]
        for pregunta in preguntas:
            examen["preguntas"].append(pregunta)
    else:
        examen_query = Examen.objects.get(id=examen_id)
        preguntas = [pregunta.strip() for pregunta in examen_query.preguntas.split("--")][:-1]
        respuestas = [respuesta.strip() for respuesta in examen_query.respuestas.split("--")][:-1]
        opciones = [opcion.strip() for opcion in examen_query.opcional.split("--")][:-1]
        crear_preguntas = [opcion.strip() for opcion in examen_query.crear_pregunta.split("--")][:-1]

        examen = dict()
        examen.update({"tema": examen_query.tema, "id": examen_query.id })

        examen.update({"preguntas": [], })
        for index in range(0,len(preguntas)):
            # Crea la respuesta aleatoria
            if not crear_preguntas[index]:
                pregunta = crear_pregunta['default'](preguntas[index])
                html_pregunta = pregunta_html['default'](pregunta)
                default = True
            else:
                pregunta = crear_pregunta[crear_preguntas[index]](preguntas[index])
                html_pregunta = pregunta_html[crear_preguntas[index]](pregunta)
                default = False

            # Crea la respuesta opcionales, si es necesario
            respuesta = respuestas[index]
            opcional = opciones[index]
            custom_respuestas = []
            if opcional:
                if default:
                    resp_correcta = respuesta_correcta[respuesta](pregunta)
                    custom_respuestas, default = respuesta_opcional[opcional](resp_correcta)
                else:
                    custom_respuestas, default = respuesta_opcional[opcional]()

            examen["preguntas"].append((html_pregunta, custom_respuestas, index + 1, pregunta, default))
        template = 'examenes/detail.html'
        cuentas_con_calificacion = google_cuentas_tema(examen_query.tema)

    # Google API info
    cuentas = google_cuentas()

    return render(request, template, {'examen': examen, 'ctas_tema': cuentas_con_calificacion, 'cuentas': cuentas})


def check_examen(request):
    """"""
    if request.method == "POST":
        numero_cuenta = request.POST['numero_cuenta']
        tema = request.POST['tema']
        existe_cta = existe_cuenta(numero_cuenta)

        if not existe_cta:
            return render(request, 'examenes/noexiste.html', {'numero_cuenta': numero_cuenta, 'existe_cuenta': existe_cta})

        if existe_calificacion(numero_cuenta, tema):
            return render(request, 'examenes/noexiste.html', {'numero_cuenta': numero_cuenta, 'existe_cuenta': existe_cta})

        solucion = dict()
        solucion.update({"tema": tema, "tiempo": request.POST['tiempo']})

        if tema == 'tema 2':
            solucion.update({"pregunta_base": request.POST['pregunta_base']})
            calificacion = []
            google_api_preguntas = []
            examen_result = []
            # Pregunta 1
            preg1 = request.POST['pregunta1']
            resp1 = ast.literal_eval(request.POST['resp1'])

            M11 = sympy.sympify(request.POST.get('1--11', 0))
            M12 = sympy.sympify(request.POST.get('1--12', 0))
            M21 = sympy.sympify(request.POST.get('1--21', 0))
            M22 = sympy.sympify(request.POST.get('1--22', 0))
            lista_verificacion_1 = [resp1[0][0] - M11, resp1[0][1] - M12, resp1[1][0] - M21, resp1[1][1] - M22]
            puntaje1 = sympy.Rational(lista_verificacion_1.count(0), 4)
            matrix_alumno = sympy.Matrix([[M11, M12], [M21, M22]])
            TT_matriz = sympy.Matrix(resp1)
            calificacion.append(puntaje1)
            examen_result.append((preg1, f'${sympy.latex(TT_matriz)}$', f'${sympy.latex(matrix_alumno)}$', puntaje1))
            google_api_preguntas.append(preg1)
            google_api_preguntas.append(f'${sympy.latex(TT_matriz)}$')
            google_api_preguntas.append(f'${sympy.latex(matrix_alumno)}$')
            google_api_preguntas.append(puntaje1)
            # Pregunta 2
            preg2 = request.POST['pregunta2']
            resp2 = ast.literal_eval(request.POST['resp2'])

            X = sympy.symbols('X')
            pol_caract_TT = TT_matriz.charpoly(X).as_expr()
            x2 = sympy.sympify(request.POST.get('2--2', 0))
            x1 = sympy.sympify(request.POST.get('2--1', 0))
            x0 = sympy.sympify(request.POST.get('2--0', 0))
            lista_verificacion_2 = [pol_caract_TT.coeff(X**2) - x2, pol_caract_TT.coeff(X**1) - x1, pol_caract_TT.subs({X:0}) - x0]
            puntaje2 = sympy.Rational(lista_verificacion_2.count(0), 3)
            calificacion.append(puntaje2)
            examen_result.append((preg2, f'$p(\lambda) = ({pol_caract_TT.coeff(X**2)})\lambda^2 + ({pol_caract_TT.coeff(X**1)})\lambda + ({pol_caract_TT.subs({X:0})})$',
                                  f'$p(\lambda) = ({x2})\lambda^2 + ({x1})\lambda + ({x0})$', puntaje2))
            google_api_preguntas.append(preg2)
            google_api_preguntas.append(f'$p(\lambda) = ({pol_caract_TT.coeff(X**2)})\lambda^2 + ({pol_caract_TT.coeff(X**1)})\lambda + ({pol_caract_TT.subs({X:0})})$')
            google_api_preguntas.append(f'$p(\lambda) = ({x2})\lambda^2 + ({x1})\lambda + ({x0})$')
            google_api_preguntas.append(puntaje2)
            # Pregunta 3
            preg3 = request.POST['pregunta3']
            resp3 = ast.literal_eval(request.POST['resp3'])

            a_l1 = sympy.sympify(request.POST.get('3--1', 0))
            a_l2 = sympy.sympify(request.POST.get('3--2', 0))
            l1, l2 = tuple(TT_matriz.eigenvals().keys())
            lista_verificacion_3 = [a_l1 - l1, a_l2 - l2]
            puntaje3 = sympy.Rational(lista_verificacion_3.count(0), 2)
            if puntaje3.is_zero:
                lista_verificacion_3 = [a_l1 - l2, a_l2 - l1]
                puntaje3 = sympy.Rational(lista_verificacion_3.count(0), 2)
            calificacion.append(puntaje3)
            examen_result.append((preg3, f'$\lambda_1 = {l1}$ y $\lambda_2 = {l2}$ ó $\lambda_1 = {l2}$ y $\lambda_2 = {l1}$',
                                  f'$\lambda_1 = {a_l1}$ y $\lambda_2 = {a_l2}$', puntaje3))
            google_api_preguntas.append(preg3)
            google_api_preguntas.append(f'$\lambda_1 = {l1}$ y $\lambda_2 = {l2}$ ó $\lambda_1 = {l2}$ y $\lambda_2 = {l1}$')
            google_api_preguntas.append(f'$\lambda_1 = {a_l1}$ y $\lambda_2 = {a_l2}$')
            google_api_preguntas.append(puntaje3)
            # Pregunta 4
            preg4 = request.POST['pregunta4']
            resp4 = ast.literal_eval(request.POST['resp4'])

            a_l1_x = sympy.sympify(request.POST.get('4--11', 0))
            a_l1_y = sympy.sympify(request.POST.get('4--12', 0))
            a_l2_x = sympy.sympify(request.POST.get('4--21', 0))
            a_l2_y = sympy.sympify(request.POST.get('4--22', 0))

            l1_x = TT_matriz.eigenvects()[0][2][0][0,0]
            l1_y = TT_matriz.eigenvects()[0][2][0][1,0]
            l2_x = TT_matriz.eigenvects()[1][2][0][0,0]
            l2_y = TT_matriz.eigenvects()[1][2][0][1,0]

            lista_verificacion_4a = [a_l1_x - l1_x, a_l1_y - l1_y, a_l2_x - l2_x, a_l2_y - l2_y]
            puntaje4a = sympy.Rational(lista_verificacion_4a.count(0), 4)

            lista_verificacion_4b = [a_l2_x - l1_x, a_l2_y - l1_y, a_l1_x - l2_x, a_l1_y - l2_y]
            puntaje4b = sympy.Rational(lista_verificacion_4b.count(0), 4)

            puntaje4 = puntaje4a if puntaje4a > puntaje4b else puntaje4b
            calificacion.append(puntaje4)
            examen_result.append((preg4, f'$\\vec{{\lambda_1}} = ({l1_x}, {l1_y})$ y $\\vec{{\lambda_2}} = ({l2_x}, {l2_y})$ ó $\\vec{{\lambda_1}} = ({l2_x}, {l2_y})$ y $\\vec{{\lambda_2}} = ({l1_x}, {l1_y})$',
                                  f'$\\vec{{\lambda_1}} = ({a_l1_x}, {a_l1_y})$ y $\\vec{{\lambda_2}} = ({a_l2_x}, {a_l2_y})$', puntaje4))
            google_api_preguntas.append(preg4)
            google_api_preguntas.append(f'$\\vec{{\lambda_1}} = ({l1_x}, {l1_y})$ y $\\vec{{\lambda_2}} = ({l2_x}, {l2_y})$ ó $\\vec{{\lambda_1}} = ({l2_x}, {l2_y})$ y $\\vec{{\lambda_2}} = ({l1_x}, {l1_y})$')
            google_api_preguntas.append(f'$\\vec{{\lambda_1}} = ({a_l1_x}, {a_l1_y})$ y $\\vec{{\lambda_2}} = ({a_l2_x}, {a_l2_y})$')
            google_api_preguntas.append(puntaje4)
            # Pregunta 5
            preg5 = request.POST['pregunta5']
            resp5 = request.POST['resp5']

            a_resp5 = request.POST.get('5', '')
            puntaje5 = 1 if a_resp5 == resp5 else 0

            calificacion.append(puntaje5)
            examen_result.append((preg5, resp5,
                                  a_resp5, puntaje5))
            google_api_preguntas.append(preg5)
            google_api_preguntas.append(resp5)
            google_api_preguntas.append(a_resp5)
            google_api_preguntas.append(puntaje5)
            # Final
            solucion["examen_result"] = examen_result
        else:
            examen_query = Examen.objects.get(tema=request.POST['tema'])
            respuestas = [respuesta.strip() for respuesta in examen_query.respuestas.split("--")][:-1]

            solucion.update({"examen_result": []})
            calificacion = []
            google_api_preguntas = []
            for index in range(0,len(respuestas)):
                respuesta = respuestas[index]
                pregunta_html = request.POST[f'pregunta{index+1}']
                pregunta_latex = request.POST[f'pregunta_latex{index+1}']
                alumno_respuesta = request.POST.get(f'{index+1}', False)
                if not alumno_respuesta:
                    faltan_respuestas = True
                    respuestas_parciales = []
                    i = 1
                    while faltan_respuestas:
                        respuesta_parcial = request.POST.get(f'{index+1}-{i}',False)
                        if respuesta_parcial == 'no_stop_here':
                            pass
                        elif respuesta_parcial:
                            respuestas_parciales.append(respuesta_parcial)
                        else:
                            faltan_respuestas = False
                        i = i + 1
                    alumno_respuesta = respuestas_parciales

                resp_correcta_html = respuesta_correcta[respuesta](pregunta_html, html=True)
                resp_correcta = respuesta_correcta[respuesta](pregunta_html)
                check_resp = respuesta_correcta_check[respuesta](resp_correcta, alumno_respuesta)
                alumno_respuesta_aux = request.POST.get(f'{index+1}',False)
                if not alumno_respuesta_aux:
                    alumno_respuesta = custom_alumno_respuesta[respuesta](alumno_respuesta)
                solucion["examen_result"].append((pregunta_latex, resp_correcta_html, alumno_respuesta, check_resp))
                google_api_preguntas.append(pregunta_latex)
                google_api_preguntas.append(resp_correcta_html)
                google_api_preguntas.append(alumno_respuesta)
                google_api_preguntas.append(check_resp)
                calificacion.append(check_resp)

        response, msg_gsheet_api = agregar_calificacion(request.POST['tema'], numero_cuenta, calificacion_final(calificacion), request.POST['tiempo'], google_api_preguntas)
        print(msg_gsheet_api)
        save_examen, msg_save_examen = save_examen_resuelto(request.POST['tema'], numero_cuenta, calificacion_final(calificacion), request.POST['tiempo'], google_api_preguntas, response)
        print(msg_save_examen)

        context = {'solucion': solucion, "calificacion_final": calificacion_final(calificacion),
                   'numero_cuenta': numero_cuenta, 'existe_cuenta': existe_cta,
                   'response': response, 'save_examen': save_examen}

        return render(request, 'examenes/solucion.html', context)

def credits_page(request):
    """"""
    return render(request, 'misc/credits.html')
