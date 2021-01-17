### Home Healthcare Routing Problem (HHCRP) with time windows in a dynamic environment 
HHCRP is similar to the traditional Vehicle Routing Problem (VRP) with some additional medical constraints. 
#### Reference:
Heching, A., Hooker, J. N., &amp; Kimura, R. (2019). A logic-based Benders approach to home healthcare delivery. Transportation Science, 53(2), 510-522. 
####
Grenouilleau, F., Lahrichi, N., & Rousseau, L. M. (2020). New decomposition methods for home care scheduling with predefined visits. Computers & Operations Research, 115, 104855.

# Objective of the problem
- To maximize the total number of patients (customers in VRP).

# Main constraints of the problem
- The planning horizon is one week.
- A patient can ask for multiple visits in a week and multiple nurses at one visit.
- Every patients are visited only once on a day.
- There should be at least one day gap between two visits to the same patient in a week.
- Every patients need to visited by the same nurse and same time every day they need the service.
- Every nurses start and end their tours at the HHC depot.
- Every nurses work maximum of 8 hrs on a day.
- Heterogeneity/Qualification (The nurses have different qualifications and only those nurses can visit the patients whose qualification is sufficient according to the patient's demand.)
- Time windows (Every patients need to be visited within a predefined window everyday.
- Synchronization (Some patients need more than one nurse to serve them. All the nurses working together should arrive at the patient's location before any of them start the service)
