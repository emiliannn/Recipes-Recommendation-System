# 🍽️ Recipes Recommendation System

A full-stack web application that delivers personalized recipe suggestions using advanced filtering techniques. Built with a modern tech stack and optimized for performance using parallel computing.

## 🌟 Key Features

### 🤝 Collaborative Filtering
- **User-Based Filtering**: Identifies users with similar preferences and recommends recipes they’ve liked or rated highly.
- **Item-Based Filtering**: Finds recipes similar to those a user has interacted with, based on shared user behavior patterns.

### 📚 Content-Based Filtering
- **Feature Composition**: Each recipe is represented by a combination of its name, description, and tags.
- **TF-IDF Vectorization**: Converts textual features into numerical vectors using Term Frequency–Inverse Document Frequency.
- **Masked TF-IDF Matrix**: Isolates the target recipe’s vector for comparison.
- **Cosine Similarity**: Measures similarity between the target recipe and others:

  Higher scores reflect greater similarity in the recipe’s textual features—such as ingredients, description, and tags—and indicate strong candidates for recommendation.

### ⚡ Parallel Computing with Dask
- Dask distributes recommendation computations across multiple cores, significantly improving performance.
