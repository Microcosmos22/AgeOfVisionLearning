"# AgeOfVisionLearning" 

This is a fresh Deep Learning project for Age of Empires II.
We want to replace all textures ingame (done) for color-coded figures, creating an easy-readible game display. Second step is to read the screen fast (Every < 0.3s) and calculate the position of all units/buildings in pixel-coordinates (done).
Third step is calculating the position of all active units/buildings in Ingame-Coordinates (absolute Map-Coordinates).
This will be the input for a Deep-Learning algorithm, which will take actions every timestep (<0.3s). At the end of the game it will evaluate all taken (Status, Action) pairs and evaluate to train the algorithm.

