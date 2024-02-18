from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import utils


totalNumberOfCustomers = 0

def createDistanceMatrix(customerList):
    global totalNumberOfCustomers            
    customers = {}
    customers[0] = (0, 0) # adding depot
    for c in customerList:        
        customers[c.id] = (c.xCoord, c.yCoord)
    totalNumberOfCustomers = len(customers)-1
    print(customers)
    distanceMatrix = [[0 for x in range(len(customers))] for y in range(len(customers))]
    for i, icust in enumerate(customers):
        for j, jcust in enumerate(customers):
            distanceMatrix[i][j] = int(utils.calculateDistance(customers[icust], customers[jcust]))
    return distanceMatrix

def createTimewindows(customerList):
    timeWindows = []
    timeWindows.append((0,0))
    for c in customerList:
        if c.deliveryWindows:
            timeWindows.append((c.deliveryWindows[0][0].hour*60+c.deliveryWindows[0][0].minute, c.deliveryWindows[0][1].hour*60+c.deliveryWindows[0][1].minute))
        else:
            timeWindows.append((c.time.hour*60+c.time.minute, c.time.hour*60+c.time.minute))
    return timeWindows

def createDataModel(customerList):
    data = {}
    data['distance_matrix'] = createDistanceMatrix(customerList)
    data['time_windows'] = createTimewindows(customerList)
    data['num_vehicles'] = 1
    data['depot'] = 0
    data['penalty'] = 10000
    return data

def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    time_dimension = routing.GetDimensionOrDie('Time')
    total_time = 0
    total_served = 0
    total_distance = 0
    service_time = 12
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        while not routing.IsEnd(index):
            time_var = time_dimension.CumulVar(index)
            if solution.Max(time_var) - solution.Min(time_var) >= service_time:
                plan_output += '{0} Time({1},{2}) -> '.format(
                manager.IndexToNode(index), solution.Min(time_var), solution.Max(time_var))
            else:
                plan_output += '{0} Time({1},{2}) -> '.format(
                    manager.IndexToNode(index), solution.Min(time_var), solution.Max(time_var)+service_time)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            total_served+=1
        time_var = time_dimension.CumulVar(index)
        plan_output += '{0} Time({1},{2})\n'.format(manager.IndexToNode(index),
                                                    solution.Min(time_var),
                                                    solution.Max(time_var))
        plan_output += 'Time of the route: {}min\n'.format(
            solution.Min(time_var))
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        print(plan_output)
        total_time += solution.Min(time_var)
        total_distance += route_distance
        total_served -= 1 # subtract 1 node because of the depot
    total_h = int(total_time/60)
    total_min = int(total_time-total_h*60)
    print('Total time of all routes: {}h {}min ({}min)'.format(total_h, total_min, total_time))
    print('Total number of served customers: {}/{}'.format(total_served, totalNumberOfCustomers))
    print('Total distance of all routes: {}m'.format(total_distance))


def solve(customerList):
    data = createDataModel(customerList)
    
    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def time_callback(from_index, to_index):
        """Returns the travel time between the two nodes."""
        # Convert from routing variable Index to time matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Add Time Windows constraint.
    time = 'Time'
    routing.AddDimension(
        transit_callback_index,
        9999999,  # allow waiting time
        9999999,  # maximum time per vehicle
        False,  # Don't force start cumul to zero.
        time)
    time_dimension = routing.GetDimensionOrDie(time)
    # Add time window constraints for each location except depot.
    for location_idx, time_window in enumerate(data['time_windows']):
        if location_idx == data['depot']:
            continue
        index = manager.NodeToIndex(location_idx)
        time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
    # Add time window constraints for each vehicle start node.
    depot_idx = data['depot']
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        time_dimension.CumulVar(index).SetRange(
            data['time_windows'][depot_idx][0],
            data['time_windows'][depot_idx][1])

    # Instantiate route start and end times to produce feasible times.
    for i in range(data['num_vehicles']):
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.Start(i)))
        routing.AddVariableMinimizedByFinalizer(
            time_dimension.CumulVar(routing.End(i)))

    # adding drop penalty to every node
    for node in range(1, len(data['distance_matrix'])):
        routing.AddDisjunction([manager.NodeToIndex(node)], data['penalty'])

    # Setting first solution heuristic.
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)
    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print('There was no direct solution found')


