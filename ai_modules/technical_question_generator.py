# ai_modules/technical_question_generator.py

TECH_TOPICS_POOL = {
    "ML Engineer": [
        {
            "question": "What is the difference between L1 and L2 regularization?",
            "answer": "L1 regularization adds the absolute values of weights to the loss function and can lead to sparse weights (feature selection). L2 adds squared weights and penalizes extreme weights, preventing overfitting by shrinking weights towards zero."
        },
        {
            "question": "How does backpropagation work in deep learning?",
            "answer": "Backpropagation computes the gradient of the loss function with respect to each weight using the chain rule, propagating errors backward from the output layer to update weights and minimize loss."
        },
        {
            "question": "Explain bias-variance trade-off.",
            "answer": "Bias is error from simple assumptions (underfitting). Variance is error from sensitivity to training noise (overfitting). The trade-off is finding the sweet spot where overall generalization error is minimized."
        },
        {
            "question": "Why do we use convolutional layers (CNNs) instead of dense layers for images?",
            "answer": "CNNs use weight sharing and local receptive fields to capture spatial features and local patterns (like edges) with far fewer parameters than fully connected dense layers."
        },
        {
            "question": "What are vector embeddings and how do vector databases search them?",
            "answer": "Vector embeddings represent data in continuous multi-dimensional space. Vector databases search them using similarity metrics like cosine similarity or Euclidean distance, often utilizing indexing methods like HNSW."
        }
    ],
    "Python Developer": [
        {
            "question": "Explain the difference between a list and a generator in Python.",
            "answer": "A list stores all its elements in memory at once. A generator yields elements lazily on demand (using yield), keeping only the current element in memory, making it highly memory-efficient for large sequences."
        },
        {
            "question": "What is the GIL (Global Interpreter Lock) in Python and how does it affect multi-threading?",
            "answer": "The GIL is a mutex that protects access to Python objects, preventing multiple threads from executing Python bytecodes at once. This makes CPU-bound multi-threading inefficient, though I/O-bound multi-threading is still useful."
        },
        {
            "question": "How do Python decorators work?",
            "answer": "Decorators are functions that take another function as an argument, extend or modify its behavior, and return a new function, all without modifying the original function's source code."
        },
        {
            "question": "What is the difference between deep copy and shallow copy in Python?",
            "answer": "A shallow copy creates a new object but references the nested child objects of the original. A deep copy recursively copies all nested objects, ensuring modifications to the copy don't affect the original."
        },
        {
            "question": "What is the time complexity of searching a value in a list vs a set in Python, and why?",
            "answer": "Searching a list is O(n) as it scans sequentially. Searching a set is O(1) average case because it uses a hash table to directly look up the item based on its hash value."
        }
    ],
    "Frontend Developer": [
        {
            "question": "Explain closure in JavaScript and give a practical use case.",
            "answer": "A closure is a function that retains access to its outer lexical scope even after the outer function has returned. It is useful for creating private variables, data encapsulation, and event handlers."
        },
        {
            "question": "What is the event loop in JavaScript?",
            "answer": "The event loop manages execution of code, processing events, and executing sub-tasks. It monitors the call stack and callback queue, pushing tasks from the queue to the stack once the stack is empty."
        },
        {
            "question": "What is the difference between Virtual DOM and Real DOM in React?",
            "answer": "The Real DOM updates the browser layout, which is slow. The Virtual DOM is a lightweight memory representation of the DOM. React updates the virtual DOM, compares it (diffing), and batches updates to the Real DOM."
        },
        {
            "question": "Explain CSS box model.",
            "answer": "The CSS box model defines the structure of elements: content area, padding (space around content), border (line around padding), and margin (space outside the border)."
        },
        {
            "question": "What is critical rendering path and how do you optimize it?",
            "answer": "The critical rendering path is the sequence of steps the browser takes to convert HTML, CSS, and JS into pixels. Optimize by minifying assets, deferring non-critical JS, and inline critical CSS."
        }
    ]
}

# General fallback questions covering various topics (DSA, DBMS, OS, CN, OOP, Java)
GENERAL_POOL = [
    {
        "question": "Explain the difference between a stack and a queue.",
        "answer": "A stack is a Last-In-First-Out (LIFO) data structure where elements are added and removed from the top. A queue is a First-In-First-Out (FIFO) data structure where elements are added at the rear and removed from the front."
    },
    {
        "question": "What is normalization in DBMS and why do we use it?",
        "answer": "Normalization is the process of organizing database tables to reduce data redundancy and dependency by splitting tables into smaller entities and linking them, avoiding insert/update anomalies."
    },
    {
        "question": "Explain the difference between a process and a thread in an Operating System.",
        "answer": "A process is an independent program execution with its own memory space. A thread is a lightweight execution unit within a process that shares the process's memory and resources."
    },
    {
        "question": "How does DNS (Domain Name System) work?",
        "answer": "DNS resolves human-readable domain names (like google.com) into machine-readable IP addresses (like 142.250.190.46) by querying hierarchical servers (root, TLD, authoritative)."
    },
    {
        "question": "What are the four pillars of OOP (Object-Oriented Programming)?",
        "answer": "The four pillars are Encapsulation (data hiding), Inheritance (reusing parent properties), Polymorphism (multiple implementations of one interface), and Abstraction (hiding implementation details)."
    }
]

def generate_technical_questions(domain, difficulty=None):
    """
    Returns a list of 5 technical questions (with reference answers) based on the domain (e.g. ML Engineer, Python Developer, etc.).
    """
    domain = domain.strip() if domain else "Python Developer"
    
    # Check if we have a pool for this specific role
    if domain in TECH_TOPICS_POOL:
        return TECH_TOPICS_POOL[domain]
        
    # If not, let's search for partial matches
    for key in TECH_TOPICS_POOL:
        if key.lower() in domain.lower() or domain.lower() in key.lower():
            return TECH_TOPICS_POOL[key]
            
    # Default fallback to general CS questions
    return GENERAL_POOL
