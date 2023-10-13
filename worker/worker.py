#!/usr/bin/env python3

"""Worker para el corrector automático.

El script:

  • recibe por entrada estándar un archivo en formato TAR con todos los
    archivos de la corrección:

      ⁃ "orig": el código del alumno, tal y como se recibió
      ⁃ "skel": el código base del TP, incluyendo pruebas públicas
      ⁃ "priv": pruebas privadas al corrector

  • ejecuta el corrector especificado con --corrector e imprime el
    resultado por salida estándar.

  • si hubo errores de ejecución (no de corrección), termina con estado de
    salida distinto de cero.
"""

import argparse
import pathlib
import os
import signal
import subprocess
import sys
import tarfile
import tempfile
import traceback
import sys

from java import CorregirJava

class ErrorAlumno(Exception):
  pass


class ProcessGroup(subprocess.Popen):
  """Creates processes in a new session, and sends signals to it.
  """
  def __init__(self, *args, **kwargs):
    kwargs["start_new_session"] = True
    super().__init__(*args, **kwargs)

  def send_signal(self, sig):
    pgid = os.getpgid(self.pid)
    os.killpg(pgid, sig)


class CorregirV2:
  """Corrector compatible con la versión 2.

  Sobreescribe en la entrega del alumno los archivos del esqueleto,
  e invoca a make.
  """
  def __init__(self, path):
    path = pathlib.Path(path)
    orig = path / "orig"
    skel = path / "skel"
    badmake = {"makefile", "GNUmakefile"}.intersection(
        p.name for p in orig.iterdir())

    if badmake:
      name = badmake.pop()
      raise ErrorAlumno(f"archivo ‘{name}’ no aceptado; solo ‘Makefile’")

    for file in orig.iterdir():
      dest = skel / file.name
      if not dest.exists():
        file.rename(dest)

    self.cwd = skel

  def run(self, timeout):
    msg = "ERROR"
    cmd = ProcessGroup(["make", "-k"], cwd=self.cwd, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
      output, _ = cmd.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
      cmd.kill()  # Will cleanup all children thanks to ProcessGroup above.
      msg = ("ERROR\n\n"
             "La última prueba mostrada tardó demasiado y no finalizó en el\n"
             "espacio de {} segundos; ya no se ejecutó el resto de pruebas."
             .format(timeout))
      output, _ = cmd.communicate()

    print("Todo OK" if cmd.returncode == 0 else msg,
          output.decode("utf-8", "replace"), sep="\n\n", end="")


CORRECTORES = {
    "v2": CorregirV2,
    "java": CorregirJava,
}


def ejecutar(corrector, timeout):
  """Función principal del script.
  """
  with tempfile.TemporaryDirectory(prefix="corrector.") as tmpdir:
    # Usamos sys.stdin.buffer para leer en binario (sys.stdin es texto).
    # Asimismo, el modo ‘r|’ (en lugar de ‘r’) indica que fileobj no es
    # seekable.
    with tarfile.open(fileobj=sys.stdin.buffer, mode="r|") as tar:
      def is_within_directory(directory, target):
          
          abs_directory = os.path.abspath(directory)
          abs_target = os.path.abspath(target)
      
          prefix = os.path.commonprefix([abs_directory, abs_target])
          
          return prefix == abs_directory
      
      def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
      
          for member in tar.getmembers():
              member_path = os.path.join(path, member.name)
              if not is_within_directory(path, member_path):
                  raise Exception("Attempted Path Traversal in Tar File")
      
          tar.extractall(path, members, numeric_owner=numeric_owner) 
          
      
      safe_extract(tar, tmpdir)

    signal.alarm(timeout + 5)
    try:
      corrector(tmpdir).run(timeout)
    except Timeout:
      # Cada corrector debería comprobar el tiempo, pero este es un error
      # genérico de última instancia.
      raise ErrorAlumno(f"El proceso tardó más de {timeout + 5} segundos")
    finally:
      # Añadir un segundo timeout para asegurar que ningún código restante
      # de ejecutar() —por ejemplo, tmpdir.cleanup()— pueda colgar al worker.
      signal.alarm(timeout // 2)


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument("--timeout", type=int, default=120,
                      help="tiempo máximo de ejecución en segundos")

  parser.add_argument("--corrector", type=str, choices=list(CORRECTORES),
                      help="corrector (lenguaje) a usar", default="v2")

  args = parser.parse_args()
  try:
    ejecutar(CORRECTORES[args.corrector], args.timeout)
  except ErrorAlumno as ex:
    print("ERROR: {}.".format(ex))
  except Timeout as ex:
    print("\n" "Aviso: se realizó la corrección, pero el "
          "sistema demoró en retornar la respuesta:\n")
    traceback.print_tb(ex.__traceback__, file=sys.stdout)


##

class Timeout(Exception):
  """Excepción para nuestra implementación de timeouts.
  """

def raise_timeout(unused_signum, unused_frame):
  """Lanza nuestra excepción Timeout.
  """
  raise Timeout

signal.signal(signal.SIGALRM, raise_timeout)

##

if __name__ == "__main__":
  main()

# vi:et:sw=2
