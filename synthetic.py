import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Seed for reproducibility (optional)
random.seed(42)
np.random.seed(42)


class CarePortalDataGenerator:
    def __init__(self):
        self.need_categories = {
            "Housing": ["bed", "mattress", "bedding", "furniture", "rent assistance"],
            "Food": ["groceries", "meal", "food pantry items", "baby formula"],
            "Clothing": ["winter coat", "shoes", "school clothes", "baby clothes"],
            "School Supplies": [
                "backpack",
                "notebooks",
                "pencils",
                "calculator",
                "school uniforms",
            ],
            "Transportation": [
                "gas card",
                "bus pass",
                "car repair",
                "uber/lyft credit",
            ],
            "Childcare": ["diapers", "wipes", "car seat", "crib", "stroller"],
            "Utilities": ["electric bill", "water bill", "heating assistance"],
            "Medical": ["prescription assistance", "medical supplies", "first aid"],
        }

        self.urgency_levels = ["Low", "Medium", "High", "Critical"]

        self.cities = [
            {
                "name": "Atlanta",
                "state": "GA",
                "zips": ["30301", "30302", "30303", "30304", "30305"],
            },
            {
                "name": "Charlotte",
                "state": "NC",
                "zips": ["28201", "28202", "28203", "28204", "28205"],
            },
            {
                "name": "Nashville",
                "state": "TN",
                "zips": ["37201", "37202", "37203", "37204", "37205"],
            },
            {
                "name": "Birmingham",
                "state": "AL",
                "zips": ["35201", "35202", "35203", "35204", "35205"],
            },
        ]

        self.church_names = [
            "Grace Community Church",
            "First Baptist Church",
            "Hope Fellowship",
            "New Life Church",
            "Trinity Methodist",
            "Cornerstone Church",
            "Redemption Church",
            "Faith Assembly",
            "Crossroads Church",
            "Harvest Church",
            "The Bridge Church",
            "Lighthouse Church",
        ]

        self.statuses = [
            "Requested",
            "Matched",
            "In Progress",
            "Fulfilled",
            "Closed",
            "Cancelled",
        ]

    def generate_donors(self, n=150):
        """Generate donor dataset"""
        donors = []
        categories = list(self.need_categories.keys())

        for i in range(1, n + 1):
            city = random.choice(self.cities)
            num_specialties = random.randint(1, 3)
            specialties = random.sample(categories, num_specialties)

            donors.append(
                {
                    "donor_id": f"D{str(i).zfill(4)}",
                    "name": f"Donor {i}",
                    "email": f"donor{i}@example.com",
                    "phone": f"555-{random.randint(1000, 9999)}",
                    "city": city["name"],
                    "state": city["state"],
                    "zip_code": random.choice(city["zips"]),
                    "specialties": ";".join(specialties),
                    "avg_response_time_hours": random.randint(2, 50),
                    "total_fulfilled": random.randint(0, 50),
                    "last_donation_date": (
                        datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364))
                    ).strftime("%Y-%m-%d"),
                    "active": random.random() > 0.1,
                }
            )

        return pd.DataFrame(donors)

    def generate_churches(self, n=30):
        """Generate church dataset"""
        churches = []

        for i in range(1, n + 1):
            city = random.choice(self.cities)
            base_name = self.church_names[i % len(self.church_names)]
            name = (
                f"{base_name} - {city['name']}"
                if i > len(self.church_names)
                else base_name
            )

            churches.append(
                {
                    "church_id": f"C{str(i).zfill(3)}",
                    "name": name,
                    "city": city["name"],
                    "state": city["state"],
                    "zip_code": random.choice(city["zips"]),
                    "contact_name": f"Pastor {chr(65 + (i % 26))}",
                    "contact_email": f"contact{i}@church.org",
                    "contact_phone": f"555-{random.randint(1000, 9999)}",
                    "active_volunteers": random.randint(10, 60),
                    "total_fulfilled": random.randint(0, 100),
                }
            )

        return pd.DataFrame(churches)

    def generate_needs(self, n=500, donors_df=None, churches_df=None):
        """Generate needs/requests dataset"""
        needs = []

        for i in range(1, n + 1):
            category = random.choice(list(self.need_categories.keys()))
            item = random.choice(self.need_categories[category])
            city = random.choice(self.cities)
            request_date = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364))
            status = random.choice(self.statuses)

            matched_date = None
            fulfilled_date = None
            assigned_donor = None
            assigned_church = None

            # Add dates and assignments for matched/fulfilled needs
            if status in ["Matched", "In Progress", "Fulfilled", "Closed"]:
                matched_date = request_date + timedelta(hours=random.randint(1, 48))
                if donors_df is not None:
                    assigned_donor = random.choice(donors_df["donor_id"].tolist())
                if churches_df is not None:
                    assigned_church = random.choice(churches_df["church_id"].tolist())

                if status in ["Fulfilled", "Closed"]:
                    fulfilled_date = matched_date + timedelta(
                        hours=random.randint(1, 120)
                    )

            needs.append(
                {
                    "need_id": f"N{str(i).zfill(5)}",
                    "request_date": request_date.strftime("%Y-%m-%d"),
                    "category": category,
                    "item_description": item,
                    "quantity": random.randint(1, 6),
                    "urgency": random.choice(self.urgency_levels),
                    "family_id": f"F{str(random.randint(1, 200)).zfill(4)}",
                    "city": city["name"],
                    "state": city["state"],
                    "zip_code": random.choice(city["zips"]),
                    "status": status,
                    "matched_date": matched_date.strftime("%Y-%m-%d")
                    if matched_date
                    else None,
                    "fulfilled_date": fulfilled_date.strftime("%Y-%m-%d")
                    if fulfilled_date
                    else None,
                    "assigned_donor_id": assigned_donor,
                    "assigned_church_id": assigned_church,
                    "notes": "Urgent need for family in crisis"
                    if random.random() > 0.7
                    else "",
                }
            )

        return pd.DataFrame(needs)

    def generate_fulfillments(self, needs_df):
        """Generate fulfillment history from fulfilled needs"""
        fulfilled_needs = needs_df[
            needs_df["status"].isin(["Fulfilled", "Closed"])
        ].copy()

        fulfillments = []
        for idx, need in fulfilled_needs.iterrows():
            request_time = pd.to_datetime(need["request_date"])
            matched_time = pd.to_datetime(need["matched_date"])
            fulfilled_time = pd.to_datetime(need["fulfilled_date"])

            response_hours = max(
                1, int((matched_time - request_time).total_seconds() / 3600)
            )
            fulfillment_hours = max(
                1, int((fulfilled_time - matched_time).total_seconds() / 3600)
            )

            fulfillments.append(
                {
                    "fulfillment_id": f"FH{str(len(fulfillments) + 1).zfill(5)}",
                    "need_id": need["need_id"],
                    "donor_id": need["assigned_donor_id"],
                    "church_id": need["assigned_church_id"],
                    "request_date": need["request_date"],
                    "matched_date": need["matched_date"],
                    "fulfilled_date": need["fulfilled_date"],
                    "response_time_hours": response_hours,
                    "fulfillment_time_hours": fulfillment_hours,
                    "category": need["category"],
                    "donor_rating": random.randint(4, 5),
                }
            )

        return pd.DataFrame(fulfillments)

    def generate_all(self, n_donors=150, n_churches=30, n_needs=500):
        """Generate complete dataset"""
        print("Generating donors...")
        donors = self.generate_donors(n_donors)

        print("Generating churches...")
        churches = self.generate_churches(n_churches)

        print("Generating needs...")
        needs = self.generate_needs(n_needs, donors, churches)

        print("Generating fulfillment history...")
        fulfillments = self.generate_fulfillments(needs)

        print("\nDataset generated successfully!")
        print(f"  - {len(donors)} donors")
        print(f"  - {len(churches)} churches")
        print(f"  - {len(needs)} needs")
        print(f"  - {len(fulfillments)} fulfillments")

        return {
            "donors": donors,
            "churches": churches,
            "needs": needs,
            "fulfillments": fulfillments,
        }

    def save_to_csv(self, data_dict, output_dir="./"):
        """Save all datasets to CSV files"""
        for name, df in data_dict.items():
            filename = f"{output_dir}{name}.csv"
            df.to_csv(filename, index=False)
            print(f"Saved {filename}")


# Usage Example
if __name__ == "__main__":
    generator = CarePortalDataGenerator()

    # Generate all data
    data = generator.generate_all(n_donors=150, n_churches=30, n_needs=500)

    # Save to CSV files
    generator.save_to_csv(data)

    # Display sample data
    print("\n--- Sample Donor Data ---")
    print(data["donors"].head())

    print("\n--- Sample Needs Data ---")
    print(data["needs"].head())

    print("\n--- Data Summary ---")
    print(f"Need Status Distribution:\n{data['needs']['status'].value_counts()}")
    print(f"\nCategory Distribution:\n{data['needs']['category'].value_counts()}")
