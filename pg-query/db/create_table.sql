-- 1. Customers Table
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    credit_limit DECIMAL(10, 2),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Equipment Categories Table
CREATE TABLE equipment_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    daily_insurance_rate DECIMAL(10, 2) NOT NULL
);

-- 3. Inventory Locations Table (moved up in creation order)
CREATE TABLE inventory_locations (
    location_id SERIAL PRIMARY KEY,
    location_name VARCHAR(100) UNIQUE NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE
);

-- 4. Employees Table (modified)
CREATE TABLE employees (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    hire_date DATE NOT NULL,
    primary_location_id INTEGER REFERENCES inventory_locations(location_id),
    certification TEXT[],
    is_active BOOLEAN DEFAULT TRUE
);

-- 5. Employee-Location Assignment Table (new junction table)
CREATE TABLE employee_locations (
    assignment_id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(employee_id),
    location_id INTEGER REFERENCES inventory_locations(location_id),
    is_primary BOOLEAN DEFAULT FALSE,
    start_date DATE NOT NULL,
    end_date DATE,
    assignment_type VARCHAR(50) CHECK (assignment_type IN ('Permanent', 'Temporary', 'Rotating')),
    UNIQUE(employee_id, location_id, start_date)
);

-- 6. Update Inventory Locations Table with manager reference
ALTER TABLE inventory_locations ADD COLUMN manager_id INTEGER REFERENCES employees(employee_id);

-- 7. Equipment Table
CREATE TABLE equipment (
    equipment_id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES equipment_categories(category_id),
    equipment_name VARCHAR(100) NOT NULL,
    model_number VARCHAR(50) NOT NULL,
    manufacturer VARCHAR(100) NOT NULL,
    purchase_date DATE NOT NULL,
    purchase_price DECIMAL(10, 2) NOT NULL,
    current_value DECIMAL(10, 2) NOT NULL,
    daily_rental_rate DECIMAL(10, 2) NOT NULL,
    weekly_rental_rate DECIMAL(10, 2) NOT NULL,
    monthly_rental_rate DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Available', 'Rented', 'Maintenance', 'Retired')),
    maintenance_interval INTEGER NOT NULL, -- Days between scheduled maintenance
    last_maintenance_date DATE,
    hours_used INTEGER DEFAULT 0,
    condition_rating INTEGER CHECK (condition_rating BETWEEN 1 AND 5),
    location_id INTEGER REFERENCES inventory_locations(location_id),
    notes TEXT
);

-- 8. Rentals Table
CREATE TABLE rentals (
    rental_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    rental_date DATE NOT NULL,
    expected_return_date DATE NOT NULL,
    actual_return_date DATE,
    total_amount DECIMAL(10, 2),
    deposit_amount DECIMAL(10, 2),
    deposit_returned BOOLEAN DEFAULT FALSE,
    status VARCHAR(20) CHECK (status IN ('Reserved', 'Active', 'Completed', 'Cancelled')),
    created_by INTEGER REFERENCES employees(employee_id),
    pickup_location_id INTEGER REFERENCES inventory_locations(location_id),
    return_location_id INTEGER REFERENCES inventory_locations(location_id),
    insurance_coverage BOOLEAN DEFAULT TRUE,
    po_number VARCHAR(50),
    notes TEXT
);

-- 9. Rental Items (Junction Table)
CREATE TABLE rental_items (
    rental_item_id SERIAL PRIMARY KEY,
    rental_id INTEGER REFERENCES rentals(rental_id),
    equipment_id INTEGER REFERENCES equipment(equipment_id),
    hourly_usage INTEGER,
    daily_rate DECIMAL(10, 2) NOT NULL,
    quantity INTEGER DEFAULT 1,
    start_condition TEXT,
    end_condition TEXT,
    damages_reported BOOLEAN DEFAULT FALSE,
    damage_description TEXT,
    damage_charges DECIMAL(10, 2) DEFAULT 0.00
);

-- 10. Maintenance Records Table
CREATE TABLE maintenance_records (
    maintenance_id SERIAL PRIMARY KEY,
    equipment_id INTEGER REFERENCES equipment(equipment_id),
    maintenance_date DATE NOT NULL,
    maintenance_type VARCHAR(50) CHECK (maintenance_type IN ('Scheduled', 'Repair', 'Inspection', 'Emergency')),
    description TEXT NOT NULL,
    cost DECIMAL(10, 2) NOT NULL,
    performed_by INTEGER REFERENCES employees(employee_id),
    hours_added INTEGER,
    parts_replaced TEXT,
    next_maintenance_date DATE,
    status VARCHAR(20) CHECK (status IN ('Scheduled', 'In Progress', 'Completed', 'Postponed')),
    notes TEXT
);

-- 11. Payments Table
CREATE TABLE payments (
    payment_id SERIAL PRIMARY KEY,
    rental_id INTEGER REFERENCES rentals(rental_id),
    payment_date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50) NOT NULL,
    transaction_reference VARCHAR(100),
    processed_by INTEGER REFERENCES employees(employee_id),
    is_refund BOOLEAN DEFAULT FALSE,
    notes TEXT
);

-- 12. Equipment Attachments Table
CREATE TABLE equipment_attachments (
    attachment_id SERIAL PRIMARY KEY,
    equipment_id INTEGER REFERENCES equipment(equipment_id),
    attachment_name VARCHAR(100) NOT NULL,
    attachment_type VARCHAR(50) NOT NULL,
    daily_rate DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('Available', 'Rented', 'Maintenance', 'Retired')),
    location_id INTEGER REFERENCES inventory_locations(location_id),
    notes TEXT
);

