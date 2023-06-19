# Ogir-Runner
Repository for my first game project: working title is OgirRun

This game was made following a YouTube tutorial : https://www.youtube.com/watch?v=AY9MnQ4x3zk
Here I a list of the changes;  

1. Changed the player images and background to a sci-fi Mars theme. 
2. Speed of enemies is now a gradual increase starting off slow and increasing as score gets higher. 
3. Adjusted rectangles to be smaller since collision detection was too sensitive: The player was triggering a hit before visible contact with enemy. 
   Also added a single variable to adjust floor level in player class
4. Created a list of backgrounds and added scrolling sky and walls function. 
   The speed on the sky background transition is a percentage of the score speed. 
   The background consists of multiple mars sky images 
   Got backgrounds from https://opengameart.org/art-search?keys=sci+fi+wall
   The scroll_wall function is called when the sky background images are changing to obscure the change. 
   I also updated the ground scrolling function to be more efficient.
   Increased speed and speed change to make game faster paced 
