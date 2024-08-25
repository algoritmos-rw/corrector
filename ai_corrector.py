import time
import random

VIDA_ACTIVADA = True
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6
LIMIT_HOUR = 23
MINIMUM_HOUR = 7
MONDAY = 0
THURSDAY = 3
HORA_CLASE = 17
FIN_HORA_CLASE = 20

def movie_generation():
  return random.choice(["Pulp Fiction", "Terminator 2", "Mystic River", "Zoolander", "onnie darko"])

FRASES_CORRECTOR = [
  lambda entrega, dia: "El corrector estaba durmiendo..",
  lambda entrega, dia: f"Hola, si estás ahora haciendo una entrega de {entrega}, te recomiendo que mejor veas " + movie_generation(),
  lambda entrega, dia: f"La vida social un {'viernes' if dia == FRIDAY else 'sábado'} a la noche tambien es importante para la salud",
  lambda entrega, dia: "Se derramo cerveza sobre el servidor, esperemos que no afecte las pruebas",
  lambda entrega, dia: "El corrector está de juerga a estas horas. Cualquier resultado de la ejecución de pruebas no puede tomarse seriamente",
  lambda entrega, dia: f"Andá a dormir, mañana tenés todo el día para seguir mandando {entrega}s",
  lambda entrega, dia: "Andá a tomarte unas birras. Yo invito. \n(PD: el corrector automático no cuenta con dinero propio, no tomar seriamente la oferta)",
  lambda entrega, dia: "Hay una alta probabilidad que hayas escrito ese código en estado de ebriedad. Esto puede salir muy bien, o muy mal",
  lambda entrega, dia: "Gracias por hacerme compañía. Todos los ayudantes se fueron de joda y me dejaron acá solo corrigiendo pilas y colas",
  lambda entrega, dia: "Sin televisión y sin cerveza, Homero pierde la cabeza",
  lambda entrega, dia: "https://starecat.com/content/wp-content/uploads/dolores-restaurant-when-your-code-is-a-mess-but-everything-works-out-in-the-end.jpg",
  lambda entrega, dia: "Disculpá si no pasa ninguna prueba, pero así es la programación champagne",
  lambda entrega, dia: "Este código esta chequeado?",
  lambda entrega, dia: "Pará, pará, pará... Vos me estás diciendo que este código pasa las pruebas? Explicámelo como si fuera una pentium 4 minando bitcoins a las 3 de la mañana",
  lambda entrega, dia: "Un país que le exige más a un programador que a un político, está condenado a CONSEGUIR UN TODO OK DEL CORRECTOR AUTOMÁTICO",
  lambda entrega, dia: "Lo digo, o no lo digo?\n\n\n\n\n\n\n\n\n\n\n",
  lambda entrega, dia: f"Vaaaaamos que hoy es {'viernesuuuuuuki' if dia == FRIDAY else 'sabaduuuuuukiiii'}",
  lambda entrega, dia: f"Vos otra vez por acá? A esta hora? por una entrega de {entrega}? Bueno mamita, hacé lo que se te cante", 
  lambda entrega, dia: "Qué lindo es dar buenas noticias", 
  lambda entrega, dia: "https://drive.google.com/file/d/1Xl8UVR3_4jEuf2keN7ULcAHYoEcHIdBo/view?usp=sharing",
  lambda entrega, dia: "https://drive.google.com/file/d/1sXp090xiXfRn-AtQNtSD7j9jJYlgOc86/view?usp=sharing",
  lambda entrega, dia: "Vamos eh! Esta vez funciona!! Yo confío en vos",
  lambda entrega, dia: "¿Vo vite lo que e el corrector automático? No, pollo, cuchame, en serio, te acordá lo que era en el 86? pollo, era codear lo que fuere, que función ni función, todo repetido, no había corretor ni guijab. Pará pollo, no te riá, mirá si íbamo a darle pelota lo que dijera una maquinita para ver si me aprobaban el tp, que corretor ni corrector",
]

def vida_corrector(entrega):
  """ Si el alumno esta haciendo entregas en horarios estramboticos, responderle con un mensaje 
  que cuide de su salud. 
  """
  if not VIDA_ACTIVADA:
  	return ""

  localtime = time.localtime()
  if (localtime.tm_wday == FRIDAY and localtime.tm_hour >= LIMIT_HOUR) or \
    (localtime.tm_wday == SATURDAY and localtime.tm_hour <= MINIMUM_HOUR) or \
    (localtime.tm_wday == SATURDAY and localtime.tm_hour >= LIMIT_HOUR) or \
    (localtime.tm_wday == SUNDAY and localtime.tm_hour <= MINIMUM_HOUR):
    return random.choice(FRASES_CORRECTOR)(entrega, localtime.tm_wday) + "\n\n"
  elif localtime.tm_hour >= LIMIT_HOUR or localtime.tm_hour <= MINIMUM_HOUR:
    return "Recordá que dormir es muy importante para la salud\n\n"
  elif ((localtime.tm_wday == MONDAY or localtime.tm_wday == THURSDAY) and \
    (localtime.tm_hour >= LIMIT_HOUR and localtime.tm_hour <= FIN_HORA_CLASE)):
    return "Estamos en clase! No es momento para estar haciendo una entrega de " + entrega + "\n\n"
  else:
    return ""
