import numpy as np

L4 = 0.389 # m
L2 = 0.524 # m
L_Beam = 0.755 # m

def deg_to_rad(deg):
    return deg * np.pi / 180

def calculate_piston_area(diam = 40):#mm
    """Calculates the area of the piston

    Args:
        diam (int, optional): _description_. Defaults to 40.

    Returns:
        folat: m^2	
    """
    diam = diam/ 1000
    areal = np.pi * (diam/2)*(diam/2)
    return areal # m^2 

def calculate_piston_force(pressure = 6, bBar= True): 
    """this function calculates the force applied on the piston
    Args:
        - pressure (float): pressure of the piston    [bar]
        - bBar (bool): if pressure is in bar set to True, else pascale
        
        Returns:
        float: force in [N]
        """
    force = 0.0
    if bBar:
        pressure = pressure* 100000

    area = calculate_piston_area()
    force = area * pressure
    return force


def calculate_force(theta, pressure, bBar): # rad
    
    """this function calculates the force and power applied on the beam
    Args:
        - theta (float): angle of the beam    [degrees]
        - pressure (float): pressure of the piston    [bar]
        - bBar (bool): if pressure is in bar set to True, else False

    Returns:
        float: force in Newtons
    """
    force = 0.0

    # Calculate Theta 3
    theta = deg_to_rad(theta)
    theta2 = np.pi - theta
    x_sq = L2**2 + L4**2 - 2*L2*L4*np.cos(theta2)
    theta3 = (L4**2 -x_sq -L2**2)/(-2*L2*np.sqrt(x_sq))
    theta3 = np.arccos(theta3)
    
    f_p = calculate_piston_force(pressure, bBar)
    
    force  = (f_p * L2* np.sin(theta3)) / (L_Beam *np.sin(theta))
    print("theta3: ", theta3)
    print("angle, theta3, force: ", angle, theta3, force)
    return force 

def calc_power(theta, theta_prev, time, pressure, bBar):
    
    """this function calculates the power applied on the beam
    Args:
        - theta (float): angle of the[degrees]
        - theta_prev (float): previous angle of the beam [degrees]
        - time (float): time between the two angles   [seconds]
        - pressure (float): pressure of the piston [bar]
        - bBar (bool): if pressure is in bar set to True, else False [bool]
        
        Returns:
        float: work in [Joules]
        float: power in [Watts]
    """

    power = 0.0
    work = 0.0
    theta = deg_to_rad(theta)
    theta2 = np.pi - theta
    x = np.sqrt(L2**2 + L4**2 - 2*L2*L4*np.cos(theta2))

    theta_prev = deg_to_rad(theta_prev)
    theta2_prev = np.pi - theta_prev
    x_prev = np.sqrt(L2**2 + L4**2 - 2*L2*L4*np.cos(theta2_prev))

    delta_x =  x_prev -x
    f_p = calculate_piston_force(pressure, bBar)
    
    work = f_p * delta_x
    power = work/time # Watts

    return work, power


if __name__ == '__main__':

    angle = 4
    prev_angle = 1
    pressure = 6
    dt = 2/50   
    
    force = calculate_force(angle, pressure, True)
    work, power = calc_power(angle, prev_angle, dt, pressure, True)
    
    force_list = []
    power_list = []
    work_list = []
    prev_angle = 69
    for angle in range(70, 120):
        force = calculate_force(angle, pressure, True)
        work, power = calc_power(angle, prev_angle, dt, pressure, True)
        work_list.append(work)
        power_list.append(power)
        force_list.append(force)
        prev_angle = angle


    import matplotlib.pyplot as plt
    # three subplots sharing both x/y axes
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)
    ax1.plot(force_list)
    ax1.set_title('Force')
    ax2.plot(work_list)
    ax2.set_title('Work')
    ax3.plot(power_list)
    ax3.set_title('Power')
    plt.xlabel('Angle [degrees]')
    
    plt.show()


    #print("Force: ", force, "N")
    #print("Work: ", work, "J")
    #print("Power: ", power, "W")

