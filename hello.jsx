import { Program } from '../types';

export const programs: Program[] = [
  {
    id: 'python-backend',
    title: 'Backend Development (Python)',
    language: 'Python',
    description: 'Master professional backend development with Python through our comprehensive 6-month intensive program. Learn Django, FastAPI, PostgreSQL, cloud deployment, and build production-ready applications that power modern web and mobile platforms.',
    icon: 'Server',
    features: [
      'Python Programming Fundamentals',
      'Django Web Framework Mastery',
      'FastAPI for High-Performance APIs',
      'PostgreSQL Database Design & Optimization',
      'RESTful API Development & Best Practices',
      'Authentication & Authorization Systems',
      'Payment Gateway Integration (M-Pesa, Stripe)',
      'Microservices Architecture Patterns',
      'Docker Containerization & Deployment',
      'AWS/Azure Cloud Platform Deployment',
      'API Testing & Documentation',
      'Performance Optimization Techniques',
      'Security Best Practices & OWASP',
      'Background Task Processing with Celery',
      'Real-time Features with WebSockets',
      'CI/CD Pipeline Setup',
      'Monitoring & Logging Systems',
      'Database Migration Strategies',
      'Code Review & Quality Assurance',
      'Industry-Standard Development Workflow'
    ],
    duration: '12 months',
    period: 12,
    level: 'Beginner to Professional',
    forWho: [
      'Complete beginners wanting to become professional backend developers',
      'Frontend developers looking to expand into full-stack development',
      'Career changers seeking high-demand backend development skills',
      'Students wanting to specialize in Python server-side development',
      'Professionals looking to advance their backend development expertise',
      'Entrepreneurs needing technical skills to build their own products',
      'Anyone passionate about building scalable web applications'
    ],
    requirements: [
      'No prior programming experience required - we start from the basics',
      'Basic computer literacy and familiarity with web browsers',
      'Strong logical thinking and problem-solving mindset',
      'Commitment to 20-25 hours per week of focused learning',
      'Reliable internet connection for online sessions and resources',
      'Willingness to collaborate and participate in code reviews'
    ],
    curriculum: [
  {
    module: 'Python Programming Foundations (Weeks 1-8)',
    topics: [
      'Python Installation & Development Environment Setup',
      'Python Syntax, Variables & Data Types',
      'Control Structures: Conditionals & Loops',
      'Functions & Scope',
      'Data Structures: Lists, Tuples, Dictionaries & Sets',
      'Object-Oriented Programming',
      'Error Handling & File I/O',
      'Python Standard Library & Modules',
      'Virtual Environments & Package Management',
      'Git Version Control & GitHub Workflow',
      'Mini Project: CLI Tool or Script Automation',
      'Debugging & Refactoring Workshop'
    ]
  },
  {
    module: 'Web Development Fundamentals (Weeks 9-16)',
    topics: [
      'HTTP Protocol & Web Architecture',
      'HTML5, CSS & JavaScript Essentials',
      'JSON & REST API Basics',
      'Database Concepts: Relational vs NoSQL',
      'SQL Fundamentals & Database Design',
      'Web Security Basics',
      'Development Tools: Postman, curl & API Testing',
      'Mini Project: Small CRUD Web App',
      'API Testing & Security Deep Dive'
    ]
  },
  {
    module: 'Django Framework Mastery (Weeks 17-24)',
    topics: [
      'Django Installation & Project Structure',
      'URL Routing, Views & Models',
      'Database Migrations & Admin Interface',
      'Templates & Forms',
      'User Authentication & Session Management',
      'Static Files & Media Handling',
      'Middleware, Testing & Debugging',
      'Signals, Management Commands',
      'Capstone Checkpoint: Django Web App with Auth & CRUD'
    ]
  },
  {
    module: 'Django REST Framework & API Development (Weeks 25-30)',
    topics: [
      'DRF Installation & Configuration',
      'Serializers, ViewSets & Routers',
      'Authentication & Permissions',
      'Pagination, Filtering & Searching',
      'API Versioning & Documentation',
      'API Testing & Error Handling',
      'Project: Task Manager or Blog API'
    ]
  },
  {
    module: 'FastAPI & Modern Python APIs (Weeks 31-36)',
    topics: [
      'FastAPI Framework & Async/Await',
      'Pydantic Models & Data Validation',
      'Routing, Parameters & Request Bodies',
      'Dependency Injection & Background Tasks',
      'WebSockets & Streaming',
      'Testing & Performance Optimization',
      'Database Integration & Security',
      'Mini Project: Real-time API or Chat Service'
    ]
  },
  {
    module: 'Database Design & PostgreSQL (Weeks 37-42)',
    topics: [
      'PostgreSQL Installation & Configuration',
      'Database Design Principles & Advanced SQL',
      'Indexes, Constraints & Transactions',
      'Stored Procedures, Triggers & Functions',
      'Query Optimization & Performance Tuning',
      'Backup & Recovery Strategies',
      'Database Security & Monitoring',
      'Database Project: Optimized Schema & Queries'
    ]
  },
  {
    module: 'Advanced Backend Services & Integration (Weeks 43-48)',
    topics: [
      'Payment Gateway Integration (M-Pesa, Stripe)',
      'SMS & Email Services Integration',
      'Cloud File Storage (AWS S3, Cloudinary)',
      'Third-Party APIs & Rate Limiting',
      'Caching Strategies with Redis/Memcached',
      'Background Jobs with Celery & Redis',
      'Real-time Notifications & Push Services',
      'Integration Project: Payment-Enabled App'
    ]
  },
  {
    module: 'Security & DevOps/Cloud Deployment (Weeks 49-54)',
    topics: [
      'OWASP Top 10 & Secure Coding Practices',
      'Authentication Security & Token Management',
      'HTTPS, SSL & Secret Management',
      'Security Monitoring & Incident Response',
      'Docker Fundamentals & Docker Compose',
      'CI/CD Pipelines with GitHub Actions',
      'Cloud Services: AWS, Azure Basics',
      'Kubernetes Introduction & Deployment Strategies'
    ]
  },
  {
    module: 'Capstone Project & Career Preparation (Weeks 55-58)',
    topics: [
      'Capstone Project Planning & Architecture Design',
      'Agile Project Management & Documentation',
      'Code Reviews & Technical Writing',
      'Portfolio Development & Presentation',
      'Resume Building & Interview Prep',
      'System Design Interview Concepts',
      'Open Source Contribution & Networking',
      'Final Project Presentation & Peer Review'
    ]
  }
],
    projects: [
      {
        title: 'E-Commerce Backend API with Payment Integration',
        description: 'Build a complete e-commerce backend with user authentication, product management, shopping cart, order processing, M-Pesa and Stripe payment integration, inventory management, and admin dashboard. Includes real-time notifications and comprehensive API documentation.'
      },
      {
        title: 'Social Media Platform Backend',
        description: 'Develop a scalable backend for a social media platform featuring user profiles, posts with media uploads, real-time messaging, friend/follow systems, news feed algorithms, content moderation, and analytics dashboard with performance optimization.'
      },
      {
        title: 'Learning Management System (LMS) API',
        description: 'Create a comprehensive LMS backend with course management, student enrollment, progress tracking, assignment submission, grading system, video streaming, discussion forums, and detailed analytics for educators and administrators.'
      },
      {
        title: 'Financial Management API with M-Pesa Integration',
        description: 'Build a fintech backend application with account management, transaction processing, M-Pesa integration, budget tracking, financial reporting, loan management, and compliance features following financial industry standards.'
      },
      {
        title: 'Real-time Chat & Collaboration Platform',
        description: 'Develop a backend for team collaboration featuring real-time messaging, file sharing, video call integration, project management tools, team workspaces, notification systems, and comprehensive user management.'
      }
    ],
    price: 5000,
    nextStart: '2025-10-01'
  },
  {
    id: 'custom-training',
    title: 'Custom Training & Mentorship',
    language: 'Flexible',
    description: 'Get personalized, one-on-one training tailored to your specific career goals, learning pace, and technical interests. Perfect for professionals, teams, or individuals with unique requirements who want focused, results-driven education.',
    icon: 'Target',
    features: [
      'Personalized Learning Path Design',
      'One-on-One Expert Mentorship',
      'Flexible Scheduling & Duration',
      'Custom Project Development',
      'Technology-Specific Deep Dives',
      'Career Guidance & Industry Insights',
      'Code Review & Best Practices',
      'Interview Preparation & Portfolio Building',
      'Team Training & Workshop Facilitation',
      'Industry-Specific Training Programs',
      'Ongoing Support & Consultation',
      'Performance Tracking & Assessment',
      'Real-World Problem Solving',
      'Professional Network Access',
      'Continuous Learning Strategy Development'
    ],
    duration: 'Flexible (1-12 months)',
    period: 0,
    level: 'All Levels (Beginner to Expert)',
    forWho: [
      'Professionals wanting to upskill in specific technologies',
      'Teams needing customized training programs',
      'Individuals with unique learning goals or constraints',
      'Career changers requiring personalized guidance',
      'Companies seeking employee development programs',
      'Entrepreneurs building technical skills for their ventures',
      'Students preparing for specific job roles or interviews',
      'Developers wanting to master advanced concepts',
      'Anyone seeking accelerated, focused learning experiences'
    ],
    requirements: [
      'Clear learning objectives and specific goals',
      'Commitment to the agreed schedule and milestones',
      'Openness to personalized feedback and coaching',
      'Willingness to work on real-world projects',
      'Basic computer literacy (level varies by program)',
      'Dedication to continuous learning and improvement'
    ],
    curriculum: [
      {
        module: 'Initial Assessment & Learning Path Design',
        topics: [
          'Comprehensive Skills Assessment & Gap Analysis',
          'Career Goals Definition & Roadmap Creation',
          'Learning Style Assessment & Methodology Selection',
          'Custom Curriculum Design Based on Objectives',
          'Timeline Planning & Milestone Definition',
          'Resource Selection & Tool Recommendation',
          'Success Metrics & Progress Tracking Setup',
          'Communication Preferences & Schedule Coordination'
        ]
      },
      {
        module: 'Personalized Technical Training',
        topics: [
          'Technology-Specific Deep Dive Sessions',
          'Hands-On Coding Practice with Expert Guidance',
          'Real-World Project Development & Implementation',
          'Code Review Sessions & Best Practice Implementation',
          'Problem-Solving Techniques & Debugging Strategies',
          'Architecture Design & System Planning',
          'Performance Optimization & Scalability Considerations',
          'Security Implementation & Vulnerability Assessment'
        ]
      },
      {
        module: 'Professional Development & Industry Preparation',
        topics: [
          'Portfolio Development & Project Showcase Creation',
          'Resume & LinkedIn Profile Optimization',
          'Technical Interview Preparation & Mock Interviews',
          'System Design Interview Training',
          'Industry Networking & Professional Relationship Building',
          'Salary Negotiation Strategies & Career Advancement',
          'Freelancing vs Employment: Pros, Cons & Strategies',
          'Personal Branding & Online Presence Development'
        ]
      },
      {
        module: 'Advanced Topics & Specialization',
        topics: [
          'Advanced Framework Features & Custom Solutions',
          'Microservices Architecture & Distributed Systems',
          'Cloud Platform Mastery & DevOps Integration',
          'Machine Learning Integration for Backend Developers',
          'Blockchain & Cryptocurrency Integration',
          'IoT Backend Development & Real-time Processing',
          'API Gateway & Service Mesh Implementation',
          'Advanced Database Optimization & Scaling Strategies'
        ]
      },
      {
        module: 'Team Training & Workshop Facilitation',
        topics: [
          'Team Skill Assessment & Training Needs Analysis',
          'Custom Workshop Design & Delivery',
          'Code Review Process Implementation',
          'Development Workflow Optimization',
          'Team Collaboration Tools & Best Practices',
          'Knowledge Sharing & Documentation Strategies',
          'Agile Development Process Implementation',
          'Quality Assurance & Testing Strategy Development'
        ]
      },
      {
        module: 'Ongoing Mentorship & Support',
        topics: [
          'Regular Progress Reviews & Goal Adjustment',
          'Industry Trend Updates & Technology Recommendations',
          'Career Guidance & Opportunity Identification',
          'Problem-Solving Support & Technical Consultation',
          'Project Planning & Architecture Review',
          'Code Quality Assessment & Improvement Strategies',
          'Professional Network Expansion & Introduction',
          'Continuous Learning Plan Development & Resource Curation'
        ]
      }
    ],
    projects: [
      {
        title: 'Custom Project Based on Your Goals',
        description: 'Work on a real-world project that aligns with your career objectives, whether it\'s building a startup MVP, improving existing systems, or preparing for specific job requirements'
      },
      {
        title: 'Technology-Specific Implementation',
        description: 'Deep dive into specific technologies, frameworks, or tools that are most relevant to your career path, with hands-on implementation and expert guidance'
      },
      {
        title: 'Portfolio Development & Optimization',
        description: 'Build and optimize a professional portfolio that showcases your skills effectively, including project documentation, code quality, and presentation strategies'
      },
      {
        title: 'Team Training & Knowledge Transfer',
        description: 'For team training: implement knowledge transfer programs, establish coding standards, and develop internal training materials for your organization'
      }
    ],
    price: 0, // Custom pricing
    nextStart: 'Flexible Start Date'
  }
];