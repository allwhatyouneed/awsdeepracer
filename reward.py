def reward_function(params):
    # Read input parameters
    all_wheels_on_track = params['all_wheels_on_track']
    distance_from_center = params['distance_from_center']
    progress = params['progress']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    track_width = params['track_width']
    is_left_of_center = params['is_left_of_center']
    speed = params['speed']
    steering = abs(params['steering_angle'])
    steps = params['steps']
    track_length = params['track_length']

    # Define reward parameters
    center_weight = 0.7  # Weight for staying close to center line
    distance_reward_weight = 0.3  # Weight for covering the longest distance
    lap_time_weight = 0.1  # Weight for beating own lap time

    # Initialize reward
    reward = 0

    # Reward for staying close to center line
    if all_wheels_on_track and distance_from_center <= (0.5 * track_width):
        reward += center_weight
    else:
        reward -= 1

    # Reward for covering the longest distance
    # Calculate distance from current waypoint to the next waypoint
    next_waypoint = waypoints[closest_waypoints[1]]
    prev_waypoint = waypoints[closest_waypoints[0]]
    track_direction = math.atan2(next_waypoint[1] - prev_waypoint[1], next_waypoint[0] - prev_waypoint[0])
    # Calculate angle between current heading and track direction
    heading = params['heading']
    track_heading = track_direction - heading
    # Calculate angle difference
    if abs(track_heading) > math.pi:
        track_heading -= math.pi * 2
    # Reward for covering the longest distance
    reward += distance_reward_weight * abs(track_heading)

    # Reward for beating own lap time
    # Calculate lap time based on progress and total steps
    current_lap_time = (steps / progress) * track_length
    best_lap_time = params['best_lap_time']
    # If current lap time is better than best lap time, reward
    if current_lap_time < best_lap_time:
        reward += lap_time_weight

    return float(reward)
