-- Indexes for frequently used queries on the equipment table
CREATE INDEX idx_equipment_availability ON equipment(status);
CREATE INDEX idx_equipment_category_status ON equipment(category_id, status);
CREATE INDEX idx_equipment_location_status ON equipment(location_id, status);
CREATE INDEX idx_equipment_maintenance_date ON equipment(last_maintenance_date);
CREATE INDEX idx_equipment_rental_rates ON equipment(daily_rental_rate, weekly_rental_rate, monthly_rental_rate);
CREATE INDEX idx_equipment_condition ON equipment(condition_rating);

-- Indexes for customers table
CREATE INDEX idx_customer_location ON customers(city, state);
CREATE INDEX idx_customer_name ON customers(company_name);
CREATE INDEX idx_customer_contact ON customers(contact_person);
CREATE INDEX idx_customer_credit ON customers(credit_limit, is_active);

-- Indexes for rentals table
CREATE INDEX idx_rental_dates ON rentals(rental_date, expected_return_date, actual_return_date);
CREATE INDEX idx_rental_status_dates ON rentals(status, rental_date, expected_return_date);
CREATE INDEX idx_rental_customer_status ON rentals(customer_id, status);
CREATE INDEX idx_rental_location_dates ON rentals(pickup_location_id, rental_date);
CREATE INDEX idx_overdue_rentals ON rentals(expected_return_date)
    WHERE actual_return_date IS NULL AND status = 'Active';

-- Indexes for rental_items table
CREATE INDEX idx_rental_items_hourly_usage ON rental_items(hourly_usage);
CREATE INDEX idx_rental_items_damages ON rental_items(damages_reported);
CREATE INDEX idx_rental_item_equipment_rental ON rental_items(equipment_id, rental_id);

-- Indexes for maintenance_records table
CREATE INDEX idx_maintenance_type_date ON maintenance_records(maintenance_type, maintenance_date);
CREATE INDEX idx_maintenance_next_date ON maintenance_records(next_maintenance_date);
CREATE INDEX idx_maintenance_status ON maintenance_records(status);
CREATE INDEX idx_equipment_upcoming_maintenance ON maintenance_records(equipment_id, next_maintenance_date)
    WHERE status != 'Completed';

-- Indexes for payments table
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_payments_method ON payments(payment_method);
CREATE INDEX idx_payments_refund ON payments(is_refund);
CREATE INDEX idx_payments_rental_date ON payments(rental_id, payment_date);

-- Indexes for employees table
CREATE INDEX idx_employee_position ON employees(position);
CREATE INDEX idx_employee_name ON employees(last_name, first_name);
CREATE INDEX idx_employee_certification ON employees USING GIN(certification);

-- Indexes for employee_locations table
CREATE INDEX idx_employee_location_dates ON employee_locations(start_date, end_date);
-- Modified to remove CURRENT_DATE which is not IMMUTABLE
CREATE INDEX idx_current_assignments ON employee_locations(employee_id, location_id, end_date);
-- Alternative approach using a static date comparison that you can update periodically
-- CREATE INDEX idx_current_assignments_alt ON employee_locations(employee_id, location_id)
--    WHERE end_date IS NULL;
