![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/61aa046b-7ad1-49e1-b95d-f1e227fcebf5)

As a professional with dual expertise in data science and medicine, I embarked on a final project for my data science boot camp at WBS Coding School that combined both disciplines. I was fortunate to obtain medical data from an eye clinic to tackle a common medical issue—cataract.

# Predicting Refractive Error in Cataract Surgery

Cataracts cloud the lens of the eye and are typically treated by replacing the old lens with an artificial one. The new lens must have the correct refractive power to ensure clear vision. Despite using advanced formulas for calculation, refractive errors greater than ±0.5 diopters often occur, leading to the need for additional vision aids.

![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/6854d27c-0fa4-40f3-95c6-8982e08cba79)

Utilizing a dataset of over 5,000 cataract lens replacement surgeries, I developed a machine learning model to predict postoperative refractive errors based on preoperative eye measurements and various lens types and powers. The goal was to create an application that assists surgeons in selecting the optimal lens power to minimize expected refractive errors.

![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/b0dce4b8-2246-44e5-a006-d48d464378be)

### Application Workflow

The application takes a PDF as input, containing precise eye measurements. It then predicts the refractive error for the given lens type and power.

[![Video of App Usage](https://img.youtube.com/vi/IcL_34IfZrU/0.jpg)](https://www.youtube.com/watch?v=IcL_34IfZrU)

Observations reveal that lens power does not have a continuous or linear relationship with refractive error, contrary to expectations based on underlying optical relationships. 

In fact, using a variety of estimators, the performance (measures as R²) did not exceed 0.3 - **making the model unfit for use at this stage**. 


### Challenges Encountered

**Data Loss:** Significant data points were lost during processing—less than 10% of the initial data was usable. Incomplete data was often due to patients being out-clinic with missing surgery outcome measurements or data not being clearly marked within the clinic's system.

**Unrecorded Clinical Decisions:** Often, the reasons for choosing a specific lens type were not documented, possibly because the surgeon had experiential preference for one type over another.

**Algorithm Limitations:** The current machine learning model does not adequately capture the complexities of optical physics, requiring further refinement.

![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/d31ace13-f348-41a5-a4e3-e37d1171b20b)
![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/2d8ef195-5d63-498a-afd8-5a33685711ac)


### Key Learnings

1. Data cleaning is indeed 90% of a data scientist's job!
2. Clinical data storage systems, such as the Entity-Attribute-Value model used here, pose significant challenges for data retrieval, particularly when documentation is sparse.
Clinical data tends to be "dirty" and error-prone, often entered manually, leading to machine-unreadable errors.
3. Information may be incomplete or misleading, with default values frequently appearing in records where not all clinical examination steps are relevant or performed, yet documentation is not updated accordingly.


### Conclusion
While the model is not yet ready for clinical use, the project has provided deep insights into the complexities of working with medical data. Quality data must be reliable, representative, and accessible—a standard that requires strategic forethought during the data collection and storage phases to ensure its utility for future scientific and clinical applications. Further assessments and enhancements are necessary to improve the model's performance, which was beyond the scope of this three-week project.

This endeavor has underscored the importance of thoughtful data management and has equipped me with invaluable experience in the practical challenges of applying machine learning in healthcare settings.
