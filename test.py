import matplotlib.pyplot as plt

# Data
categories = ['Orders', 'Shipments', 'Remaining Storage']
percentages = [70, 50, 30]

# Create horizontal bar chart
plt.figure(figsize=(10, 5))
plt.barh(categories, percentages, color=['blue', 'green', 'red'])

# Add annotations and labels
for index, value in enumerate(percentages):
    plt.text(value, index, f'{value}%')

plt.xlabel('Percentage')
plt.title('Warehouse Utilization')
plt.xlim(0, 100)  # Set the x limits to be from 0 to 100 for percentage
plt.show()
