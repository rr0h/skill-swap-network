# 🗄️ Database Schema - Skill Swap Network

Complete database schema documentation for the Skill Swap Network application.

## 📊 Entity Relationship Diagram

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│     User        │────────>│   UserSkill      │         │    Category     │
│                 │         │                  │         │                 │
│ - id            │         │ - id             │         │ - id            │
│ - username      │         │ - user_id (FK)   │         │ - name          │
│ - email         │         │ - skill_name     │         │ - description   │
│ - password      │         │ - skill_type     │         │ - icon          │
│ - bio           │         │ - proficiency    │         │ - created_at    │
│ - profile_image │         │ - created_at     │         └─────────────────┘
│ - location      │         └──────────────────┘                  │
│ - phone         │                                                │
│ - created_at    │                                                │
└─────────────────┘                                                │
        │                                                          │
        │                                                          │
        │         ┌──────────────────┐                            │
        └────────>│      Skill       │<───────────────────────────┘
                  │                  │
                  │ - id             │
                  │ - title          │
                  │ - description    │
                  │ - category_id(FK)│
                  │ - user_id (FK)   │
                  │ - level          │
                  │ - duration       │
                  │ - location_pref  │
                  │ - is_active      │
                  │ - views_count    │
                  │ - created_at     │
                  └──────────────────┘
                          │
                          │
                          ├──────────────────────────────────┐
                          │                                  │
                          ▼                                  ▼
                  ┌──────────────────┐            ┌──────────────────┐
                  │  SkillRequest    │            │     Review       │
                  │                  │            │                  │
                  │ - id             │            │ - id             │
                  │ - sender_id (FK) │            │ - reviewer_id(FK)│
                  │ - receiver_id(FK)│            │ - reviewed_id(FK)│
                  │ - skill_id (FK)  │            │ - skill_id (FK)  │
                  │ - message        │            │ - request_id(FK) │
                  │ - status         │            │ - rating         │
                  │ - created_at     │            │ - comment        │
                  │ - accepted_at    │            │ - comm_rating    │
                  │ - completed_at   │            │ - know_rating    │
                  └──────────────────┘            │ - patience_rating│
                          │                       │ - created_at     │
                          │                       └──────────────────┘
                          ▼
                  ┌──────────────────┐
                  │ RequestMessage   │
                  │                  │
                  │ - id             │
                  │ - request_id (FK)│
                  │ - sender_id (FK) │
                  │ - message        │
                  │ - is_read        │
                  │ - created_at     │
                  └──────────────────┘

┌─────────────────┐
│  Notification   │
│                 │
│ - id            │
│ - user_id (FK)  │
│ - type          │
│ - title         │
│ - message       │
│ - link          │
│ - is_read       │
│ - created_at    │
└─────────────────┘
```

## 📋 Table Descriptions

### 1. User (Custom User Model)

Extends Django's AbstractUser with additional fields.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| username | String(150) | Unique username | Required, Unique |
| email | String(254) | Email address | Required, Unique |
| password | String(128) | Hashed password | Required |
| first_name | String(150) | First name | Optional |
| last_name | String(150) | Last name | Optional |
| bio | Text(500) | User biography | Optional |
| profile_image | ImageField | Profile picture | Default: default.jpg |
| location | String(100) | City/Region | Optional |
| phone | String(15) | Phone number | Optional |
| date_of_birth | Date | Birth date | Optional |
| profile_completed | Boolean | Profile completion flag | Default: False |
| is_staff | Boolean | Staff status | Default: False |
| is_active | Boolean | Active status | Default: True |
| date_joined | DateTime | Registration date | Auto-set |
| created_at | DateTime | Created timestamp | Auto-set |
| updated_at | DateTime | Updated timestamp | Auto-update |

**Relationships:**
- One-to-Many with Skill (as user)
- One-to-Many with UserSkill
- One-to-Many with SkillRequest (as sender)
- One-to-Many with SkillRequest (as receiver)
- One-to-Many with Review (as reviewer)
- One-to-Many with Review (as reviewed_user)
- One-to-Many with Notification

**Indexes:**
- username (unique)
- email (unique)

---

### 2. UserSkill

Skills that users can teach or want to learn.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| user_id | ForeignKey | User reference | Required, CASCADE |
| skill_name | String(100) | Skill name | Required |
| skill_type | String(10) | 'offer' or 'want' | Required |
| proficiency_level | String(20) | Skill level | Default: intermediate |
| created_at | DateTime | Created timestamp | Auto-set |

**Choices:**
- skill_type: 'offer', 'want'
- proficiency_level: 'beginner', 'intermediate', 'advanced', 'expert'

**Constraints:**
- Unique together: (user, skill_name, skill_type)

---

### 3. Category

Skill categories for organization.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| name | String(100) | Category name | Required, Unique |
| description | Text | Category description | Optional |
| icon | String(50) | FontAwesome icon class | Default: fa-folder |
| created_at | DateTime | Created timestamp | Auto-set |

**Relationships:**
- One-to-Many with Skill

**Indexes:**
- name (unique)

---

### 4. Skill

Skills that can be taught or learned.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| title | String(200) | Skill title | Required |
| description | Text | Skill description | Required |
| category_id | ForeignKey | Category reference | Optional, SET_NULL |
| user_id | ForeignKey | Skill owner | Required, CASCADE |
| level | String(20) | Difficulty level | Default: intermediate |
| duration | String(100) | Estimated duration | Optional |
| location_preference | String(20) | Teaching location | Default: both |
| is_active | Boolean | Active status | Default: True |
| views_count | Integer | View counter | Default: 0 |
| created_at | DateTime | Created timestamp | Auto-set |
| updated_at | DateTime | Updated timestamp | Auto-update |

**Choices:**
- level: 'beginner', 'intermediate', 'advanced', 'expert'
- location_preference: 'online', 'in_person', 'both'

**Relationships:**
- Many-to-One with User
- Many-to-One with Category
- One-to-Many with SkillRequest
- One-to-Many with Review

**Indexes:**
- user_id
- category_id
- is_active

---

### 5. SkillRequest

Skill exchange requests between users.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| sender_id | ForeignKey | Request sender | Required, CASCADE |
| receiver_id | ForeignKey | Request receiver | Required, CASCADE |
| skill_id | ForeignKey | Requested skill | Required, CASCADE |
| message | Text | Request message | Required |
| status | String(20) | Request status | Default: pending |
| created_at | DateTime | Created timestamp | Auto-set |
| updated_at | DateTime | Updated timestamp | Auto-update |
| accepted_at | DateTime | Acceptance time | Optional |
| completed_at | DateTime | Completion time | Optional |

**Choices:**
- status: 'pending', 'accepted', 'rejected', 'completed', 'cancelled'

**Relationships:**
- Many-to-One with User (sender)
- Many-to-One with User (receiver)
- Many-to-One with Skill
- One-to-Many with RequestMessage
- One-to-One with Review

**Constraints:**
- Unique together: (sender, skill, status)

**Indexes:**
- sender_id
- receiver_id
- skill_id
- status

---

### 6. RequestMessage

Messages within skill requests.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| request_id | ForeignKey | Request reference | Required, CASCADE |
| sender_id | ForeignKey | Message sender | Required, CASCADE |
| message | Text | Message content | Required |
| is_read | Boolean | Read status | Default: False |
| created_at | DateTime | Created timestamp | Auto-set |

**Relationships:**
- Many-to-One with SkillRequest
- Many-to-One with User

**Indexes:**
- request_id
- sender_id
- is_read

---

### 7. Review

Reviews for completed skill exchanges.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| reviewer_id | ForeignKey | Review author | Required, CASCADE |
| reviewed_user_id | ForeignKey | Reviewed user | Required, CASCADE |
| skill_id | ForeignKey | Skill reference | Required, CASCADE |
| request_id | ForeignKey | Request reference | Optional, CASCADE |
| rating | Integer | Overall rating (1-5) | Required, 1-5 |
| comment | Text | Review comment | Required |
| communication_rating | Integer | Communication (1-5) | Default: 5 |
| knowledge_rating | Integer | Knowledge (1-5) | Default: 5 |
| patience_rating | Integer | Patience (1-5) | Default: 5 |
| created_at | DateTime | Created timestamp | Auto-set |
| updated_at | DateTime | Updated timestamp | Auto-update |

**Relationships:**
- Many-to-One with User (reviewer)
- Many-to-One with User (reviewed_user)
- Many-to-One with Skill
- One-to-One with SkillRequest

**Constraints:**
- Unique together: (reviewer, request)
- rating: 1-5
- communication_rating: 1-5
- knowledge_rating: 1-5
- patience_rating: 1-5

**Indexes:**
- reviewer_id
- reviewed_user_id
- skill_id
- rating

---

### 8. Notification

User notifications.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | BigInteger | Primary key | Auto-increment |
| user_id | ForeignKey | Notification recipient | Required, CASCADE |
| notification_type | String(20) | Notification type | Required |
| title | String(200) | Notification title | Required |
| message | Text | Notification message | Required |
| link | String(500) | Related link | Optional |
| is_read | Boolean | Read status | Default: False |
| created_at | DateTime | Created timestamp | Auto-set |

**Choices:**
- notification_type: 'request_received', 'request_accepted', 'request_rejected', 'new_message', 'new_review', 'system'

**Relationships:**
- Many-to-One with User

**Indexes:**
- user_id
- is_read
- notification_type

---

## 🔑 Key Relationships

1. **User ↔ Skill**: One user can offer many skills
2. **User ↔ UserSkill**: One user can have many skills (offered/wanted)
3. **Category ↔ Skill**: One category contains many skills
4. **User ↔ SkillRequest**: Users can send/receive many requests
5. **Skill ↔ SkillRequest**: One skill can have many requests
6. **SkillRequest ↔ RequestMessage**: One request can have many messages
7. **SkillRequest ↔ Review**: One request can have one review
8. **User ↔ Review**: Users can give/receive many reviews
9. **User ↔ Notification**: One user can have many notifications

## 📈 Performance Considerations

### Indexes
- All foreign keys are automatically indexed
- Additional indexes on frequently queried fields:
  - User.username, User.email
  - Skill.is_active
  - SkillRequest.status
  - Review.rating
  - Notification.is_read

### Query Optimization
- Use `select_related()` for foreign key relationships
- Use `prefetch_related()` for reverse foreign key relationships
- Implement pagination for large result sets
- Cache frequently accessed data

## 🔒 Security Considerations

1. **Password Storage**: Passwords are hashed using PBKDF2
2. **CSRF Protection**: All forms include CSRF tokens
3. **SQL Injection**: Django ORM prevents SQL injection
4. **XSS Protection**: Template auto-escaping enabled
5. **Access Control**: Login required decorators on sensitive views

---

**Last Updated:** December 2024
