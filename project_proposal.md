# MenuMatch AI

## Project Overview
MenuMatch AI is a mobile-first dining assistant that helps users decide what to order at any restaurant. Users snap a photo of a physical menu, and the app uses OCR to extract dish names and prices, GPS to identify the restaurant, and NLP to analyze online review sentiment — then delivers categorized dish recommendations tailored to the user's tastes and dietary preferences.

## Problem Statement
Diners face decision paralysis when confronted with unfamiliar menus, especially while traveling or exploring new neighborhoods. Reading dozens of Yelp or Google reviews is time-consuming, and star ratings alone don't reveal which specific dishes are worth ordering. Tourists and locals alike waste money on mediocre items while missing the restaurant's signature dishes.

## Target Audience
Food-loving millennials and Gen Z diners, travelers exploring new cities, and health-conscious eaters who want quick, trustworthy order recommendations without scrolling through lengthy review threads.

## Features

### 1. OCR Menu Scan
Capture a photo of any printed or digital menu. On-device and cloud OCR extract dish names, descriptions, and prices into a structured list the user can browse and filter.

### 2. GPS Restaurant Identification
Automatic GPS geolocation matches the user's coordinates to nearby restaurants in Google Places / Foursquare APIs, linking the scanned menu to the correct venue and its review corpus.

### 3. Review Sentiment Analysis
NLP pipelines scrape and analyze recent Google, TripAdvisor, and social media reviews. Sentiment scores and keyword extraction surface which dishes reviewers praise, criticize, or mention most often.

### 4. Categorized Recommendations
The recommendation engine groups dishes into actionable categories — **Must Try**, **Safe Bet**, **Hidden Gem**, and **Skip It** — based on sentiment scores, mention frequency, and the user's stated preferences (spicy, vegetarian, budget, etc.).

## Expected Outcomes
- Reduce average menu decision time from 5+ minutes to under 30 seconds.
- Increase diner satisfaction by surfacing crowd-validated dishes instead of guesswork.
- Provide restaurants with anonymized aggregate insights on which menu items drive positive sentiment.
