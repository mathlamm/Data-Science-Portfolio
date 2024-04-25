![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Spotipy](https://img.shields.io/badge/Spotipy-1DB954?style=for-the-badge&logo=spotify&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)

## Project Summary:
The goal of this project was to introduce automation to the playlist curation process at Moosic, a startup providing expertly crafted playlists. By leveraging unsupervised machine learning techniques, 
I created clusters of similar songs from a dataset of audio features collected via the Spotify API. These clusters served as the basis for new playlists. 
The task involved evaluating whether Spotify's audio features can effectively capture the "mood" of a song—a quality typically assessed by human experts—and determining if the K-Means algorithm is suitable for 
generating playlists that resonate with listeners.

## Techniques Used:
- **Unsupervised Machine Learning**: Utilized the K-Means clustering algorithm to group songs with similar audio features, paving the way for automated playlist generation.
- **Data Cleaning and Preprocessing**: Performed necessary steps to clean the dataset for optimal machine learning performance, including handling missing values and outliers.
- **Feature Scaling**: Applied scaling techniques to normalize the range of audio feature variables, ensuring that no single feature would dominate the clustering process due to its scale.
- **Principal Component Analysis (PCA)**: Implemented PCA to reduce the dimensionality of the dataset, enhancing computational efficiency and potentially improving the clustering by highlighting the most relevant variations in the data.
- **Integration with OpenAI API**: Made use of OpenAI's API to categorize songs into genres, adding another layer of sophistication to the clustering process by considering the genre as a potential feature or label for assessment.

The end result was a 5-min presentation showing the result of my prototype that uses data-driven insights to automate the playlist curation process. The success of this prototype has been evaluated based on its ability to cluster songs that align with human judgments of similarity and mood.

## Files:
- main code in *Moosic_Playlists.ipynb*
- tables see *.csv* and *.pkl* files

## Presentation
![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/5da6b2cf-35d9-4b9f-a1a7-5e0a576a1e3f)
![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/5340d580-ef66-49ab-81c8-fa9c00a855ad)
![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/78db7855-347f-4568-bdd4-fcf5bb2683e2)
![image](https://github.com/mathlamm/Data-Science-Portfolio/assets/43820711/5309777d-4f05-4921-880a-1732e1733bd6)

