# Food Ordering API

This project is a **backend REST API** built as part of **SolutionWorks**, a platform that showcases **ready-to-use website templates** for small businesses such as restaurants, barbershops, salons, and local services.

The **Food Ordering API** is designed to support the **restaurant templates** in SolutionWorks by handling menu items, orders, carts, and user roles.

---

## Project Context: SolutionWorks

**SolutionWorks** is a project that provides **free and reusable website templates** for small businesses.

Templates include:
- Restaurant websites
- Barbershop websites
- Salon websites
- Other small business websites

This API represents **one core backend step** for the **restaurant template**, enabling real-world features such as online ordering and order management.

---

## Features

- RESTful API design
- Menu item management
- Category support
- Order and cart system
- Role-based access (admin, customer, delivery crew)
- Authentication and permissions
- Clean and scalable backend structure

---

## Tech Stack

- **Python**
- **Django**
- **Django REST Framework**
- **Pipenv** (dependency management)
- **SQLite** (development database)

---
## 📡 API Endpoints (Overview)

### Categories
| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/categories` | List all categories |
| POST | `/api/categories` | Create a category (manager only) |

---

### Menu Items
| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/menu-items` | List all menu items |
| POST | `/api/menu-items` | Create a menu item (manager only) |
| GET | `/api/menu-items/{id}` | Retrieve a menu item (manager only)|
| PUT | `/api/menu-items/{id}` | Update a menu item (manager only)|
| DELETE | `/api/menu-items/{id}` | Delete a menu item (manager only)|

---

### Cart
| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/cart/menu-items` | View current user's cart |
| POST | `/api/cart/menu-items` | Add item to cart |
| DELETE | `/api/cart/menu-items` | Clear cart |

---

### Orders
| Method | Endpoint | Description |
|------|---------|-------------|
| GET | `/api/orders` | List orders |
| POST | `/api/orders` | Create a new order |
| GET | `/api/orders/{id}` | Retrieve an order |
| PATCH | `/api/orders/{id}` | Update order status (delivery crew and manager only) |

---

### Role Management

| Role | Endpoint | Purpose |
|----|--------|---------|
| Manager | `/api/groups/manager/users` | Manage restaurant managers (superuser only)|
| Delivery Crew | `/api/groups/delivery-crew/users` | Manage delivery crew members (manager only)|


