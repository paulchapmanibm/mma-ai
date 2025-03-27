-- First, let's create the employees (without assigning primary_location_id yet since there's a circular reference)
INSERT INTO employees (first_name, last_name, position, email, phone, hire_date, certification, is_active)
VALUES
    -- Seattle Employees (Larger City - 8 employees + 1 manager)
    ('Michael', 'Chen', 'Branch Manager', 'mchen@heavyrentalco.com', '206-555-1001', '2019-06-15', ARRAY['OSHA Certified', 'Equipment Management Certification'], TRUE),
    ('Sarah', 'Johnson', 'Operations Supervisor', 'sjohnson@heavyrentalco.com', '206-555-1002', '2020-03-22', ARRAY['OSHA Certified', 'Heavy Equipment Operator License'], TRUE),
    ('David', 'Wilson', 'Senior Equipment Technician', 'dwilson@heavyrentalco.com', '206-555-1003', '2018-11-10', ARRAY['Diesel Mechanic Certification', 'Hydraulic Systems Specialist'], TRUE),
    ('Emily', 'Rodriguez', 'Rental Coordinator', 'erodriguez@heavyrentalco.com', '206-555-1004', '2021-02-15', ARRAY['Customer Service Certification'], TRUE),
    ('James', 'Taylor', 'Equipment Operator', 'jtaylor@heavyrentalco.com', '206-555-1005', '2020-08-17', ARRAY['CDL Class A', 'Crane Operator Certification'], TRUE),
    ('Maria', 'Garcia', 'Maintenance Technician', 'mgarcia@heavyrentalco.com', '206-555-1006', '2022-01-10', ARRAY['Mobile Equipment Maintenance Certification'], TRUE),
    ('Robert', 'Lee', 'Delivery Driver', 'rlee@heavyrentalco.com', '206-555-1007', '2021-05-22', ARRAY['CDL Class A', 'Hazmat Endorsement'], TRUE),
    ('Jennifer', 'Wong', 'Equipment Specialist', 'jwong@heavyrentalco.com', '206-555-1008', '2022-03-15', ARRAY['Equipment Sales Certification'], TRUE),
    ('Thomas', 'Anderson', 'Safety Coordinator', 'tanderson@heavyrentalco.com', '206-555-1009', '2019-09-20', ARRAY['OSHA Safety Manager Certification', 'First Aid Instructor'], TRUE),
    
    -- Houston Employees (Larger City - 7 employees + 1 manager)
    ('Carlos', 'Martinez', 'Branch Manager', 'cmartinez@heavyrentalco.com', '713-555-2001', '2018-04-10', ARRAY['OSHA Certified', 'MBA', 'Equipment Management Certification'], TRUE),
    ('Jessica', 'Brown', 'Operations Supervisor', 'jbrown@heavyrentalco.com', '713-555-2002', '2019-08-15', ARRAY['OSHA Certified', 'Project Management Professional'], TRUE),
    ('William', 'Jackson', 'Senior Equipment Technician', 'wjackson@heavyrentalco.com', '713-555-2003', '2020-01-22', ARRAY['Master Mechanic Certification', 'Welding Certification'], TRUE),
    ('Amanda', 'Davis', 'Rental Coordinator', 'adavis@heavyrentalco.com', '713-555-2004', '2021-03-18', ARRAY['Sales Certification', 'Customer Service Excellence'], TRUE),
    ('Luis', 'Hernandez', 'Equipment Operator', 'lhernandez@heavyrentalco.com', '713-555-2005', '2019-11-10', ARRAY['CDL Class A', 'Heavy Equipment Operator Certification'], TRUE),
    ('Samantha', 'Clark', 'Maintenance Technician', 'sclark@heavyrentalco.com', '713-555-2006', '2022-02-15', ARRAY['Diesel Engine Specialist', 'Hydraulic Systems Certification'], TRUE),
    ('Richard', 'Thompson', 'Delivery Driver', 'rthompson@heavyrentalco.com', '713-555-2007', '2020-09-05', ARRAY['CDL Class A', 'Hazmat Endorsement'], TRUE),
    ('Kelly', 'White', 'Yard Coordinator', 'kwhite@heavyrentalco.com', '713-555-2008', '2021-06-12', ARRAY['Inventory Management Certification', 'Forklift Operator'], TRUE),
    
    -- Chicago Employees (Larger City - 6 employees + 1 manager)
    ('Daniel', 'Miller', 'Branch Manager', 'dmiller@heavyrentalco.com', '312-555-3001', '2017-07-15', ARRAY['OSHA Certified', 'Equipment Management Certification', 'MBA'], TRUE),
    ('Nicole', 'Harris', 'Operations Supervisor', 'nharris@heavyrentalco.com', '312-555-3002', '2019-05-20', ARRAY['OSHA Certified', 'Project Management Professional'], TRUE),
    ('Anthony', 'Robinson', 'Senior Equipment Technician', 'arobinson@heavyrentalco.com', '312-555-3003', '2018-09-15', ARRAY['Master Mechanic Certification', 'Electrical Systems Specialist'], TRUE),
    ('Stephanie', 'Lewis', 'Rental Coordinator', 'slewis@heavyrentalco.com', '312-555-3004', '2020-04-22', ARRAY['Customer Service Certification', 'Sales Training'], TRUE),
    ('Marcus', 'Walker', 'Equipment Operator', 'mwalker@heavyrentalco.com', '312-555-3005', '2019-10-10', ARRAY['CDL Class A', 'Multiple Equipment Operator Licenses'], TRUE),
    ('Olivia', 'Allen', 'Maintenance Technician', 'oallen@heavyrentalco.com', '312-555-3006', '2021-01-18', ARRAY['HVAC Certification', 'Preventative Maintenance Specialist'], TRUE),
    ('George', 'Scott', 'Delivery Driver', 'gscott@heavyrentalco.com', '312-555-3007', '2020-07-05', ARRAY['CDL Class A', 'Tanker Endorsement'], TRUE),
    
    -- Miami Employees (Medium City - 5 employees + 1 manager)
    ('Alejandro', 'Rodriguez', 'Branch Manager', 'arodriguez@heavyrentalco.com', '305-555-4001', '2018-03-10', ARRAY['OSHA Certified', 'Business Administration Degree'], TRUE),
    ('Sophia', 'Perez', 'Operations Supervisor', 'sperez@heavyrentalco.com', '305-555-4002', '2019-06-15', ARRAY['OSHA Certified', 'Supply Chain Management'], TRUE),
    ('Brian', 'Turner', 'Senior Equipment Technician', 'bturner@heavyrentalco.com', '305-555-4003', '2020-02-22', ARRAY['Hydraulic Systems Specialist', 'Diesel Engine Certification'], TRUE),
    ('Isabella', 'Sanchez', 'Rental Coordinator', 'isanchez@heavyrentalco.com', '305-555-4004', '2021-04-18', ARRAY['Bilingual Customer Service', 'Sales Certification'], TRUE),
    ('Tyler', 'Morris', 'Equipment Operator', 'tmorris@heavyrentalco.com', '305-555-4005', '2019-09-10', ARRAY['CDL Class A', 'Marine Equipment Experience'], TRUE),
    ('Natalie', 'Diaz', 'Maintenance Technician', 'ndiaz@heavyrentalco.com', '305-555-4006', '2022-01-15', ARRAY['Mechanical Engineering Degree', 'Welding Certification'], TRUE),
    
    -- Denver Employees (Medium City - 4 employees + 1 manager)
    ('Christopher', 'Baker', 'Branch Manager', 'cbaker@heavyrentalco.com', '720-555-5001', '2019-02-15', ARRAY['OSHA Certified', 'Business Management Degree'], TRUE),
    ('Rebecca', 'Adams', 'Operations Supervisor', 'radams@heavyrentalco.com', '720-555-5002', '2020-04-22', ARRAY['OSHA Certified', 'Logistics Management'], TRUE),
    ('Justin', 'Phillips', 'Senior Equipment Technician', 'jphillips@heavyrentalco.com', '720-555-5003', '2018-08-10', ARRAY['Electrical Systems Specialist', 'Hydraulic Certification'], TRUE),
    ('Lauren', 'Campbell', 'Rental Coordinator', 'lcampbell@heavyrentalco.com', '720-555-5004', '2021-03-18', ARRAY['Contract Management', 'Customer Service Excellence'], TRUE),
    ('Kevin', 'Evans', 'Equipment Operator', 'kevans@heavyrentalco.com', '720-555-5005', '2020-07-15', ARRAY['CDL Class A', 'Mountain Operation Experience', 'Snow Equipment Specialist'], TRUE),
    
    -- Atlanta Employees (Medium City - 5 employees + 1 manager)
    ('Jonathan', 'Coleman', 'Branch Manager', 'jcoleman@heavyrentalco.com', '404-555-6001', '2018-05-10', ARRAY['OSHA Certified', 'Equipment Management Certification'], TRUE),
    ('Michelle', 'Foster', 'Operations Supervisor', 'mfoster@heavyrentalco.com', '404-555-6002', '2019-07-22', ARRAY['OSHA Certified', 'Project Scheduling Certification'], TRUE),
    ('Brandon', 'Russell', 'Senior Equipment Technician', 'brussell@heavyrentalco.com', '404-555-6003', '2020-03-15', ARRAY['Powertrain Specialist', 'Electronics Diagnostics'], TRUE),
    ('Rachel', 'Jenkins', 'Rental Coordinator', 'rjenkins@heavyrentalco.com', '404-555-6004', '2021-01-18', ARRAY['Account Management', 'Customer Service Training'], TRUE),
    ('Derrick', 'Howard', 'Equipment Operator', 'dhoward@heavyrentalco.com', '404-555-6005', '2019-11-10', ARRAY['CDL Class A', 'Excavator Specialist'], TRUE),
    ('Angela', 'Price', 'Maintenance Technician', 'aprice@heavyrentalco.com', '404-555-6006', '2022-02-15', ARRAY['Preventative Maintenance Certification'], TRUE);
    
-- Now update inventory_locations with manager references
UPDATE inventory_locations SET manager_id = 1 WHERE location_id = 1; -- Michael Chen manages Seattle
UPDATE inventory_locations SET manager_id = 10 WHERE location_id = 2; -- Carlos Martinez manages Houston
UPDATE inventory_locations SET manager_id = 18 WHERE location_id = 3; -- Daniel Miller manages Chicago
UPDATE inventory_locations SET manager_id = 25 WHERE location_id = 4; -- Alejandro Rodriguez manages Miami
UPDATE inventory_locations SET manager_id = 31 WHERE location_id = 5; -- Christopher Baker manages Denver
UPDATE inventory_locations SET manager_id = 36 WHERE location_id = 6; -- Jonathan Coleman manages Atlanta

-- Now update employees with their primary_location_id
-- Seattle employees
UPDATE employees SET primary_location_id = 1 WHERE employee_id BETWEEN 1 AND 9;
-- Houston employees
UPDATE employees SET primary_location_id = 2 WHERE employee_id BETWEEN 10 AND 17;
-- Chicago employees
UPDATE employees SET primary_location_id = 3 WHERE employee_id BETWEEN 18 AND 24;
-- Miami employees
UPDATE employees SET primary_location_id = 4 WHERE employee_id BETWEEN 25 AND 30;
-- Denver employees
UPDATE employees SET primary_location_id = 5 WHERE employee_id BETWEEN 31 AND 35;
-- Atlanta employees
UPDATE employees SET primary_location_id = 6 WHERE employee_id BETWEEN 36 AND 41;

-- Create employee location assignments (making sure all employees are assigned to their primary location)
INSERT INTO employee_locations (employee_id, location_id, is_primary, start_date, assignment_type)
VALUES
    -- Seattle employees
    (1, 1, TRUE, '2019-06-15', 'Permanent'),
    (2, 1, TRUE, '2020-03-22', 'Permanent'),
    (3, 1, TRUE, '2018-11-10', 'Permanent'),
    (4, 1, TRUE, '2021-02-15', 'Permanent'),
    (5, 1, TRUE, '2020-08-17', 'Permanent'),
    (6, 1, TRUE, '2022-01-10', 'Permanent'),
    (7, 1, TRUE, '2021-05-22', 'Permanent'),
    (8, 1, TRUE, '2022-03-15', 'Permanent'),
    (9, 1, TRUE, '2019-09-20', 'Permanent'),
    
    -- Houston employees
    (10, 2, TRUE, '2018-04-10', 'Permanent'),
    (11, 2, TRUE, '2019-08-15', 'Permanent'),
    (12, 2, TRUE, '2020-01-22', 'Permanent'),
    (13, 2, TRUE, '2021-03-18', 'Permanent'),
    (14, 2, TRUE, '2019-11-10', 'Permanent'),
    (15, 2, TRUE, '2022-02-15', 'Permanent'),
    (16, 2, TRUE, '2020-09-05', 'Permanent'),
    (17, 2, TRUE, '2021-06-12', 'Permanent'),
    
    -- Chicago employees
    (18, 3, TRUE, '2017-07-15', 'Permanent'),
    (19, 3, TRUE, '2019-05-20', 'Permanent'),
    (20, 3, TRUE, '2018-09-15', 'Permanent'),
    (21, 3, TRUE, '2020-04-22', 'Permanent'),
    (22, 3, TRUE, '2019-10-10', 'Permanent'),
    (23, 3, TRUE, '2021-01-18', 'Permanent'),
    (24, 3, TRUE, '2020-07-05', 'Permanent'),
    
    -- Miami employees
    (25, 4, TRUE, '2018-03-10', 'Permanent'),
    (26, 4, TRUE, '2019-06-15', 'Permanent'),
    (27, 4, TRUE, '2020-02-22', 'Permanent'),
    (28, 4, TRUE, '2021-04-18', 'Permanent'),
    (29, 4, TRUE, '2019-09-10', 'Permanent'),
    (30, 4, TRUE, '2022-01-15', 'Permanent'),
    
    -- Denver employees
    (31, 5, TRUE, '2019-02-15', 'Permanent'),
    (32, 5, TRUE, '2020-04-22', 'Permanent'),
    (33, 5, TRUE, '2018-08-10', 'Permanent'),
    (34, 5, TRUE, '2021-03-18', 'Permanent'),
    (35, 5, TRUE, '2020-07-15', 'Permanent'),
    
    -- Atlanta employees
    (36, 6, TRUE, '2018-05-10', 'Permanent'),
    (37, 6, TRUE, '2019-07-22', 'Permanent'),
    (38, 6, TRUE, '2020-03-15', 'Permanent'),
    (39, 6, TRUE, '2021-01-18', 'Permanent'),
    (40, 6, TRUE, '2019-11-10', 'Permanent'),
    (41, 6, TRUE, '2022-02-15', 'Permanent'),
    
    -- Some employees with secondary assignments (rotational or temporary)
    (3, 2, FALSE, '2023-01-15', 'Temporary'), -- Seattle technician helping in Houston
    (12, 1, FALSE, '2023-02-10', 'Temporary'), -- Houston technician helping in Seattle
    (20, 6, FALSE, '2022-11-15', 'Rotating'), -- Chicago technician rotating to Atlanta
    (27, 5, FALSE, '2023-03-01', 'Temporary'), -- Miami technician helping in Denver
    (38, 4, FALSE, '2022-12-01', 'Rotating'); -- Atlanta technician rotating to Miami
