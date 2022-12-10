# Rover_Search_And_Return
## Description:

For at least three decades, scientists have advocated the return of geological samples from Mars. One early 
concept was the Sample Collection for Investigation of Mars (SCIM) proposal, which involved sending a 
spacecraft in a grazing pass through Mars's upper atmosphere to collect dust and air samples without 
landing or orbiting.
As of late 1999, the MSR mission was anticipated to be launched from Earth in 2003 and 2005. Each was to 
deliver a rover and a Mars ascent vehicle, and a French supplied Mars orbiter with Earth return capability 
was to be included in 2005. Sample containers orbited by both MAVs were to reach Earth in 2008. This 
mission concept, considered by NASA's Mars Exploration Program to return samples by 2008, was cancelled 
following a program review

![image](https://user-images.githubusercontent.com/88388782/206855025-a35b4c66-6fa6-4c69-a2a8-7ffa21a13088.png)

In this project, we’ll do computer vision for robotics.We are going to build a Sample & Return Rover in 
simulation. Mainly, we’ll control the robot from images streamed from a camera mounted on the robot. The 
project aims to do autonomous mapping and navigation given an initial map of the environment. 
Realistically speaking, the hard work is done now that you have the mapping component! You will have the 
option to choose whether to send orders like the throttle, brake, and steering with each new image the 
rover's camera produces.

## Phase I Requirements:

1. Your pipeline should be able to map at least 40% of the environment at 60% fidelity.<br>
    It should repaint the map image to distinguish between navigable terrain, obstacles and rock samples.<br>
    
2. You’re required to locate at least one rock in the environment.<br>

3. You should also implement debugging mode where each step of your pipeline is 
  illustrated with the vehicle operation.<br>
## Project Walkthrough  
<a href="https://www.youtube.com/watch?v=KgOsW1BRLDo">Project WalkThrough Video </a>

## Results:

[Demo](https://drive.google.com/file/d/17WQwoDwrEGJ0lwJeK-VyCjucjPP-Kiec/view)

![image](https://user-images.githubusercontent.com/88388782/206856298-4b364c6c-248e-4b90-84fa-b054d9ac2d3b.png)

## Contributers:
<table>
  <tr>
    <th>Name</th>
    <th>Id</th>
  </tr>
  <tr>
    <td>Ahmed Elsayed Rashad Mohamed</td>
    <td>1900730</td>
  </tr>
  <tr>
    <td>Nada Amin Abdelsattar Ali</td>
    <td>1900594</td>
  </tr>
  
  <tr>
    <td>Heba Mahmoud Abd Elhafez Bakry</td>
    <td>1900402</td>
  </tr>
  
  <tr>
    <td>Jumana Emad Eldin Saleh Mohamed Elhak</td>
    <td>1900980</td>
  </tr>
  
  <tr>
    <td>Mariam samir wassef</td>
    <td>1900313</td>
  </tr>
  
</table>

## How To Run The Code
1. Download Simulator [Linux](https://s3-us-west-1.amazonaws.com/udacity-robotics/Rover+Unity+Sims/Linux_Roversim.zip)
2. Clone The Repo 
3. Create A new Environment 
4. Download Dependencies [RoboND-Python-Starterkit](https://github.com/ryan-keenan/RoboND-Python-Starterkit)
5. Run drive_rover.py File
6. open the simulator and **Select Autonomous Mode**
7. Enjoy! 😉
