# **Canyoning API Webserver**

## Table Of Contents

  - [R1](#R1)
  - [R2](#R2)
  - [R3](#R3)
  - [R4](#R4)
  - [R5](#R5)
  - [R6](#R6)
  - [R7](#R7)
  - [R8](#R8)
  - [R9](#R9)
  - [R10](#R10)

---

## R1 Identification of the problem you are trying to solve by building this particular app.

This project will provide a functioning webserver designed specifically for the canyoning community. It will provide a centralised place for information on Australian canyons and a direct forum for users to discuss particular canyons. Currently, information and discussions are spread over multiple websites and Facebook groups, making it difficult to find consistent information and resulting in many disjointed and confusing discussions where topics are not always immediately obvious and information can get easily lost in nested comments and over-filled news feeds.

---

## R2 Why is it a problem that needs solving?

Canyoning can be a dangerous and even fatal adventure pursuit without correct information. Most incidents in canyons are due to human error, whether through bad technique, inaction, or often poor planning. This project aims to make canyoning safer by:

1. Making basic information about specific canyons easily accessible, such as minimum rope length required, difficulty, and number of abseils.
2. Crowd sourcing information regarding conditions by providing the ability to comment on specific canyons to let others know of any changes such as high flow, rock and tree falls, and broken abseil anchors.

---

## R3 Why have you chosen this database system. What are the drawbacks compared to others?

The chosen database system for this project is PostgreSQL, a Relational Database Management System (RDBMS) using Structured Query Language (SQL) to access it. This type of database system stores data in tables with rows and columns, and uses SQL to query the database. NoSQL is the alternative to an RDBMS and stores data in JSON format. 



---

## R4 Identify and discuss the key functionalities and benefits of an ORM

---

## R5 API Endpoint Documentation

---

## R6 ERD

---

## R7 Third party services

- SQLAlchemy
- Flask (Marshmallow, Bcrypt, JWT Extended)
- psycopg2
- dotenv

---

## R8 Describe your projects models in terms of the relationships they have with each other

- User Model
- Canyon Model
- Comment Model

---

## R9 Discuss the database relations to be implemented in your application

- User Table
- Canyon Table
- Comment Table

---

## R10 Describe the way tasks are allocated and tracked in your project

Trello was used for project management during development of this API. The kanban board was used to create specific cards to be completed during development. These included the initial file setup, creating blueprints, models, routes, authentication and validation. Each card contained a checklist of items required to complete the goal of that card. Cards were color coded according to whether they were part of the design, setup or actual API code. Cards were also assigned due dates and these dates were generally met.

Trello Link
Screenshots