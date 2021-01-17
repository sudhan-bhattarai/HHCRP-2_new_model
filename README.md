### Home Healthcare Routing Problem (HHCRP) with time windows in a dynamic environment 
Home Healthcare (HHC) is an enterprise providing regular medical services to the disabled and elderly people at their own houses. A HHCRP is a type of conventional vehicle routing problem (VRP) in which a set of vehicles available at the depot go out to serve a set of predefined customers and finally come back to the depot. In HHCRP, a fleet of nurses with necessary resources go out to visit the patients at their houses in predefined order and finally come back to the HHC depot.

#### Objective of the problem
- To maximize the total number of patients accepted in the planning horizon. (customers in VRP).
- Other objectives can be used according to the output we want.

#### Main constraints of the problem
- The planning horizon is one week.
- A patient can ask for multiple visits in a week and multiple nurses at one visit.
- Every patients are visited only once on a day.
- There should be at least one day gap between two visits to the same patient in a week. If a patient asks for 3 visits in a week then there is only one combination of the days (Mon-Wed-Fri) avialable for him/her.
- Every patients need to visited by the same nurse every day they need the service.
- Every nurses start and end their tours at the HHC depot.
- Every nurses work maximum of 8 hrs on a day.
- Heterogeneity/Qualification (The nurses have different qualifications and only those nurses can visit the patients whose qualification is sufficient to satisfy the patients' demand.)
- Time windows (Every patients need to be visited within a predefined time window everyday.
- Synchronization (Some patients need more than one nurse to serve them. All the nurses working together should arrive at the patient's location before any of them start the service)

#### Files:
- To run the algorithm, download all the files in same path and execute the solve.py file in a python3 editor/console.
- Mathematical formulation is in the file: problem_definition_HHCRP.pdf (Latex script is in .tex file.)
- distance.py to calculate the distance between nodes.
- decision_variables.py to define the variables.
- master_constraints.py to add the assignment constraints to the model.
- sub_constraints.py to add the scheduling constraints to the model.
- solve.py to solve the MILP model.

#### Reference:
Heching, A., Hooker, J. N., &amp; Kimura, R. (2019). A logic-based Benders approach to home healthcare delivery. Transportation Science, 53(2), 510-522. 

Grenouilleau, F., Lahrichi, N., & Rousseau, L. M. (2020). New decomposition methods for home care scheduling with predefined visits. Computers & Operations Research, 115, 104855.
