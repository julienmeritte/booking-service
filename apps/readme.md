## hotel_api

- GET /hotels
- GET /hotel/{id}
- POST /hotel
- PUT /hotel/{id}
- DELETE /hotel/{id}

- GET /rooms
- GET /rooms/hotel/{id}
- GET /room/{id}
- POST /room/{hotel_id}
- PUT /room/{id}
- DELETE /room/{id}

- GET /room-categories
- GET /room-category/{id}
- POST /room-category
- PUT /room-category/{id}
- DELELE /room-category/{id}

- GET /services
- GET /service/{id}
- POST /service
- PUT /service/{id}
- DELETE /service/{id}

- GET /discount-types
- POST /discount-type
- PUT /discount-type/{id}
- DLETE /discount-type/{id}

- GET /discounts
- GET /discounts/{id-type}
- GET /discount/{id}
- POST /discount
- PUT /discount/{id}
- DELETE /discount/{id}


## user_api

- GET /users
- GET /user/{id}
- POST /user
- PUT /user/{id}
- DELETE /user/{id}

- GET /user/{id}/role
- PUT /user/{id}/role


## reservation_api

- GET /reservation/{id}
- POST /reservation
- PUT /reservation/{id}
- DELETE /reservation/{id}

- GET /reservations/user/{user-id}

- GET /reservations/hotel/{hotel-id}/{page}
- GET /reservations/room/{room-id}/{page}

- GET /reservations/hotel/{hotel-id}/{week}
- GET /reservations/room/{room-id}/{week}

- GET /calendar/hotel/{hotel-id}/{week}
- GET /calendar/hotel/{hotel-id}/{date}
- GET /calendar/room/{room-id}/{week}
- GET /calendar/room/{room-id}/{date}

- GET /available/hotel/{hotel-id}/{week}
- GET /available/hotel/{hotel-id}/{day}

- GET /available/room/{room-id}/{week}
- GET /available/room/{room-id}/{day}


## mailing_api

- POST /create-account
- POST /reservation-confirmation
- POST /reservation-annulation


# Test tools

https://www.bcrypt.fr

mariadb --user=clo5_user "-pXZe&pR5%2397" clo5db

pytest --log-cli-level=DEBUG