# Self-Driving-Car

This project is base on Udacity's Self-Driving Car Simulator.

![sdccar](https://user-images.githubusercontent.com/31696557/39665376-bb419dd4-50b0-11e8-83b4-e85b2eec666b.jpg)

## How it is going to look(Video) !

[![](http://img.youtube.com/vi/UmtLtpY1XBs/0.jpg)](https://www.youtube.com/watch?v=UmtLtpY1XBs "SDC")


## Dependencies

You can install depedencies by running the following command in Anaconda prompt:

```
# OpenCV
conda install -c conda-forge opencv

# Theano
conda install mingw libpython
conda install mkl=2017.0.3

# Keras
pip install keras
```

After installing all the dependencies, Change the backend of the Keras to "theano".<br/>
For that, Go to C:\Users\YourSystemName\.keras and open Kersas.json file.<br/>
Change the backend to "thenao".<br/>
It would look something like this:
```
{
    "backend": "theano",
    "image_data_format": "channels_last",
    "floatx": "float32",
    "epsilon": 1e-07
}
```

Also, you need to have Unity3D game engine, which can be downloaded from [here](https://unity3d.com/) and install it.

To install Tensorflow, follow this Youtube video:

[![Install Tensorflow-GPU in 5 mins - EASY!!](http://img.youtube.com/vi/tPq6NIboLSc/0.jpg)](http://www.youtube.com/watch?v=tPq6NIboLSc "Install Tensorflow-GPU in 5 mins - EASY!!")

### Steps
1. Create an env. <Br/>
```conda create -n tensorflow_gpu python=3.7```

2. Activate the env<Br/>
```conda activate tensorflow_gpu```

3. Install jupyter beforehand (since it downgrade the tensorflow version, if it is executed after tensorflow has been installed)<Br/>
```conda install -c anaconda jupyter```

4. Install the kernel<Br/>
```pip install ipykernel```<Br/>
```python -m ipykernel install --user --name tensorflow_gpu --display-name "tensorflow_gpu"```

6. Install tensorflow gpu<Br/>
```conda install -c anaconda tensorflow-gpu```

7. And, finally, install Keras<Br/>
```pip install keras```

## Working with Unity3D Game Engine.
1) Launch Unity3D Game Engine.
2) Select "Open Project", select "Self Driving Car", from this project.
3) Your project will open in Unity3D.

## Workflow

This project is divided into three parts:

1) Data Generation.
2) Training the data.
3) Testing.

### Data Generation

In Unity3D simulator environment, we drive the car manually, using keyboard or joystick, and simulataneously, captures the frames or image, using python PIL library through Anaconda’s Spyder, and accessing their associated Steering Angle, Throttle, Velocity, and sending these values and storing it in a CSV file, along with the images.

#### How To:
1) In "DataGeneration.py" file, change the directory, where the csv file is going to be saved.
2) In "DataGeneration.py" file, change the directory, where all your images will be going to be saved.
3) In Unity3D simulator, in Hierarchy, select car, and then in Inspector, under "Car user Control" script, check Generate Data, and uncheck Drive Car.<br/>
![car generatecar inspector](https://user-images.githubusercontent.com/31696557/39665840-c4405090-50b7-11e8-9e4f-d74937a0ca8c.png)
4) In Unity3D simulator, in Hierarchy, select Network, in Inspector, active(or check) "Network Data Gen" script, and inactive(uncheck) "Network Con" script.<br/>
![network datagen inspector](https://user-images.githubusercontent.com/31696557/39665856-ff1e5144-50b7-11e8-94e1-97ce57a7fe14.png)
5) Run the simulator in unity3D, then run the program "DataGeneration.py" from spyder. Drive the car manually using keyboard or JoyStick.

### Train the data

First, the data saved in CSV file is loaded, and image processing is done. In Image processing, the size of the mage is decreased. The actual size was (420, 750) , which was actually very big. It’s size was reduced to (66, 200). Then, the images, and Steering Angle are splitted into training and validation datasets, so that we can use some data for training, and some data for testing.
Then, we apply series of Convolutional Neural Networks on image training datasets, followed by training the model, using Mean Squared Error loss function. This will create several “.h5” files, which we will be used for testing.

#### How To:
1) Just run the script, "TrainCNN.py".

### Testing

First, image is captured and current steering angle, throttle, and velocity from Unity3D simulator is send over to the socket TCP connection to the Spyder. The image is processed, reducing its size to (66, 200). Then we predict the Steering Angle on the basis of the image, and corresponding throttle value is calculated from the equation. This Steering Angle and Throttle is send back to the Unity3D simulator, and applies to the car, which starts driving by itself. Then again, image is captured, steering angle, throttle, and velocity is send back to the Spyder, and it goes on. It captures the frames(or an image) at 5 frames per seconds.

#### How To:
1) In "Drive.py" file, change the directory, to load the model, which was created by training the data in TrainCNN.py.
2) Next, change the directory of "filename", where all current data in a CSV file will be going to be saved.
3) And then, change the directory of "path", where all the current images will be going to be saved.
4) In Unity3D simulator, in Hierarchy, select car, and then in Inspector, under "Car user Control" script, check Drive Car, and uncheck Generate Data.<br/>
![car drivecar inspector](https://user-images.githubusercontent.com/31696557/39666518-7f06294a-50c2-11e8-92f8-5ff9fa3b3d04.png)
5) In Unity3D simulator, in Hierarchy, select Network, in Inspector, active(or check) "Network Con" script, and inactive(uncheck)  "Network Data Gen" script.<br/>
![network drivecar inspector](https://user-images.githubusercontent.com/31696557/39666523-a9b2b9ba-50c2-11e8-8c55-45d0b2c3be2e.png)
6) Run the simulator in unity3D, then run the program "Drive.py" from spyder. Car will start driving by itself.

### Caution!
Before running the codes, try to change the path of each files and images.

### More Information:
To know more about Convolutional Neural Network, check [this](https://adeshpande3.github.io/A-Beginner%27s-Guide-To-Understanding-Convolutional-Neural-Networks/) github page.<br/>
Check [this](https://images.nvidia.com/content/tegra/automotive/images/2016/solutions/pdf/end-to-end-dl-using-px.pdf) and [this](http://cs231n.stanford.edu/reports/2017/pdfs/626.pdf) for Self Driving Car.
