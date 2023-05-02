import numpy as np

L4 = 0.2 # m
L3 = 0.2 # m
L2 = 0.2 # m
L_Beam = 0.9 # m



def calculate_piston_area(diam = 40):#mm
    '''
    Calculate the area of the piston
    diam: mm
    return: m^2
    '''
    areal = np.pi * (diam/2)*(diam/2)
    return areal/1000 # m^2 

def calculate_piston_force(pressure = 6, bBar= True): 
    '''
    Calculate the force of the piston
    pressure: Pascal, if bBar = True, then bar
    return: Newton
    '''
    if bBar:
        pressure = pressure * 100000

    area = calculate_piston_area()
    force = area * pressure
    return force


def calculate_force(theta, pressure, bBar): # rad
    
    """this function calculates that applied on the beam
    Args:
        theta (float): angle of the beam
        pressure (float): pressure of the piston
        bBar (bool): if pressure is in bar set to True, else False

    Returns:
        float: force in Newtons
    """
    force = 0.0

    # Calculate Theta 3
    theta2 = 180 - theta
    x_sq = L2**2 + L4**2 - 2*L2*L4*np.cos(theta2)
    theta3 = (L4**2 -x_sq -L2**2)/(-2*L2*np.sqrt(x_sq))
    theta3 = np.arccos(theta3)
    
    f_p = calculate_piston_force(pressure, bBar)
    force  = (f_p * L2* np.sin(theta3)) / (L_Beam *np.sin(theta))

    return force 


if __name__ == '__main__':

    angle = 90

    force = calculate_force(angle, 6, True)
    print("Force: ", force, "N")

