##CSV to ICS file converter used for calendar tasks. Pulls only relevant columns for population
##Modification of 1 to have all of the necessary optional columns
## This is the one to use!
from ics import Calendar, Event
import pandas as pd
from datetime import datetime

def parse_date_iso(date_str):
    """Parse ISO 8601 date strings into offset-naive datetime."""
    if pd.isna(date_str) or not str(date_str).strip():
        return None
    try:
        # Parse ISO format datetime
        return datetime.fromisoformat(date_str.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        print(f"Could not parse date: {date_str}")
        return None

def clean_string(value):
    """Clean string values and remove square brackets."""
    return str(value).replace("[", "").replace("]", "") if pd.notna(value) else ""

def csv_to_ics(csv_file_path, output_ics_path):
    """Convert CSV to iCalendar (ICS) file."""
    # Load CSV
    df = pd.read_csv(csv_file_path)

    # Create Calendar
    calendar = Calendar()

    for _, row in df.iterrows():
        try:
            # Parse dates
            start_date = parse_date_iso(row["Start Date (date)"])
            end_date = parse_date_iso(row["End Date (date)"])

            # Skip if essential fields are missing
            if not row["Task Name"] or not start_date or not end_date:
                print(f"Skipping event due to missing essential data: {row['Task Name']}")
                continue

            # Skip if end date is before start date
            if end_date < start_date:
                print(f"Error processing event: {row['Task Name']}. End must not be before begin.")
                continue

            # Create Event
            event = Event()
            event.name = row["Task Name"]
            event.begin = start_date
            event.end = end_date

            # Optional fields
            description = []
        
            if pd.notna(row.get("Event Type (drop down)")):
                description.append(f"Event Type: {row['Event Type (drop down)']}")
            if pd.notna(row.get("Attendance Type (drop down)")):
                description.append(f"Attendance: {row['Attendance Type (drop down)']}")
            if pd.notna(row.get("Event Lead (users)")):
                description.append(f"Event Lead: {clean_string(row['Event Lead (users)'])}")
            if pd.notna(row.get("Attendee # (number)")):
                try:
                    attendees = int(float(row["Attendee # (number)"]))
                    description.append(f"Attendees: {attendees}")
                except ValueError:
                    print(f"Invalid attendee number for event: {row['Task Name']}")
            if pd.notna(row.get("Location (location)")):
                description.append(f"Location: {clean_string(row['Location (location)'])}")
            if pd.notna(row.get("Link (short text)")):
                description.append(f"Link: {row['Link (short text)']}")
            if pd.notna(row.get("Description of Project (text)")):
                description.append(f"Description: {row['Description of Project (text)']}")

            event.description = "\n".join(description) if description else None
            event.location = clean_string(row.get("Location (location)", ""))
            event.url = row.get("Link (short text)", None) if isinstance(row.get("Link (short text)"), str) else None

            calendar.events.add(event)

        except Exception as e:
            print(f"Error processing event: {row['Task Name']}. Error: {e}")

    # Write to ICS File
    with open(output_ics_path, "w", encoding="utf-8") as file:
        file.writelines(calendar)

    print(f"ICS file created successfully at {output_ics_path}")

# Example usage
new_csv_path = "D:/ASPIRE ERC Internship Files/Calendar Management 2025/Clickup to Tockify Exports/1 13 Clickup Full View Export/LastImport.csv"
output_ics_path = "D:/ASPIRE ERC Internship Files/Calendar Management 2025/Clickup to Tockify Exports/1 13 Clickup Full View Export/113 Tockify Calendar Export3.ics"


csv_to_ics(new_csv_path, output_ics_path)
