"# AgeOfVisionLearning" 

This is a fresh Deep Learning project for Age of Empires II.
We want to replace all textures ingame (done) for color-coded figures, creating an easy-readible game display. Second step is to read the screen fast (Every < 0.3s) and get the position of all units/buildings in pixel-coordinates (done).
Third step is transform pixel positions to Ingame-Coordinates (absolute Map-Coordinates) by reading the position of the screen in the Minimap.
This will be the input for a Reinforcement-Learning algorithm, which will take Actions according to the current State, trying to maximize the Score.
