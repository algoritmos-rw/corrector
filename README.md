### “Worker” para pruebas de la cátedra, v3: _less is more_

Este rama contiene una Github Action que corre `make -k` con las dependencias especificadas en el archivo packages.txt. Se usa desde algo2_skel para correr las pruebas cada vez que se cambian.

El antiguo `corrector.py` fue [integrado][i1] en [el sistema de entregas][algo2_entregas]; `worker.py` sigue existiendo en la rama _master_, y también fue [integrado][i2] en [dato/sisyphus].

[dato/sisyphus]: https://github.com/dato/sisyphus
[algo2_entregas]: https://github.com/algoritmos-rw/algo2_sistema_entregas
[i1]: https://github.com/algoritmos-rw/algo2_sistema_entregas/commit/6eb674b46e
[i2]: https://github.com/dato/sisyphus/commit/0703e9cf22b6142330d1b415a1b06796f

### Pasos para agregar un lenguaje: 

* Actualizar `packages.txt`
* Revisar el `Dockerfile` en caso de necesitarse algo extra (i.e. librerías)
* Mandar PR contra esta rama (`v3`)
* [Esperar a que termine de buildearse la imagen](https://github.com/algoritmos-rw/corrector/actions)
* Mergear PR y esperar a que buildee nuevamente. 
* Ingresar en el server del corrector y ejecutar: 

	```
	sudo docker pull algoritmosrw/corrector:v3
	cd /srv/algo2/corrector/repo/worker
	sudo docker build -t algoritmosrw/corrector .
	```

Eventualmente no será más necesario el último comando, y en vez de `:v3` será a latest, pero por ahora se mantiene así. 
