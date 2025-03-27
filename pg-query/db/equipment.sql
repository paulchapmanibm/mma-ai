-- First, let's create equipment categories
INSERT INTO equipment_categories (category_name, description, daily_insurance_rate)
VALUES
    ('Excavator', 'Hydraulic excavators for digging and material handling', 75.00),
    ('Loader', 'Front loaders for moving materials', 65.00),
    ('Bulldozer', 'Tracked vehicles for pushing large quantities of soil', 85.00),
    ('Skid Steer', 'Compact loaders for tight spaces', 45.00),
    ('Backhoe', 'Combination of excavator and loader capabilities', 60.00),
    ('Trencher', 'Machines for digging trenches', 40.00),
    ('Compactor', 'Equipment for soil and asphalt compaction', 35.00),
    ('Concrete Mixer', 'For mixing and delivering concrete', 30.00),
    ('Generator', 'Mobile power generation units', 25.00),
    ('Air Compressor', 'High-pressure air supply equipment', 20.00),
    ('Forklift', 'Material handling equipment for lifting and moving', 35.00),
    ('Scissor Lift', 'Vertical lifting platforms', 40.00),
    ('Boom Lift', 'Aerial work platforms with extensible arms', 55.00),
    ('Telehandler', 'Telescopic handlers for lifting at height and reach', 70.00),
    ('Light Tower', 'Mobile lighting systems for work sites', 15.00);

-- Now insert equipment (at least 2 of each type across all locations)
INSERT INTO equipment (category_id, equipment_name, model_number, manufacturer, purchase_date, purchase_price, current_value, daily_rental_rate, weekly_rental_rate, monthly_rental_rate, status, maintenance_interval, last_maintenance_date, hours_used, condition_rating, location_id, notes)
VALUES
    -- Excavators
    (1, 'CAT 320 Excavator', '320-GC-2022', 'Caterpillar', '2022-03-15', 225000.00, 198000.00, 450.00, 2700.00, 9000.00, 'Available', 250, '2024-02-10', 1250, 4, 1, 'Medium-sized excavator with standard bucket'),
    (1, 'Komatsu PC210 Excavator', 'PC210LC-11', 'Komatsu', '2023-01-20', 235000.00, 220000.00, 475.00, 2850.00, 9500.00, 'Available', 250, '2024-01-05', 750, 5, 2, 'Includes quick coupler and hydraulic thumb'),
    (1, 'Hitachi ZX130 Excavator', 'ZX130-6', 'Hitachi', '2022-06-12', 175000.00, 155000.00, 350.00, 2100.00, 7000.00, 'Available', 200, '2024-02-20', 980, 4, 3, 'Compact excavator for urban projects'),
    (1, 'Volvo EC220 Excavator', 'EC220E', 'Volvo', '2021-11-25', 245000.00, 195000.00, 485.00, 2910.00, 9700.00, 'Maintenance', 250, '2024-03-01', 1680, 3, 4, 'Undergoing hydraulic system maintenance'),
    
    -- Loaders
    (2, 'CAT 966 Wheel Loader', '966M', 'Caterpillar', '2023-02-15', 320000.00, 305000.00, 550.00, 3300.00, 11000.00, 'Available', 300, '2024-01-15', 820, 5, 5, 'Large capacity general purpose bucket'),
    (2, 'John Deere 644 Loader', '644K', 'John Deere', '2022-05-10', 290000.00, 265000.00, 525.00, 3150.00, 10500.00, 'Rented', 300, '2023-12-10', 1120, 4, 6, 'Currently on rental at downtown project'),
    (2, 'Komatsu WA320 Loader', 'WA320-8', 'Komatsu', '2021-08-22', 260000.00, 220000.00, 500.00, 3000.00, 10000.00, 'Available', 300, '2024-02-05', 1520, 3, 1, 'Medium-sized loader with fork attachment available'),
    (2, 'Volvo L90 Loader', 'L90H', 'Volvo', '2023-04-18', 275000.00, 265000.00, 515.00, 3090.00, 10300.00, 'Available', 300, '2024-03-01', 590, 5, 2, 'Includes multi-purpose bucket and forks'),
    
    -- Bulldozers
    (3, 'CAT D6 Dozer', 'D6T', 'Caterpillar', '2022-09-30', 380000.00, 350000.00, 650.00, 3900.00, 13000.00, 'Available', 350, '2024-02-15', 980, 4, 3, 'Medium bulldozer with semi-U blade'),
    (3, 'Komatsu D65 Dozer', 'D65PX-18', 'Komatsu', '2023-03-12', 395000.00, 375000.00, 675.00, 4050.00, 13500.00, 'Rented', 350, '2024-01-10', 650, 5, 4, 'Wide track model for soft terrain'),
    (3, 'John Deere 700K Dozer', '700K', 'John Deere', '2021-11-15', 325000.00, 280000.00, 600.00, 3600.00, 12000.00, 'Available', 350, '2024-02-01', 1250, 3, 5, 'Smaller dozer with 6-way blade'),
    (3, 'Case 1650M Dozer', '1650M', 'Case', '2022-07-22', 340000.00, 310000.00, 625.00, 3750.00, 12500.00, 'Maintenance', 350, '2024-03-05', 875, 4, 6, 'Undergoing track replacement'),
    
    -- Skid Steers
    (4, 'Bobcat S76 Skid Steer', 'S76', 'Bobcat', '2023-05-10', 65000.00, 60000.00, 225.00, 1350.00, 4500.00, 'Available', 150, '2024-02-25', 450, 5, 1, 'Vertical lift path, includes bucket and forks'),
    (4, 'CAT 262D3 Skid Steer', '262D3', 'Caterpillar', '2022-08-15', 70000.00, 62000.00, 235.00, 1410.00, 4700.00, 'Available', 150, '2024-01-20', 780, 4, 2, 'High flow hydraulics package'),
    (4, 'John Deere 332G Skid Steer', '332G', 'John Deere', '2023-02-28', 68000.00, 64000.00, 230.00, 1380.00, 4600.00, 'Rented', 150, '2023-12-15', 410, 5, 3, 'Large capacity model with multiple attachments'),
    (4, 'Kubota SSV75 Skid Steer', 'SSV75', 'Kubota', '2022-10-05', 62000.00, 54000.00, 220.00, 1320.00, 4400.00, 'Available', 150, '2024-02-10', 650, 4, 4, 'Compact but powerful model'),
    
    -- Backhoes
    (5, 'JCB 3CX Backhoe', '3CX', 'JCB', '2022-04-18', 110000.00, 98000.00, 325.00, 1950.00, 6500.00, 'Available', 200, '2024-01-15', 920, 4, 5, 'Classic backhoe with extend-a-hoe feature'),
    (5, 'CAT 420 Backhoe', '420XE', 'Caterpillar', '2023-01-25', 130000.00, 122000.00, 345.00, 2070.00, 6900.00, 'Available', 200, '2024-02-20', 580, 5, 6, 'Premium model with pilot controls'),
    (5, 'Case 580 Backhoe', '580SN', 'Case', '2021-10-15', 115000.00, 95000.00, 330.00, 1980.00, 6600.00, 'Maintenance', 200, '2024-03-01', 1380, 3, 1, 'Undergoing boom repair'),
    (5, 'John Deere 310SL Backhoe', '310SL', 'John Deere', '2022-11-30', 125000.00, 112000.00, 340.00, 2040.00, 6800.00, 'Available', 200, '2024-01-10', 760, 4, 2, 'Tool carrier version with quick coupler'),
    
    -- Trenchers
    (6, 'Vermeer RTX550 Trencher', 'RTX550', 'Vermeer', '2023-03-20', 95000.00, 90000.00, 280.00, 1680.00, 5600.00, 'Available', 150, '2024-02-05', 410, 5, 3, 'Ride-on trencher with 6" chain'),
    (6, 'Ditch Witch RT45 Trencher', 'RT45', 'Ditch Witch', '2022-06-15', 85000.00, 75000.00, 260.00, 1560.00, 5200.00, 'Rented', 150, '2023-12-20', 680, 4, 4, 'With both trencher and backhoe attachments'),
    (6, 'Toro TRX-26 Trencher', 'TRX-26', 'Toro', '2022-09-10', 25000.00, 21000.00, 180.00, 1080.00, 3600.00, 'Available', 100, '2024-01-25', 520, 4, 5, 'Walk-behind model for tight access areas'),
    (6, 'Barreto 1824TK Trencher', '1824TK', 'Barreto', '2023-02-05', 22000.00, 20000.00, 175.00, 1050.00, 3500.00, 'Available', 100, '2024-02-15', 320, 5, 6, 'Track-mounted walk-behind trencher'),
    
    -- Compactors
    (7, 'CAT CB10 Roller', 'CB10', 'Caterpillar', '2022-08-25', 115000.00, 102000.00, 290.00, 1740.00, 5800.00, 'Available', 200, '2024-01-30', 780, 4, 1, 'Tandem vibratory roller for asphalt'),
    (7, 'Bomag BW211 Roller', 'BW211D-5', 'Bomag', '2023-04-10', 125000.00, 118000.00, 300.00, 1800.00, 6000.00, 'Available', 200, '2024-02-25', 450, 5, 2, 'Single drum soil compactor'),
    (7, 'Wacker RD12 Roller', 'RD12A', 'Wacker Neuson', '2022-05-20', 28000.00, 24000.00, 175.00, 1050.00, 3500.00, 'Rented', 150, '2023-11-15', 680, 4, 3, 'Small walk-behind roller'),
    (7, 'Multiquip MVC88 Plate Compactor', 'MVC88VTHW', 'Multiquip', '2023-01-15', 3500.00, 3200.00, 75.00, 450.00, 1500.00, 'Available', 100, '2024-02-10', 420, 5, 4, 'Forward plate compactor'),
    
    -- Concrete Mixers
    (8, 'Multiquip MC94S Mixer', 'MC94S', 'Multiquip', '2022-10-15', 3800.00, 3300.00, 85.00, 510.00, 1700.00, 'Available', 100, '2024-01-20', 550, 4, 5, '9 cubic foot concrete mixer'),
    (8, 'Crown C9 Mixer', 'C9', 'Crown Construction', '2023-03-05', 4200.00, 3900.00, 90.00, 540.00, 1800.00, 'Available', 100, '2024-02-20', 320, 5, 6, 'Heavy duty mixer with Honda engine'),
    (8, 'Terex Advance FD4000 Mixer Truck', 'FD4000', 'Terex', '2021-09-30', 195000.00, 165000.00, 450.00, 2700.00, 9000.00, 'Maintenance', 250, '2024-03-01', 1820, 3, 1, '11 cubic yard front discharge mixer truck'),
    (8, 'Oshkosh S-Series Mixer Truck', 'S-Series', 'Oshkosh', '2022-07-15', 210000.00, 185000.00, 475.00, 2850.00, 9500.00, 'Available', 250, '2024-01-15', 1250, 4, 2, '12 cubic yard rear discharge mixer truck'),
    
    -- Generators
    (9, 'Generac XG10000E Generator', 'XG10000E', 'Generac', '2023-01-10', 3500.00, 3200.00, 95.00, 570.00, 1900.00, 'Available', 100, '2024-02-05', 450, 5, 3, '10kW portable generator'),
    (9, 'Honda EB10000 Generator', 'EB10000', 'Honda', '2022-06-20', 6800.00, 6000.00, 115.00, 690.00, 2300.00, 'Available', 100, '2024-01-25', 680, 4, 4, '10kW industrial generator'),
    (9, 'CAT XQ230 Generator', 'XQ230', 'Caterpillar', '2021-11-15', 75000.00, 65000.00, 350.00, 2100.00, 7000.00, 'Rented', 200, '2023-12-10', 1450, 3, 5, '230kW towable generator'),
    (9, 'Cummins C150D6R Generator', 'C150D6R', 'Cummins', '2022-09-05', 65000.00, 59000.00, 325.00, 1950.00, 6500.00, 'Available', 200, '2024-02-15', 950, 4, 6, '150kW towable generator'),
    
    -- Air Compressors
    (10, 'Atlas Copco XAS 110 Compressor', 'XAS 110', 'Atlas Copco', '2022-05-28', 28000.00, 24000.00, 165.00, 990.00, 3300.00, 'Available', 150, '2024-01-20', 780, 4, 1, 'Towable 110 CFM diesel air compressor'),
    (10, 'Doosan P185 Compressor', 'P185WDO', 'Doosan', '2023-02-15', 30000.00, 28000.00, 175.00, 1050.00, 3500.00, 'Available', 150, '2024-02-10', 450, 5, 2, 'Towable 185 CFM diesel air compressor'),
    (10, 'Sullair 375H Compressor', '375H', 'Sullair', '2022-07-10', 52000.00, 46000.00, 225.00, 1350.00, 4500.00, 'Maintenance', 150, '2024-03-01', 950, 3, 3, 'Towable 375 CFM diesel air compressor'),
    (10, 'Ingersoll Rand VHP700 Compressor', 'VHP700WIR', 'Ingersoll Rand', '2021-12-18', 58000.00, 48000.00, 245.00, 1470.00, 4900.00, 'Available', 150, '2024-01-10', 1280, 4, 4, 'Towable 700 CFM diesel air compressor'),
    
    -- Forklifts
    (11, 'Toyota 8FGU25 Forklift', '8FGU25', 'Toyota', '2022-09-15', 35000.00, 31000.00, 195.00, 1170.00, 3900.00, 'Available', 150, '2024-02-05', 820, 4, 5, '5000 lb capacity propane forklift'),
    (11, 'Hyster H80FT Forklift', 'H80FT', 'Hyster', '2023-03-20', 38000.00, 36000.00, 205.00, 1230.00, 4100.00, 'Available', 150, '2024-01-25', 480, 5, 6, '8000 lb capacity diesel forklift'),
    (11, 'Crown FC 4500 Forklift', 'FC 4500', 'Crown', '2022-06-10', 32000.00, 28000.00, 185.00, 1110.00, 3700.00, 'Rented', 150, '2023-11-20', 960, 4, 1, '4000 lb capacity electric forklift'),
    (11, 'CAT DP70N Forklift', 'DP70N', 'Caterpillar', '2021-10-25', 65000.00, 55000.00, 275.00, 1650.00, 5500.00, 'Available', 200, '2024-02-15', 1320, 3, 2, '15000 lb capacity diesel forklift'),
    
    -- Scissor Lifts
    (12, 'Genie GS-1930 Scissor Lift', 'GS-1930', 'Genie', '2023-01-15', 15000.00, 14000.00, 150.00, 900.00, 3000.00, 'Available', 100, '2024-02-10', 420, 5, 3, '19 ft electric scissor lift'),
    (12, 'Skyjack SJIII 3219 Scissor Lift', 'SJIII 3219', 'Skyjack', '2022-05-20', 14500.00, 12500.00, 145.00, 870.00, 2900.00, 'Available', 100, '2024-01-20', 680, 4, 4, '19 ft electric scissor lift'),
    (12, 'JLG 4069LE Scissor Lift', '4069LE', 'JLG', '2022-08-10', 45000.00, 40000.00, 225.00, 1350.00, 4500.00, 'Maintenance', 150, '2024-02-28', 520, 4, 5, '40 ft electric rough terrain scissor lift'),
    (12, 'Hy-Brid HB-1430 Scissor Lift', 'HB-1430', 'Hy-Brid', '2023-04-05', 12000.00, 11500.00, 135.00, 810.00, 2700.00, 'Available', 100, '2024-02-15', 280, 5, 6, '14 ft lightweight scissor lift'),
    
    -- Boom Lifts
    (13, 'JLG 450AJ Boom Lift', '450AJ', 'JLG', '2022-07-12', 95000.00, 85000.00, 350.00, 2100.00, 7000.00, 'Available', 200, '2024-01-15', 780, 4, 1, '45 ft diesel articulating boom lift'),
    (13, 'Genie Z-45/25J Boom Lift', 'Z-45/25J', 'Genie', '2023-02-28', 98000.00, 93000.00, 365.00, 2190.00, 7300.00, 'Available', 200, '2024-02-20', 450, 5, 2, '45 ft diesel articulating boom lift'),
    (13, 'JLG 600S Boom Lift', '600S', 'JLG', '2021-11-10', 135000.00, 115000.00, 425.00, 2550.00, 8500.00, 'Rented', 200, '2023-12-05', 1250, 3, 3, '60 ft diesel straight boom lift'),
    (13, 'Genie S-65 Boom Lift', 'S-65', 'Genie', '2022-09-25', 140000.00, 126000.00, 440.00, 2640.00, 8800.00, 'Available', 200, '2024-01-30', 860, 4, 4, '65 ft diesel straight boom lift'),
    
    -- Telehandlers
    (14, 'JCB 507-42 Telehandler', '507-42', 'JCB', '2022-06-15', 110000.00, 98000.00, 385.00, 2310.00, 7700.00, 'Available', 200, '2024-02-05', 820, 4, 5, '7000 lb capacity, 42 ft reach telehandler'),
    (14, 'CAT TL943D Telehandler', 'TL943D', 'Caterpillar', '2023-03-10', 125000.00, 118000.00, 405.00, 2430.00, 8100.00, 'Available', 200, '2024-01-25', 480, 5, 6, '9000 lb capacity, 43 ft reach telehandler'),
    (14, 'Genie GTH-844 Telehandler', 'GTH-844', 'Genie', '2022-09-20', 145000.00, 130000.00, 425.00, 2550.00, 8500.00, 'Maintenance', 200, '2024-02-25', 750, 4, 1, '8000 lb capacity, 44 ft reach telehandler'),
    (14, 'JLG 1055 Telehandler', '1055', 'JLG', '2021-12-05', 155000.00, 130000.00, 450.00, 2700.00, 9000.00, 'Available', 200, '2024-01-10', 1180, 3, 2, '10000 lb capacity, 55 ft reach telehandler'),
    
    -- Light Towers
    (15, 'Generac MLT6 Light Tower', 'MLT6', 'Generac', '2023-01-25', 15000.00, 14000.00, 120.00, 720.00, 2400.00, 'Available', 100, '2024-02-15', 450, 5, 3, 'Towable light tower with 4 metal halide lamps'),
    (15, 'Doosan L8 Light Tower', 'L8', 'Doosan', '2022-08-15', 16500.00, 14500.00, 125.00, 750.00, 2500.00, 'Available', 100, '2024-01-20', 680, 4, 4, 'Towable light tower with LED lamps'),
    (15, 'Wacker Neuson LTV6 Light Tower', 'LTV6', 'Wacker Neuson', '2022-05-10', 14500.00, 12500.00, 115.00, 690.00, 2300.00, 'Rented', 100, '2023-11-15', 790, 4, 5, 'Vertical mast light tower'),
    (15, 'Terex AL5 Light Tower', 'AL5', 'Terex', '2023-04-05', 17000.00, 16500.00, 130.00, 780.00, 2600.00, 'Available', 100, '2024-02-10', 280, 5, 6, 'Compact light tower with LED technology');
