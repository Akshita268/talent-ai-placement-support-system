# ai_modules/roadmap_generator.py

ROLE_ROADMAP_DETAILS = {
    "ML Engineer": {
        "required_skills": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Pandas", "Scikit-Learn"],
        "interview_topics": ["Bias-Variance Tradeoff", "Overfitting vs Underfitting", "CNN vs RNN vs Transformers", "Loss functions & Optimizers", "Regularization techniques"],
        "weekly": [
            "Week 1: Fundamentals of Mathematics & Statistics (Linear Algebra, Calculus, Probability)",
            "Week 2: Advanced NumPy & Pandas data processing and analysis pipelines",
            "Week 3: Classical ML algorithms with Scikit-Learn (regression, classification, evaluation metrics)",
            "Week 4: Deep Learning basics with PyTorch (neural networks, backpropagation, activation functions)",
            "Week 5: Specialization topics: CNNs for Computer Vision, NLP basics, or Vector DBs"
        ],
        "monthly": [
            "Month 1: Focus on mathematical theory, algorithm design, and simple tabular models.",
            "Month 2: Move to PyTorch/TensorFlow, train deep learning networks, and study CNN architectures.",
            "Month 3: Learn model deployment (Flask/FastAPI APIs, Docker, ONNX) and model profiling."
        ],
        "projects": [
            "Project 1: Predict housing prices using XGBoost and deploy as a simple Flask API.",
            "Project 2: Train a YOLOv8 object detection model on custom data and run inference on video streams.",
            "Project 3: Build a semantic search engine using all-MiniLM-L6-v2 embeddings and a vector database (SQLite/FAISS)."
        ],
        "resources": [
            "Coursera: Machine Learning Specialization by Andrew Ng",
            "Kaggle Learning: Intro to Deep Learning & TensorFlow",
            "Fast.ai: Practical Deep Learning for Coders",
            "Book: Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow"
        ]
    },
    "Backend Developer": {
        "required_skills": ["Python", "Flask/FastAPI/Django", "SQL & Databases", "REST APIs", "Docker", "Data Structures & Algorithms"],
        "interview_topics": ["Database Normalization & Indexing", "Caching strategies with Redis", "Concurrency in Python & GIL", "REST API architecture", "Thread vs Process"],
        "weekly": [
            "Week 1: Advanced Python (generators, decorators, concurrency, async/await)",
            "Week 2: Web Frameworks (Flask/Django/FastAPI routing, requests, middleware)",
            "Week 3: Databases & SQL (complex joins, indexing, query execution optimization, migrations)",
            "Week 4: RESTful API design standards, security best practices (JWT, OAuth), and unit testing",
            "Week 5: Containerization basics using Docker and multi-service orchestration with Docker Compose"
        ],
        "monthly": [
            "Month 1: Master Python core architectures, server routing, and simple SQLite CRUD APIs.",
            "Month 2: Deep dive into Postgres/MySQL, database normalization, caching (Redis), and background tasks (Celery).",
            "Month 3: Study system design (load balancers, message queues like RabbitMQ/Kafka, Dockerized deployment)."
        ],
        "projects": [
            "Project 1: Develop a fully-featured REST API for an E-commerce system with auth, reviews, and SQLite.",
            "Project 2: Create a real-time messaging server using Flask-SocketIO and Redis for message queuing.",
            "Project 3: Architect a multi-container microservice system orchestrated via Docker Compose with an API gateway."
        ],
        "resources": [
            "Real Python: Flask & Django Web Development Tutorials",
            "Designing Data-Intensive Applications by Martin Kleppmann",
            "RESTful API Design Best Practices (HTTP Specs)",
            "Docker Docs: Getting Started Guide & Compose Reference"
        ]
    },
    "Frontend Developer": {
        "required_skills": ["HTML5/CSS3", "JavaScript (ES6+)", "React.js", "Tailwind CSS", "Bootstrap 5", "State Management (Redux/Context)"],
        "interview_topics": ["DOM manipulation & Virtual DOM", "React Lifecycle & Hooks", "CSS Flexbox & Grid layouts", "Async JavaScript & Event Loop", "Frontend performance optimization"],
        "weekly": [
            "Week 1: Semantic HTML5, CSS layout systems (Flexbox, Grid, custom properties)",
            "Week 2: Modern JavaScript (ES6+, DOM manipulation, Event loop, Async/Await)",
            "Week 3: React Fundamentals (JSX, components lifecycle, state, props, custom hooks)",
            "Week 4: State Management (Context API, Redux Toolkit) and UI libraries (Tailwind, Bootstrap 5)",
            "Week 5: Frontend tooling (Vite, Webpack), performance optimization (lazy loading, CDN usage), and SEO"
        ],
        "monthly": [
            "Month 1: Build complex responsive layouts with CSS animations and vanilla JS interactions.",
            "Month 2: Learn React hook architectures, nested routing, dynamic data fetching, and state control.",
            "Month 3: Build interactive dashboards, integrate complex charts, and run lighthouse performance audits."
        ],
        "projects": [
            "Project 1: Build a responsive landing page mockup using glassmorphism, CSS gradients, and animations.",
            "Project 2: Build a personal portfolio dashboard in React showcasing resume metrics, dynamically loaded via APIs.",
            "Project 3: Create a complex Kanban Task Board with drag-and-drop support, dark/light theme, and localStorage sync."
        ],
        "resources": [
            "MDN Web Docs: CSS Layouts, Grid, and Flexbox Guides",
            "javascript.info: Modern JavaScript Tutorials",
            "React Docs: Beta Hooks & State Management Guide",
            "Tailwind CSS Documentation & UI Component Guides"
        ]
    },
    "Data Analyst": {
        "required_skills": ["SQL (joins, window functions)", "Excel", "Tableau/Power BI", "Python (Pandas, NumPy)", "Statistics & Data Visualization"],
        "interview_topics": ["SQL Window Functions & CTEs", "Data cleaning & handling missing values", "Hypothesis testing & p-values", "Dashboard design principles", "Correlation vs Causation"],
        "weekly": [
            "Week 1: Advanced SQL queries (CTE, window functions, aggregations, subqueries)",
            "Week 2: Python for Data Analysis (Pandas manipulation, NumPy arrays)",
            "Week 3: Data Visualization libraries (Matplotlib, Seaborn) and Storytelling with Data",
            "Week 4: Business Intelligence tools (Tableau or Power BI dashboards creation)",
            "Week 5: Descriptive and inferential statistics (hypothesis testing, distribution analysis)"
        ],
        "monthly": [
            "Month 1: Master SQL query generation and design robust relational database schemas.",
            "Month 2: Automate data cleaning pipelines in Python and build clean statistical visualization charts.",
            "Month 3: Design interactive BI dashboards representing sales funnel conversion data."
        ],
        "projects": [
            "Project 1: Write an automated Python script to scrape, clean, and analyze job posting trends.",
            "Project 2: Design an interactive Tableau dashboard tracking business revenue growth across regions.",
            "Project 3: Conduct a cohort analysis on user retention using PostgreSQL window functions."
        ],
        "resources": [
            "SQLZoo & LeetCode: SQL Practice Problems",
            "Pandas & NumPy Reference Documentation",
            "Tableau Training: Free Desktop & Server Tutorials",
            "Storytelling with Data by Cole Nussbaumer Knaflic"
        ]
    },
    "Full Stack Developer": {
        "required_skills": ["Frontend (HTML/CSS/JS/React)", "Backend (Flask/Node.js/Python)", "Databases (SQL/NoSQL)", "REST APIs", "Docker"],
        "interview_topics": ["End-to-end user authentication (JWT/OAuth)", "State synchronization between front & back", "Database query optimization", "CORS & web security basics", "Full stack deployment pipeline"],
        "weekly": [
            "Week 1: Modern JavaScript/TypeScript & responsive styling standards (Tailwind, CSS Grid)",
            "Week 2: Backend foundation with Flask or Node.js/Express, routing and DB schema setup",
            "Week 3: React frontend development, connecting state to backend REST APIs",
            "Week 4: Database query optimization, migrations, session cookies and JWT authentication",
            "Week 5: Complete deployment configuration using Docker on cloud platforms"
        ],
        "monthly": [
            "Month 1: Build secure responsive CRUD applications connecting React to a local Flask database.",
            "Month 2: Add payment integration, background emails, caching, and deploy containers.",
            "Month 3: Focus on system design, microservices, load balancing, and scaling database reads."
        ],
        "projects": [
            "Project 1: Create a Job Portal website where students upload PDFs, parsing them to score relevance.",
            "Project 2: Design a collaboration dashboard with real-time kanban boards, live chat, and file sharing.",
            "Project 3: Build a custom SaaS product with subscription auth, usage trackers, and dashboard charts."
        ],
        "resources": [
            "The Odin Project: Full Stack JavaScript Course",
            "Full Stack Open: Deep Dive Into Modern Web Development",
            "Backend Systems Design Guide by ByteByteGo",
            "JWT.io & OAuth 2.0 Web Authentication Architecture Standards"
        ]
    }
}

def generate_roadmap(target_role, missing_skills=None, average_scores=None):
    """
    Generates a dictionary containing a weekly curriculum, monthly targets, tailored projects,
    required skills, interview topics, and learning resources.
    """
    # Standardize target role to matches
    matched_role = "Backend Developer"
    target_role_lower = (target_role or "").lower()
    for role in ROLE_ROADMAP_DETAILS:
        if role.lower() in target_role_lower or target_role_lower in role.lower():
            matched_role = role
            break
            
    details = ROLE_ROADMAP_DETAILS[matched_role]
    
    # Custom adjustments based on missing skills
    weekly_plan = list(details["weekly"])
    monthly_plan = list(details["monthly"])
    projects = list(details["projects"])
    
    if missing_skills:
        # Normalize and filter out empty items
        clean_missing = [s.strip() for s in missing_skills if s.strip()]
        if clean_missing:
            skills_str = ", ".join(clean_missing)
            weekly_plan.append(f"Week 6 (Special Focus): Work specifically on mastering missing skills: {skills_str}")
            monthly_plan.append(f"Month 4: Create a dedicated open-source repository integrating: {skills_str}")
        
    return {
        "role": matched_role,
        "weekly": weekly_plan,
        "monthly": monthly_plan,
        "projects": projects,
        "required_skills": details.get("required_skills", []),
        "interview_topics": details.get("interview_topics", []),
        "resources": details.get("resources", [])
    }
