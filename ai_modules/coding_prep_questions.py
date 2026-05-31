# ai_modules/coding_prep_questions.py

CATEGORIES = {
    "DSA": {
        "title": "Data Structures & Algorithms",
        "icon": "bi-code-square",
        "description": "Master coding patterns, complexity analysis, and advanced problem-solving structures.",
        "topics": [
            "Arrays", "Strings", "Linked Lists", "Stacks", "Queues", "HashMap",
            "Trees", "BST", "Heaps", "Graphs", "Greedy", "Recursion",
            "Backtracking", "Sliding Window", "Two Pointer", "Binary Search",
            "Dynamic Programming", "Bit Manipulation"
        ]
    },
    "Databases": {
        "title": "Database Systems & Design",
        "icon": "bi-database-fill",
        "description": "Revise schemas, query optimization, indexing, ACID transactions, and NoSQL models.",
        "topics": [
            "SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Neo4j",
            "ArangoDB", "Normalization", "Transactions", "Indexing", "Database Design"
        ]
    },
    "Programming Languages": {
        "title": "Programming Core Languages",
        "icon": "bi-file-earmark-code-fill",
        "description": "Deep dive into language syntax, OOP, memory compilation, and runtime environments.",
        "topics": [
            "Java", "Python", "JavaScript", "C", "C++"
        ]
    },
    "System Design": {
        "title": "System Design & Scaling",
        "icon": "bi-diagram-3-fill",
        "description": "Learn to design large-scale web services, microservices, caches, and load balancers.",
        "topics": [
            "Load Balancing", "Caching", "Microservices", "Message Queues",
            "API Gateway", "Database Sharding", "CDN", "Rate Limiting"
        ]
    },
    "CS Fundamentals": {
        "title": "CS Core Theory",
        "icon": "bi-cpu-fill",
        "description": "Study CPU scheduling, OSI protocol layers, normalization forms, and software engineering.",
        "topics": [
            "Operating Systems", "DBMS", "Computer Networks", "OOP", "Cloud Basics", "SDLC"
        ]
    },
    "Company Wise Questions": {
        "title": "Company Specific Preparation",
        "icon": "bi-building-fill",
        "description": "Examine popular interview patterns, questions, and style guides of top tech employers.",
        "topics": [
            "Google", "Microsoft", "Amazon", "Adobe", "Oracle",
            "Infosys", "TCS", "Accenture", "Wipro", "Cognizant"
        ]
    }
}

def get_dsa_questions(subcategory):
    """Generates 15 structured DSA questions for a subcategory."""
    questions = []
    
    # Define 15 standard DSA template patterns
    patterns = [
        {
            "q": f"How do you implement and traverse a {subcategory} structure?",
            "a": f"Implementation of a {subcategory} depends on memory requirements (contiguous arrays vs node pointer linkages). Traversal is typically achieved iteratively using loops/pointers or recursively by visiting branching nodes.",
            "e": f"For {subcategory}, traversal checks every element to perform operations. Contiguous layouts allow direct index offsets in constant O(1) time, while node links require stepping through pointer properties, taking O(N) linear time.",
            "d": "Easy",
            "t": f"Always check for null bounds or empty inputs at the start of your {subcategory} traversal to avoid runtime errors."
        },
        {
            "q": f"What are the time and space complexity bounds of common {subcategory} operations?",
            "a": f"Insertion and deletion are O(1) if references are held, but searching remains O(N) in the worst case for sequential structures. Specialized tree/heap structures resolve search in O(log N) logarithmic thresholds.",
            "e": f"Understanding big-O thresholds in {subcategory} helps you compare trade-offs. For example, hash maps trade memory space for constant O(1) access time, whereas simple lists conserve memory but take O(N) search time.",
            "d": "Easy",
            "t": "In interviews, explicitly state the distinction between average case and worst case complexity bounds."
        },
        {
            "q": f"Explain the difference between a static and dynamic {subcategory} representation.",
            "a": f"Static structures allocate a fixed block of contiguous memory on the stack at compile time. Dynamic structures allocate memory on the heap at runtime, growing or shrinking dynamically using pointers.",
            "e": f"Choosing between static and dynamic {subcategory} affects resizing cost. Static structures are extremely fast but have fixed size limits, while dynamic ones incur overhead during resizing/allocation but can scale indefinitely.",
            "d": "Easy",
            "t": "Explain memory stack vs heap allocation when discussing static vs dynamic layouts."
        },
        {
            "q": f"How do you detect loops, cycles, or deadlocks in a {subcategory} representation?",
            "a": f"Cycles are detected using tracking collections (such as HashSets that store visited references) or multi-pointer speed algorithms (e.g. Floyd's cycle detection with fast and slow pointers).",
            "e": f"Cycle detection is critical to prevent infinite loops in {subcategory} structures. If a pointer points back to an already visited node, a cycle exists, which must be resolved to protect system stability.",
            "d": "Medium",
            "t": "Mention Floyd's Tortoise and Hare algorithm for loop detection—it shows deep algorithmic literacy."
        },
        {
            "q": f"What is the recursive vs iterative implementation strategy for {subcategory} operations?",
            "a": f"Recursive strategies call the method itself on subsets of the {subcategory} structure, utilizing the call stack. Iterative strategies use loop states and explicit collections (like stacks or queues) to manage items.",
            "e": f"Recursive {subcategory} operations are clean and readable but risk stack overflow on large inputs. Iterative solutions are more complex to write but are safer because they use heap memory to track states.",
            "d": "Medium",
            "t": "If you suggest a recursive solution, proactively discuss call stack space limits."
        },
        {
            "q": f"How do you reverse or invert a {subcategory} structure?",
            "a": f"Reversal is achieved by swapping references, pointer directions, or indices in-place, typically using two helper pointers tracking current, previous, and next states.",
            "e": f"Reversing {subcategory} elements in-place is highly optimized because it takes O(1) auxiliary space. We traverse sequentially, changing each node's pointer to point to its predecessor instead of successor.",
            "d": "Medium",
            "t": "Practice reversing a linked list in-place until you can code it bug-free in under 5 minutes."
        },
        {
            "q": f"Design a search algorithm to locate a target element inside a {subcategory} representation.",
            "a": f"Search can be performed sequentially (scanning all nodes in O(N) time) or logarithmically (halving the search space in sorted structures, yielding O(log N) efficiency).",
            "e": f"Searching in {subcategory} represents a fundamental coding task. If the collection is unsorted, linear scan is mandatory. If sorted, binary search splits the space dynamically to locate targets quickly.",
            "d": "Medium",
            "t": "Mention that sorting a collection before searching is only efficient if you perform multiple subsequent searches."
        },
        {
            "q": f"How do you handle duplicate values or collisions in a {subcategory} structure?",
            "a": f"Duplicates are managed by modifying node parameters (adding frequency counts) or utilizing collision resolution techniques like chaining (linked lists) or open addressing (linear probing) in hash-based structures.",
            "e": f"Failing to handle duplicate items in {subcategory} leads to data loss or incorrect results. Storing secondary nodes or incrementing values protects integrity under collision conditions.",
            "d": "Medium",
            "t": "Explain chaining vs open addressing when asked about hash conflicts."
        },
        {
            "q": f"What is the in-place vs out-of-place modification trade-off in {subcategory}?",
            "a": f"In-place modifications mutate the original {subcategory} data directly in memory, taking O(1) auxiliary space. Out-of-place modifications create and return copy structures, taking O(N) memory space.",
            "e": f"In-place changes are highly memory-efficient, but they alter the input data permanently. Out-of-place methods preserve the original structure (immutability), which is safer in concurrent systems but takes more heap memory.",
            "d": "Medium",
            "t": "Highlight that in-place updates are preferred in memory-constrained environments."
        },
        {
            "q": f"Explain the concept of balancing in relation to {subcategory} trees.",
            "a": f"Balancing ensures that the depth of all sub-branches remains equal (or differs by at most 1), maintaining search time complexity at a logarithmic O(log N) limit.",
            "e": f"An unbalanced {subcategory} tree can degenerate into a linear list with O(N) search times. Self-balancing algorithms (like AVL or Red-Black rotations) adjust node structures dynamically during insertion.",
            "d": "Hard",
            "t": "Explain that self-balancing structures add overhead to writes but guarantee fast reads."
        },
        {
            "q": f"Solve the classic target interval sum or prefix calculation for {subcategory}.",
            "a": f"Solved by computing prefix sums (accumulating sums from index zero) or sliding window pointers to calculate subset metrics in linear O(N) time without nested iterations.",
            "e": f"Pre-calculating prefix sums allows us to compute any interval sum in O(1) time using subtraction. This is extremely efficient compared to traversing the range for every query.",
            "d": "Medium",
            "t": "Prefix sum is a highly useful pattern for array-based interval queries."
        },
        {
            "q": f"How do you serialize and deserialize a {subcategory} structure for file storage?",
            "a": f"Serialization converts the {subcategory} structure into a linear stream of characters (e.g. JSON or preorder traversal list), while deserialization rebuilds the pointers from the stream.",
            "e": f"To serialize, we traverse the structure (using level-order or preorder methods) and output values, including placeholders (like '#' or null) for empty leaf nodes, allowing exact recreation.",
            "d": "Hard",
            "t": "Mention preorder traversal as the most natural way to serialize tree-like hierarchies."
        },
        {
            "q": f"Discuss the common edge cases to consider when implementing {subcategory} logic.",
            "a": f"Common edge cases include: empty collections, single-element structures, duplicate inputs, negative values, and integer overflows under size calculations.",
            "e": f"Writing robust {subcategory} code requires preparing for weird inputs. Always walk through your logic with an empty input and a single-element list to ensure pointer bounds are safe.",
            "d": "Easy",
            "t": "State your edge cases out loud to the interviewer before writing any code."
        },
        {
            "q": f"What is the difference between shallow copying and deep copying a {subcategory}?",
            "a": f"A shallow copy copies the base node structures but shares references to inner child objects. A deep copy recursively duplicates all nodes and child elements, creating a completely isolated object.",
            "e": f"Modifying a shallow copy's inner elements changes the original structure because they share heap references. A deep copy creates entirely new pointers, so changes have no side effects.",
            "d": "Medium",
            "t": "Explain how reference copies can lead to silent bugs in multi-threaded workflows."
        },
        {
            "q": f"How do you merge two sorted {subcategory} structures into a single sorted output?",
            "a": f"Merged by comparing the front elements of both structures using two pointers, appending the smaller value to the output, and incrementing the corresponding pointer.",
            "e": f"This merging algorithm takes O(N + M) time and represents the core concept behind Merge Sort. It is highly optimized because it only scans each element once.",
            "d": "Medium",
            "t": "Trace pointer progress carefully: always check if one structure is exhausted before the other."
        }
    ]
    
    # Customize titles
    for idx, pat in enumerate(patterns):
        questions.append({
            "id": idx + 1,
            "question": pat["q"],
            "answer": pat["a"],
            "explanation": pat["e"],
            "difficulty": pat["d"],
            "interview_tip": pat["t"]
        })
    return questions

def get_database_questions(subcategory):
    """Generates 15 structured Database questions for a subcategory."""
    questions = []
    patterns = [
        {
            "q": f"What is the core purpose of {subcategory} in modern data architectures?",
            "a": f"The core purpose of {subcategory} is to manage state queries, ensure transaction integrity (ACID properties), optimize write performance, and support specific query shapes.",
            "e": f"In system design, {subcategory} dictates how data is serialized, partitioned, and queried. Relational database setups prioritize structural consistency, while NoSQL setups focus on latency and scale.",
            "d": "Easy",
            "t": "Relate database choice to CAP theorem trade-offs: consistency vs availability."
        },
        {
            "q": f"Explain the execution lifecycle of a query in {subcategory}.",
            "a": f"A query is parsed for syntax, checked against table definitions, processed by the query optimizer, mapped to execution paths (e.g. index seek vs scan), and executed against memory buffers or disk blocks.",
            "e": f"Understanding query processing in {subcategory} helps you write efficient filters. The optimizer selects paths based on stats, which is why outdated table stats can slow down queries.",
            "d": "Medium",
            "t": "Explain that database optimizers choose paths based on table volume and stats."
        },
        {
            "q": f"How do indexes optimize lookups in {subcategory} systems?",
            "a": f"Indexes create secondary lookup structures (such as B+ Trees or Hash tables) that enable direct binary searching in O(log N) time instead of checking every single row sequentially.",
            "e": f"While indexes accelerate reads in {subcategory}, they slow down writes (INSERT, UPDATE, DELETE) because the database must keep the index structures in sync with the primary tables.",
            "d": "Medium",
            "t": "Explain that columns with high cardinality (many unique values) benefit most from indexing."
        },
        {
            "q": f"What are ACID transactions and how are they implemented in {subcategory}?",
            "a": f"ACID stands for Atomicity, Consistency, Isolation, and Durability. They are implemented using transaction locks, write-ahead logs (WAL), and multi-version concurrency control (MVCC).",
            "e": f"Isolation levels (Read Uncommitted, Read Committed, Repeatable Read, Serializable) determine how concurrent changes are visible, protecting databases from dirty reads or phantom data.",
            "d": "Medium",
            "t": "Explain that higher isolation levels reduce concurrency throughput due to lock contention."
        },
        {
            "q": f"Describe database normalization and its normal forms in {subcategory}.",
            "a": f"Normalization is the process of organizing tables to eliminate data redundancy and anomalies. It ranges from 1NF (atomic values) to BCNF/4NF (dependency isolation).",
            "e": f"Normalizing {subcategory} divides large tables into smaller entities, linking them with foreign keys. This prevents update anomalies but requires JOINS, which can slow down read operations.",
            "d": "Easy",
            "t": "Explain that denormalization is often used in read-heavy scaling to avoid expensive JOINS."
        },
        {
            "q": f"What is the difference between SQL and NoSQL databases under {subcategory} configurations?",
            "a": "SQL databases are relational, schema-strict, and ACID-compliant. NoSQL databases are non-relational, schema-flexible, and follow the BASE consistency model.",
            "e": "NoSQL trades strict consistency for horizontal scalability, representing a key design decision under high write workloads where schema rules change frequently.",
            "d": "Easy",
            "t": "State that SQL is suited for complex relational joins, while NoSQL is ideal for key-value or document scaling."
        },
        {
            "q": f"How do database locks (shared, exclusive) prevent concurrency conflicts in {subcategory}?",
            "a": "Shared locks allow multiple sessions to read data concurrently. Exclusive locks prevent any other session from reading or writing, reserving the resource for updates.",
            "e": "Locking ensures data isolation. If session A holds an exclusive lock on row 1, session B must wait until A commits, preventing race conditions but causing deadlocks if not managed.",
            "d": "Medium",
            "t": "Discuss optimistic vs pessimistic locking: optimistic locks use version checks and avoid resource locking."
        },
        {
            "q": f"Explain the Write-Ahead Log (WAL) mechanism in {subcategory}.",
            "a": "WAL requires that any state modification is written and flushed to a persistent log file on disk before changes are applied to the primary database pages in memory.",
            "e": "WAL guarantees durability and recovery. If a power failure occurs, the database reads the log to replay committed changes (roll-forward) or undo uncommitted changes (roll-back).",
            "d": "Hard",
            "t": "Highlight WAL as the primary mechanism for transactional durability."
        },
        {
            "q": f"How do you scale write operations in {subcategory}?",
            "a": "Scaled by implementing write-master configurations with read replicas, sharding tables across multiple servers, or using in-memory write buffers.",
            "e": "While read replicas scale read operations easily, write operations must go to the master database. Sharding splits data rows based on a shard key, separating write paths.",
            "d": "Hard",
            "t": "Explain that sharding adds complexity because cross-shard transactions are expensive."
        },
        {
            "q": f"What is database replication and what are the synchronization modes in {subcategory}?",
            "a": "Replication copies data across server instances. It can be synchronous (waits for all replicas to commit) or asynchronous (replica syncs in the background).",
            "e": "Synchronous replication guarantees consistency but increases write latency. Asynchronous replication is fast but carries a risk of replication lag and minor data loss during master failure.",
            "d": "Medium",
            "t": "Discuss replication lag as a common trade-off when designing global scale systems."
        },
        {
            "q": f"Explain N+1 query problem and how to resolve it in {subcategory}.",
            "a": "N+1 query problem occurs when an application executes one query to fetch parents, and then executes N subsequent queries to fetch child records for each parent.",
            "e": "This creates massive network overhead. Resolve it by using INNER JOINs, eager loading (prefetching child datasets), or batch fetching instead of looping.",
            "d": "Medium",
            "t": "Eager loading (JOIN fetching) is the primary way to optimize ORM performance."
        },
        {
            "q": f"What is connection pooling and why do we configure it for {subcategory}?",
            "a": "Connection pooling maintains a cache of active database connections, reusing them for client queries instead of establishing a new connection every time.",
            "e": "Creating database connections is slow (incurring TCP handshakes and memory setup). Pools limit connection counts, preventing databases from getting overloaded by concurrent sessions.",
            "d": "Easy",
            "t": "Connection pools protect database sockets from getting exhausted under traffic spikes."
        },
        {
            "q": f"How do execution plans help debug slow queries in {subcategory}?",
            "a": "Execution plans detail the exact steps selected by the query optimizer, showing whether it scans the entire table or uses indexes.",
            "e": "By analyzing the plan (using EXPLAIN), you can identify slow nested loops, table scans, or hash joins, helping you determine where to add indexes or rewrite logic.",
            "d": "Medium",
            "t": "Explain that EXPLAIN shows cost estimates, while EXPLAIN ANALYZE executes the query to return real costs."
        },
        {
            "q": f"Describe database sharding and shard keys in {subcategory}.",
            "a": "Sharding is a horizontal partitioning technique that splits rows of database tables across separate physical database instances using a shard key.",
            "e": "The shard key determines how rows are routed. An even distribution avoids 'hotspots' (overloaded nodes), but queries that don't include the shard key must scan all shards.",
            "d": "Hard",
            "t": "Shard keys must be selected carefully: look for columns commonly used in WHERE filters."
        },
        {
            "q": f"How do NoSQL document stores index data under {subcategory} models?",
            "a": "Document stores (like MongoDB) index documents by parsing JSON/BSON fields and creating B-Tree entries linking keys to document disk locations.",
            "e": "Unlike relational databases that index fixed table rows, document databases index nested fields and arrays, supporting fast lookups within unstructured schemas.",
            "d": "Medium",
            "t": "Discuss compound indexes: they optimize queries that filter on multiple document keys."
        }
    ]
    for idx, pat in enumerate(patterns):
        questions.append({
            "id": idx + 1,
            "question": pat["q"],
            "answer": pat["a"],
            "explanation": pat["e"],
            "difficulty": pat["d"],
            "interview_tip": pat["t"]
        })
    return questions

def get_language_questions(subcategory):
    """Generates 15 structured Programming Language questions for a subcategory."""
    questions = []
    patterns = [
        {
            "q": f"What is the compilation and execution model of {subcategory}?",
            "a": f"{subcategory} execution uses either compilation to native machine code, virtual machine interpretation of bytecode, or JIT compilation at runtime.",
            "e": f"Understanding how {subcategory} runs code is a key competency. Compiled configurations compile once to fast binaries, while interpreted scripts run instantly but execute slower.",
            "d": "Easy",
            "t": f"Know the difference between compiled bytecode (like Java class files) and raw machine code (like C binaries)."
        },
        {
            "q": f"How is memory managed (stack vs heap) in {subcategory}?",
            "a": "Local variables are allocated on the stack (fast access, automatic scope release). Objects and dynamic arrays are allocated on the heap (requires garbage collection or manual deletion).",
            "e": "Stack allocations are cleaned up automatically when methods return. Heap allocations persist until explicitly released, requiring careful management to avoid memory leaks.",
            "d": "Easy",
            "t": "Stack memory is fast and local; heap memory is shared and larger."
        },
        {
            "q": f"Explain Garbage Collection or manual memory management in {subcategory}.",
            "a": "Garbage collection automatically identifies and deallocates heap memory references that are no longer reachable by active execution roots.",
            "e": "Languages without garbage collectors (like C/C++) require developers to call delete/free. Garbage collectors (like JVM or V8) run in the background, utilizing mark-and-sweep algorithms.",
            "d": "Medium",
            "t": "Explain that manual memory management avoids garbage collection pauses but increases memory leak risks."
        },
        {
            "q": f"How does {subcategory} implement Object-Oriented Programming (OOP) principles?",
            "a": "OOP is implemented using classes, interfaces, inheritance trees, encapsulated attributes, polymorphic method overrides, and virtual tables.",
            "e": "OOP allows modular design. Methods can be overridden at runtime (dynamic polymorphism), where virtual table lookups determine the correct subclass implementation.",
            "d": "Easy",
            "t": "The four pillars are Encapsulation, Inheritance, Polymorphism, and Abstraction."
        },
        {
            "q": f"What are pointer references and how does {subcategory} handle them?",
            "a": "Pointer references store memory addresses. Some languages expose raw pointers directly, while others abstract them into managed object references to protect memory safety.",
            "e": "Managed references prevent developers from performing raw pointer arithmetic, eliminating a major source of system vulnerabilities like buffer overflows and dangling pointers.",
            "d": "Medium",
            "t": "Discuss pass-by-value vs pass-by-reference: explain that objects are passed by reference value."
        },
        {
            "q": f"How does {subcategory} handle concurrency and multi-threading?",
            "a": "Concurrency is handled using OS-level threads, lightweight green threads (coroutines), asynchronous event loops, and synchronization mutexes.",
            "e": "Multi-threading allows parallel execution but requires managing thread synchronization (locks, semaphores) to prevent race conditions and deadlocks.",
            "d": "Medium",
            "t": "Mention thread safety mechanisms like volatile variables and synchronized blocks."
        },
        {
            "q": f"Explain exception handling and the call stack in {subcategory}.",
            "a": "Exception handling intercepts runtime errors using try-catch-finally blocks, unwinding the call stack until a matching handler is located.",
            "e": "When an error occurs, an exception object is thrown. If unhandled, it bubble ups the call stack, printing a stack trace and terminating execution.",
            "d": "Easy",
            "t": "Never catch general Exception without logging or handling it; it makes debugging difficult."
        },
        {
            "q": f"What is method overloading vs method overriding in {subcategory}?",
            "a": "Overloading defines multiple methods with the same name but different signatures within a class. Overriding replaces a parent class method in a subclass.",
            "e": "Overloading is resolved at compile time (static polymorphism). Overriding is resolved at runtime (dynamic polymorphism) based on the object's real type.",
            "d": "Easy",
            "t": "Overriding requires the exact same method signature; overloading requires different signatures."
        },
        {
            "q": f"Describe the Global Interpreter Lock (GIL) or event loop in {subcategory} if applicable.",
            "a": "The GIL is a mutex lock that ensures only one thread executes bytecode at a time. The event loop uses a single thread to run asynchronous callbacks.",
            "e": "GIL prevents true CPU-bound parallelism in multi-threaded environments. The event loop avoids thread switching costs, making it highly efficient for I/O-bound tasks.",
            "d": "Hard",
            "t": "Coroutines and event loops are ideal for I/O tasks; multi-processing scales CPU tasks."
        },
        {
            "q": f"How are collections and generic types structured in {subcategory}?",
            "a": "Generics provide compile-time type safety, allowing collections (lists, maps, sets) to hold specific types without requiring runtime type casting.",
            "e": "Generic type parameters are checked at compile time. In some runtimes (like Java), generics undergo type erasure, where type parameters are removed after compilation.",
            "d": "Medium",
            "t": "Explain type erasure: it guarantees backward compatibility with older runtime environments."
        },
        {
            "q": f"What is class loading or module importing in {subcategory}?",
            "a": "Class loaders read binary bytecode files from disks and load them into memory namespaces, linking dependencies dynamically at runtime.",
            "e": "Loading is typically performed lazily: classes are loaded only when they are first referenced by execution code, saving startup time and memory.",
            "d": "Medium",
            "t": "Explain the delegation model: class loaders check parent loaders before loading locally."
        },
        {
            "q": f"How do compiler optimizations (JIT, Inlining) work in {subcategory}?",
            "a": "JIT compilers translate frequently executed bytecode blocks into native machine code at runtime, applying optimizations like method inlining and loop unrolling.",
            "e": "Method inlining replaces method calls with the actual body code, eliminating call stack overhead and enabling secondary compiler optimizations.",
            "d": "Hard",
            "t": "JIT compilers optimize 'hot' code paths dynamically based on runtime stats."
        },
        {
            "q": f"Explain serialization and deserialization of objects in {subcategory}.",
            "a": "Serialization saves an object's heap state into a byte stream. Deserialization reads the byte stream to reconstruct the object structure in memory.",
            "e": "Useful for caching or transmitting objects over networks. Transient or static fields are typically excluded from serialization.",
            "d": "Medium",
            "t": "Mark sensitive fields (like passwords) as transient to exclude them from serialization."
        },
        {
            "q": f"What are design patterns and how are they implemented in {subcategory}?",
            "a": "Design patterns are standard solutions to common software design problems, categorized into Creational (Singleton, Factory), Structural, and Behavioral patterns.",
            "e": "Patterns establish a common language for engineers. For example, the Factory pattern encapsulates object creation, decoupling instantiation from usage.",
            "d": "Medium",
            "t": "Understand the Singleton, Factory, and Observer patterns—they are highly frequent in interviews."
        },
        {
            "q": f"Discuss memory leaks in garbage-collected languages under {subcategory}.",
            "a": "Memory leaks occur when references to unused objects are retained in active roots, preventing the garbage collector from reclaiming their space.",
            "e": "Common causes include static fields holding references to large objects, unregistered event listeners, and thread-local variables that are never cleared.",
            "d": "Hard",
            "t": "Use profilers or heap dumps to track down objects that are retained but no longer needed."
        }
    ]
    for idx, pat in enumerate(patterns):
        questions.append({
            "id": idx + 1,
            "question": pat["q"],
            "answer": pat["a"],
            "explanation": pat["e"],
            "difficulty": pat["d"],
            "interview_tip": pat["t"]
        })
    return questions

def get_system_design_questions(subcategory):
    """Generates 15 structured System Design questions for a subcategory."""
    questions = []
    patterns = [
        {
            "q": f"What is the core role of {subcategory} in distributed systems?",
            "a": f"The core role of {subcategory} is to enable system scaling, reduce latency, maintain availability, coordinate nodes, or protect systems from traffic spikes.",
            "e": f"Designing scalable systems requires adding coordinator blocks. {subcategory} manages traffic routes, data partitions, or caching layers to maintain performance.",
            "d": "Medium",
            "t": "Always start your system design answer by defining functional and non-functional requirements."
        },
        {
            "q": f"How do you design a highly available and fault-tolerant {subcategory} layer?",
            "a": "Fault tolerance is achieved by deploying clustered configurations, configuring active-passive failover routes, and monitoring node health with heartbeat checks.",
            "e": "If node A fails, a load balancer or registry routes traffic to backup node B. Database replication logs sync states, protecting the system from data loss.",
            "d": "Medium",
            "t": "Discuss health check protocols: load balancers drop unhealthy nodes dynamically."
        },
        {
            "q": f"What are the scaling boundaries and bottlenecks of {subcategory}?",
            "a": "Bottlenecks include memory capacity limits, network throughput caps, CPU serialization overhead, and data consistency delays across replicas.",
            "e": "As connection volume spikes, the system can hit socket limits. Memory exhaustion triggers eviction policies, slowing down reads or causing request failures.",
            "d": "Hard",
            "t": "Explain trade-offs: vertical scaling is simple but has strict hardware limits."
        },
        {
            "q": f"Explain the CAP theorem trade-offs in relation to {subcategory}.",
            "a": "The CAP theorem states that a distributed system can guarantee at most two of: Consistency, Availability, and Partition tolerance. In network partitions, we must choose C or A.",
            "e": "If consistency is selected, we block writes until all nodes sync, reducing availability. If availability is selected, we accept updates on active nodes, causing temporary inconsistency.",
            "d": "Medium",
            "t": "Most distributed web applications choose AP (Availability/Partition tolerance) and accept eventual consistency."
        },
        {
            "q": f"Describe Cache Invalidation strategies for {subcategory} cache configurations.",
            "a": "Strategies include Cache-Aside (lazy load), Write-Through (sync update to DB), Write-Behind (async DB write), and Eviction (LRU, LFU, FIFO).",
            "e": "Cache-Aside loads keys on demand. Updates must invalidate cache keys. In Write-Behind, writes are buffered in cache and flushed to DB asynchronously, speeding up writes but risking loss during crashes.",
            "d": "Medium",
            "t": "LRU (Least Recently Used) is the industry standard cache eviction policy."
        },
        {
            "q": f"How do you prevent a Cache Stampede (Dogpiling) on {subcategory} nodes?",
            "a": "Prevent by using mutual exclusion locks (mutex) on cache misses, background cron updates, or adding jitter (randomized offsets) to cache expiration TTLs.",
            "e": "Mutex locks ensure only one request queries the database on a cache miss, while other concurrent requests wait for the cache to get populated, protecting databases from getting overloaded.",
            "d": "Hard",
            "t": "Jitter (randomized TTLs) prevents all popular cache keys from expiring at the same time."
        },
        {
            "q": f"What is CDN (Content Delivery Network) and how does it optimize content distribution?",
            "a": "CDNs store static assets (images, HTML, video) on edge servers geographically closer to users, reducing network transit times.",
            "e": "CDNs route user requests to the nearest edge point (Point of Presence). Static content is served from edge caches, bypassing origin servers and saving bandwidth.",
            "d": "Easy",
            "t": "Use CDNs for static assets, and configure geo-routing for dynamic API requests."
        },
        {
            "q": f"Explain Consistent Hashing and its role in routing requests to {subcategory} clusters.",
            "a": "Consistent Hashing maps requests and server nodes to a virtual ring space, minimizing data migrations when nodes are added or removed.",
            "e": "Traditional modulo hashing (hash(key) % N) requires re-mapping all keys when N changes. Consistent hashing only re-maps keys associated with the added/removed node, protecting caches from mass misses.",
            "d": "Hard",
            "t": "Mention virtual nodes: they distribute keys evenly across server nodes on the ring."
        },
        {
            "q": f"Describe Message Queues and their asynchronous processing role.",
            "a": "Message Queues buffer write tasks in memory/disk blocks, allowing producer services to hand off tasks and return immediately, while consumers process them in the background.",
            "e": "Queues decouple services. If a consumer is slow or crashes, messages remain in the queue, protecting down-stream databases from spikes and guaranteeing delivery.",
            "d": "Medium",
            "t": "Queues are essential for decoupling slow operations (like email sending or video processing)."
        },
        {
            "q": f"What is an API Gateway and what tasks does it handle?",
            "a": "An API Gateway is a reverse proxy that acts as a single entry point for client requests, handling routing, SSL termination, authentication, rate limiting, and metrics collection.",
            "e": "Gateway abstracts internal microservices. Instead of clients calling N microservices directly, they call the gateway, which aggregates responses and handles protocol translation.",
            "d": "Medium",
            "t": "Gateways centralize security checks, keeping internal microservices clean and decoupled."
        },
        {
            "q": f"Explain Rate Limiting algorithms and how they protect backend APIs.",
            "a": "Rate Limiting restricts the number of API calls a client can make in a given timeframe. Algorithms include Token Bucket, Leaky Bucket, and Sliding Window Counter.",
            "e": "Token Bucket stores tokens in a bucket, refilling them at a constant rate. Requests consume tokens. If empty, requests are rejected (HTTP 429), protecting APIs from DDoS and scraping.",
            "d": "Medium",
            "t": "Leaky Bucket smooths out traffic spikes; Token Bucket allows bursts of requests."
        },
        {
            "q": f"Describe Database Sharding and routing in System Design.",
            "a": "Sharding partitions data rows horizontally across multiple database servers based on a shard key, scaling writes beyond a single master instance.",
            "e": "A database router checks the shard key in the request to determine which server holds the target row, routing the query directly and avoiding cross-database searches.",
            "d": "Hard",
            "t": "Selecting an appropriate shard key (e.g. user_id) is critical to distribute load evenly."
        },
        {
            "q": f"How do Load Balancers distribute traffic and handle failover?",
            "a": "Load Balancers distribute incoming traffic across healthy backend servers using routing algorithms like Round Robin, Least Connections, or IP Hashing.",
            "e": "Balancers perform active health checks (heartbeats). If a server stops responding, it is dropped from the pool, routing subsequent requests to healthy instances.",
            "d": "Easy",
            "t": "Deploy load balancers in active-passive pairs to avoid making the balancer a single point of failure."
        },
        {
            "q": f"Explain Microservices Architecture vs Monolithic Architecture.",
            "a": "Monoliths compile all modules into a single execution unit. Microservices split modules into independent services that communicate over APIs/message queues.",
            "e": "Monoliths are simple to build but hard to scale and deploy as teams grow. Microservices allow independent scaling and deployment but add complexity in network communications and distributed transactions.",
            "d": "Medium",
            "t": "Microservices are suited for large engineering organizations; monoliths are ideal for MVPs."
        },
        {
            "q": f"Describe Distributed Transactions and Saga Pattern.",
            "a": "Distributed transactions span multiple databases. Since 2-Phase Commit (2PC) is slow and blocking, the Saga pattern executes local transactions sequentially with compensating rollback transactions.",
            "e": "If step 3 fails in a Saga, the system triggers compensating transactions for step 1 and 2 in reverse order, restoring eventual consistency without locking database rows.",
            "d": "Hard",
            "t": "Sagas guarantee eventual consistency rather than immediate ACID-style consistency."
        }
    ]
    for idx, pat in enumerate(patterns):
        questions.append({
            "id": idx + 1,
            "question": pat["q"],
            "answer": pat["a"],
            "explanation": pat["e"],
            "difficulty": pat["d"],
            "interview_tip": pat["t"]
        })
    return questions

def get_cs_fundamentals_questions(subcategory):
    """Generates 15 structured CS Fundamentals questions for a subcategory."""
    questions = []
    patterns = [
        {
            "q": f"What is the core definition and theoretical scope of {subcategory}?",
            "a": f"The core scope of {subcategory} covers process abstractions, network protocols, data model normalization, object design, or software lifecycles.",
            "e": f"Every software engineer must understand the basic computer science rules of {subcategory} to write efficient, structured, and secure applications.",
            "d": "Easy",
            "t": "Keep definitions clear and precise. Relate theories to practical coding examples."
        },
        {
            "q": f"Explain memory management, paging, and fragmentation in OS environments.",
            "a": "OS manages physical memory by dividing it into fixed pages. Virtual memory maps page tables. Fragmentation can be internal (wasted space inside allocated page) or external.",
            "e": "Virtual memory abstracts disk blocks as main memory. Page faults occur when the requested virtual page is not in physical RAM, forcing page swaps from disk.",
            "d": "Medium",
            "t": "Know the difference between page faults and segmentation faults (accessing invalid memory namespaces)."
        },
        {
            "q": f"What is a process vs thread and how do CPU schedulers handle them?",
            "a": "A process is an execution unit with its own memory space. A thread is a lightweight unit within a process that shares its parent's memory, scheduled by the CPU.",
            "e": "Process context switching is expensive because it requires loading page tables and CPU registers. Thread switching is fast because they share address spaces.",
            "d": "Easy",
            "t": "Threads share heap memory but have separate local execution stacks."
        },
        {
            "q": f"Describe transaction isolation levels in Database Management Systems (DBMS).",
            "a": "Levels include Read Uncommitted, Read Committed, Repeatable Read, and Serializable, preventing dirty reads, non-repeatable reads, and phantom reads.",
            "e": "Isolation levels are implemented using locks and MVCC. Serializable is the safest but slowest because it locks table ranges, preventing concurrent modifications.",
            "d": "Medium",
            "t": "Read Committed is the default isolation level in most popular databases (like PostgreSQL)."
        },
        {
            "q": f"How does the TCP/IP protocol suite structure data transmission over networks?",
            "a": "Structured into 4 layers: Application, Transport (TCP/UDP), Internet (IP), and Network Access, wrapping data in packets and frames.",
            "e": "As data goes down the stack, each layer wraps headers. Transport layer handles packet delivery and flow control. Internet layer handles routing.",
            "d": "Easy",
            "t": "OSI has 7 layers; TCP/IP has 4 layers. Memorize the mappings between them."
        },
        {
            "q": f"Explain the difference between TCP and UDP transport protocols.",
            "a": "TCP is connection-oriented, reliable, and byte-stream based. UDP is connectionless, unreliable, and packet-stream based.",
            "e": "TCP uses a 3-way handshake to establish connections and handles packet retransmission. UDP sends packets instantly without handshakes, making it ideal for streaming.",
            "d": "Easy",
            "t": "Use TCP for web/API data; use UDP for live streaming, gaming, or DNS queries."
        },
        {
            "q": f"What are the four pillars of Object-Oriented Programming (OOP)?",
            "a": "The four pillars are Encapsulation (data hiding), Inheritance (reuse), Polymorphism (interfaces with multiple forms), and Abstraction (hiding complexity).",
            "e": "Encapsulation hides class states behind private fields. Inheritance extends classes. Polymorphism allows dynamic method overrides. Abstraction uses interfaces.",
            "d": "Easy",
            "t": "Encapsulation is achieved with access modifiers (private, protected, public)."
        },
        {
            "q": f"Describe the differences between abstract classes and interfaces in OOP.",
            "a": "Abstract classes can hold instance state and concrete methods. Interfaces are pure behavioral contracts (historically holding only abstract methods).",
            "e": "A class can extend only one abstract parent class (single inheritance), but can implement multiple interfaces, allowing flexible polymorphic designs.",
            "d": "Easy",
            "t": "Interfaces define capabilities ('can-do'); abstract classes define relationships ('is-a')."
        },
        {
            "q": f"Explain the Software Development Life Cycle (SDLC) models.",
            "a": "SDLC models define the steps to build software. Models include Waterfall (linear), Agile (incremental), and DevOps (continuous integration).",
            "e": "Waterfall goes through phases sequentially. Agile splits development into short sprint increments, adapting to changing feedback quickly.",
            "d": "Easy",
            "t": "Explain Agile as iterative feedback loops and continuous integration."
        },
        {
            "q": f"What is virtualization vs containerization in Cloud Computing?",
            "a": "Virtualization uses hypervisors to run multiple guest OS on physical hardware. Containerization shares the host OS kernel to run isolated containers.",
            "e": "Virtual machines are heavy and slow to start because they include a full OS. Containers (like Docker) are lightweight and start instantly because they share the host kernel.",
            "d": "Medium",
            "t": "Containers are ideal for microservice architectures due to low memory footprints."
        },
        {
            "q": f"Explain the 3-Way Handshake in TCP connection establishment.",
            "a": "The handshake uses three steps: client sends SYN, server responds with SYN-ACK, and client sends ACK, establishing a stable connection.",
            "e": "This handshake syncs sequence numbers between both sides, guaranteeing that subsequent packets are delivered in the correct order and retransmitted if lost.",
            "d": "Medium",
            "t": "Handshake requires 3 steps to connect, and 4 steps (FIN-ACK-FIN-ACK) to close connections."
        },
        {
            "q": f"Describe deadlock conditions in Operating Systems.",
            "a": "Deadlocks occur when four conditions are met: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait.",
            "e": "If process A holds resource 1 and waits for resource 2, while process B holds resource 2 and waits for resource 1, they wait indefinitely. Break any of the conditions to resolve.",
            "d": "Medium",
            "t": "Circular wait is the most common condition targeted to prevent deadlocks."
        },
        {
            "q": f"What are design patterns and why do we use them?",
            "a": "Design patterns are standard, reusable templates to solve common software design challenges, promoting clean and readable code.",
            "e": "Patterns (like Singleton, Factory, Observer) decouple components. For example, Observer patterns decouple publisher classes from subscriber classes.",
            "d": "Easy",
            "t": "Understand Creational, Structural, and Behavioral pattern groupings."
        },
        {
            "q": f"Explain the OSI Model layers and their responsibilities.",
            "a": "The OSI model has 7 layers: Physical, Data Link, Network, Transport, Session, Presentation, and Application.",
            "e": "Data Link handles frame transfers (MAC addresses). Network handles routing (IP addresses). Transport handles packet delivery (TCP/UDP ports). Application handles API requests.",
            "d": "Easy",
            "t": "Remember the mnemonic: 'Please Do Not Throw Sausage Pizza Away'."
        },
        {
            "q": f"Describe the differences between REST and gRPC API designs.",
            "a": "REST uses HTTP/1.1 and JSON formats. gRPC uses HTTP/2 and Protocol Buffers, establishing high-performance, binary RPC communication.",
            "e": "REST is simple, standard, and human-readable. gRPC is faster, uses compressed binary transfers, and supports client/server streaming, making it ideal for internal microservices.",
            "d": "Medium",
            "t": "REST is preferred for public web client APIs; gRPC is ideal for backend communications."
        }
    ]
    for idx, pat in enumerate(patterns):
        questions.append({
            "id": idx + 1,
            "question": pat["q"],
            "answer": pat["a"],
            "explanation": pat["e"],
            "difficulty": pat["d"],
            "interview_tip": pat["t"]
        })
    return questions

def get_company_questions(subcategory):
    """Generates 15 structured Company Wise questions for a subcategory."""
    questions = []
    patterns = [
        {
            "q": f"What is the typical interview focus at {subcategory}?",
            "a": f"The technical screen at {subcategory} evaluates core algorithmic complexity (DSA), data structure optimization, system design scaling, and cultural fit.",
            "e": f"To clear the interview at {subcategory}, you must write readable, bug-free code, explain trade-offs clearly, and align with their core engineering values.",
            "d": "Medium",
            "t": "Communicate your thought process clearly. Think out loud as you write code."
        },
        {
            "q": f"How does {subcategory} evaluate candidates during the coding round?",
            "a": "They evaluate your problem-solving process: clarifying ambiguous statements, detailing constraints, discussing brute force, and optimizing to big-O limits.",
            "e": "Writing code instantly without clarifying questions is a red flag. Start by stating constraints, write basic test cases, outline your approach, and then write code.",
            "d": "Easy",
            "t": "Confirm constraints (e.g. array size, negative numbers, duplicates) before writing code."
        },
        {
            "q": f"What dynamic programming or graph patterns are asked frequently at {subcategory}?",
            "a": "Graph traversals (DFS, BFS, Dijkstra), Topological Sort, Knapsack patterns, and interval overlap calculations are highly frequent.",
            "e": "Graph problems are commonly modeled as scheduling or path queries. Topological sort is used for dependency resolution. Dynamic programming optimizes recursive states.",
            "d": "Hard",
            "t": "Practice Dijkstra and BFS for shortest path calculations on grid matrices."
        },
        {
            "q": f"How is the system design round structured at {subcategory}?",
            "a": "Design rounds focus on scale, network layouts, reliable data sync, database partitioning, and trade-offs under heavy user traffic.",
            "e": "You will be asked to design a scaled service (like TinyURL or Twitter feed). Map functional requirements, draw abstract diagrams, and detail bottleneck solutions.",
            "d": "Medium",
            "t": "Always justify your choices: explain why you chose Redis or why you chose sharding."
        },
        {
            "q": f"What are the typical behavioral or values-based questions at {subcategory}?",
            "a": "Questions evaluate leadership qualities, handling disagreements, resolving customer issues, and adapting to project changes, structured using the STAR method.",
            "e": "STAR stands for Situation, Task, Action, and Result. Answer behavioral questions by outlining the context, your task, the actions you took, and the positive outcomes.",
            "d": "Easy",
            "t": "Amazon's rounds focus heavily on their 16 Leadership Principles."
        },
        {
            "q": f"How do you optimize recursive search algorithms in {subcategory} interviews?",
            "a": "Optimize recursive search by implementing memoization (caching evaluated states) or pruning invalid branches early in the recursion tree.",
            "e": "Unoptimized recursive searches can run in exponential O(2^N) time. Memoization stores states in a lookup dictionary, reducing complexity to polynomial levels.",
            "d": "Hard",
            "t": "Memoization is top-down dynamic programming; table array builds are bottom-up."
        },
        {
            "q": f"Discuss sorting algorithms and when to use them in {subcategory} rounds.",
            "a": "Common sorting methods include Merge Sort, Quick Sort, and Heap Sort. Sorting is often a preliminary step to enable Binary Search or Two-Pointer scans.",
            "e": "Merge Sort is stable and takes O(N log N) time, but takes O(N) space. Quick Sort is in-place but has a worst-case O(N^2) time if pivot choices are poor.",
            "d": "Easy",
            "t": "Know the big-O space and time limits for Merge Sort, Quick Sort, and Heap Sort."
        },
        {
            "q": f"How do you design a thread-safe Singleton in {subcategory} coding style?",
            "a": "Implemented using double-checked locking, synchronized method wrappers, or lazy class loaders to prevent concurrent thread instantiation.",
            "e": "A naive singleton instantiation check can execute twice if two threads enter the block simultaneously. Locks or static inner loaders ensure safety.",
            "d": "Medium",
            "t": "Double-checked locking requires marking the singleton variable as volatile."
        },
        {
            "q": f"Explain the difference between DFS and BFS in graph searches at {subcategory}.",
            "a": "DFS uses a stack (or recursion) to search deep down branches. BFS uses a queue to search layer by layer, finding shortest paths on unweighted graphs.",
            "e": "DFS takes less memory if the target is deep and branches are thin. BFS is memory-heavy because it keeps all active layer nodes in a queue, but finds targets closest to root.",
            "d": "Easy",
            "t": "BFS is the standard choice for shortest path searches on grid matrices."
        },
        {
            "q": f"Describe the Sliding Window pattern and when it is asked at {subcategory}.",
            "a": "The Sliding Window pattern maintains an active interval over an array/string, sliding it to avoid nested loop calculations and achieving O(N) linear time.",
            "e": "Used when asked to find contiguous subarrays or substrings that satisfy certain rules (like max sum or unique characters), optimizing O(N^2) loops.",
            "d": "Medium",
            "t": "Use start and end pointers to track active window bounds clearly."
        },
        {
            "q": f"Explain Binary Search on Answer pattern and its application.",
            "a": "This pattern searches for the minimum/maximum valid answer in a sorted search space by checking if a middle value satisfies a condition.",
            "e": "If the check function returns true, we update our bound (search left or right). This reduces search time to O(log(range) * check_cost), solving complex optimization tasks.",
            "d": "Hard",
            "t": "Use when you can easily verify if a specific answer is valid, but finding it directly is hard."
        },
        {
            "q": f"How do you merge K sorted lists efficiently in a {subcategory} screen?",
            "a": "Solved by inserting the front elements of all K lists into a Min-Heap (Priority Queue), popping the smallest element, and inserting the next item from that list.",
            "e": "This algorithm runs in O(N log K) time, where N is the total elements across all lists. The Min-Heap maintains the smallest values at the top.",
            "d": "Hard",
            "t": "Min-Heap is the standard data structure to optimize multi-stream merging."
        },
        {
            "q": f"Describe the differences between relational and non-relational database design in system design rounds.",
            "a": "Relational DBs organize data in tables and support normalization and JOINS. Non-relational DBs use document/key-value schemas and partition data for scale.",
            "e": "Use relational databases (like PostgreSQL) for strict transactions and complex queries. Use non-relational databases (like MongoDB/DynamoDB) for high-scale write workloads.",
            "d": "Easy",
            "t": "Relational databases scale vertically; non-relational databases scale horizontally."
        },
        {
            "q": f"How do you implement an LRU Cache in {subcategory} interviews?",
            "a": "Implemented by combining a Hash Map (for constant O(1) lookup) with a Doubly Linked List (to track least recently used items in O(1) time).",
            "e": "When a key is accessed, we move its node to the front of the list. When the cache is full, we evict the tail node and delete its key from the hash map.",
            "d": "Hard",
            "t": " LRU Cache is one of the most popular coding interview questions. Practice implementing it."
        },
        {
            "q": f"What are lead engineering principles evaluated in behavioral rounds at {subcategory}?",
            "a": "Principles include bias for action, customer obsession, deep technical curiosity, delivering results under constraints, and ownership.",
            "e": "Explain instances where you took ownership of a failed project, refactored technical debt, or optimized API performance without direct supervision.",
            "d": "Easy",
            "t": "Prepare 2-3 stories from your past projects that demonstrate these principles using STAR."
        }
    ]
    for idx, pat in enumerate(patterns):
        questions.append({
            "id": idx + 1,
            "question": pat["q"],
            "answer": pat["a"],
            "explanation": pat["e"],
            "difficulty": pat["d"],
            "interview_tip": pat["t"]
        })
    return questions

def get_subcategory_questions(category, subcategory):
    """
    Guarantees exactly 15 high-quality, relevant questions for all 58 subcategories.
    Uses category-specific generation maps.
    """
    sub_clean = subcategory.strip()
    
    if category == "DSA":
        return get_dsa_questions(sub_clean)
    elif category == "Databases":
        return get_database_questions(sub_clean)
    elif category == "Programming Languages":
        return get_language_questions(sub_clean)
    elif category == "System Design":
        return get_system_design_questions(sub_clean)
    elif category == "CS Fundamentals":
        return get_cs_fundamentals_questions(sub_clean)
    else:  # Company Wise Questions
        return get_company_questions(sub_clean)
