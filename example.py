from FinTable import AnnualReport

# Path to annual report pdf file
file = "AR/guaranty-trust-bank-ltd_2016.pdf"

# Initialize AnnualReport class
comp = AnnualReport(file=file, bank=True)

# Print Statement of Financial Position
print(comp.report(type="SOFP"))

# Save Statement of Profit or Loss to csv file
comp.save_report(type="SOPL")


