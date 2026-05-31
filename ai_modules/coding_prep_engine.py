# ai_modules/coding_prep_engine.py

CATEGORIES = {
    "DSA": {
        "title": "Data Structures & Algorithms",
        "icon": "bi-code-square",
        "description": "Master core structures, traversal methods, complexity optimization, and algorithmic patterns.",
        "topics": [
            "Arrays", "Strings", "Linked Lists", "Stacks", "Queues", "HashMap",
            "Trees", "BST", "Heaps", "Graphs", "Recursion", "Backtracking",
            "Greedy", "Sliding Window", "Two Pointer", "Binary Search",
            "Dynamic Programming", "Bit Manipulation"
        ]
    },
    "Databases": {
        "title": "Database Systems & Design",
        "icon": "bi-database-fill",
        "description": "Revise relational schemas, SQL querying, transactional integrity, NoSQL setups, and database scaling.",
        "topics": [
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Cassandra",
            "Neo4j", "ArangoDB", "Database Design", "Normalization", "Transactions", "Indexing"
        ]
    },
    "Programming Languages": {
        "title": "Programming Core Concepts",
        "icon": "bi-file-earmark-code-fill",
        "description": "Deep dive into OOP pillars, memory management, garbage collection, and runtime processes of popular languages.",
        "topics": [
            "Java", "Python", "JavaScript", "C", "C++"
        ]
    },
    "System Design": {
        "title": "System Design & Architecture",
        "icon": "bi-diagram-3-fill",
        "description": "Learn to design scalable, distributed, highly available, and reliable web applications.",
        "topics": [
            "Load Balancing", "Caching", "CDN", "Microservices", "Database Sharding",
            "Message Queues", "Rate Limiting", "API Gateway"
        ]
    },
    "CS Fundamentals": {
        "title": "Core Computer Science",
        "icon": "bi-cpu-fill",
        "description": "Study CPU scheduling, memory management, protocol layers, networking models, and software engineering processes.",
        "topics": [
            "Operating Systems", "DBMS", "Computer Networks", "OOP", "SDLC", "Cloud Basics"
        ]
    },
    "Company Wise Questions": {
        "title": "Company Specific Preparation",
        "icon": "bi-building-fill",
        "description": "Prepare specifically for interview patterns, style guides, and frequently asked patterns of top tech firms.",
        "topics": [
            "Google", "Microsoft", "Amazon", "Adobe", "Oracle",
            "Infosys", "TCS", "Accenture", "Wipro", "Cognizant"
        ]
    }
}

# Pre-written premium datasets for key topics
PREMIUM_TOPICS = {
    "Sliding Window": {
        "difficulty": "Medium",
        "importance": "Extremely High (Asked in 45% of top tech coding rounds)",
        "explanation": "The Sliding Window pattern is used to perform a required operation on a specific window size of a given array or linked list, such as finding the longest subarray containing all 1s. It avoids nested loops and reduces O(N^2) complexities down to linear time O(N) by maintaining a running window rather than recalculating from scratch.",
        "faqs": [
            {
                "q": "When should I use the sliding window pattern?",
                "a": "Use this pattern when you are asked to find a subarray, substring, or sublist that satisfies a certain condition (e.g., maximum sum, longest unique substring) and the elements are sequential."
            },
            {
                "q": "What is the difference between fixed and variable window size?",
                "a": "In a fixed window (e.g., Max Sum Subarray of size K), the window size stays constant, and we slide it by incrementing both bounds. In a variable window (e.g., Longest Substring with K Unique Characters), we expand the right boundary until the condition is violated, then shrink from the left boundary to recover validity."
            }
        ],
        "mistakes": [
            "Off-by-one errors when updating window bounds (left and right indices).",
            "Failing to update auxiliary state (like element count maps) when sliding or shrinking the window.",
            "Incorrect condition checking that leads to infinite loops inside the expansion/shrinking logic."
        ],
        "tips": [
            "Always visualize the window bounds using two pointer variables (e.g., 'start' and 'end').",
            "Write a dry run using a simple test case with a window size of 2 or 3.",
            "Use a Hash Map or Frequency Array to keep track of characters or frequencies inside the active window."
        ],
        "model_answer": {
            "title": "Problem: Find the Maximum Sum Subarray of Size K",
            "language": "Python",
            "code": """def max_sub_array_of_size_k(k, arr):
    max_sum, window_sum = 0, 0
    window_start = 0

    for window_end in range(len(arr)):
        window_sum += arr[window_end]  # Add the next element
        
        # Slide the window if we've hit size 'k'
        if window_end >= k - 1:
            max_sum = max(max_sum, window_sum)
            window_sum -= arr[window_start]  # Subtract the element going out
            window_start += 1  # Slide the window ahead
            
    return max_sum

# Time Complexity: O(N)
# Space Complexity: O(1)"""
        }
    },
    "SQL": {
        "difficulty": "Easy to Medium",
        "importance": "Mandatory (Asked in almost all backend, data science, and analyst interviews)",
        "explanation": "Structured Query Language (SQL) is the standard language for relational database management. SQL allows users to query, update, delete, and insert database records, as well as define schemas and control access permissions. Query optimization (writing indexes, avoiding full-table scans, using appropriate joins) is a major focus in developer interviews.",
        "faqs": [
            {
                "q": "What is the difference between WHERE and HAVING clauses?",
                "a": "WHERE filters rows before any groupings are made, while HAVING filters group aggregates (used in conjunction with GROUP BY)."
            },
            {
                "q": "What is the difference between INNER, LEFT, RIGHT, and FULL Joins?",
                "a": "INNER JOIN returns records with matching values in both tables. LEFT JOIN returns all records from the left table and matched from the right. RIGHT JOIN returns the inverse. FULL JOIN returns all records when there is a match in either table."
            }
        ],
        "mistakes": [
            "Using SELECT * in production queries, which increases network overhead.",
            "Performing operations or function calls on indexed columns inside the WHERE clause, which disables index scanning (SARGability issues).",
            "Forgetting to index foreign keys, leading to slow JOIN executions."
        ],
        "tips": [
            "Understand the Logical Query Processing Order: FROM -> JOIN -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT.",
            "Practice writing correlated subqueries vs Common Table Expressions (CTEs) for readability.",
            "Use EXPLAIN ANALYZE to check execution plans and find bottlenecks."
        ],
        "model_answer": {
            "title": "Problem: Find the Second Highest Salary from an Employee Table",
            "language": "SQL",
            "code": """-- Standard ANSI SQL solution using subquery
SELECT MAX(Salary) AS SecondHighestSalary
FROM Employee
WHERE Salary < (SELECT MAX(Salary) FROM Employee);

-- Alternative solution using LIMIT and OFFSET (MySQL/PostgreSQL)
SELECT Salary
FROM Employee
ORDER BY Salary DESC
LIMIT 1 OFFSET 1;

-- CTE & Window Function Solution (Recommended for scalability)
WITH RankedSalaries AS (
    SELECT Salary,
           DENSE_RANK() OVER (ORDER BY Salary DESC) as rnk
    FROM Employee
)
SELECT Salary
FROM RankedSalaries
WHERE rnk = 2;"""
        }
    },
    "Caching": {
        "difficulty": "Medium",
        "importance": "High (Core component of System Design and Architecture interviews)",
        "explanation": "Caching is the process of storing copies of data in temporary storage (typically in-memory caches like Redis or Memcached) to serve read requests much faster than loading from database disks. Caching reduces database load, minimizes API latency, and improves overall system scaling.",
        "faqs": [
            {
                "q": "What are Cache Invalidation strategies?",
                "a": "Key strategies include Cache-Aside (Lazy Loading), Write-Through (write cache and database simultaneously), Write-Behind/Write-Back (write cache first, sync to DB asynchronously), and Eviction policies (LRU, LFU, FIFO)."
            },
            {
                "q": "What is Cache Stampede and how do you prevent it?",
                "a": "Cache Stampede (or dogpiling) occurs when a popular cache key expires, and multiple parallel requests query the database at the same time. Prevent it using mutual exclusion locks (mutex), background renewal, or randomizing expiration times."
            }
        ],
        "mistakes": [
            "Caching dynamic or frequently changing data without a solid Time-to-Live (TTL) configuration.",
            "Not handling Cache Penetration: failing to cache empty/null results, which allows hackers to overload databases with queries for non-existent IDs.",
            "Ignoring memory capacity limits and eviction triggers on in-memory storage."
        ],
        "tips": [
            "Always state in your system design interview that caching is not a source of truth.",
            "Explain how Redis can be used for distributed caching, while local caching (like Guava/Ehcache) is faster but lacks node sync.",
            "Know your cache eviction policies: Least Recently Used (LRU) is the most standard choice."
        ],
        "model_answer": {
            "title": "Architecture: Cache-Aside Implementation Flow",
            "language": "Python (Redis Example)",
            "code": """import redis
import json

cache = redis.Redis(host='localhost', port=6379, db=0)

def get_user_profile(user_id):
    # 1. Try to read from Cache (In-Memory)
    cached_data = cache.get(f"user:{user_id}")
    if cached_data:
        print("Cache Hit!")
        return json.loads(cached_data)
        
    print("Cache Miss!")
    # 2. Fetch from Database (Slow Disk I/O)
    user_profile = db_fetch_user_profile(user_id)
    
    # 3. Write back to Cache with an Expiration TTL of 1 hour
    cache.setex(f"user:{user_id}", 3600, json.dumps(user_profile))
    
    return user_profile

def db_fetch_user_profile(user_id):
    # Mock database read
    return {"id": user_id, "name": "John Doe", "role": "Software Engineer"}"""
        }
    },
    "Google": {
        "difficulty": "Hard",
        "importance": "Company Specific Insight",
        "explanation": "Google technical interviews focus heavily on deep knowledge of core algorithms, complex data structures (like Tries, Segment Trees, Disjoint Set Union), time/space complexity analysis, and scalable system architectures. They assess your ability to clarify ambiguous statements, approach problems methodically, verify edge cases, and write structured, bug-free, scalable code.",
        "faqs": [
            {
                "q": "What algorithmic patterns does Google ask most frequently?",
                "a": "Graph algorithms (DFS, BFS, Dijkstra, Topo Sort), Dynamic Programming, Binary Search on Answer, and advanced trees are highly frequent."
            },
            {
                "q": "How is the system design round structured at Google?",
                "a": "They focus heavily on scale, trade-offs, network layouts, security protocols, container setups, reliability metrics (SRE perspective), and vector space applications."
            }
        ],
        "mistakes": [
            "Jumping straight into code without clarifying the inputs, outputs, constraints, and edge cases.",
            "Struggling to compute the mathematical complexity (big-O time and space) of recursive or graph algorithms.",
            "Failing to structure code with helper functions, making it hard to debug or test."
        ],
        "tips": [
            "Think out loud. Communicating your thought process is just as important as writing the final solution.",
            "Always state the baseline brute force solution first, then show how you can optimize it.",
            "Create a list of edge cases (e.g., null values, empty lists, duplicate elements, negative numbers) and write dry tests on the whiteboard."
        ],
        "model_answer": {
            "title": "Google Classic Problem: Find Longest Path in a Graph Matrix (DFS + Memoization)",
            "language": "C++",
            "code": """#include <vector>
#include <algorithm>
using namespace std;

class Solution {
    int rows, cols;
    vector<vector<int>> memo;
    int dirs[4][2] = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};

    int dfs(vector<vector<int>>& matrix, int r, int c) {
        if (memo[r][c] != 0) return memo[r][c];
        int max_len = 1;
        
        for (auto dir : dirs) {
            int nr = r + dir[0];
            int nc = c + dir[1];
            
            // Check boundaries and increasing condition
            if (nr >= 0 && nr < rows && nc >= 0 && nc < cols && matrix[nr][nc] > matrix[r][c]) {
                max_len = max(max_len, 1 + dfs(matrix, nr, nc));
            }
        }
        return memo[r][c] = max_len;
    }

public:
    int longestIncreasingPath(vector<vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) return 0;
        rows = matrix.size();
        cols = matrix[0].size();
        memo = vector<vector<int>>(rows, vector<int>(cols, 0));
        
        int longest_path = 0;
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                longest_path = max(longest_path, dfs(matrix, i, j));
            }
        }
        return longest_path;
    }
};"""
        }
    }
}

def get_coding_prep_content(category, topic):
    """
    Returns structured data for a selected category and subtopic.
    Generates dynamic, rich template-based content if a premium dataset is not pre-written.
    """
    topic_clean = topic.strip()
    
    # 1. Check if we have pre-written premium content
    if topic_clean in PREMIUM_TOPICS:
        data = PREMIUM_TOPICS[topic_clean]
        return {
            "category": category,
            "topic": topic_clean,
            "difficulty": data["difficulty"],
            "importance": data["importance"],
            "explanation": data["explanation"],
            "faqs": data["faqs"],
            "mistakes": data["mistakes"],
            "tips": data["tips"],
            "model_answer": data["model_answer"]
        }
        
    # 2. Fallback Generation Engine (categorized heuristics)
    difficulty = "Medium"
    importance = f"Frequently Asked (Very high priority for {category} interviews)"
    explanation = ""
    faqs = []
    mistakes = []
    tips = []
    model_answer = {
        "title": f"Interview Preparation Example: {topic_clean}",
        "language": "Python",
        "code": "# Coding explanation placeholder"
    }
    
    if category == "DSA":
        difficulty = "Medium" if topic_clean not in ["Arrays", "Strings", "Linked Lists"] else "Easy"
        if topic_clean in ["Dynamic Programming", "Graphs", "Backtracking"]:
            difficulty = "Hard"
        explanation = f"In technical DSA interviews, {topic_clean} represents a critical conceptual framework. Preparing this topic involves understanding memory layout, structural pointers, spatial relations, and traversal complexities. Mastering this helps you solve complex, algorithmic puzzles with optimized time and auxiliary space constraints."
        faqs = [
            {
                "q": f"How is {topic_clean} stored or represented in memory?",
                "a": "It depends on the storage method (contiguous blocks vs pointer nodes). Contiguous layouts allow constant-time indexed lookup, while node-pointer links require traversal but support dynamic growth."
            },
            {
                "q": f"What is the average time complexity of standard operations in {topic_clean}?",
                "a": "Standard queries typically range from O(1) using hashing, O(log N) using search divisions, to O(N) for linear checks. Optimizing these thresholds is key to passing tech screens."
            }
        ]
        mistakes = [
            "Failing to handle null inputs, empty objects, or boundary indices (leads to pointer/array exceptions).",
            "Creating unnecessary helper arrays that violate in-place memory constraints (O(N) space instead of O(1)).",
            "Not recognizing loops or cycles, resulting in infinite iterations or stack overflow exceptions."
        ]
        tips = [
            "Start by sketching the inputs on paper. Map nodes, values, pointers, or indices dynamically.",
            "Write the simple, brute force iterative solution first, then optimize using pointers, hashing, or memoization.",
            "Always state the time and space complexity explicitly as you trace through the algorithm."
        ]
        
        # Provide specialized code blocks for basic DSA concepts
        if topic_clean == "Arrays":
            model_answer = {
                "title": "Problem: Reverse an Array In-Place (Two Pointer approach)",
                "language": "Python",
                "code": """def reverse_array_in_place(arr):
    left = 0
    right = len(arr) - 1
    
    while left < right:
        # Swap elements in place
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
        
    return arr

# Time Complexity: O(N)
# Space Complexity: O(1)"""
            }
        elif topic_clean == "Linked Lists":
            model_answer = {
                "title": "Problem: Reverse a Singly Linked List",
                "language": "Python",
                "code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next  # Temporarily store next node
        curr.next = prev       # Reverse pointer
        prev = curr            # Move prev pointer forward
        curr = next_temp       # Move current pointer forward
        
    return prev  # New head of reversed list

# Time Complexity: O(N)
# Space Complexity: O(1)"""
            }
        else:
            model_answer = {
                "title": f"Algorithmic Pattern: {topic_clean} Basic Structure",
                "language": "Python",
                "code": f"""def solve_with_{topic_clean.lower().replace(' ', '_')}(data_input):
    # Initial state setup
    result = None
    
    # Core traversal, division, or pointer logic
    # TODO: Optimize bounds and handle base constraints
    
    return result"""
            }
            
    elif category == "Databases":
        difficulty = "Medium" if topic_clean not in ["SQL", "Normalization"] else "Easy"
        if topic_clean in ["Cassandra", "Neo4j", "ArangoDB", "Database Design"]:
            difficulty = "Hard"
        explanation = f"The study of {topic_clean} involves understanding how data is modeled, normalized, queried, and stored on disks. Interviews evaluate transactional consistency (ACID), querying costs, scaling strategies (clustering, replica nodes), and index scans. Choosing between SQL and NoSQL for {topic_clean} determines system capabilities."
        faqs = [
            {
                "q": f"What are the main use cases for {topic_clean}?",
                "a": f"Used to model application states under defined consistency patterns. Relational {topic_clean} systems excel in transactional integrity, while non-relational configurations focus on high throughput and dynamic data schemas."
            },
            {
                "q": f"How do indexes speed up lookups in {topic_clean}?",
                "a": "Indexes create tree structures (like B+ Trees or hash directories) that allow query search in O(log N) instead of sequential full scans, though they add overhead to inserts and updates."
            }
        ]
        mistakes = [
            "Failing to handle database normalization, resulting in data anomalies and duplicates.",
            "Over-indexing tables: adding indexes to columns that are rarely searched, which slows down write workloads.",
            "Ignoring locking behavior (locks, deadlocks, transaction isolation levels) under heavy concurrent access."
        ]
        tips = [
            "Always align your database choice (SQL vs NoSQL) with the ACID vs BASE requirements of the application.",
            "Trace index seek vs table scans when answering database query optimization questions.",
            "Be prepared to draw Entity-Relationship (ER) diagrams or define schema structures clearly."
        ]
        model_answer = {
            "title": f"Database Schema / Query Setup for {topic_clean}",
            "language": "SQL",
            "code": f"""-- Basic {topic_clean} layout or query optimization example
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index creation to speed up searches
CREATE INDEX idx_user_email ON users(email);"""
        }
        
    elif category == "Programming Languages":
        difficulty = "Easy"
        if topic_clean in ["C++", "C"]:
            difficulty = "Medium"
        explanation = f"{topic_clean} is a widely used programming language with unique syntax, execution engines, and compile-time features. Interviewers evaluate object-oriented structures, variable scope, multithreading libraries, and specific runtime execution processes (JVM, v8, etc.) in {topic_clean}."
        faqs = [
            {
                "q": f"How does {topic_clean} manage memory execution?",
                "a": f"Variables are managed via stack allocations for local frames, and heap allocations for dynamic objects. Garbage collectors or developer-managed deletions release unused segments."
            },
            {
                "q": f"Is {topic_clean} a compiled or interpreted language?",
                "a": f"Depending on the environment, it uses direct compilation to native binaries, VM-based byte-code compilation, or line-by-line interpretation at runtime."
            }
        ]
        mistakes = [
            "Not understanding thread safety, leading to race conditions or data corruption.",
            "Failing to manage pointers or memory references, causing segmentation faults or memory leaks.",
            "Misunderstanding reference equality vs value equality (e.g., comparing string pointers instead of string contents)."
        ]
        tips = [
            "Know the core features of the language version (e.g., Java 8 streams, Python 3 async, C++ smart pointers).",
            "Explain compiler or virtual machine details (like JVM JIT compilation) to stand out in interviews.",
            "Be prepared to write code that conforms to standard style guides (PEP8, Google Java Guide, etc.)."
        ]
        
        # Provide specific language reference codes
        if topic_clean == "Python":
            model_answer = {
                "title": "Python Core Concept: List Comprehensions & Generators",
                "language": "Python",
                "code": """# List comprehension (evaluates immediately, stores in memory)
squares_list = [x**2 for x in range(1000)]

# Generator expression (lazy evaluation, memory-efficient)
squares_gen = (x**2 for x in range(1000))

# Iterate generator on demand
for val in squares_gen:
    if val > 100:
        break
    print(val)"""
            }
        elif topic_clean == "Java":
            model_answer = {
                "title": "Java Core Concept: Singleton Pattern (Thread-safe Double-Checked Locking)",
                "language": "Java",
                "code": """public class DatabaseConnection {
    private static volatile DatabaseConnection instance;
    
    private DatabaseConnection() {
        // Private constructor prevents instantiation
    }
    
    public static DatabaseConnection getInstance() {
        if (instance == null) {
            synchronized (DatabaseConnection.class) {
                if (instance == null) {
                    instance = new DatabaseConnection();
                }
            }
        }
        return instance;
    }
}"""
            }
        else:
            model_answer = {
                "title": f"Idiomatic syntax example in {topic_clean}",
                "language": topic_clean,
                "code": f"""// Typical structure for coding in {topic_clean}
#include <iostream>
using namespace std;

int main() {{
    cout << "Preparing for " << "{topic_clean}" << " interviews!" << endl;
    return 0;
}}"""
            }
            
    elif category == "System Design":
        difficulty = "Hard"
        explanation = f"In large-scale web applications, {topic_clean} is a foundational architectural element. Interviewers evaluate how you implement {topic_clean} to scale reads/writes, maintain consistent availability, handle server failures, and minimize data delivery times across zones."
        faqs = [
            {
                "q": f"How does {topic_clean} fit into a multi-tier system?",
                "a": f"It acts as an intermediate coordinator or distribution layer between client edge applications and central services to route traffic, cache queries, or buffer write events."
            },
            {
                "q": f"How do we handle single point of failure (SPOF) with {topic_clean}?",
                "a": "SPOF is avoided by setting up clustered backups, database replicas, active-passive configurations, and load-balanced distributions with heartbeat checks."
            }
        ]
        mistakes = [
            "Failing to specify how system consistency is maintained (CAP theorem trade-offs).",
            "Assuming network calls are free and reliable: ignoring latency, retries, and network partitions.",
            "Not discussing monitoring, alerting, logging, and metrics collection for scaled components."
        ]
        tips = [
            "Start with requirements gathering: clarify Read/Write scale (QPS), storage capacity, and SLA expectations.",
            "Draw a clear diagram mapping: DNS -> Load Balancer -> Web Servers -> Cache -> Database.",
            "Always justify your choices: explain why you chose SQL vs NoSQL, or LRU vs LFU caching."
        ]
        model_answer = {
            "title": f"Architectural Pattern: Integrating {topic_clean} in Scaled Systems",
            "language": "System Design Architecture",
            "code": f"""[Client Applications]
        |
        v
  [Load Balancer]
   /    |    \\
  v     v     v
[API Gateway / {topic_clean}]  <-->  [Distributed Cache (Redis)]
  |     |     |
  v     v     v
[Microservices Clusters]
        |
        v
[Database Replica Nodes]"""
        }
        
    elif category == "CS Fundamentals":
        difficulty = "Medium"
        explanation = f"Mastery of {topic_clean} is essential to understanding the foundational computing models. Interviews evaluate thread contexts, data packets, packet routing protocols, security handshakes, software lifecycle stages, and virtualization structures in {topic_clean}."
        faqs = [
            {
                "q": f"Why is {topic_clean} crucial for software stability?",
                "a": "It establishes predictable abstractions for memory layout, thread contexts, data packets, and encapsulation boundaries, preventing logic conflicts and leakage."
            },
            {
                "q": f"What are the standard models or paradigms of {topic_clean}?",
                "a": "Depending on the topic, this covers OSI networking layers, transaction isolation levels, process execution models, or software design lifecycles."
            }
        ]
        mistakes = [
            "Forgetting core architectural rules (e.g., violating encapsulation, breaking OSI layer separation).",
            "Struggling to write correct pseudo-code or query flows representing fundamental concepts.",
            "Confusing virtual resources (threads, sockets) with physical resources (CPU cores, network bandwidth)."
        ]
        tips = [
            "Keep definitions structured and precise: use clear diagrams or maps where appropriate.",
            "Relate theoretical concepts to real-world applications (e.g., explaining TCP handshakes via API loading times).",
            "Understand the historical reasoning behind major paradigms (e.g., why agile replaced waterfall SDLC)."
        ]
        model_answer = {
            "title": f"Conceptual Map: {topic_clean} Fundamental Structure",
            "language": "Text Diagram",
            "code": f"""======================================================
Core Concept Map: {topic_clean}
======================================================
1. Primary Abstraction: Defines variables, constraints, or states.
2. Interface/Boundary: Standard API calls or communication rules.
3. Underlying Hardware: Routes instructions down to physical registers.
4. Optimization Strategy: Reduces resource constraints and latency.
======================================================."""
        }
        
    else:  # Company Wise Questions
        difficulty = "Hard" if topic_clean in ["Google", "Microsoft", "Amazon", "Adobe"] else "Medium"
        explanation = f"Preparing for interviews at {topic_clean} requires understanding their specific hiring philosophy, online test patterns, coding style guides, and common system architecture topics. {topic_clean} focuses on core competencies, problem-solving speed, clean documentation, and cultural alignment."
        faqs = [
            {
                "q": f"What is the recruitment process at {topic_clean}?",
                "a": "Typically consists of a screening resume parse, an online coding assessment (1-3 questions), 2-4 virtual technical rounds, and a behavioral/values check."
            },
            {
                "q": f"Does {topic_clean} focus more on theory or coding?",
                "a": "They evaluate a balance: deep theoretical fundamentals (OS, DBMS, networking) are tested alongside writing readable, bug-free algorithms."
            }
        ]
        mistakes = [
            "Ignoring the company's core values or leadership principles (e.g., Amazon's Leadership Principles, Google's Googliness).",
            "Writing unreadable code without explaining variables, comments, or complexity details.",
            "Struggling to answer behavior/scenario questions using structural methods like STAR."
        ]
        tips = [
            "Practice mock interview sessions under time pressure: aim for 20-30 minutes per coding problem.",
            "Look up recent interview transcripts for this company to identify trends in question topics.",
            "Align your behavioral answers with the company's public missions and engineering values."
        ]
        model_answer = {
            "title": f"Frequently Asked Interview Question at {topic_clean}",
            "language": "Python",
            "code": f"""# Typical pattern asked during {topic_clean} coding interviews
def solve_interview_problem(nums, target):
    # HashMap approach to find targets in constant lookup time O(1)
    seen = {{}}
    for i, num in enumerate(nums):
        diff = target - num
        if diff in seen:
            return [seen[diff], i]
        seen[num] = i
    return []

# Time Complexity: O(N)
# Space Complexity: O(N)"""
        }

    return {
        "category": category,
        "topic": topic_clean,
        "difficulty": difficulty,
        "importance": importance,
        "explanation": explanation,
        "faqs": faqs,
        "mistakes": mistakes,
        "tips": tips,
        "model_answer": model_answer
    }
