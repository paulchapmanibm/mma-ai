-- Insert data into maintenance_records table
INSERT INTO maintenance_records (equipment_id, maintenance_date, maintenance_type, description, cost, performed_by, hours_added, parts_replaced, next_maintenance_date, status, notes)
VALUES
    -- Seattle Location Equipment Maintenance
    (1, '2023-08-15', 'Scheduled', '250-hour maintenance service including oil change, filter replacement, and hydraulic system check', 1250.00, 3, 0, 'Oil filters, hydraulic filters, air filters', '2024-02-10', 'Completed', 'Regular maintenance completed on schedule'),
    (1, '2024-02-10', 'Scheduled', '500-hour maintenance service with full fluid replacement and system diagnostics', 2100.00, 3, 0, 'All filters, hydraulic fluid, engine oil, coolant', '2024-08-10', 'Completed', 'Machine operating within specifications'),
    (2, '2023-07-05', 'Scheduled', '250-hour service maintenance performed', 1350.00, 3, 0, 'Oil filters, hydraulic filters', '2024-01-05', 'Completed', 'Regular maintenance completed on schedule'),
    (2, '2024-01-05', 'Scheduled', '500-hour comprehensive service', 2200.00, 3, 0, 'All filters, hydraulic fluid, engine oil', '2024-07-05', 'Completed', 'Extended service life expectancy'),
    (3, '2024-02-20', 'Scheduled', '250-hour maintenance check and fluid change', 1150.00, 6, 0, 'Oil filters, hydraulic filters, air filters', '2024-08-20', 'Completed', 'Machine in excellent condition'),
    (4, '2024-03-01', 'Repair', 'Hydraulic cylinder seal replacement and control valve adjustment', 3200.00, 3, 25, 'Hydraulic cylinder seals, control valve kit', '2024-09-01', 'Completed', 'Repair needed due to normal wear and tear'),
    (5, '2023-10-15', 'Scheduled', '300-hour maintenance service', 1450.00, 6, 0, 'All filters, engine oil', '2024-04-15', 'Completed', 'Regular maintenance performed'),
    (6, '2024-01-15', 'Inspection', 'Annual safety inspection and certification', 850.00, 3, 0, 'None', '2025-01-15', 'Completed', 'Machine passed all safety checks'),
    (7, '2023-12-10', 'Scheduled', '300-hour maintenance service', 1500.00, 6, 0, 'All filters, engine oil, transmission fluid', '2024-06-10', 'Completed', 'No issues found'),
    (8, '2024-03-20', 'Emergency', 'Hydraulic hose burst repair and system flush', 2800.00, 3, 15, 'Hydraulic hoses, hydraulic fluid', '2024-09-20', 'Completed', 'Emergency repair completed within 24 hours'),
    (13, '2024-01-20', 'Scheduled', '150-hour maintenance service', 750.00, 6, 0, 'Oil filter, air filter, fuel filter', '2024-07-20', 'Completed', 'Machine in good operating condition'),
    
    -- Houston Location Equipment Maintenance
    (10, '2023-09-10', 'Scheduled', '350-hour maintenance service', 1750.00, 12, 0, 'All filters, hydraulic fluid, engine oil', '2024-03-10', 'Completed', 'Regular maintenance performed'),
    (10, '2024-01-10', 'Repair', 'Track assembly replacement and undercarriage inspection', 4800.00, 12, 30, 'Track assembly, idler wheels', '2024-07-10', 'Completed', 'Wear and tear due to harsh terrain operation'),
    (11, '2023-12-15', 'Scheduled', '350-hour maintenance service', 1700.00, 15, 0, 'All filters, engine oil, hydraulic fluid', '2024-06-15', 'Completed', 'Regular maintenance performed'),
    (12, '2024-03-05', 'Scheduled', '350-hour maintenance check', 1800.00, 12, 0, 'All filters, engine oil, hydraulic fluid', '2024-09-05', 'In Progress', 'Machine temporarily out of service for maintenance'),
    (15, '2023-11-15', 'Scheduled', '150-hour service', 850.00, 15, 0, 'Oil filter, air filter', '2024-05-15', 'Completed', 'Minor adjustments made to hydraulic system'),
    (16, '2024-02-20', 'Repair', 'Chain drive adjustment and lubrication system repair', 1200.00, 12, 10, 'Chain tensioner, lubrication pump', '2024-08-20', 'Completed', 'Machine back in service after repairs'),
    (19, '2024-01-20', 'Scheduled', '200-hour maintenance service', 950.00, 15, 0, 'All filters, engine oil', '2024-07-20', 'Completed', 'Regular maintenance performed'),
    (22, '2023-10-20', 'Emergency', 'Engine overheating investigation and cooling system repair', 2500.00, 12, 25, 'Water pump, thermostat, coolant', '2024-04-20', 'Completed', 'Cooling system completely rebuilt'),
    
    -- Chicago Location Equipment Maintenance
    (20, '2023-09-15', 'Scheduled', '200-hour service check', 1100.00, 20, 0, 'All filters, engine oil', '2024-03-15', 'Completed', 'Regular maintenance performed'),
    (23, '2024-02-05', 'Scheduled', '200-hour maintenance service', 1150.00, 23, 0, 'All filters, engine oil', '2024-08-05', 'Completed', 'Machine in good operating condition'),
    (24, '2023-12-20', 'Repair', 'Boom cylinder seal replacement', 1800.00, 20, 15, 'Boom cylinder seals, hydraulic fluid', '2024-06-20', 'Completed', 'Repair due to normal wear and tear'),
    (27, '2024-01-25', 'Scheduled', '100-hour service', 650.00, 23, 0, 'Oil filter, air filter', '2024-07-25', 'Completed', 'Regular maintenance performed'),
    (29, '2023-11-10', 'Inspection', 'Annual safety certification and inspection', 800.00, 20, 0, 'None', '2024-11-10', 'Completed', 'All safety standards met'),
    (30, '2024-03-01', 'Emergency', 'Engine failure diagnosis and starter motor replacement', 1900.00, 23, 20, 'Starter motor, battery', '2024-09-01', 'Completed', 'Quick repair turnaround to minimize downtime'),
    (34, '2024-02-10', 'Scheduled', '150-hour maintenance check', 750.00, 20, 0, 'All filters, engine oil', '2024-08-10', 'Completed', 'Machine operating within specifications'),
    
    -- Miami Location Equipment Maintenance
    (33, '2023-10-05', 'Scheduled', '150-hour service', 800.00, 27, 0, 'All filters, engine oil', '2024-04-05', 'Completed', 'Regular maintenance performed'),
    (33, '2024-02-25', 'Repair', 'Control panel replacement and electrical system diagnosis', 2300.00, 27, 15, 'Control panel, wiring harness', '2024-08-25', 'Completed', 'Repair due to saltwater exposure damage'),
    (36, '2023-12-05', 'Scheduled', '150-hour maintenance check', 700.00, 30, 0, 'All filters, engine oil', '2024-06-05', 'Completed', 'Machine in good operating condition'),
    (39, '2024-01-30', 'Inspection', 'Safety compliance inspection', 550.00, 27, 0, 'None', '2025-01-30', 'Completed', 'All safety standards met'),
    (46, '2023-11-20', 'Scheduled', '200-hour maintenance service', 1050.00, 30, 0, 'All filters, hydraulic fluid, engine oil', '2024-05-20', 'Completed', 'Regular maintenance performed'),
    (53, '2024-03-15', 'Emergency', 'Boom failure investigation and hydraulic system repair', 3800.00, 27, 30, 'Hydraulic valves, hoses, boom cylinder', '2024-09-15', 'In Progress', 'Major repair to critical component'),
    
    -- Denver Location Equipment Maintenance
    (43, '2023-08-10', 'Scheduled', '200-hour maintenance check', 1050.00, 33, 0, 'All filters, engine oil', '2024-02-10', 'Completed', 'Regular maintenance performed'),
    (43, '2024-02-10', 'Scheduled', '400-hour comprehensive service', 1950.00, 33, 0, 'All filters, engine oil, hydraulic fluid, cooling system flush', '2024-08-10', 'Completed', 'Extended maintenance due to mountain operation'),
    (47, '2023-11-05', 'Repair', 'Air compressor rebuild', 1400.00, 33, 15, 'Compressor pump, pressure switch, air filters', '2024-05-05', 'Completed', 'Repair due to altitude operation stress'),
    (47, '2024-03-01', 'Inspection', 'State safety compliance inspection', 600.00, 33, 0, 'None', '2025-03-01', 'Completed', 'Passed all safety requirements'),
    (21, '2024-01-25', 'Scheduled', '100-hour service', 550.00, 33, 0, 'Oil filter, air filter', '2024-07-25', 'Completed', 'Regular maintenance performed'),
    (29, '2023-09-20', 'Scheduled', '150-hour maintenance', 750.00, 33, 0, 'All filters, engine oil', '2024-03-20', 'Completed', 'Machine in good operating condition'),
    
    -- Atlanta Location Equipment Maintenance
    (31, '2023-10-10', 'Scheduled', '150-hour service', 850.00, 38, 0, 'All filters, engine oil', '2024-04-10', 'Completed', 'Regular maintenance performed'),
    (31, '2024-02-15', 'Repair', 'Hydraulic pump replacement', 2200.00, 38, 20, 'Hydraulic pump, fittings, hydraulic fluid', '2024-08-15', 'Completed', 'Repair due to normal wear and tear'),
    (35, '2023-12-15', 'Scheduled', '100-hour maintenance', 600.00, 41, 0, 'Oil filter, air filter, fuel filter', '2024-06-15', 'Completed', 'Machine in good operating condition'),
    (44, '2024-01-05', 'Scheduled', '200-hour service check', 1100.00, 38, 0, 'All filters, engine oil, hydraulic fluid', '2024-07-05', 'Completed', 'Regular maintenance performed'),
    (44, '2024-03-10', 'Inspection', 'Annual certification and safety inspection', 750.00, 41, 0, 'None', '2025-03-10', 'Completed', 'All safety standards met'),
    (51, '2023-11-25', 'Emergency', 'Hydraulic system failure and contamination cleanup', 3500.00, 38, 25, 'Hydraulic pump, valves, filters, hydraulic fluid', '2024-05-25', 'Completed', 'Complete system flush and rebuild required'),
    (52, '2024-02-25', 'Scheduled', '200-hour maintenance service', 1150.00, 41, 0, 'All filters, engine oil', '2024-08-25', 'Completed', 'Machine operating within specifications'),
    (60, '2023-09-10', 'Scheduled', '100-hour service', 580.00, 38, 0, 'Oil filter, air filter', '2024-03-10', 'Completed', 'Regular maintenance performed'),
    (60, '2024-03-10', 'Scheduled', '200-hour comprehensive service', 950.00, 41, 0, 'All filters, engine oil, bulb replacement', '2024-09-10', 'In Progress', 'Scheduled maintenance in progress');
