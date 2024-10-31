# GitHub User Data Analysis - Shanghai

- **This project uses the GitHub API to scrape and analyze profiles of users in Shanghai with over 200 followers.**
- **One of the most interesting findings is that hireable developers tend to follow fewer people but have slightly more followers.**
- **Developers should consider keeping their profiles up-to-date and sharing more about themselves to increase visibility and engagement.**

## Project Overview

This project collects and analyzes data from GitHub users in Shanghai who have more than 200 followers. By connecting to the GitHub API, we gather information about user profiles and repositories, which are then saved in two datasets (`users.csv` and `repositories.csv`). Key features of this dataset include user profiles, follower counts, repository information, and development trends among active GitHub users.

## Dataset Features

### Users Dataset (`users.csv`)
- **login**: Unique username of the user on GitHub.
- **name**: Full name of the user (if available).
- **company**: The company they work at, cleaned to ensure readability.
- **location**: User’s location, which helps confirm they are based in Shanghai.
- **email**: Public email address (if shared).
- **hireable**: Whether the user has marked themselves as hireable.
- **bio**: Short bio provided by the user.
- **public_repos**: Total number of public repositories the user has.
- **followers**: Number of followers on GitHub.
- **following**: Number of other users they follow.
- **created_at**: Date the user joined GitHub.

### Repositories Dataset (`repositories.csv`)
- **login**: The user ID associated with the repository.
- **full_name**: Full name of the repository.
- **created_at**: Date the repository was created.
- **stargazers_count**: Number of stars the repository has received.
- **watchers_count**: Number of users watching the repository.
- **language**: Main programming language used in the repository.
- **has_projects**: Whether the repository has projects enabled.
- **has_wiki**: Whether the repository has an active wiki.
- **license_name**: Name of the license under which the repository is distributed.

## Data Scraping and Cleaning Process

1. **API Connection**: The GitHub API is accessed using a personal access token to ensure seamless data retrieval while managing rate limits effectively. The `requests` library is used for all HTTP requests, and pagination is implemented to fetch large datasets.
   
2. **Data Cleaning**: The `company` field is cleaned to remove any leading `@` symbols and whitespace, and all values are converted to uppercase for consistency. Missing values are filled with empty strings for easy handling in further analysis.

3. **Retry Logic**: A retry mechanism with exponential backoff is implemented to handle any temporary network issues or GitHub rate limits, ensuring reliable data fetching even with API restrictions.

## Analysis Summary

Each of the questions was answered by performing specific analyses on the `users.csv` and `repositories.csv` data:

1. **Top 5 Users by Followers**:
   - Sorted users by the `followers` column in descending order and selected the top 5 entries. This helped identify the most followed users in Shanghai, shedding light on popular developers in the region.

2. **Earliest Registered Users**:
   - Converted `created_at` to datetime format and sorted in ascending order. The top 5 entries highlighted the earliest adopters, offering insights into GitHub’s initial traction in Shanghai.

3. **Most Popular Licenses**:
   - Filtered out missing `license_name` values in `repositories.csv` and counted occurrences. This allowed us to identify the most commonly used licenses among Shanghai developers, useful for understanding licensing preferences.

4. **Leader Strength Analysis**:
   - Calculated a `leader_strength` metric as `followers / (1 + following)` for each user, ranking them by influence and leadership within the GitHub community.

5. **Correlation Studies**:
   - Analyzed correlations between `followers` and `public_repos`, `has_projects` and `has_wiki`, and more. This helped uncover interesting patterns, such as the likelihood of hireable users sharing their email.

6. **Programming Language Popularity**:
   - Counted `language` values in `repositories.csv` to determine the most frequently used programming languages, revealing popular technologies among Shanghai-based developers.

7. **Weekend Repository Creation**:
   - Analyzed the `created_at` field in `repositories.csv` to find which users most frequently create repositories on weekends, offering insights into active developers.

## Insights and Recommendations

### Interesting Findings
- **Hireable Developers**: Hireable users in Shanghai tend to have a higher likelihood of sharing their email addresses and often have longer bios, which could attract more attention from potential collaborators or recruiters.
- **Language Popularity**: JavaScript emerged as the most popular programming language, followed by Python, which aligns with trends in web and software development.
- **Repository Projects and Wikis**: Users who enable the “Projects” feature on their repositories also frequently enable the “Wiki” feature, indicating a focus on comprehensive documentation and project management.

### Recommendations for Developers
- **Engage Your Audience**: Developers can increase their visibility by keeping profiles complete and marking themselves as hireable. Having an up-to-date bio and a few active repositories can make a big difference in profile views.
- **Document Your Work**: Enabling repository features like “Wiki” and “Projects” not only helps in managing personal projects but also enhances credibility and clarity for collaborators.

## Running the Script

To run this script locally:
1. **Set Up Environment**: Place your GitHub API token in a `.env` file with the key `GITHUB_TOKEN` for secure access.
2. **Install Requirements**: Install `requests`, `pandas`, and `tenacity` to manage API requests, data manipulation, and retries.
3. **Run**: Execute the script to generate `users.csv` and `repositories.csv` files, which are stored in the main project directory.

```bash
python analysis.py
```

## Final Thoughts

This project provides a window into the world of GitHub developers in Shanghai, offering insights into engagement trends, popular programming languages, and user interaction patterns. By continuously updating profiles and engaging with the community, developers can leverage GitHub to build networks and showcase their skills.

## Future Improvements

- **Extended Analysis**: Additional data points like user contributions or most forked repositories could offer deeper insights into developer activity.
- **Interactive Dashboard**: A dashboard displaying user analytics could provide a visual summary of key findings, making the data more accessible and engaging for stakeholders.
