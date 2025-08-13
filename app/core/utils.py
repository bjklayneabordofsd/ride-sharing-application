from django.db import connection
from django.contrib.auth import get_user_model

User = get_user_model()

def get_long_trips_report():
    """
    Get report of trips that took more than 1 hour from pickup to dropoff.
    Groups by month and driver.
    """
    
    # Get the actual table name from the User model
    user_table = User._meta.db_table
    
    # SQLite compatible SQL - handles both patterns
    sql = f"""
    SELECT 
        strftime('%Y-%m', pickup_event.created_at) as month,
        driver.first_name || ' ' || driver.last_name as driver_name,
        driver.id_user as driver_id,
        COUNT(DISTINCT r.id_ride) as trip_count
    FROM ride r
    INNER JOIN ride_event pickup_event ON r.id_ride = pickup_event.id_ride 
        AND (pickup_event.description LIKE "%to 'pickup'%" 
             OR pickup_event.description LIKE "Ride created with status 'pickup'%")
    INNER JOIN ride_event dropoff_event ON r.id_ride = dropoff_event.id_ride 
        AND dropoff_event.description LIKE "%to 'dropoff'%"
    INNER JOIN {user_table} driver ON r.id_driver = driver.id_user
    WHERE 
        (julianday(dropoff_event.created_at) - julianday(pickup_event.created_at)) * 24 > 1
    GROUP BY strftime('%Y-%m', pickup_event.created_at), driver.id_user
    ORDER BY month DESC, driver_name
    """
    
    with connection.cursor() as cursor:
        cursor.execute(sql)
        columns = [col[0] for col in cursor.description]
        
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


def get_long_trips_report_formatted():
    """Get the report formatted as a string for display."""
    try:
        results = get_long_trips_report()
        
        if not results:
            return "No trips found that took more than 1 hour."
        
        output = "Month\t\tDriver\t\t\tCount of Trips > 1 hr\n"
        output += "-" * 60 + "\n"
        
        for row in results:
            output += f"{row['month']}\t\t{row['driver_name']:<20}\t{row['trip_count']}\n"
        
        return output
    except Exception as e:
        return f"Error generating report: {str(e)}"