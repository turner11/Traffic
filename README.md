# Traffic

A demonstration of connecting to real life traffic camers and monitoring traffic (detection + tracking).  

The story behind this project is that as [good developer](https://www.techinasia.com/talk/3-great-virtues-of-a-programmer-laziness-impatience-and-hubris),  [@coffeelover82](https://github.com/coffeelover82) got impatient with the traffic light on his way to work, that without any apparent good reason made him wait every day at 5:00 AM while no other cars were to be seen.   
Being the fineshmaker that he is, he decided to get back at that damn traffic light, and optimze traffic lights world wide.  
This project is the the work in progress of this effort.  

![](media/example.gif)

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

You will be asked to choose a camera from a list.

You can also pass the camera as an argument:
```
cd path/to/repo
python play.py -c 70
```

Or specify location of an existing local video file:
```
cd path/to/repo
python play.py -c /path/to/video/file.avi
```

#### Commands
While viewing the stream, the following commands are available:  
**s** - For tracking a specific region of interest.  
**q** - For closing the window.  
