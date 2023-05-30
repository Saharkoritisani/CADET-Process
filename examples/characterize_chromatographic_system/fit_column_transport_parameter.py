from column_transport_parameters import optimization_problem
from scipy.optimize import minimize
from column_transport_parameters import process
from column_transport_parameters import simulator
from column_transport_parameters import comparator

x0 = [0.5, 0.05]

##version 1
#def loss(x):
#    return optimization_problem.evaluate_objectives(x)

#res = minimize(loss,x0, bounds=[(0.1,0.5),(1e-10,0.1)], method='nelder-mead',
#               options={'xatol': 1e-8, 'disp': True})
## version 2##
def loss(x):
    return optimization_problem.evaluate_objectives(x,untransform= True)



res = minimize(loss,x0, bounds=[(0,1),(0,1)], method='nelder-mead',
               options={'xatol': 1e-8, 'disp': True})
print(optimization_problem.untransform(res.x))

results_x =  optimization_problem.untransform(res.x)

process.flow_sheet.units_dict['column'].bed_porosity=results_x[0]
process.flow_sheet.units_dict['column'].axial_dispersion = results_x[1]
simulation_results= simulator.simulate(process)
comparator.plot_comparison(simulation_results)