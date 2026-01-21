# How the Automated Researcher Works

This application is an intelligent agent designed to autonomously conduct web research on any given topic. It follows a structured workflow to search, gather, analyze, and report information.

## Workflow Steps

The research process is orchestrated by a state graph (using `langgraph`) that executes the following steps sequentially:

### 1. Initialization
- **Input**: You provide a research topic (e.g., "Future of Solid State Batteries").
- The system initializes a research state to track progress, errors, and data.

### 2. Search (Search Node)
- **Tool**: Serper API (Google Search).
- **Action**: The agent queries Google with your specific topic.
- **Output**: It retrieves the top search results (default is 3), including titles, links, and snippets.

### 3. Scraping (Scrape Node)
- **Tool**: Custom Scraper Service (using `requests`, `newspaper3k`, or `BeautifulSoup`).
- **Action**: The agent visits each URL found in the search step.
- **Process**:
    - It attempts to download the full HTML content.
    - It parses the main text, removing ads, navigation bars, and boilerplate code.
    - It handles potential access errors (like 403 Forbidden) gracefully.
- **Output**: A collection of cleaned, raw text content from the successful sources.

### 4. Summarization (Summarize Node)
- **Tool**: Large Language Model (OpenAI GPT-4 or Anthropic Claude, depending on config).
- **Action**: The cleaned text from all sources is sent to the LLM with a specific prompt.
- **Prompting**: The AI is instructed to act as a professional research analyst. It is asked to:
    - Write an executive summary.
    - Identify key trends and insights.
    - Highlight statistics.
    - Note conflicting views.
    - Provide actionable takeaways.
- **Output**: A comprehensive, well-structured research briefing in Markdown format.

### 5. Delivery (Upload Node)
- **Tool**: Google Drive API.
- **Action**: The Markdown briefing is converted into a structured document (internally processed).
- **Output**: The final document is uploaded to your specified Google Drive folder (or root).
- **Result**: The application returns a direct link to the uploaded document.

---

## 50 Example Research Titles

You can use any of these titles to test the capabilities of the Automated Researcher:

### Technology & AI
1. "The Impact of Generative AI on Software Engineering Jobs"
2. "Current State of Quantum Computing in 2025"
3. "Advancements in Humanoid Robotics: Tesla Optimus vs Boston Dynamics"
4. "The Future of 6G Networks and Connectivity"
5. "Cybersecurity Threats in the Age of IoT"
6. "Ethical Implications of Brain-Computer Interfaces"
7. "The Rise of Edge Computing in Industrial Automation"
8. "Developments in Solid State Batteries for EVs"
9. "The Role of AI in Personalized Medicine"
10. "Open Source vs Closed Source AI Models: A Comparative Analysis"

### Business & Finance
11. "Global Economic Outlook for Q3 2025"
12. "The Impact of Remote Work on Commercial Real Estate"
13. "Cryptocurrency Regulation Trends in the EU and US"
14. "The Rise of FinTech in Emerging Markets"
15. "Supply Chain Resilience Strategies Post-2020"
16. "The Future of Neobanks vs Traditional Banking"
17. "Impact of ESG Scores on Corporate Investment"
18. "Gig Economy Trends and Labor Laws"
19. "The Subscription Economy: Growth and Saturation"
20. "Micro-SaaS Business Models for 2025"

### Health & Science
21. "CRISPR Technology: Recent Breakthroughs in 2024-2025"
22. "The Gut Microbiome and Mental Health Connection"
23. "Advances in Early Detection of Alzheimer's Disease"
24. "The Future of mRNA Vaccines Beyond COVID-19"
25. "Impact of Microplastics on Human Health"
26. "Vertical Farming: Viability for Urban Food Security"
27. "Lab-Grown Meat: Consumer Acceptance and Regulation"
28. "Space Tourism: Market Projections and Key Players"
29. "Fusion Energy: Progress at ITER and Private Sector"
30. "Telemedicine Adoption Rates Post-Pandemic"

### Society & Culture
31. "The Impact of Social Media Algorithms on Polarization"
32. "Trends in Digital Nomad Visas Globally"
33. "The Evolution of Online Education and Micro-credentials"
34. "Sustainable Fashion: Greenwashing vs Genuine Change"
35. "The Psychology of Metaverse and Virtual Reality"
36. "Urban Planning for Climate Resilient Cities"
37. "Universal Basic Income Experiments: Results so far"
38. "The Future of Public Transportation in Smart Cities"
39. "Impact of Streaming Services on the Film Industry"
40. "Gen Z Consumer Behavior and Purchasing Habits"

### History & Miscellaneous
41. "The History of the Silk Road and Modern Implications"
42. "Comparative Analysis of Ancient Roman vs Modern Engineering"
43. "The Evolution of Coffee Culture Globally"
44. "Psychological Effects of Color in Marketing"
45. "The Science of Sleep Optimization"
46. "History of Venture Capital in Silicon Valley"
47. "The Mathematics of Traffic Flow Optimization"
48. "Biomimicry in Modern Architecture"
49. "The Economics of Hosting the Olympics"
50. "Philosophy of Stoicism in Modern Leadership"
