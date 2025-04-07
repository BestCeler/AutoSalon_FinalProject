# Auto Salon - Final Project

## Features

### Databases
 - [ ] Car Database
   - [ ] model - foreign key to Model
   - [ ] manual / auto
   - [ ] color - foreign key
   - [ ] Date of establishment
   - [ ] price
   - [ ] rentable / sellable
   - [ ] test drive 0/1
   - [ ] SPZ
   - [ ] location = city

- [ ] Model Database
  - [ ] name
  - [ ] field of range
  - [ ] description
  - [ ] number of seats
  - [ ] pictures

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


