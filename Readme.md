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

- [ ] User Database
  - [ ] privileges
  - [ ] e-mail
  - [ ] username
  - [ ] full name
  - [ ] phone number
  - [ ] address
    - [ ] country
      - [ ] state if US
    - [ ] city
    - [ ] postcode
    - [ ] street
    - [ ] is voluntary

- [ ] Orders
  - [ ] order number
  - [ ] date of order
  - [ ] user
  - [ ] shop address

-[ ] Order Line
  - [ ] Order - FK to Orders
  - [ ] product
  - [ ] price
  - [ ] amount
  - [ ] warranty

- [ ] Test Drive
  - [ ] Date / time
  - [ ] user
  - [ ] location
  - [ ] product

- [ ] Rents
  - [ ] user
  - [ ] price
  - [ ] product - FK to Cars
  - [ ] datetime from
  - [ ] datetime to
  - [ ] location


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