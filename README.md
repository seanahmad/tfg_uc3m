![alt text](img/logo.jpg)
# TFG UC3M

##_v1.0.0_

### Tarea principal: Detección de semáforos y clasificación
Dataset: Lisa y/o Bosch
Stack: Pytorch con PyCharm como IDE. En principio en local para pruebas, luego con integración con GCP (https://www.jetbrains.com/devops/google-cloud/)

Descripción: Implementar SSD en pytorch; no necesariamente de cero, mejor usar como base algún repo de github (https://github.com/amdegroot/ssd.pytorch, https://github.com/qfgaohao/pytorch-ssd, https://github.com/lufficc/SSD, https://github.com/ShuangXieIrene/ssds.pytorch, https://github.com/ecr23xx/ssd.pytorch, https://github.com/mehdidc/ssd-pytorch, https://github.com/kweisamx/SSD-PyTorch, https://github.com/lxtGH/SSD-pytorch, https://github.com/kuangliu/pytorch-ssd, https://github.com/detectRecog/ssd-pytorch).

Implementar retinanet en pytorch, igual, con un repo base (https://github.com/yhenon/pytorch-retinanet, https://github.com/kuangliu/pytorch-retinanet, https://github.com/qqadssp/RetinaNet-Pytorch).

Implementar Faster R-CNN en pytorch etc (https://github.com/jwyang/faster-rcnn.pytorch, https://github.com/chenyuntc/simple-faster-rcnn-pytorch, https://medium.com/@fractaldle/guide-to-build-faster-rcnn-in-pytorch-95b10c273439).

Analizar y comparar los resultados obtenidos y su rendimiento bajo arquitectura resnet y mobilenet. El objetivo es conseguir algo rápido, todo lo que supere los 50ms es una puta mierda. Las soluciones posibles serían limitar las capas o disminuir el tamaño de la imagen.

#### Create virtualenv
This is required once before installing dependencies
```
virtualenv -p python3.6 venv
```
#### Activate virtualenv
This is required before installing dependencies or running the project.
```
source venv/bin/activate
```
Once virtualenv is activated, your prompt will change. To deactivate it, run
```
deactivate
```
#### Install dependencies
With virtualenv enabled, run
```
pip install -r requirements.txt
```
#### Run the Project
With virtualenv enabled, run
```
python main.py
```
