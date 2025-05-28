import matplotlib.pyplot as plt
import numpy as np

# Sample data (scores from 1-10)
categories = ['Technical Knowledge', 'Communication', 'Problem Solving', 
              'Cultural Fit', 'Experience']
values = [8, 6, 9, 7, 5]  # Score for each category

# Create the radar chart
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, polar=True)

# Number of categories
N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]  # Close the loop

# Add the values for each category
values += values[:1]  # Close the loop
ax.plot(angles, values, linewidth=2, linestyle='solid')
ax.fill(angles, values, alpha=0.25)

# Add category labels
plt.xticks(angles[:-1], categories)

# Add value labels (0-10 scale)
ax.set_rlabel_position(0)
plt.yticks([2, 4, 6, 8, 10], ['2', '4', '6', '8', '10'], color="grey", size=7)
plt.ylim(0, 10)

plt.title('Interview Performance Evaluation', size=15)
plt.savefig('interview_radar.png')
plt.show()