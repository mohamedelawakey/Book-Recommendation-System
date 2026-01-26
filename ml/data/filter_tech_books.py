import re
import pandas as pd

goodreads_merged = r'merged/v1/goodreads_merged.csv'
df = pd.read_csv(goodreads_merged, low_memory=False)

tech_keywords = [
    # Programming Languages & Runtimes
    'python', 'javascript', 'typescript', 'java', 'c++', 'c#', 'rust',
    'golang', 'ruby', 'kotlin', 'swift', 'dart', 'php', 'scala', 'elixir',
    'haskell', 'lua', 'clojure', 'f#', 'fortran', 'assembly', 'solidity',
    'zig', 'carbon', 'mojo', 'node.js', 'bun', 'deno',

    # Frameworks & Libraries
    'react', 'angular', 'vue.js', 'svelte', 'next.js', 'nuxt.js', 'express.js',
    'nestjs', 'fastapi', 'django', 'flask', 'spring boot', 'laravel',
    'asp.net', 'ruby on rails', 'tailwindcss',    'bootstrap', 'pytorch',
    'tensorflow', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib',
    'opencv', 'langchain', 'llama-index', 'flutter', 'react native', 'ionic',

    # AI, ML & Data Science (2026 Trends)
    'artificial intelligence', 'machine learning', 'deep learning',
    'generative ai', 'genai', 'large language models', 'llm', 'nlp',
    'natural language processing', 'computer vision', 'neural networks',
    'reinforcement learning', 'transformers', 'bert', 'gpt-4', 'gpt-5',
    'prompt engineering', 'retrieval-augmented generation', 'rag', 'ai agents',
    'vector embeddings', 'data mining', 'big data', 'data engineering',
    'analytics', 'statistics', 'mlops',

    # Backend, APIs & Architecture
    'backend', 'microservices', 'serverless', 'rest api', 'graphql', 'grpc',
    'trpc', 'websockets', 'soap', 'api gateway', 'message queue', 'kafka',
    'rabbitmq', 'redis', 'system design', 'software architecture',
    'design patterns', 'monolith', 'event-driven', 'mvc', 'soa',

    # Infrastructure, Cloud & DevOps
    'devops', 'cloud computing', 'aws', 'amazon web services', 'azure',
    'google cloud', 'gcp', 'docker', 'kubernetes', 'k8s', 'terraform',
    'ansible', 'jenkins', 'ci/cd', 'github actions', 'linux', 'unix',
    'ubuntu', 'bash', 'powershell', 'nginx', 'apache', 'prometheus', 'grafana',
    'terraform', 'infrastructure as code', 'iac', 'sre', 'site reliability',

    # Databases & Storage
    'database', 'sql', 'nosql', 'postgresql', 'mysql', 'mongodb', 'cassandra',
    'elasticsearch', 'dynamodb', 'redis', 'neo4j', 'pinecone', 'milvus',
    'weaviate', 'supabase', 'prisma', 'drizzle', 'sharding', 'replication',
    'acid', 'data warehouse', 'data lake',

    # Software Engineering & Methodology
    'coding', 'programming', 'software engineering', 'clean code',
    'solid principles', 'agile', 'scrum', 'kanban', 'tdd',
    'test driven development', 'unit testing', 'integration testing',
    'debugging', 'version control', 'git', 'github', 'gitlab', 'bitbucket',
    'refactoring', 'object-oriented', 'oop', 'functional programming',

    # Cybersecurity & Web Security
    'cybersecurity', 'information security', 'ethical hacking',
    'penetration testing', 'encryption', 'cryptography', 'oauth', 'jwt',
    'auth0', 'firewall', 'zero trust', 'ssl', 'tls', 'vulnerability',

    # Emerging Tech & Others
    'blockchain', 'web3', 'smart contracts', 'ethereum', 'iot',
    'internet of things', 'quantum computing', 'augmented reality',
    'virtual reality', 'xr', 'game development', 'unreal engine', 'unity',
    'embedded systems', 'rtos', 'webassembly', 'wasm'
]


pattern = '|'.join([re.escape(word) for word in tech_keywords])

text_series = (
    df['Name'].fillna('') + ' ' + df.get('Description', '').fillna('')
).str.lower()

df['tech_score'] = text_series.str.count(pattern)
tech_df = df[df['tech_score'] > 0]
tech_df['Rating'] = pd.to_numeric(tech_df['Rating'], errors='coerce')
tech_df = tech_df.sort_values(by='Rating', ascending=False)

tech_df.to_csv('filtered/v1/tech_books_filtered.csv', index=False)
