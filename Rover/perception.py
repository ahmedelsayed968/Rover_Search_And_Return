import numpy as np
import cv2

# Define a function to perform a perspective transform
# I've used the example grid image above to choose source points for the
# grid cell in front of the rover (each grid cell is 1 square meter in the sim)
# Define a function to perform a perspective transform
def perspect_transform(img, src, dst):
    M = cv2.getPerspectiveTransform(src, dst)
    mask=cv2.warpPerspective(np.ones_like(img[:,:,0]),M, (img.shape[1],img.shape[0]))
    warped = cv2.warpPerspective(img, M, (img.shape[1], img.shape[0]))
    
    return warped,mask

dst = 3
bottom_offset = 5
source = np.float32([[14, 140],
                     [300, 140],
                     [200, 95],
                     [120, 95]])

destination = np.float32([[image.shape[1] / 2 - dst, image.shape[0] - bottom_offset],
                          [image.shape[1] / 2 + dst, image.shape[0] - bottom_offset],
                          [img.shape[1] / 2 + dst, image.shape[0] - 2*dst - bottom_offset],
                          [img.shape[1] / 2 - dst, image.shape[0] - 2*dst - bottom_offset]])


warped, mask = perspect_transform(rock_img, source, destination)
fig=plt.figure(figsize=(12,3))
plt.subplot(121)
plt.imshow(warped)
plt.subplot(122)
plt.imshow(mask,cmap='gray')
#scipy.misc.imsave('../output/warped_example.jpg', warped)
# Identify pixels above the threshold
# Threshold of RGB > 160 does a nice job of identifying ground pixels only
def find_navigable(img, rgb_thresh=(150, 150, 150)):
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:, :, 0])
    #boolean array
    above_thresh = (img[:, :, 0] > rgb_thresh[0]) \
                  & (img[:, :, 1] > rgb_thresh[1]) \
                  & (img[:, :, 2] > rgb_thresh[2])
    # Index the array of zeros with the boolean array and set to 1
    color_select[above_thresh] = 1
    return color_select


def find_rock(img, rgb_thresh=(110, 110, 50)):
    #boolean array
    thresh = (img[:, :, 0] > rgb_thresh[0]) \
          & (img[:, :, 1] > rgb_thresh[1]) \
          & (img[:, :, 2] < rgb_thresh[2])
    # Create an array of zeros same xy size as img, but single channel
    color_select = np.zeros_like(img[:, :, 0])
    # Index the array of zeros with the boolean array and set to 1
    color_select[thresh] = 1
    return color_select


# Define a function to convert from image coords to rover coords
def rover_coords(binary_img):
    # Identify nonzero pixels
    ypos, xpos = binary_img.nonzero()
    # Calculate pixel positions with reference to the rover position being at the 
    # center bottom of the image.  
    x_pixel = -(ypos - binary_img.shape[0]).astype(np.float)
    y_pixel = -(xpos - binary_img.shape[1]/2 ).astype(np.float)
    return x_pixel, y_pixel


# Define a function to convert to radial coords in rover space
def to_polar_coords(x_pixel, y_pixel):
    # Convert (x_pixel, y_pixel) to (distance, angle) 
    # in polar coordinates in rover space
    # Calculate distance to each pixel
    dist = np.sqrt(x_pixel**2 + y_pixel**2)
    # Calculate angle away from vertical for each pixel
    angles = np.arctan2(y_pixel, x_pixel)
    return dist, angles

# Define a function to map rover space pixels to world space
def rotate_pix(xpix, ypix, yaw):
    # Convert yaw to radians
    yaw_rad = yaw * np.pi / 180
    xpix_rotated = (xpix * np.cos(yaw_rad)) - (ypix * np.sin(yaw_rad))
                            
    ypix_rotated = (xpix * np.sin(yaw_rad)) + (ypix * np.cos(yaw_rad))
    # Return the result  
    return xpix_rotated, ypix_rotated

def translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale): 
    # Apply a scaling and a translation
    xpix_translated = (xpix_rot / scale) + xpos
    ypix_translated = (ypix_rot / scale) + ypos
    # Return the result  
    return xpix_translated, ypix_translated


# Define a function to apply rotation and translation (and clipping)
# Once you define the two functions above this function should work
def pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale):
    # Apply rotation
    xpix_rot, ypix_rot = rotate_pix(xpix, ypix, yaw)
    # Apply translation
    xpix_tran, ypix_tran = translate_pix(xpix_rot, ypix_rot, xpos, ypos, scale)
    # Perform rotation, translation and clipping all at once
    x_pix_world = np.clip(np.int_(xpix_tran), 0, world_size - 1)
    y_pix_world = np.clip(np.int_(ypix_tran), 0, world_size - 1)
    # Return the result
    return x_pix_world, y_pix_world

def perception_step(Rover):
    # Perform perception steps to update Rover()
    # TODO: 
    # NOTE: camera image is coming to you in Rover.img
    # 1) Define source and destination points for perspective transform
    # 2) Apply perspective transform
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    threshed = find_navigable(warped)
    obs_map = np.absolute(np.float32(threshed)-1)*mask
    navigable_terrain = find_navigable(warped)
    obstacle = np.absolute(np.float32(navigable_terrain)-1)*mask
    rock_sample = find_rock(warped)

    # 4) Update Rover.vision_image (this will be displayed on left side of screen)
    # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
    #          Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
    #          Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image
    warped[:, :, 0] = obstacle * 255
    warped[:, :, 1] = rock_sample * 255
    warped[:, :, 2] = navigable_terrain*255
    Rover.vision_image[:, :, 0] = warped[:, :, 0]
    Rover.vision_image[:, :, 1] = warped[:, :, 1]
    Rover.vision_image[:, :, 2] = warped[:, :, 2]
    
    # 5) Convert map image pixel values to rover-centric coords
    yaw = Rover.yaw

    xpix, ypix = rover_coords(navigable_terrain)
    xpos = Rover.pos[0]
    ypos = Rover.pos[1]
    x_pixel_rocks, y_pixel_rocks = rover_coords(rock_sample)
    x_pixel_obstacles, y_pixel_obstacles = rover_coords(obstacle)
    # 6) Convert rover-centric pixel values to world coordinates
    world_size = Rover.worldmap.shape[0]
    scale = 2 * dst_size
    x_world, y_world = pix_to_world(xpix, ypix, xpos, ypos, yaw, world_size, scale)
    obsxpix, obsypix = rover_coords(obs_map)
    obs_x_world, obs_y_world = pix_to_world(obsxpix, obsypix, xpos, ypos, yaw, world_size, scale)
    
    # 7) Update Rover worldmap (to be displayed on right side of screen)
    # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
    #          Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
    #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    Rover.worldmap[y_world, x_world, 2] = 255
    Rover.worldmap[obs_y_world, obs_x_world, 0] = 255
    nav_pix = Rover.worldmap[:, :, 2] > 0
    Rover.worldmap[nav_pix, 0] = 0

    rock_map = find_rock(warped)
    if rock_map.any():
        rock_x, rock_y = rover_coords(rock_map)
        rock_x_world, rock_y_world = pix_to_world(
            rock_x, rock_y, xpos, ypos, yaw, world_size, scale)

        Rover.worldmap[rock_y_world, rock_x_world, :] = 255
        
    # 8) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
    # Rover.nav_dists = rover_centric_pixel_distances
    # Rover.nav_angles = rover_centric_angles
    distance_nav, nav_angle = to_polar_coords(xpix, ypix)
    Rover.nav_dists = distance_nav
    Rover.nav_angles = nav_angle

    dist, angles = to_polar_coords(x_pixel_rocks, y_pixel_rocks)
    Rover.samples_dists = dist
    Rover.samples_angles = angles
    
 

    
    return Rover
