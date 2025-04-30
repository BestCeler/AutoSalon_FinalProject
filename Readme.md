# Auto Salon - Final Project

## Features

### Databases
 - [x] Car Database
   - [x] model - foreign key to Model
   - [x] manual / auto
   - [x] color - foreign key
   - [x] Date of establishment
   - [x] price
   - [x] rentable / sellable
   - [x] test drive 0/1
   - [x] SPZ
   - [x] location = city

- [x] Model Database
  - [x] name
  - [x] field of range
  - [x] description
  - [x] number of seats
  - [x] pictures

- [x] User Database
  - [x] privileges
  - [x] e-mail
  - [x] username
  - [x] full name
  - [x] phone number
  - [x] address
    - [x] country
      - [x] state if US
    - [x] city
    - [x] postcode
    - [x] street
    - [ ] is voluntary

- [x] Orders
  - [x] order number
  - [x] date of order
  - [x] user
  - [x] shop address

-[x] Order Line
  - [x] Order - FK to Orders
  - [x] product
  - [x] price
  - [x] amount
  - [x] warranty

- [x] Test Drive
  - [x] Date / time
  - [x] user
  - [x] location
  - [x] product

- [x] Rents
  - [x] user
  - [x] price
  - [x] product - FK to Cars
  - [x] datetime from
  - [x] datetime to
  - [x] location


### Web

- [ ] Main Page
  - [ ] login / register
  - [ ] Cars

- [ ] Cars Page
  - [ ] filters
    - [ ] for rent
    - [ ] for sale
    - [ ] for test drive
    - [ ] color
    - [ ] price
    - [ ] model
  - [ ] model
  - [ ] price
  - [ ] color
  - [ ] drive distance

- [ ] User Page
  - [ ] rents (m:n -> Rents)
  - [ ] orders
  - [ ] test drives


------------

# Progress
### 08-04-2025
- creation of the cars models
- creation of admin
- creation of db object creation in admin panel
- first establishment of views

### 09-04-2025
- update to cars
- created basic dbs for user and orders

### 10-04-2025
- forms and models for users and orders done
- views for users done
- started on pages for user authentication

### 14-04-2025
- attempts at creating orders

### 22-04-2025
- work on orders proceeds in an orderly fashion
- Eldritch gods consulted

### 28-04-2025
- orders finished
- working on processing orders

### 29-04-2025
- TODO: script for order_processing