function [braking_distance, braking_time] = getBrakingInfoFromV(Initial_Speed)
    % Vehicle
    vehicle_Length          = 4.65;     % Length of the vehicle         [m]
    vehicle_Width           = 1.78;     % Width of the vehicle          [m]
    vehicle_Initial_Speed   = Initial_Speed/3.6;   % Initial speed of the vehicle  [m/s]

    vehicle_Mass            = 1145;     % Mass of the vehicle           [kg]
    vehicle_Area            = 2.5;      % Frontal area of the vehicle   [m2]
    vehicle_Cd              = 0.35;     % Drag coefficient              [-]
    air_Density             = 1;        % Air density                   [kg/m3]
    
    [braking_distance, braking_time]= getBrakingParameters(vehicle_Length, vehicle_Width, vehicle_Initial_Speed, vehicle_Mass, vehicle_Area, vehicle_Cd);
end


%% Vehicle braking to a stop
% Simulation and animation of a road vehicle braking to a stop with
% position, speed, acceleration and braking force plots.
%
%%

function [final_position,braking_time] = getBrakingParameters(vehicle_Length, vehicle_Width, vehicle_Initial_Speed, vehicle_Mass, Area, vehicle_Cd)
   % clear ; close all ; clc

    %% Scenario

    % Road
    road_Width              = 10;       % Road width                    [m]
    road_Margin             = 2;        % Road margin                   [m]
    air_Density             = 1;        % Air density                   [kg/m3]
    % Lumped air drag coefficient [N(s/m)2]
    C = 0.5 * Area * vehicle_Cd *air_Density;


    % Vehicle struct
    vehicle.C = C;
    vehicle.M = vehicle_Mass;

    % Parameters
    tf      = 100;                      % Final time                    [s]
    % OBS: tf must be larger than the stopping time.
    fR      = 30;                       % Frame rate                    [fps]
    dt      = 1/fR;                     % Time resolution               [s]
    TSPAN   = linspace(0,tf,tf*fR);     % Time                          [s]

    %% Braking force

    % Brake
    brake_Time_Constant     = 0.5;        % Brake time constant           [s]
    brake_Force_Max         = 5000;     % Brake max. force              [N]
    % Braking force during time span [N]
    FbBrakingForce          = brake_Force_Max*(1-exp(-brake_Time_Constant*TSPAN));

    % Brake struct
    brake.time  = TSPAN;
    brake.force = FbBrakingForce;

    %% Simulation

    % Initial conditions [position speed]
    Z0 = [0 vehicle_Initial_Speed];

    % Options:
    % Simulation ends when v=0 (See auxiliary function)
    options = odeset('events',@vehicleAtRest);
    % Integration
    [TOUT,ZOUT] = ode45(@(t,z) vehicle_braking_dynamics(t,z,vehicle,brake),TSPAN,Z0,options);

    % States
    vehicle_position    = ZOUT(:,1);
    vehicle_speed       = ZOUT(:,2);

    %test last_postition
    %size(vehicle_position)
    final_position  = vehicle_position(end);
    final_speed = vehicle_speed(end);
    braking_time = TOUT(end)
end

function dz = vehicle_braking_dynamics(t,z,vehicle,brake)

    % States
    % z1 = z(1);
    z2 = z(2);

    % Parameters
    C = vehicle.C;
    M = vehicle.M;

    % Brake force
    timeBraking  = brake.time;
    forceBraking = brake.force;
    Fb = interp1(timeBraking,forceBraking,t);

    % State Equations
    dz(1,1) = z2;
    dz(2,1) = -(Fb + C*z2^2)/M;

end

function [speed,isterminal,direction] = vehicleAtRest(~,z)
    speed       = z(2);
    isterminal  = 1;
    direction   = 0;
end
