# Traffic

A demonstration of connecting to real life traffic camers and monitoring traffic (detection + tracking).  

## Main Dependencies
1. [open cv](https://github.com/skvark/opencv-python)
2. [yolo](https://pjreddie.com/darknet/yolo/)
3. [RxPY](https://github.com/ReactiveX/RxPY)

All requierements are available in [Pipfile](https://github.com/turner11/Traffic/blob/master/Pipfile)

## Setting up

To install required dependencies run:
```
cd path/to/repo
pipenv install 
```

For downloading pre trained yolo weights run the[setup.py](https://github.com/turner11/Traffic/blob/master/settings/setup.py)

## Code execution:
For running the code run [play.py](https://github.com/turner11/Traffic/blob/master/play.py)
```
cd path/to/repo
python play.py
```

You will be asked to choose a camera from a list. You can also pass the camera as an argument:
```
cd path/to/repo
python play.py -c 70
```

#### Commands:
*s* - For tracking a specific region of interest.  
*q* - For closing the window.  
